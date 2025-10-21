#!/usr/bin/env python3
"""
Batch evolution runner for Generations 24-40
This allows me to define multiple strategy variations and test them sequentially
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from borderline_gpt import BorderlineGPT
import copy

def run_test(num_games=100):
    """Run games and return results"""
    results = {'R': 0, 'B': 0, 'Draw': 0}

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
            print(f"Error in game {game_num}: {e}")

    return results

def calculate_win_rate(results):
    """Calculate Red's win percentage of decisive games"""
    decisive = results['R'] + results['B']
    if decisive == 0:
        return 0
    return (results['R'] * 100) // decisive

# Strategy definitions for generations 24-30
# Each generation is defined by parameters that will be applied to AggressiveConnectorAI

strategies = {
    24: {
        "name": "Sacrifice Converter",
        "description": "Lower combat to lose battles, gain converted pieces",
        "params": {
            "vertical": 90,
            "connection": 50,
            "combat": 20,  # Reduced from 35
            "pip_power": 12,  # Reduced from 18 (prefer losing)
            "edges": [75, 40],  # Still edges
            "home_bonus": 30,
            "target_bonus": 45,
        }
    },
    25: {
        "name": "Ultra Speed",
        "description": "Maximum vertical, minimum everything else",
        "params": {
            "vertical": 100,  # MAX
            "connection": 60,
            "combat": 25,
            "pip_power": 20,  # Want to win when necessary
            "edges": [80, 45],
            "home_bonus": 35,
            "target_bonus": 50,
        }
    },
    26: {
        "name": "Tempo Blocker",
        "description": "Block Blue's expansion before pushing",
        "params": {
            "vertical": 75,  # Lower - not rushing yet
            "connection": 40,
            "combat": 40,  # HIGH - must fight
            "pip_power": 22,
            "edges": [70, 35],
            "middle_penalty": -30,  # NEW - block Blue's rows 3-4
            "home_bonus": 40,  # Build strong base
        }
    },
}

if __name__ == "__main__":
    print("Batch Evolution Runner - Gen 24-26")
    print("=" * 50)

    for gen_num in [24, 25, 26]:
        strategy = strategies[gen_num]
        print(f"\nGen {gen_num}: {strategy['name']}")
        print(f"Strategy: {strategy['description']}")
        print("Running 100 games...")

        # NOTE: This script defines strategies but doesn't modify borderline_gpt.py
        # I'll need to manually update the code with each generation's parameters

        print("(Requires manual parameter update in borderline_gpt.py)")
        print("See gen24_strategies.md for full details")
