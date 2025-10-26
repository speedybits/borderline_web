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
app.config['SECRET_KEY'] = 'borderline_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global game state
current_game = None
game_sessions = {}
pending_placement = None  # Stores {piece, row, col, rotation, piece_index}
replay_state = None  # Stores {game: BorderlineGPT, move_history: [], current_move: int, is_playing: bool}

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
    """Initialize a new game using proper BorderlineGPT constructor"""
    global current_game, replay_state

    # Clear replay state when starting a new game
    replay_state = None

    mode = data.get('mode', 'human_vs_human')
    red_type = data.get('red_type', 'human')
    blue_type = data.get('blue_type', 'human')

    print(f"Starting new game: {mode}")
    print(f"  Red: {red_type}, Blue: {blue_type}")

    # For GUI, we need to manually construct with GUI-specific players
    # Create game with default AI players first
    current_game = BorderlineGPT()

    # Replace players based on type
    if red_type == 'human':
        current_game.red_player = borderline_gpt.GUIHumanPlayer('R', 'Red Player')
    elif red_type == 'random':
        current_game.red_player = borderline_gpt.RandomPlayer('R', 'Red Random')
    else:  # ai
        red_strategy = data.get('red_strategy', 'aggressive')
        if red_strategy == 'aggressive':
            current_game.red_player = borderline_gpt.AggressiveConnectorAI('R', 'Red Aggressive')
        else:
            current_game.red_player = borderline_gpt.DefensiveTerritoryAI('R', 'Red Defensive')

    if blue_type == 'human':
        current_game.blue_player = borderline_gpt.GUIHumanPlayer('B', 'Blue Player')
    elif blue_type == 'random':
        current_game.blue_player = borderline_gpt.RandomPlayer('B', 'Blue Random')
    else:  # ai
        blue_strategy = data.get('blue_strategy', 'defensive')
        if blue_strategy == 'aggressive':
            current_game.blue_player = borderline_gpt.AggressiveConnectorAI('B', 'Blue Aggressive')
        else:
            current_game.blue_player = borderline_gpt.DefensiveTerritoryAI('B', 'Blue Defensive')

    # Reset current player to Red (Red always starts)
    current_game.current_player = current_game.red_player

    print(f"🎮 GAME INITIALIZED")
    print(f"   Mode: {mode}")
    print(f"   Red: {type(current_game.red_player).__name__}")
    print(f"   Blue: {type(current_game.blue_player).__name__}")
    print(f"   Starting player: {current_game.current_player.color} ({type(current_game.current_player).__name__})")
    print(f"   Turn: {current_game.turn_count}")

    # Get initial game state using API
    state = get_game_state()
    emit('game_started', state, broadcast=True)

    # If Red is AI, make first move
    if red_type in ['ai', 'random']:
        process_ai_turn()

