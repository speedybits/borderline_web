#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from borderline_gpt import BorderlineGPT

def run_silent_game():
    """Run a single game with competing strategies and return the winner"""
    # Red uses Aggressive Connector, Blue uses Defensive Territory
    game = BorderlineGPT(red_strategy='aggressive', blue_strategy='defensive')

    # Disable all print statements by redirecting stdout
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')

    try:
        # Run the game loop silently
        while not game.game_over and game.turn_count < 200:
            game.play_turn()

        # Restore stdout
        sys.stdout.close()
        sys.stdout = original_stdout

        # Determine result
        if game.winner:
            return game.winner.color  # 'R' or 'B'
        else:
            return 'Draw'

    except Exception as e:
        # Restore stdout in case of error
        sys.stdout.close()
        sys.stdout = original_stdout
        print(f"Error in game: {e}")
        import traceback
        traceback.print_exc()
        return 'Error'

def run_strategy_battle(num_games=100):
    """Run games with Red (Aggressive) vs Blue (Defensive) strategies"""
    print("=" * 70)
    print("BORDERLINE GPT - STRATEGY BATTLE")
    print("=" * 70)
    print()
    print("Red AI Strategy:  AGGRESSIVE CONNECTOR")
    print("  - Focuses on direct vertical path from row 0 to row 7")
    print("  - Prioritizes forward progress over territory control")
    print("  - Engages in combat to clear the path")
    print("  - Prefers center columns for direct connection")
    print()
    print("Blue AI Strategy: DEFENSIVE TERRITORY CONTROLLER")
    print("  - Builds wide horizontal control before advancing")
    print("  - Expands methodically row-by-row")
    print("  - Avoids combat when possible")
    print("  - Spreads across multiple columns for stability")
    print()
    print(f"Running {num_games} games...")
    print("=" * 70)
    print()

    results = {'R': 0, 'B': 0, 'Draw': 0, 'Error': 0}

    for game_num in range(1, num_games + 1):
        if game_num % 10 == 0:
            print(f"Completed {game_num} games...")

        result = run_silent_game()
        results[result] += 1

    # Calculate percentages
    total_games = sum(results.values())

    print()
    print("=" * 70)
    print(f"RESULTS AFTER {total_games} GAMES")
    print("=" * 70)
    print()
    print(f"Red (Aggressive) wins:     {results['R']:3d} ({results['R']/total_games*100:5.1f}%)")
    print(f"Blue (Defensive) wins:     {results['B']:3d} ({results['B']/total_games*100:5.1f}%)")
    print(f"Draws:                     {results['Draw']:3d} ({results['Draw']/total_games*100:5.1f}%)")
    if results['Error'] > 0:
        print(f"Errors:                    {results['Error']:3d} ({results['Error']/total_games*100:5.1f}%)")

    print(f"\nTotal games: {total_games}")

    # Additional analysis
    if results['R'] + results['B'] > 0:
        decisive_games = results['R'] + results['B']
        print()
        print("=" * 70)
        print(f"DECISIVE GAMES ANALYSIS ({decisive_games} games with a winner)")
        print("=" * 70)
        print(f"Red (Aggressive) win rate:   {results['R']/decisive_games*100:.1f}%")
        print(f"Blue (Defensive) win rate:   {results['B']/decisive_games*100:.1f}%")
        print()

        # Determine winner
        if results['R'] > results['B']:
            margin = results['R'] - results['B']
            print(f"🏆 WINNER: Red AI (Aggressive Connector Strategy)")
            print(f"   Victory margin: {margin} games ({margin/total_games*100:.1f}%)")
        elif results['B'] > results['R']:
            margin = results['B'] - results['R']
            print(f"🏆 WINNER: Blue AI (Defensive Territory Strategy)")
            print(f"   Victory margin: {margin} games ({margin/total_games*100:.1f}%)")
        else:
            print(f"⚖️  TIE: Both strategies won equal number of games!")

    print()
    print("=" * 70)

    return results

if __name__ == "__main__":
    run_strategy_battle(100)
