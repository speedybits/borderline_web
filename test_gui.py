#!/usr/bin/env python3
"""
Test suite for GUI server functionality
Tests the Flask server and game logic without browser
"""

import sys
import json
from gui_server import app, socketio, current_game
from flask_socketio import SocketIOTestClient

def test_flask_app():
    """Test that Flask app initializes"""
    print("=" * 60)
    print("TEST 1: Flask App Initialization")
    print("=" * 60)

    assert app is not None, "Flask app should exist"
    assert socketio is not None, "SocketIO should exist"
    print("✓ Flask app initialized successfully")
    print()

def test_game_creation():
    """Test game initialization via Socket.IO"""
    print("=" * 60)
    print("TEST 2: Game Creation via Socket.IO")
    print("=" * 60)

    client = socketio.test_client(app)
    assert client.is_connected(), "Client should connect"
    print("✓ Socket.IO client connected")

    # Start a game
    client.emit('start_game', {
        'mode': 'human_vs_ai',
        'red_type': 'human',
        'blue_type': 'ai',
        'red_strategy': 'aggressive',
        'blue_strategy': 'defensive'
    })

    # Wait for response
    received = client.get_received()
    print(f"✓ Received {len(received)} messages from server")

    # Check for game_started event
    game_started = False
    for msg in received:
        if msg['name'] == 'game_started':
            game_started = True
            print(f"✓ Game started event received")
            print(f"  Game state keys: {msg['args'][0].keys()}")
            break

    assert game_started, "Should receive game_started event"

    client.disconnect()
    print()

def test_piece_placement():
    """Test placing a piece on the board"""
    print("=" * 60)
    print("TEST 3: Piece Placement")
    print("=" * 60)

    client = socketio.test_client(app)

    # Start game
    client.emit('start_game', {
        'mode': 'human_vs_human',
        'red_type': 'human',
        'blue_type': 'human',
        'red_strategy': 'aggressive',
        'blue_strategy': 'defensive'
    })

    # Clear received messages
    client.get_received()

    # Try to place a piece on Red's home row
    print("Attempting to place piece at (0, 3)...")
    client.emit('place_piece', {
        'row': 0,
        'col': 3,
        'piece': None  # Will use first available piece
    })

    # Check response
    received = client.get_received()
    print(f"✓ Received {len(received)} messages")

    piece_placed = False
    for msg in received:
        print(f"  Message: {msg['name']}")
        if msg['name'] == 'piece_placed':
            piece_placed = True
            data = msg['args'][0]
            print(f"✓ Piece placed successfully at ({data['row']}, {data['col']})")
            print(f"  Piece color: {data['piece']['color']}")
            print(f"  Piece power: {data['piece']['power']}")
            break
        elif msg['name'] == 'placement_error':
            print(f"✗ Placement error: {msg['args'][0]['message']}")

    assert piece_placed, "Should successfully place piece"

    client.disconnect()
    print()

def test_invalid_placement():
    """Test that invalid placements are rejected"""
    print("=" * 60)
    print("TEST 4: Invalid Placement Rejection")
    print("=" * 60)

    client = socketio.test_client(app)

    # Start game
    client.emit('start_game', {
        'mode': 'human_vs_human',
        'red_type': 'human',
        'blue_type': 'human'
    })

    client.get_received()

    # Try to place on opponent's home row (should fail)
    print("Attempting invalid placement at (5, 3) - Blue's home row...")
    client.emit('place_piece', {
        'row': 5,
        'col': 3,
        'piece': None
    })

    received = client.get_received()

    error_received = False
    for msg in received:
        if msg['name'] == 'placement_error':
            error_received = True
            print(f"✓ Invalid placement rejected: {msg['args'][0]['message']}")
            break

    assert error_received, "Should reject invalid placement"

    client.disconnect()
    print()