@socketio.on('stop_game')
def handle_stop_game():
    """Stop the current game and clear all server state"""
    global current_game, pending_placement, replay_state

    print("Stopping game and clearing all server state...")

    # Clear all server state
    current_game = None
    pending_placement = None
    replay_state = None

    emit('game_stopped', {'status': 'stopped'})
    print("Game stopped, all state cleared")

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

    row = data.get('row')
    col = data.get('col')
    piece_index = data.get('piece_index', 0)  # Default to first piece if not specified

    # CRITICAL: Only allow human players to place pieces via UI
    if not isinstance(current_game.current_player, borderline_gpt.GUIHumanPlayer):
        print(f"❌ REJECTED PLACEMENT - Not human player's turn")
        print(f"   Attempted placement: row={row}, col={col}, piece_index={piece_index}")
        print(f"   Current player: {current_game.current_player.color} ({type(current_game.current_player).__name__})")
        print(f"   Red player type: {type(current_game.red_player).__name__}")
        print(f"   Blue player type: {type(current_game.blue_player).__name__}")
        print(f"   Turn count: {current_game.turn_count}")
        print(f"   Game over: {current_game.game_over}")
        emit('placement_error', {
            'message': f'Not your turn - AI ({current_game.current_player.color}) is playing'
        })
        return

    print(f"✓ ACCEPTED PLACEMENT REQUEST")
    print(f"   Player: {current_game.current_player.color} ({type(current_game.current_player).__name__})")
    print(f"   Position: row={row}, col={col}")
    print(f"   Piece index: {piece_index}")
    print(f"   Turn: {current_game.turn_count}")

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
    global pending_placement, current_game

    if not pending_placement:
        emit('error', {'message': 'No piece to rotate'})
        return

    # CRITICAL: Only allow human players to rotate pieces
    if not isinstance(current_game.current_player, borderline_gpt.GUIHumanPlayer):
        emit('placement_error', {
            'message': 'Not your turn - AI is playing'
        })
        print(f"Rejected rotation - current player is {type(current_game.current_player).__name__}, not GUIHumanPlayer")
        pending_placement = None  # Clear the invalid pending placement
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
    """Confirm and finalize piece placement - USE GAME ENGINE API"""
    global current_game, pending_placement

    if not pending_placement:
        emit('error', {'message': 'No pending placement'})
        return

    # CRITICAL: Only allow human players to confirm placements
    if not isinstance(current_game.current_player, borderline_gpt.GUIHumanPlayer):
        emit('placement_error', {
            'message': 'Not your turn - AI is playing'
        })
        print(f"Rejected confirm - current player is {type(current_game.current_player).__name__}, not GUIHumanPlayer")
        pending_placement = None  # Clear the invalid pending placement
        return

    # Get placement details
    row = pending_placement['row']
    col = pending_placement['col']
    rotation = pending_placement['rotation']
    piece_index = pending_placement['piece_index']

    # Clear pending placement
    pending_placement = None

    # Convert rotation from degrees (0, 90, 180, 270) to count (0, 1, 2, 3)
    rotation_count = rotation // 90

    # Build move in API format
    move = {
        'player': current_game.current_player.color,
        'piece_index': piece_index,
        'position': [row, col],
        'rotation': rotation_count
    }

    # Call game engine API - it does EVERYTHING (validation, placement, combat, victory)
    print(f"🎯 EXECUTING MOVE")
    print(f"   Player: {move['player']}")
    print(f"   Position: {move['position']}")
    print(f"   Piece index: {move['piece_index']}")
    print(f"   Rotation: {move['rotation']} ({rotation_count * 90}°)")

    result = current_game.execute_move(move)

    print(f"   Result: {'VALID' if result['valid'] else 'INVALID'}")
    if result['valid']:
        print(f"   New current player: {current_game.current_player.color} ({type(current_game.current_player).__name__})")
        print(f"   New turn: {current_game.turn_count}")

    # Just broadcast the result - NO game logic here!
    if not result['valid']:
        emit('placement_invalid', {
            'message': result['reason'],
            'row': row,
            'col': col
        }, broadcast=True)
        return

    # Valid move - build response from events
    combat_result = None
    removed_pieces = []

    for event in result['events']:
        if event['type'] == 'combat':
            combat_result = event['combat_data']
        elif event['type'] == 'piece_removed':
            removed_pieces.append({
                'row': event['row'],
                'col': event['col'],
                'piece': event['piece'],  # Already JSON from API
                'reason': event['reason']
            })

    # Get placed piece from events
    placed_piece = None
    for event in result['events']:
        if event['type'] == 'piece_placed':
            placed_piece = event['piece']
            break

    # Build response (game state already updated by engine)
    response = {
        'row': row,
        'col': col,
        'piece': placed_piece,
        'combat': combat_to_dict(combat_result),
        'removed_pieces': removed_pieces,
        'game_state': api_state_to_gui_state(result['game_state'])
    }

    emit('piece_placed', response, broadcast=True)

    # Check if current player is AI (not human)
    # CRITICAL: Use isinstance check, not hasattr, because GUIHumanPlayer also has choose_move!
    if not result['game_over'] and not isinstance(current_game.current_player, borderline_gpt.GUIHumanPlayer):
        socketio.sleep(0.5)  # Brief pause for visualization
        process_ai_turn()

