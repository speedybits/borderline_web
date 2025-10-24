#!/usr/bin/env python3
"""
Example: Dynamic Piece Management
Demonstrates gifting pieces, creating custom pieces, and special abilities
"""

from borderline_gpt import BorderlineGPT
import random

def print_separator(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")

def print_player_pieces(game):
    """Show how many pieces each player has"""
    state = game.get_game_state()
    print(f"Red pieces: {len(state['players']['R']['pieces_remaining'])}")
    print(f"Blue pieces: {len(state['players']['B']['pieces_remaining'])}")

def example_1_gift_random():
    """Example 1: Gift random piece to current player"""
    print_separator("Example 1: Gift Random Piece")

    game = BorderlineGPT()

    print("Initial pieces:")
    print_player_pieces(game)

    # Gift random piece to Red
    result = game.gift_random_piece('R')
    print(f"\n✓ {result['message']}")
    print(f"  Power: {result['piece']['power']}")
    print(f"  Added at index: {result['piece_index']}")

    print("\nAfter gifting:")
    print_player_pieces(game)

def example_2_custom_piece():
    """Example 2: Create and gift custom piece"""
    print_separator("Example 2: Custom Piece Creation")

    game = BorderlineGPT()

    # Create an L-shape piece
    print("Creating custom L-shape piece...")
    pip_positions = [
        [0, 0],
        [1, 0],
        [1, 1],
        [2, 0]
    ]

    result = game.create_custom_piece('R', pip_positions)
    print(f"✓ {result['message']}")
    print(f"  Power: {result['piece']['power']}")
    print("\n  Shape:")
    for i, row in enumerate(result['piece']['pips']):
        print(f"  {row}")

    # Now add it to hand
    add_result = game.add_piece_to_hand('R', result['piece'])
    print(f"\n✓ {add_result['message']}")

def example_3_game_with_gifting():
    """Example 3: Play game with periodic piece gifting"""
    print_separator("Example 3: Game with Periodic Gifting")

    game = BorderlineGPT()
    gift_interval = 3

    print(f"Playing game with gifts every {gift_interval} turns...\n")

    turn_count = 0
    while not game.game_over and turn_count < 15:
        # Get valid moves
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            print("No valid moves!")
            break

        # Play random move
        move = random.choice(valid_moves)
        result = game.execute_move(move)

        if result['valid']:
            turn_count += 1
            player = 'R' if turn_count % 2 == 1 else 'B'

            print(f"Turn {turn_count}: {player} played")

            # Gift piece every N turns
            if turn_count % gift_interval == 0:
                # Gift to both players
                for p in ['R', 'B']:
                    gift_result = game.gift_random_piece(p)
                    print(f"  🎁 Gifted {gift_result['piece']['power']}-power piece to {p}")

            if result['game_over']:
                print(f"\n🎉 Game Over! Winner: {result['winner']}")
                break

    print(f"\nFinal piece counts:")
    print_player_pieces(game)

def example_4_sacrifice_mechanic():
    """Example 4: Sacrifice multiple pieces for super piece"""
    print_separator("Example 4: Sacrifice for Super Piece")

    game = BorderlineGPT()

    print("Initial pieces:")
    print_player_pieces(game)

    # Get first 3 pieces from Red
    state = game.get_game_state()
    red_pieces = state['players']['R']['pieces_remaining']

    print(f"\nSacrificing first 3 pieces from Red:")
    total_power = 0
    for i in range(3):
        print(f"  Piece {i}: {red_pieces[i]['power']} power")
        total_power += red_pieces[i]['power']

    # Remove them (in reverse to maintain indices)
    for idx in [2, 1, 0]:
        game.remove_piece_from_hand('R', idx)

    print(f"\nTotal power sacrificed: {total_power}")

    # Create super piece based on power
    if total_power >= 10:
        pip_positions = [
            [0, 0], [0, 1], [0, 2],
            [1, 0], [1, 1], [1, 2],
            [2, 0], [2, 1], [2, 2]
        ]  # 9-pip super piece
        piece_name = "9-pip super piece"
    else:
        pip_positions = [
            [0, 1],
            [1, 0], [1, 1], [1, 2],
            [2, 1]
        ]  # Plus shape
        piece_name = "5-pip plus piece"

    result = game.gift_custom_piece_to_hand('R', pip_positions)
    print(f"\n✓ Created and gifted {piece_name}")
    print(f"  Power: {result['piece']['power']}")

    print("\nAfter sacrifice:")
    print_player_pieces(game)

def example_5_piece_trading():
    """Example 5: Trade pieces between players"""
    print_separator("Example 5: Piece Trading")

    game = BorderlineGPT()

    state = game.get_game_state()
    red_piece = state['players']['R']['pieces_remaining'][0]
    blue_piece = state['players']['B']['pieces_remaining'][0]

    print("Before trade:")
    print(f"  Red piece 0: {red_piece['power']} power")
    print(f"  Blue piece 0: {blue_piece['power']} power")

    # Swap pieces
    result = game.swap_pieces_between_players(0, 0)

    print(f"\n✓ {result['message']}")

    state = game.get_game_state()
    red_piece_after = state['players']['R']['pieces_remaining'][-1]
    blue_piece_after = state['players']['B']['pieces_remaining'][-1]

    print("\nAfter trade (new pieces added at end):")
    print(f"  Red received: {red_piece_after['power']} power (was Blue's)")
    print(f"  Blue received: {blue_piece_after['power']} power (was Red's)")

def example_6_dynamic_difficulty():
    """Example 6: Help losing player with bonus pieces"""
    print_separator("Example 6: Dynamic Difficulty")

    game = BorderlineGPT()

    # Play a few turns
    for _ in range(6):
        valid_moves = game.get_valid_moves()
        if valid_moves:
            move = random.choice(valid_moves)
            game.execute_move(move)

    state = game.get_game_state()
    red_on_board = state['players']['R']['pieces_on_board']
    blue_on_board = state['players']['B']['pieces_on_board']

    print(f"Current board state:")
    print(f"  Red pieces on board: {red_on_board}")
    print(f"  Blue pieces on board: {blue_on_board}")

    # Determine losing player
    if red_on_board < blue_on_board:
        losing_player = 'R'
        difference = blue_on_board - red_on_board
    elif blue_on_board < red_on_board:
        losing_player = 'B'
        difference = red_on_board - blue_on_board
    else:
        losing_player = None
        difference = 0

    if losing_player and difference >= 2:
        print(f"\n{losing_player} is behind by {difference} pieces!")
        print("Gifting bonus piece to help...")

        # Gift powerful piece
        result = game.gift_custom_piece_to_hand(losing_player, [
            [0, 1],
            [1, 0], [1, 1], [1, 2],
            [2, 1]
        ])  # Plus shape

        print(f"✓ Gifted {result['piece']['power']}-power bonus piece!")
    else:
        print("\nGame is balanced, no bonus needed.")

def main():
    print("=" * 60)
    print("  BORDERLINE - PIECE MANAGEMENT EXAMPLES")
    print("=" * 60)

    examples = [
        ("Gift Random Piece", example_1_gift_random),
        ("Custom Piece Creation", example_2_custom_piece),
        ("Game with Periodic Gifting", example_3_game_with_gifting),
        ("Sacrifice for Super Piece", example_4_sacrifice_mechanic),
        ("Piece Trading", example_5_piece_trading),
        ("Dynamic Difficulty", example_6_dynamic_difficulty),
    ]

    for i, (name, func) in enumerate(examples, 1):
        try:
            func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")

        if i < len(examples):
            input("\nPress Enter to continue to next example...")

    print("\n" + "=" * 60)
    print("  All examples completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
