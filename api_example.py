#!/usr/bin/env python3
"""
Example script demonstrating the Borderline Game API

This shows how to:
1. Create a game
2. Execute moves using JSON API
3. Handle game events
4. Save and replay games
"""

from borderline_gpt import BorderlineGPT
import random
import json

def print_board_simple(game_state):
    """Simple text representation of the board"""
    dims = game_state['board_dimensions']
    print(f"\n  ", end="")
    for col in range(dims['width']):
        print(f"{col} ", end="")
    print()
    for row in range(dims['height']):
        print(f"{row} ", end="")
        for col in range(dims['width']):
            piece = game_state['board'][row][col]
            if piece is None:
                print(". ", end="")
            else:
                print(f"{piece['player_color']} ", end="")
        print()
    print()

def main():
    print("=" * 60)
    print("Borderline Game API Example")
    print("=" * 60)

    # Create a new game
    game = BorderlineGPT()
    print(f"\nGame created with ID: {game.game_id}")

    # Get initial state
    state = game.get_game_state()
    print(f"Initial state:")
    print(f"  Turn: {state['turn']}")
    print(f"  Current player: {state['current_player']}")
    print(f"  Red pieces: {len(state['players']['R']['pieces_remaining'])}")
    print(f"  Blue pieces: {len(state['players']['B']['pieces_remaining'])}")

    print_board_simple(state)

    # Play a few turns using the API
    print("\n" + "=" * 60)
    print("Playing 10 turns...")
    print("=" * 60)

    for turn in range(10):
        # Get valid moves
        valid_moves = game.get_valid_moves()

        if not valid_moves:
            print(f"\nNo valid moves for {game.current_player.color}")
            break

        # Choose a random valid move
        move = random.choice(valid_moves)

        print(f"\nTurn {turn + 1}: {move['player']} playing")
        print(f"  Piece index: {move['piece_index']}")
        print(f"  Position: {move['position']}")
        print(f"  Rotation: {move['rotation']}")

        # Execute the move
        result = game.execute_move(move)

        if not result['valid']:
            print(f"  ERROR: {result['reason']}")
            break

        # Process events
        print(f"  Events:")
        for event in result['events']:
            if event['type'] == 'piece_placed':
                print(f"    - Piece placed at ({event['row']}, {event['col']})")
                print(f"      Power: {event['piece']['power']}")
            elif event['type'] == 'combat':
                combat = event['combat_data']
                print(f"    - COMBAT!")
                print(f"      {combat['attacker_color']} (power {combat['attacker_power']}) vs {combat['defender_color']} (power {combat['defender_power']})")
                print(f"      Winner: {combat['winner']}")
            elif event['type'] == 'piece_removed':
                print(f"    - Piece removed at ({event['row']}, {event['col']})")
                print(f"      Reason: {event['reason']}")

        # Check for game over
        if result['game_over']:
            print(f"\n{'=' * 60}")
            print(f"GAME OVER! Winner: {result['winner']}")
            print(f"{'=' * 60}")
            break

    # Show final board
    final_state = game.get_game_state()
    print("\nFinal board:")
    print_board_simple(final_state)

    # Show final stats
    print("Final statistics:")
    print(f"  Total turns: {final_state['turn']}")
    print(f"  Red pieces remaining: {len(final_state['players']['R']['pieces_remaining'])}")
    print(f"  Red pieces on board: {final_state['players']['R']['pieces_on_board']}")
    print(f"  Blue pieces remaining: {len(final_state['players']['B']['pieces_remaining'])}")
    print(f"  Blue pieces on board: {final_state['players']['B']['pieces_on_board']}")

    # Save the game
    print(f"\n{'=' * 60}")
    print("Saving game...")
    filename = game.export_game()
    print(f"Game saved to: {filename}")

    # Show move history
    history = game.get_move_history()
    print(f"\nMove history ({len(history)} moves):")
    for i, move in enumerate(history[:5]):  # Show first 5
        print(f"  {i+1}. {move['player']} piece {move['piece_index']} to {move['position']} (rotation: {move['rotation']})")
    if len(history) > 5:
        print(f"  ... and {len(history) - 5} more moves")

    # Demonstrate replay
    print(f"\n{'=' * 60}")
    print("Testing replay functionality...")
    replayed_game = BorderlineGPT.replay_game(filename)
    replayed_state = replayed_game.get_game_state()

    print(f"Replayed game:")
    print(f"  Game ID: {replayed_state['game_id']}")
    print(f"  Turns: {replayed_state['turn']}")
    print(f"  Game over: {replayed_state['game_over']}")
    print(f"  Winner: {replayed_state['winner']}")

    # Verify replay matches
    if replayed_state['turn'] == final_state['turn']:
        print("\n✓ Replay successful! Game state matches.")
    else:
        print("\n✗ Replay mismatch!")

    print(f"\n{'=' * 60}")
    print("Example complete!")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