def test_ai_response():
    """Test that AI responds after human move"""
    print("=" * 60)
    print("TEST 5: AI Response")
    print("=" * 60)

    client = socketio.test_client(app)

    # Start human vs AI game
    client.emit('start_game', {
        'mode': 'human_vs_ai',
        'red_type': 'human',
        'blue_type': 'ai'
    })

    client.get_received()

    # Human (Red) makes a move
    print("Human (Red) placing piece...")
    client.emit('place_piece', {
        'row': 0,
        'col': 3,
        'piece': None
    })

    # Give AI time to respond
    import time
    time.sleep(1)

    received = client.get_received()

    ai_moved = False
    for msg in received:
        if msg['name'] == 'ai_moved':
            ai_moved = True
            data = msg['args'][0]
            print(f"✓ AI responded with move at ({data['row']}, {data['col']})")
            print(f"  AI piece power: {data['piece']['power']}")
            break
        elif msg['name'] == 'ai_thinking':
            print(f"  AI is thinking...")

    assert ai_moved, "AI should respond with a move"

    client.disconnect()
    print()

def test_game_state():
    """Test game state tracking"""
    print("=" * 60)
    print("TEST 6: Game State Tracking")
    print("=" * 60)

    client = socketio.test_client(app)

    client.emit('start_game', {'mode': 'human_vs_human'})
    received = client.get_received()

    # Find game_started message
    game_state = None
    for msg in received:
        if msg['name'] == 'game_started':
            game_state = msg['args'][0]
            break

    assert game_state is not None, "Should receive game state"

    print(f"✓ Game state received")
    print(f"  Current player: {game_state['current_player']}")
    print(f"  Turn count: {game_state['turn_count']}")
    print(f"  Red pieces: {game_state['red_pieces_remaining']}")
    print(f"  Blue pieces: {game_state['blue_pieces_remaining']}")
    print(f"  Board size: {game_state['board']['width']}x{game_state['board']['height']}")
    print(f"  Game over: {game_state['game_over']}")

    assert game_state['current_player'] == 'R', "Red should start"
    assert game_state['turn_count'] == 0, "Should start at turn 0"
    assert game_state['red_pieces_remaining'] == 16, "Should have 16 red pieces"
    assert game_state['blue_pieces_remaining'] == 16, "Should have 16 blue pieces"
    assert not game_state['game_over'], "Game should not be over"

    client.disconnect()
    print()

def test_multiple_moves():
    """Test a sequence of moves"""
    print("=" * 60)
    print("TEST 7: Multiple Move Sequence")
    print("=" * 60)

    client = socketio.test_client(app)

    client.emit('start_game', {'mode': 'human_vs_human'})
    client.get_received()

    moves = [
        (0, 3, 'Red'),
        (5, 3, 'Blue'),
        (0, 4, 'Red'),
        (5, 4, 'Blue'),
    ]

    for row, col, expected_color in moves:
        print(f"Placing {expected_color} piece at ({row}, {col})...")
        client.emit('place_piece', {'row': row, 'col': col, 'piece': None})

        received = client.get_received()

        placed = False
        for msg in received:
            if msg['name'] == 'piece_placed':
                placed = True
                data = msg['args'][0]
                actual_color = 'Red' if data['piece']['color'] == 'R' else 'Blue'
                print(f"  ✓ {actual_color} piece placed")

                # Check piece count decreased
                state = data['game_state']
                red_count = state['red_pieces_remaining']
                blue_count = state['blue_pieces_remaining']
                print(f"  Pieces remaining: Red={red_count}, Blue={blue_count}")
                break
            elif msg['name'] == 'placement_error':
                print(f"  ✗ Error: {msg['args'][0]['message']}")
                placed = False
                break

        if not placed and msg['name'] != 'placement_error':
            print(f"  ✗ No response received for move")

    client.disconnect()
    print()

def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("BORDERLINE GUI TEST SUITE")
    print("=" * 60)
    print()

    tests = [
        test_flask_app,
        test_game_creation,
        test_piece_placement,
        test_invalid_placement,
        test_ai_response,
        test_game_state,
        test_multiple_moves,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ TEST FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ TEST ERROR: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    print()

    if failed == 0:
        print("✓ ALL TESTS PASSED!")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
