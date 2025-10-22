#!/usr/bin/env python3
"""Optimize Red strategy to win >90% against random Blue"""

from borderline_gpt import BorderlineGPT
import sys
import os

def test_strategy(red_strategy, num_games=100, description=""):
    """Test a strategy and return win rate"""
    results = {'R': 0, 'B': 0, 'Draw': 0}
    total_turns = 0
    max_turns = 0

    print(f"\n{'='*70}")
    print(f"Testing: {description}")
    print(f"Strategy: {red_strategy}")
    print(f"Turn limit: 10000 (effectively unlimited)")
    print(f"{'='*70}")

    for i in range(num_games):
        game = BorderlineGPT(red_strategy=red_strategy, blue_random=True)

        # Silence output
        sys.stdout = open(os.devnull, 'w')
        while not game.game_over and game.turn_count < 10000:  # Very high limit instead of no limit
            game.play_turn()
        sys.stdout = sys.__stdout__

        total_turns += game.turn_count
        max_turns = max(max_turns, game.turn_count)

        if game.winner:
            results[game.winner.color] += 1
        else:
            results['Draw'] += 1

        if (i+1) % 20 == 0:
            avg_turns = total_turns / (i+1)
            print(f"  Progress: {i+1}/{num_games} games - R:{results['R']} B:{results['B']} D:{results['Draw']} - Avg turns: {avg_turns:.1f}")

    decisive = results['R'] + results['B']
    if decisive > 0:
        red_pct = (results['R'] * 100.0) / decisive
        total_pct = (results['R'] * 100.0) / num_games
    else:
        red_pct = 0
        total_pct = 0

    avg_turns = total_turns / num_games if num_games > 0 else 0

    print(f"\nResults: Red={results['R']} Random={results['B']} Draw={results['Draw']}")
    print(f"Red win rate: {red_pct:.1f}% of decisive games ({decisive} decisive)")
    print(f"Red win rate: {total_pct:.1f}% of all games")
    print(f"Average turns per game: {avg_turns:.1f}")
    print(f"Maximum turns in any game: {max_turns}")

    return results, red_pct, total_pct

# Test different strategies (focusing on aggressive which performed best)
strategies = [
    ('aggressive', 'Aggressive Strategy vs Random (NO TURN LIMIT)'),
]

results_summary = []

for strategy, desc in strategies:
    results, decisive_pct, total_pct = test_strategy(strategy, 100, desc)
    results_summary.append((strategy, desc, results, decisive_pct, total_pct))

# Print summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
for strategy, desc, results, decisive_pct, total_pct in results_summary:
    print(f"{desc:30s} | R:{results['R']:3d} B:{results['B']:3d} D:{results['Draw']:3d} | {decisive_pct:5.1f}% (decisive) | {total_pct:5.1f}% (all)")

# Find best
best = max(results_summary, key=lambda x: x[4])  # Sort by total_pct
print(f"\nBest strategy: {best[1]} with {best[4]:.1f}% win rate")

if best[4] >= 90:
    print(f"\n✓✓✓ SUCCESS! Strategy '{best[0]}' achieves >90% win rate!")
else:
    print(f"\n✗ Need to develop better strategy. Current best: {best[4]:.1f}%")
    print("\nSuggestion: The 'aggressive' strategy prioritizes forward movement.")
    print("Against random, this should be very effective.")
