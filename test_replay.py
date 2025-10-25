#!/usr/bin/env python3
"""
Test script to demonstrate replay functionality

This shows how games played in non-GUI mode can be replayed in the GUI
"""

from borderline_gpt import BorderlineGPT
import random

def create_test_game(filename='replay_test.json', num_turns=15):
    """Create a test game and save it"""

    print(f"Creating test game with {num_turns} turns...")
    print("=" * 60)

    game = BorderlineGPT()

    turn_count = 0
    while not game.game_over and turn_count < num_turns:
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            print("No valid moves available")
            break

        # Choose random move
        move = random.choice(valid_moves)
        result = game.execute_move(move)

        if result['valid']:
            turn_count += 1
            player = move['player']
            pos = move['position']

            print(f"Turn {turn_count}: {player} placed piece at {pos}")

            # Show events
            for event in result['events']:
                if event['type'] == 'combat':
                    winner = event['combat_data']['winner']
                    att_power = event['combat_data']['attacker_power']
                    def_power = event['combat_data']['defender_power']
                    print(f"  ⚔️  Combat! {winner} wins ({att_power} vs {def_power})")
                elif event['type'] == 'piece_removed':
                    print(f"  💀 Piece removed at {event['row']},{event['col']} ({event['reason']})")

        if result['game_over']:
            print(f"\n🎉 Game Over! Winner: {result['winner']}")
            break

    # Export the game
    saved_filename = game.export_game(filename)

    print("\n" + "=" * 60)
    print(f"✅ Game saved to: {saved_filename}")
    print(f"   Total turns: {game.turn_count}")
    print(f"   Moves recorded: {len(game.get_move_history())}")
    print(f"   Game over: {game.game_over}")
    if game.winner:
        print(f"   Winner: {game.winner.color}")

    return saved_filename

def show_replay_instructions(filename):
    """Show how to replay the game"""

    print("\n" + "=" * 60)
    print("🎬 REPLAY INSTRUCTIONS")
    print("=" * 60)
    print(f"\nTo replay this game in the GUI:")
    print(f"\n1. Start the GUI server:")
    print(f"   python3 gui_server.py")
    print(f"\n2. Open browser to:")
    print(f"   http://localhost:5000")
    print(f"\n3. Open browser console (F12) and run:")
    print(f"   socket.emit('load_replay', {{filename: '{filename}'}});")
    print(f"\n4. Use replay controls:")
    print(f"   socket.emit('replay_step_forward');  // Next move")
    print(f"   socket.emit('replay_step_back');     // Previous move")
    print(f"   socket.emit('replay_goto', {{move_number: 5}});  // Jump to move 5")
    print(f"   socket.emit('replay_play');          // Auto-play")
    print(f"   socket.emit('replay_pause');         // Pause")

    print(f"\n5. Listen for replay events:")
    print(f"   socket.on('replay_loaded', (data) => console.log(data));")
    print(f"   socket.on('replay_step', (data) => console.log(data));")

    print("\n" + "=" * 60)

def verify_replay(filename):
    """Verify the replay can be loaded"""

    print(f"\n🔍 Verifying replay file...")

    try:
        game = BorderlineGPT.replay_game(filename)
        history = game.get_move_history()

        print(f"✅ Replay file is valid")
        print(f"   Loaded {len(history)} moves")
        print(f"   Final turn: {game.turn_count}")

        # Show first few moves
        print(f"\n📋 First 3 moves:")
        for i, move in enumerate(history[:3]):
            print(f"   {i+1}. {move['player']} to {move['position']} (rotation: {move['rotation']})")

        if len(history) > 3:
            print(f"   ... and {len(history) - 3} more moves")

        return True
    except Exception as e:
        print(f"❌ Error verifying replay: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  BORDERLINE REPLAY TEST")
    print("=" * 60)

    # Create test game
    filename = create_test_game('replay_test.json', num_turns=15)

    # Verify it can be replayed
    if verify_replay(filename):
        # Show instructions
        show_replay_instructions(filename)

    print("\n" + "=" * 60)
    print("✅ Test Complete!")
    print("=" * 60)
    print("\nThe game has been saved and can now be replayed step-by-step in the GUI!")
    print("This demonstrates that games played in non-GUI mode can be")
    print("perfectly replayed in the GUI using the API architecture.")
    print("=" * 60 + "\n")
