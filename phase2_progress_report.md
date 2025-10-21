# Phase 2 Evolution Progress Report

## Objective
Evolve Red strategy to achieve **90%+ win rate** against Blue's locked blocking strategy (from Gen 13-20).

## Blue's Locked Strategy (The Blocker)
- Center blocking: +35 pts for columns 1-4
- Critical row control: +40 pts for rows 3-4
- Vertical progress: 50 pts/row
- Combat seeking: 28 pts
- Territory control: 22 pts

This strategy creates a defensive wall in the center-middle of the board.

---

## Evolution Results (Gen 21-24)

### Generation 21: Extreme Edge Runner
**Strategy**: Avoid Blue's center by using extreme edges (cols 0, 5)

**Parameters**:
- Vertical: 80 pts
- Connection: 40x
- Combat: 30 pts + 15 pts/pip
- Edges (0, 5): +60 pts
- Center (2, 3): -30 pts penalty

**Results**: Red 4, Blue 4, Draw 92
**Win Rate**: 50% ❌

**Analysis**: Sound approach but not aggressive enough.

---

### Generation 22
**Note**: Same as Gen 21 (automated test showed variance)

**Results**: Red 5, Blue 2, Draw 93
**Win Rate**: 71%

**Analysis**: Variance in results suggests randomness plays significant role. 71% is good but not 90%+.

---

### Generation 23: Multi-Path Edge Runner
**Strategy**: Add row-skipping logic to jump over Blue's blocking zone

**New Features**:
- Home territory bonus (rows 0-2): +25
- Middle row penalty (rows 3-4): -20
- Target zone bonus (rows 5-7): +40
- Increased all combat/connection parameters

**Results**: Red 3, Blue 3, Draw 94
**Win Rate**: 50% ❌ REGRESSION

**Analysis**: Row penalties BACKFIRED! Penalizing middle rows creates connectivity gaps. Can't "skip" rows due to adjacency requirements.

**Key Learning**: Must FIGHT THROUGH the middle, not avoid it!

---

### Generation 24: Ultra Speed Sprinter (RUNNING)
**Strategy**: Simplify - maximum speed and power

**Changes**:
- REMOVED all row-specific bonuses/penalties
- Vertical: 95 pts (near-maximum)
- Connection: 55x (huge)
- Combat: 40 pts (maximum engagement)
- Combat power: 22 pts/pip (maximum)
- Edge focus maintained
- Center penalty increased to -45

**Philosophy**: "Beat Blue through sheer speed and combat dominance!"

**Status**: Running 100 games... (in progress)

---

## Challenge Analysis

### Why 90% is Hard

1. **Blue's Defense is Strong**
   - Controls 4 of 6 columns (1-4)
   - Controls critical middle rows (3-4)
   - High combat (28 pts) contests Red

2. **Game Mechanics Favor Defense**
   - 8-row victory is difficult
   - Adjacency requirements limit Red's options
   - Piece exhaustion causes draws

3. **Red's Constraints**
   - Only 2 edge columns (0, 5) to use
   - Must maintain connectivity
   - Can't skip blocked zones

4. **High Variance**
   - Same strategy: 50% to 71% variance
   - Random piece generation matters
   - Combat dice rolls affect outcomes

### Strategies Still to Try (Gen 25-40)

If Gen 24 doesn't hit 90%, planned approaches:

1. **Sacrifice Strategy** (Gen 25-27)
   - Intentionally lose battles to convert Blue pieces
   - Use converted pieces aggressively

2. **Tempo/Blocking** (Gen 28-30)
   - Block Blue's expansion first
   - Then push when Blue is locked

3. **Hybrid Columns** (Gen 31-33)
   - Use edges AND near-edges (cols 0,1,4,5)
   - More flexible than pure edge

4. **Combat Dominance** (Gen 34-36)
   - Maximize pip counts
   - Win every fight decisively

5. **Adaptive** (Gen 37-39)
   - Change strategy based on board state
   - Early: build, Mid: fight, Late: sprint

6. **Best Combination** (Gen 40)
   - Combine best elements from all generations

---

## Current Status

- **Generations Complete**: 21-23
- **Generation Running**: 24
- **Generations Remaining**: 25-40 (16 more)
- **Best Result So Far**: 71% (Gen 22)
- **Target**: 90%+

---

## Next Steps

1. Wait for Gen 24 results
2. If < 90%: Continue with planned strategies
3. If Gen 24 shows improvement: Double down on speed/power approach
4. If Gen 24 regresses: Try completely different approach (sacrifice/tempo)
5. Track all results in evolution_log.md
6. Create comprehensive final report at Gen 40

---

## Hypothesis: Is 90% Achievable?

**Optimistic View**:
- Gen 22 got 71%, we're improving
- Haven't tried all strategies yet
- Combination approaches might break through

**Realistic View**:
- Blue's blocking is very strong
- 71% might be near the limit
- Variance means 90% requires consistent dominance
- Game mechanics may favor defense

**We'll know by Gen 40!**