def process_ai_turn():
    """Process AI player's turn using API"""
    global current_game

    if not current_game or current_game.game_over:
        return

    # Check if current player is AI (not human)
    # CRITICAL: Use isinstance check, not hasattr, because GUIHumanPlayer also has choose_move!
    if not isinstance(current_game.current_player, borderline_gpt.GUIHumanPlayer):
        print(f"🤖 AI TURN STARTING")
        print(f"   Player: {current_game.current_player.color} ({type(current_game.current_player).__name__})")
        print(f"   Turn: {current_game.turn_count}")

        # Notify that AI is thinking
        emit('ai_thinking', {
            'player': current_game.current_player.color
        }, broadcast=True)

        # Get AI move
        ai_result = current_game.current_player.choose_move(current_game.board)

        if ai_result[0] is None:
            # AI has no valid moves
            emit('ai_no_moves', {
                'player': current_game.current_player.color
            }, broadcast=True)
            current_game.switch_player()
            current_game.turn_count += 1
            return

        piece, row, col, rotation_degrees, piece_idx = ai_result

        # Convert rotation from degrees to count for API
        rotation_count = rotation_degrees // 90

        # Build move in API format
        move = {
            'player': current_game.current_player.color,
            'piece_index': piece_idx,
            'position': [row, col],
            'rotation': rotation_count
        }

        print(f"🎯 AI EXECUTING MOVE")
        print(f"   Player: {move['player']}")
        print(f"   Position: {move['position']}")
        print(f"   Piece index: {move['piece_index']}")
        print(f"   Rotation: {move['rotation']} ({rotation_degrees}°)")

        # Execute move through API
        result = current_game.execute_move(move)

        print(f"   Result: {'VALID' if result['valid'] else 'INVALID'}")
        if result['valid']:
            print(f"   New current player: {current_game.current_player.color} ({type(current_game.current_player).__name__})")
            print(f"   New turn: {current_game.turn_count}")

        if not result['valid']:
            # This shouldn't happen with a properly functioning AI
            print(f"ERROR: AI made invalid move: {result['reason']}")
            emit('error', {'message': f"AI error: {result['reason']}"}, broadcast=True)
            return

        # Valid move - build response from events
        combat_result = None
        removed_pieces = []

        for event in result['events']:
            if event['type'] == 'combat':
                combat_result = event['combat_data']
            elif event['type'] == 'piece_removed':
                removed_pieces.append({
                    'row': event['row'],
                    'col': event['col'],
                    'piece': event['piece'],  # Already JSON from API
                    'reason': event['reason']
                })

        # Get placed piece from events
        placed_piece = None
        for event in result['events']:
            if event['type'] == 'piece_placed':
                placed_piece = event['piece']
                break

        # Build response
        response = {
            'row': row,
            'col': col,
            'piece': placed_piece,
            'combat': combat_to_dict(combat_result),
            'removed_pieces': removed_pieces,
            'game_state': api_state_to_gui_state(result['game_state'])
        }

        emit('ai_moved', response, broadcast=True)

        # If next player is also AI, continue with their turn
        if not result['game_over'] and hasattr(current_game.current_player, 'choose_move'):
            socketio.sleep(0.5)
            process_ai_turn()

def api_state_to_gui_state(api_state):
    """Convert API game state format to GUI format"""
    return {
        'board': {
            'width': api_state['board_dimensions']['width'],
            'height': api_state['board_dimensions']['height'],
            'grid': [[convert_api_piece(cell) for cell in row] for row in api_state['board']]
        },
        'current_player': api_state['current_player'],
        'turn_count': api_state['turn'],
        'game_over': api_state['game_over'],
        'winner': api_state['winner'],
        'red_pieces_remaining': len(api_state['players']['R']['pieces_remaining']),
        'blue_pieces_remaining': len(api_state['players']['B']['pieces_remaining']),
        'red_pieces': [convert_api_piece(p) for p in api_state['players']['R']['pieces_remaining']],
        'blue_pieces': [convert_api_piece(p) for p in api_state['players']['B']['pieces_remaining']]
    }

