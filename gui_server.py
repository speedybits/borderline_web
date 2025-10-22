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
    piece_config = data.get('piece')  # 3x3 pip configuration

    print(f"Placement request: ({row}, {col})")

    # Create piece from configuration
    piece = Piece(current_game.current_player.color)
    if piece_config:
        piece.pips = piece_config

    # Validate placement
    if not current_game.board.is_valid_placement(row, col):
        emit('placement_error', {
            'message': 'Invalid placement location',
            'row': row,
            'col': col
        })
        return

    # Place piece
    current_game.board.grid[row][col] = piece
    current_game.current_player.pieces.remove(piece)

    # Check for combat
    combat_result = current_game.board.check_combat(row, col, piece)

    # Check for victory
    current_game.check_victory()

    # Build response
    response = {
        'row': row,
        'col': col,
        'piece': piece_to_dict(piece),
        'combat': combat_result,
        'game_state': get_game_state()
    }

    emit('piece_placed', response, broadcast=True)

    # If game not over and next player is AI, make AI move
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

        row, col, piece = result

        # Place piece
        current_game.board.grid[row][col] = piece
        current_game.current_player.pieces.remove(piece)

        # Check for combat
        combat_result = current_game.board.check_combat(row, col, piece)

        # Check for victory
        current_game.check_victory()

        # Build response
        response = {
            'row': row,
            'col': col,
            'piece': piece_to_dict(piece),
            'combat': combat_result,
            'game_state': get_game_state()
        }

        emit('ai_moved', response, broadcast=True)

        # Continue if next player is also AI
        if not current_game.game_over:
            current_game.switch_player()
            current_game.turn_count += 1

            # Check if next player is also AI
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
        'blue_pieces_remaining': len(current_game.blue_player.pieces)
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
        'power': piece.calculate_power()
    }

if __name__ == '__main__':
    print("=" * 60)
    print("BORDERLINE - TRON GUI Server")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
