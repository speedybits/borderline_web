#!/usr/bin/env python3
"""
Borderline GUI Server V2
Uses BorderlineGPT game engine directly - no duplicate logic
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from borderline_gpt import BorderlineGPT, GUIHumanPlayer, RandomPlayer, AggressiveConnectorAI, DefensiveTerritoryAI
import sys
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'borderline_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global game state
current_game = None
pending_placement = None  # Stores {piece, row, col, rotation, piece_index} for rotation mode

@app.route('/')
def index():
    """Serve the main game page"""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid if 'request' in dir() else 'unknown'}")
    emit('connection_established', {'status': 'connected'})

@socketio.on('start_game')
def handle_start_game(data):
    """Initialize a new game using BorderlineGPT engine"""
    global current_game

    mode = data.get('mode', 'human_vs_human')
    red_type = data.get('red_type', 'human')
    blue_type = data.get('blue_type', 'human')

    print(f"Starting new game: {mode}")
    print(f"  Red: {red_type}, Blue: {blue_type}")

    # Create game instance
    current_game = BorderlineGPT.__new__(BorderlineGPT)
    current_game.board = BorderlineGPT.GameBoard() if hasattr(BorderlineGPT, 'GameBoard') else __import__('borderline_gpt').GameBoard()
    current_game.turn_count = 0
    current_game.game_over = False
    current_game.winner = None

    # Import GameBoard if needed
    from borderline_gpt import GameBoard
    current_game.board = GameBoard()

    # Create players based on type
    if red_type == 'human':
        current_game.red_player = GUIHumanPlayer('R', 'Red Player')
    elif red_type == 'random':
        current_game.red_player = RandomPlayer('R', 'Red Random')
    else:  # ai
        red_strategy = data.get('red_strategy', 'aggressive')
        if red_strategy == 'aggressive':
            current_game.red_player = AggressiveConnectorAI('R', 'Red Aggressive')
        else:
            current_game.red_player = DefensiveTerritoryAI('R', 'Red Defensive')

    if blue_type == 'human':
        current_game.blue_player = GUIHumanPlayer('B', 'Blue Player')
    elif blue_type == 'random':
        current_game.blue_player = RandomPlayer('B', 'Blue Random')
    else:  # ai
        blue_strategy = data.get('blue_strategy', 'defensive')
        if blue_strategy == 'aggressive':
            current_game.blue_player = AggressiveConnectorAI('B', 'Blue Aggressive')
        else:
            current_game.blue_player = DefensiveTerritoryAI('B', 'Blue Defensive')

    # Set current player to Red (Red starts)
    current_game.current_player = current_game.red_player

    # Add switch_player method
    def switch_player():
        if current_game.current_player == current_game.red_player:
            current_game.current_player = current_game.blue_player
        else:
            current_game.current_player = current_game.red_player
    current_game.switch_player = switch_player

    # Get initial game state
    state = get_game_state()
    emit('game_started', state, broadcast=True)

    # If Red is AI, trigger first turn
    if red_type in ['ai', 'random']:
        execute_turn()

@socketio.on('get_state')
def handle_get_state():
    """Send current game state to client"""
    if current_game:
        state = get_game_state()
        emit('game_state', state)
    else:
        emit('error', {'message': 'No active game'})

@socketio.on('place_piece')
def handle_place_piece(data):
    """Handle initial piece placement from client (enters rotation mode) - NO VALIDATION YET"""
    global current_game, pending_placement

    if not current_game:
        emit('error', {'message': 'No active game'})
        return

    if current_game.game_over:
        emit('error', {'message': 'Game is over'})
        return

    # Only allow if current player is human
    if not isinstance(current_game.current_player, GUIHumanPlayer):
        emit('error', {'message': 'Not your turn'})
        return

    row = data.get('row')
    col = data.get('col')
    piece_index = data.get('piece_index', 0)

    print(f"Placement request: ({row}, {col}), piece_index={piece_index}")

    # Check if player has pieces
    if not current_game.current_player.has_pieces():
        emit('placement_error', {
            'message': 'No pieces remaining',
            'row': row,
            'col': col
        })
        return

    # Validate piece index
    if piece_index < 0 or piece_index >= len(current_game.current_player.pieces):
        emit('placement_error', {
            'message': f'Invalid piece index: {piece_index}',
            'row': row,
            'col': col
        })
        return

    # Get the selected piece
    piece = current_game.current_player.pieces[piece_index]

    # Store pending placement (don't validate or place on board yet - allow experimentation!)
    pending_placement = {
        'piece': piece,
        'row': row,
        'col': col,
        'rotation': 0,
        'piece_index': piece_index
    }

    # Send piece to client for rotation mode
    response = {
        'row': row,
        'col': col,
        'piece': piece_to_dict(piece),
        'rotation': 0
    }

    emit('piece_pending_rotation', response, broadcast=True)

@socketio.on('rotate_piece')
def handle_rotate_piece(data):
    """Handle piece rotation during placement"""
    global pending_placement

    if not pending_placement:
        emit('error', {'message': 'No piece to rotate'})
        return

    # Rotate the piece by 90 degrees
    pending_placement['rotation'] = (pending_placement['rotation'] + 90) % 360
    rotated_piece = pending_placement['piece'].rotate(pending_placement['rotation'])

    response = {
        'row': pending_placement['row'],
        'col': pending_placement['col'],
        'piece': piece_to_dict(rotated_piece),
        'rotation': pending_placement['rotation']
    }

    emit('piece_rotated', response, broadcast=True)

@socketio.on('confirm_placement')
def handle_confirm_placement(data):
    """Confirm and finalize piece placement - USE GAME ENGINE"""
    global current_game, pending_placement

    if not pending_placement:
        emit('error', {'message': 'No pending placement'})
        return

    # Apply rotation to piece
    piece = pending_placement['piece'].rotate(pending_placement['rotation'])
    row = pending_placement['row']
    col = pending_placement['col']
    piece_index = pending_placement['piece_index']
    rotation = pending_placement['rotation']

    # Clear pending placement
    pending_placement = None

    # Set the move for the human player and let game engine handle it
    current_game.current_player.pending_move = (piece, row, col, rotation, piece_index)

    # Execute the turn using game engine
    execute_turn()

def execute_turn():
    """Execute one turn using the game engine"""
    global current_game

    if not current_game or current_game.game_over:
        return

    # Capture game state before turn
    before_board = [[current_game.board.grid[r][c] for c in range(current_game.board.width)]
                    for r in range(current_game.board.height)]
    before_current_player = current_game.current_player

    # Execute turn using game engine (suppressing print output)
    import io
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        current_game.play_turn()
    finally:
        sys.stdout = old_stdout

    # Build response with game state
    state = get_game_state()

    # Check if turn was successful by seeing if player switched
    if current_game.current_player != before_current_player or current_game.game_over:
        emit('turn_complete', {
            'game_state': state,
            'game_over': current_game.game_over,
            'winner': current_game.winner.color if current_game.winner else None
        }, broadcast=True)

        # If game not over and next player is AI, continue
        if not current_game.game_over and hasattr(current_game.current_player, 'choose_move') and not isinstance(current_game.current_player, GUIHumanPlayer):
            socketio.sleep(0.5)
            execute_turn()
    else:
        # Move was invalid
        emit('placement_invalid', {
            'message': 'Invalid placement - must connect to existing pieces or home row'
        }, broadcast=True)

def get_game_state():
    """Convert game state to dictionary for JSON"""
    if not current_game:
        return None

    return {
        'board': board_to_dict(current_game.board),
        'current_player': current_game.current_player.color,
        'turn_count': current_game.turn_count,
        'game_over': current_game.game_over,
        'winner': current_game.winner.color if current_game.winner else None,
        'red_pieces_remaining': len(current_game.red_player.pieces),
        'blue_pieces_remaining': len(current_game.blue_player.pieces),
        'red_pieces': [piece_to_dict(p) for p in current_game.red_player.pieces],
        'blue_pieces': [piece_to_dict(p) for p in current_game.blue_player.pieces]
    }

def board_to_dict(board):
    """Convert board to dictionary"""
    grid = []
    for row in range(board.height):
        grid_row = []
        for col in range(board.width):
            piece = board.grid[row][col]
            if piece:
                grid_row.append(piece_to_dict(piece))
            else:
                grid_row.append(None)
        grid.append(grid_row)
    return {
        'width': board.width,
        'height': board.height,
        'grid': grid
    }

def piece_to_dict(piece):
    """Convert piece to dictionary"""
    return {
        'color': piece.player_color,
        'pips': piece.pips,
        'power': piece.get_power_level()
    }

if __name__ == '__main__':
    print("=" * 60)
    print("BORDERLINE - GUI Server V2")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