def convert_api_piece(piece_json):
    """Convert API piece format to GUI format"""
    if piece_json is None:
        return None
    return {
        'color': piece_json['player_color'],
        'pips': piece_json['pips'],
        'power': piece_json['power']
    }

def get_game_state():
    """Convert game state to dictionary for JSON"""
    if not current_game:
        return None

    # Use API to get state
    api_state = current_game.get_game_state()
    return api_state_to_gui_state(api_state)

def piece_to_dict(piece):
    """Convert GamePiece object to dictionary (for rotation preview)"""
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

# ==================== REPLAY MODE ====================

@socketio.on('load_replay')
def handle_load_replay(data):
    """Load a game from JSON file for replay"""
    global replay_state, current_game

    filename = data.get('filename', 'replay_demo.json')

    try:
        # Load the game
        replayed_game = BorderlineGPT.replay_game(filename)
        move_history = replayed_game.get_move_history()

        # Create fresh game for step-by-step replay
        fresh_game = BorderlineGPT()

        replay_state = {
            'game': fresh_game,
            'move_history': move_history,
            'current_move': -1,  # Start before first move
            'is_playing': False,
            'total_moves': len(move_history)
        }

        # Set as current game for rendering
        current_game = fresh_game

        # Send initial state
        emit('replay_loaded', {
            'success': True,
            'total_moves': len(move_history),
            'game_state': api_state_to_gui_state(fresh_game.get_game_state()),
            'message': f'Loaded replay with {len(move_history)} moves'
        }, broadcast=True)

    except Exception as e:
        emit('replay_error', {
            'success': False,
            'message': f'Failed to load replay: {str(e)}'
        })

@socketio.on('replay_step_forward')
def handle_replay_step_forward():
    """Execute next move in replay"""
    global replay_state, current_game

    if not replay_state:
        emit('replay_error', {'message': 'No replay loaded'})
        return

    if replay_state['current_move'] >= replay_state['total_moves'] - 1:
        emit('replay_error', {'message': 'Already at end of replay'})
        return

    # Execute next move
    replay_state['current_move'] += 1
    move = replay_state['move_history'][replay_state['current_move']]

    result = replay_state['game'].execute_move(move)

    if result['valid']:
        # Extract events for animation
        combat_result = None
        removed_pieces = []

        for event in result['events']:
            if event['type'] == 'combat':
                combat_result = event['combat_data']
            elif event['type'] == 'piece_removed':
                removed_pieces.append({
                    'row': event['row'],
                    'col': event['col'],
                    'piece': event['piece'],
                    'reason': event['reason']
                })

        # Get placed piece
        placed_piece = None
        for event in result['events']:
            if event['type'] == 'piece_placed':
                placed_piece = event['piece']
                break

        emit('replay_step', {
            'move_number': replay_state['current_move'] + 1,
            'total_moves': replay_state['total_moves'],
            'move': move,
            'row': move['position'][0],
            'col': move['position'][1],
            'piece': placed_piece,
            'combat': combat_to_dict(combat_result),
            'removed_pieces': removed_pieces,
            'game_state': api_state_to_gui_state(result['game_state']),
            'game_over': result['game_over'],
            'winner': result['winner']
        }, broadcast=True)
    else:
        emit('replay_error', {'message': f'Move failed: {result["reason"]}'})

