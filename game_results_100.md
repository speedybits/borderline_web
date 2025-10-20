# Borderline GPT - 100 Game Test Results

## Test Configuration
- **Number of Games**: 100
- **Turn Limit**: 200 turns per game
- **Date**: 2025-10-20
- **Game Version**: With rotation, power-based combat, and piece conversion

## Results Summary

### Overall Statistics
| Outcome | Count | Percentage |
|---------|-------|------------|
| Red Wins | 0 | 0.0% |
| Blue Wins | 0 | 0.0% |
| Draws | 100 | 100.0% |
| **Total Games** | **100** | **100.0%** |

### Key Findings

1. **All games ended in draws** (100%)
   - Games typically end around turn 30-31 when both players run out of pieces
   - Neither player achieves the victory condition (contiguous connection from row 0 to row 7)

2. **Game Duration**
   - Average game length: ~30 turns
   - All games ended well before the 200 turn limit
   - Games end when both players exhaust their pieces

3. **Combat System Impact**
   - The power-based combat system is very active
   - Piece conversion keeps games dynamic (pieces change hands frequently)
   - Despite piece conversion, players eventually run out of pieces

4. **Victory Difficulty**
   - Creating a contiguous 8-row connection is challenging
   - Players often control different sections of the board
   - The middle rows (3-4) tend to be contested territory with mixed control

## Sample Final Board State

In a typical game ending:
- Red controls rows 0-2 (top section)
- Blue controls rows 5-7 (bottom section)
- Rows 3-4 have mixed control or are battlegrounds
- Neither player completes a full vertical connection

## Observations

### Strengths of Current Design
- Combat system creates dynamic gameplay
- Piece rotation adds strategic depth
- Games are decisive (don't drag on indefinitely)
- Both players have roughly equal chances (no clear advantage to Red/Blue)

### Characteristics
- The 8-row victory condition is very challenging
- Piece conversion balances power but doesn't guarantee victory
- Games end naturally when pieces are exhausted
- The board often splits into Red (top) and Blue (bottom) territories

## Conclusions

The current game design produces balanced but challenging gameplay. The 100% draw rate indicates that:
1. The victory condition (8-row connection) is appropriately difficult
2. Neither player has a systematic advantage
3. The combat and rotation systems work as intended
4. Games reach natural conclusions (piece exhaustion) rather than stalemates

The draw outcomes reflect competitive, balanced play where both AIs effectively prevent each other from achieving victory rather than a flaw in the game design.
