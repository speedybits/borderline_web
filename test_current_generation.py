#!/usr/bin/env python3
"""Simple test runner for current generation strategies"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from borderline_gpt import BorderlineGPT

def run_generation_test(num_games=100):
    """Run games and return results"""
    results = {'R': 0, 'B': 0, 'Draw': 0, 'Error': 0}

    for game_num in range(1, num_games + 1):
        game = BorderlineGPT(red_strategy='aggressive', blue_strategy='defensive')

        # Silence output
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

        try:
            while not game.game_over and game.turn_count < 200:
                game.play_turn()

            sys.stdout.close()
            sys.stdout = original_stdout

            if game.winner:
                results[game.winner.color] += 1
            else:
                results['Draw'] += 1

        except Exception as e:
            sys.stdout.close()
            sys.stdout = original_stdout
            results['Error'] += 1

    return results

if __name__ == "__main__":
    print("Running 100 games...")
    results = run_generation_test(100)
    print(f"Red: {results['R']}, Blue: {results['B']}, Draw: {results['Draw']}")