@socketio.on('replay_step_back')
def handle_replay_step_back():
    """Go back one move in replay"""
    global replay_state, current_game

    if not replay_state:
        emit('replay_error', {'message': 'No replay loaded'})
        return

    if replay_state['current_move'] < 0:
        emit('replay_error', {'message': 'Already at start of replay'})
        return

    # Reset to start and replay up to current_move - 1
    replay_state['current_move'] -= 1
    target_move = replay_state['current_move']

    # Create fresh game
    fresh_game = BorderlineGPT()

    # Replay moves up to target
    for i in range(target_move + 1):
        move = replay_state['move_history'][i]
        fresh_game.execute_move(move)

    replay_state['game'] = fresh_game
    current_game = fresh_game

    emit('replay_step_back', {
        'move_number': replay_state['current_move'] + 1,
        'total_moves': replay_state['total_moves'],
        'game_state': api_state_to_gui_state(fresh_game.get_game_state())
    }, broadcast=True)

@socketio.on('replay_goto')
def handle_replay_goto(data):
    """Jump to specific move in replay"""
    global replay_state, current_game

    if not replay_state:
        emit('replay_error', {'message': 'No replay loaded'})
        return

    target_move = data.get('move_number', 0) - 1  # Convert to 0-indexed

    if target_move < -1 or target_move >= replay_state['total_moves']:
        emit('replay_error', {'message': 'Invalid move number'})
        return

    # Create fresh game and replay to target
    fresh_game = BorderlineGPT()

    for i in range(target_move + 1):
        move = replay_state['move_history'][i]
        fresh_game.execute_move(move)

    replay_state['game'] = fresh_game
    replay_state['current_move'] = target_move
    current_game = fresh_game

    emit('replay_goto', {
        'move_number': target_move + 1,
        'total_moves': replay_state['total_moves'],
        'game_state': api_state_to_gui_state(fresh_game.get_game_state())
    }, broadcast=True)

@socketio.on('replay_play')
def handle_replay_play():
    """Start auto-playing replay"""
    global replay_state

    if not replay_state:
        emit('replay_error', {'message': 'No replay loaded'})
        return

    replay_state['is_playing'] = True
    emit('replay_playing', {'is_playing': True}, broadcast=True)

    # Auto-advance will be handled by client with replay_step_forward

@socketio.on('replay_pause')
def handle_replay_pause():
    """Pause auto-playing replay"""
    global replay_state

    if not replay_state:
        emit('replay_error', {'message': 'No replay loaded'})
        return

    replay_state['is_playing'] = False
    emit('replay_paused', {'is_playing': False}, broadcast=True)

@socketio.on('get_replay_state')
def handle_get_replay_state():
    """Get current replay state"""
    global replay_state

    if not replay_state:
        emit('replay_state', {
            'loaded': False
        })
        return

    emit('replay_state', {
        'loaded': True,
        'current_move': replay_state['current_move'] + 1,
        'total_moves': replay_state['total_moves'],
        'is_playing': replay_state['is_playing']
    })

@socketio.on('load_replay_data')
def handle_load_replay_data(data):
    """Load a game from JSON data (for file uploads)"""
    global replay_state, current_game

    try:
        game_data = data.get('game_data')
        if not game_data:
            emit('replay_error', {'message': 'No game data provided'})
            return

        # Extract move history from uploaded data
        move_history = game_data.get('move_history', [])

        if not move_history:
            emit('replay_error', {'message': 'No move history found in uploaded file'})
            return

        # Create fresh game for step-by-step replay
        fresh_game = BorderlineGPT()

        replay_state = {
            'game': fresh_game,
            'move_history': move_history,
            'current_move': -1,  # Start before first move
            'is_playing': False,
            'total_moves': len(move_history)
        }

        # Set as current game for rendering
        current_game = fresh_game

        # Send initial state
        emit('replay_loaded', {
            'success': True,
            'total_moves': len(move_history),
            'game_state': api_state_to_gui_state(fresh_game.get_game_state()),
            'message': f'Loaded replay from upload with {len(move_history)} moves'
        }, broadcast=True)

        print(f"Loaded replay from upload: {len(move_history)} moves")

    except Exception as e:
        emit('replay_error', {
            'success': False,
            'message': f'Failed to load replay data: {str(e)}'
        })
        print(f"Error loading replay data: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("BORDERLINE - GUI Server")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
