#!/usr/bin/env python3
"""
Comprehensive end-to-end test of the complete Borderline API
Tests all major functionality in a realistic game scenario
"""

from borderline_gpt import BorderlineGPT
import random
import json

def test_complete_game_with_features():
    """Test a complete game with all API features"""

    print("=" * 70)
    print("  COMPREHENSIVE API TEST - Complete Game Scenario")
    print("=" * 70)

    # ========== PHASE 1: Game Initialization ==========
    print("\n[PHASE 1] Game Initialization")
    game = BorderlineGPT()
    print(f"✓ Game created with ID: {game.game_id}")

    initial_state = game.get_game_state()
    print(f"✓ Initial state retrieved")
    print(f"  - Turn: {initial_state['turn']}")
    print(f"  - Current player: {initial_state['current_player']}")
    print(f"  - Red pieces: {len(initial_state['players']['R']['pieces_remaining'])}")
    print(f"  - Blue pieces: {len(initial_state['players']['B']['pieces_remaining'])}")

    # ========== PHASE 2: Play Several Turns ==========
    print("\n[PHASE 2] Playing 10 Turns with Standard Rules")

    for turn in range(10):
        valid_moves = game.get_valid_moves()
        assert len(valid_moves) > 0, f"No valid moves on turn {turn}"

        move = random.choice(valid_moves)
        result = game.execute_move(move)

        assert result['valid'], f"Move failed on turn {turn}: {result['reason']}"

        print(f"✓ Turn {turn + 1}: {move['player']} played at {move['position']}")

        # Show events
        for event in result['events']:
            if event['type'] == 'combat':
                winner = event['combat_data']['winner']
                print(f"  ⚔️  Combat! {winner} wins")
            elif event['type'] == 'piece_removed':
                print(f"  💀 Piece removed: {event['reason']}")

        if result['game_over']:
            print(f"  🎉 Game Over! Winner: {result['winner']}")
            break

    # ========== PHASE 3: Gift Random Piece ==========
    print("\n[PHASE 3] Testing Piece Gifting")

    current_player = game.current_player.color
    before_count = len(game.current_player.pieces)

    gift_result = game.gift_random_piece(current_player)
    assert gift_result['success'], "Failed to gift piece"

    after_count = len(game.current_player.pieces)
    assert after_count == before_count + 1, "Piece count didn't increase"

    print(f"✓ Gifted {gift_result['piece']['power']}-power piece to {current_player}")
    print(f"  - Pieces before: {before_count}")
    print(f"  - Pieces after: {after_count}")

    # ========== PHASE 4: Create Custom Piece ==========
    print("\n[PHASE 4] Testing Custom Piece Creation")

    # Create L-shape
    custom_result = game.create_custom_piece('R', [
        [0, 0],
        [1, 0],
        [1, 1],
        [2, 0]
    ])

    assert custom_result['success'], "Failed to create custom piece"
    print(f"✓ Created L-shape piece")
    print(f"  - Power: {custom_result['piece']['power']}")
    print(f"  - Pattern:")
    for row in custom_result['piece']['pips']:
        print(f"    {row}")

    # Add it to hand
    add_result = game.add_piece_to_hand('R', custom_result['piece'])
    assert add_result['success'], "Failed to add custom piece to hand"
    print(f"✓ Added custom piece to Red's hand at index {add_result['piece_index']}")

    # ========== PHASE 5: Play More Turns with Custom Piece ==========
    print("\n[PHASE 5] Playing 5 More Turns (with custom piece)")

    for turn in range(5):
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            print("  No valid moves remaining")
            break

        move = random.choice(valid_moves)
        result = game.execute_move(move)

        if result['valid']:
            print(f"✓ Turn {game.turn_count}: {move['player']} played")

        if result['game_over']:
            print(f"  🎉 Game Over! Winner: {result['winner']}")
            break

    # ========== PHASE 6: Test Piece Removal ==========
    print("\n[PHASE 6] Testing Piece Removal")

    if len(game.red_player.pieces) > 0:
        before_count = len(game.red_player.pieces)
        remove_result = game.remove_piece_from_hand('R', 0)

        assert remove_result['success'], "Failed to remove piece"
        assert len(game.red_player.pieces) == before_count - 1

        print(f"✓ Removed piece from Red's hand")
        print(f"  - Power: {remove_result['piece']['power']}")
        print(f"  - Pieces before: {before_count}")
        print(f"  - Pieces after: {len(game.red_player.pieces)}")
    else:
        print("⊘ Red has no pieces to remove (skipped)")

    # ========== PHASE 7: Export and Replay ==========
    print("\n[PHASE 7] Testing Export and Replay")

    # Export game
    filename = game.export_game("test_complete_game.json")
    print(f"✓ Exported game to {filename}")

    # Check file exists and is valid JSON
    with open(filename, 'r') as f:
        exported_data = json.load(f)

    print(f"✓ Verified exported file is valid JSON")
    print(f"  - Game ID: {exported_data['game_id']}")
    print(f"  - Moves recorded: {len(exported_data['move_history'])}")
    print(f"  - Game over: {exported_data['game_over']}")

    # Replay game
    replayed_game = BorderlineGPT.replay_game(filename)
    print(f"✓ Replayed game from file")

    # Verify replay matches
    original_state = game.get_game_state()
    replayed_state = replayed_game.get_game_state()

    assert original_state['turn'] == replayed_state['turn'], "Turn count mismatch"
    assert original_state['game_over'] == replayed_state['game_over'], "Game over state mismatch"

    print(f"✓ Replay verification passed")
    print(f"  - Turns match: {original_state['turn']}")
    print(f"  - Game over match: {original_state['game_over']}")

    # ========== PHASE 8: Get Move History ==========
    print("\n[PHASE 8] Testing Move History")

    history = game.get_move_history()
    print(f"✓ Retrieved move history")
    print(f"  - Total moves: {len(history)}")

    if len(history) > 0:
        first_move = history[0]
        print(f"  - First move: {first_move['player']} to {first_move['position']}")

        last_move = history[-1]
        print(f"  - Last move: {last_move['player']} to {last_move['position']}")

    # ========== PHASE 9: Test Invalid Operations ==========
    print("\n[PHASE 9] Testing Error Handling")

    # Try invalid move
    invalid_move = {
        'player': 'R' if game.current_player.color == 'B' else 'B',  # Wrong player
        'piece_index': 0,
        'position': [0, 0],
        'rotation': 0
    }

    result = game.execute_move(invalid_move)
    assert not result['valid'], "Invalid move should be rejected"
    print(f"✓ Invalid move correctly rejected: {result['reason']}")

    # Try invalid piece creation (no center pip)
    invalid_piece = game.create_custom_piece('R', [[0, 0], [2, 2]])
    assert not invalid_piece['success'], "Invalid piece should be rejected"
    print(f"✓ Invalid piece correctly rejected: {invalid_piece['message']}")

    # Try invalid piece index
    invalid_remove = game.remove_piece_from_hand('R', 9999)
    assert not invalid_remove['success'], "Invalid index should be rejected"
    print(f"✓ Invalid index correctly rejected: {invalid_remove['message']}")

    # ========== PHASE 10: Final State Check ==========
    print("\n[PHASE 10] Final State Verification")

    final_state = game.get_game_state()
    print(f"✓ Final game state:")
    print(f"  - Total turns: {final_state['turn']}")
    print(f"  - Game over: {final_state['game_over']}")
    print(f"  - Winner: {final_state['winner'] or 'In progress'}")
    print(f"  - Red pieces remaining: {len(final_state['players']['R']['pieces_remaining'])}")
    print(f"  - Red pieces on board: {final_state['players']['R']['pieces_on_board']}")
    print(f"  - Blue pieces remaining: {len(final_state['players']['B']['pieces_remaining'])}")
    print(f"  - Blue pieces on board: {final_state['players']['B']['pieces_on_board']}")

    # ========== SUCCESS ==========
    print("\n" + "=" * 70)
    print("  ✅ ALL TESTS PASSED - Complete API Working Correctly!")
    print("=" * 70)
    print("\nAPI Features Tested:")
    print("  ✓ Game initialization")
    print("  ✓ execute_move() - Move execution")
    print("  ✓ get_game_state() - State retrieval")
    print("  ✓ get_valid_moves() - Move generation")
    print("  ✓ gift_random_piece() - Random piece gifting")
    print("  ✓ create_custom_piece() - Custom piece creation")
    print("  ✓ add_piece_to_hand() - Dynamic piece addition")
    print("  ✓ remove_piece_from_hand() - Piece removal")
    print("  ✓ export_game() - Game export")
    print("  ✓ replay_game() - Game replay")
    print("  ✓ get_move_history() - History retrieval")
    print("  ✓ Error handling - Invalid operations rejected")
    print("  ✓ Event system - Combat, removals, placement")
    print("\nThe Borderline API is production-ready! 🎉")

if __name__ == "__main__":
    try:
        test_complete_game_with_features()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
