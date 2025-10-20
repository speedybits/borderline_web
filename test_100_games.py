#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from borderline_gpt import BorderlineGPT

def run_silent_game():
    """Run a single game silently and return the winner"""
    game = BorderlineGPT()
    
    # Disable all print statements by redirecting stdout
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    
    try:
        # Run the game loop silently
        while not game.game_over and game.turn_count < 200:  # Increased limit for thorough games
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
        return 'Error'

def run_100_games():
    """Run 100 games and collect statistics"""
    print("Running 100 games of Borderline GPT...")
    print("This may take a moment...\n")
    
    results = {'R': 0, 'B': 0, 'Draw': 0, 'Error': 0}
    
    for game_num in range(1, 101):
        if game_num % 10 == 0:
            print(f"Completed {game_num} games...")
        
        result = run_silent_game()
        results[result] += 1
    
    # Calculate percentages
    total_games = sum(results.values())
    
    print(f"\n=== RESULTS AFTER {total_games} GAMES ===")
    print(f"Red wins:     {results['R']:3d} ({results['R']/total_games*100:5.1f}%)")
    print(f"Blue wins:    {results['B']:3d} ({results['B']/total_games*100:5.1f}%)")
    print(f"Draws:        {results['Draw']:3d} ({results['Draw']/total_games*100:5.1f}%)")
    if results['Error'] > 0:
        print(f"Errors:       {results['Error']:3d} ({results['Error']/total_games*100:5.1f}%)")
    
    print(f"\nTotal games: {total_games}")
    
    # Additional analysis
    if results['R'] + results['B'] > 0:
        decisive_games = results['R'] + results['B']
        print(f"\nOf {decisive_games} decisive games:")
        print(f"Red win rate: {results['R']/decisive_games*100:.1f}%")
        print(f"Blue win rate: {results['B']/decisive_games*100:.1f}%")

if __name__ == "__main__":
    run_100_games()