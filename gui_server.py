#!/usr/bin/env python3
"""
Borderline GUI Server
Flask + Socket.IO server for web-based GUI
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import borderline_gpt
from borderline_gpt import BorderlineGPT
import sys
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'borderline_tron_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global game state
current_game = None
game_sessions = {}

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
    """Initialize a new game"""
    global current_game

    mode = data.get('mode', 'human_vs_human')
    red_type = data.get('red_type', 'human')
    blue_type = data.get('blue_type', 'human')

    print(f"Starting new game: {mode}")
    print(f"  Red: {red_type}, Blue: {blue_type}")

    # Create players based on type
    red_strategy = data.get('red_strategy', 'aggressive')
    blue_strategy = data.get('blue_strategy', 'defensive')
    blue_random = (blue_type == 'random')

    # Initialize game
    current_game = BorderlineGPT(
        red_strategy=red_strategy,
        blue_strategy=blue_strategy,
        blue_random=blue_random
    )

    # Get initial game state
    state = get_game_state()
    emit('game_started', state, broadcast=True)

    # If Red is AI, make first move
    if red_type in ['ai', 'random']:
        process_ai_turn()

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
    """Handle piece placement from client"""
    global current_game

    if not current_game:
        emit('error', {'message': 'No active game'})
        return

    if current_game.game_over:
        emit('error', {'message': 'Game is over'})
        return

    row = data.get('row')
    col = data.get('col')
    piece_index = data.get('piece_index', 0)  # Default to first piece if not specified

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

    # Get existing player pieces on the board
    player_pieces = current_game.board.get_player_pieces(current_game.current_player.color)

    # Validate placement using proper game rules
    if not current_game.board.can_place_piece(piece, row, col, player_pieces):
        emit('placement_error', {
            'message': 'Invalid placement - must connect to existing pieces or home row',
            'row': row,
            'col': col
        })
        return

    # Check for combat BEFORE placing (need to check adjacency first)
    all_pieces = current_game.board.get_player_pieces('R') + current_game.board.get_player_pieces('B')
    adjacent_pips = current_game.board.check_pip_adjacency(piece, row, col, all_pieces)

    # Remove piece from player's hand and place on board
    current_game.current_player.pieces.pop(piece_index)
    current_game.board.grid[row][col] = piece

    # Resolve combat (if any)
    combat_result = current_game.board.resolve_combat(piece, row, col, adjacent_pips)

    # Check for victory
    victory = current_game.board.check_victory(current_game.current_player.color)
    if victory:
        current_game.winner = current_game.current_player
        current_game.game_over = True

    # Build response
    response = {
        'row': row,
        'col': col,
        'piece': piece_to_dict(piece),
        'combat': combat_to_dict(combat_result),
        'game_state': get_game_state()
    }

    emit('piece_placed', response, broadcast=True)

    # If game not over, switch player and check if AI should move
    if not current_game.game_over:
        current_game.switch_player()
        current_game.turn_count += 1

        # Check if current player is AI (has choose_move method)
        if hasattr(current_game.current_player, 'choose_move'):
            socketio.sleep(0.5)  # Brief pause for visualization
            process_ai_turn()

def process_ai_turn():
    """Process AI player's turn"""
    global current_game

    if not current_game or current_game.game_over:
        return

    # Check if current player is AI (not human)
    if hasattr(current_game.current_player, 'choose_move'):
        # Notify that AI is thinking
        emit('ai_thinking', {
            'player': current_game.current_player.color
        }, broadcast=True)

        # Get AI move
        result = current_game.current_player.choose_move(current_game.board)

        if result[0] is None:
            # AI has no valid moves
            emit('ai_no_moves', {
                'player': current_game.current_player.color
            }, broadcast=True)
            current_game.switch_player()
            current_game.turn_count += 1
            return

        piece, row, col, rotation, piece_idx = result

        # Check for combat BEFORE placing
        all_pieces = current_game.board.get_player_pieces('R') + current_game.board.get_player_pieces('B')
        adjacent_pips = current_game.board.check_pip_adjacency(piece, row, col, all_pieces)

        # Remove piece from player's hand using the index (AI already selected the specific piece)
        current_game.current_player.pieces.pop(piece_idx)

        # Place piece on board
        current_game.board.grid[row][col] = piece

        # Resolve combat (if any)
        combat_result = current_game.board.resolve_combat(piece, row, col, adjacent_pips)

        # Check for victory
        victory = current_game.board.check_victory(current_game.current_player.color)
        if victory:
            current_game.winner = current_game.current_player
            current_game.game_over = True

        # Build response
        response = {
            'row': row,
            'col': col,
            'piece': piece_to_dict(piece),
            'combat': combat_to_dict(combat_result),
            'game_state': get_game_state()
        }

        emit('ai_moved', response, broadcast=True)

        # Switch player if game not over
        if not current_game.game_over:
            current_game.switch_player()
            current_game.turn_count += 1

            # If next player is also AI, continue with their turn
            # Note: Using iteration instead of recursion to avoid stack overflow
            if hasattr(current_game.current_player, 'choose_move'):
                socketio.sleep(0.5)
                process_ai_turn()

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

def combat_to_dict(combat):
    """Convert combat result to JSON-serializable dictionary"""
    if not combat:
        return None

    # Convert defenders list (which contains GamePiece objects) to serializable format
    defenders_serializable = []
    for defender in combat['defenders']:
        defenders_serializable.append({
            'row': defender['row'],
            'col': defender['col'],
            'power': defender['power']
        })

    return {
        'combat_occurred': True,
        'attacker_pos': combat['attacker_pos'],
        'attacker_power': combat['attacker_power'],
        'attacker_roll': combat['attacker_roll'],
        'attacker_total': combat['attacker_total'],
        'attacker_color': combat['attacker_color'],
        'defenders': defenders_serializable,
        'defender_power': combat['defender_power'],
        'defender_roll': combat['defender_roll'],
        'defender_total': combat['defender_total'],
        'defender_color': combat['defender_color'],
        'winner': combat['winner']
    }

if __name__ == '__main__':
    print("=" * 60)
    print("BORDERLINE - TRON GUI Server")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
