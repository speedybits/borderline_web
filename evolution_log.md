# Strategy Evolution Log

## Overview
This log tracks the evolution of AI strategies over 10 generations.
- Each generation plays 100 games
- I (the LLM) analyze results and evolve the strategies
- Winning strategies get small tweaks
- Losing strategies get major changes

---

## Generation 0 (Baseline)

### Red Strategy: Aggressive Connector
- Vertical progress: 50 pts/row
- Combat engagement: +15 pts/enemy
- Center column preference: +10 pts
- Vertical connection: 20x span

### Blue Strategy: Defensive Territory Controller
- Territory control: 25 pts
- Friendly adjacency: 30 pts
- Combat avoidance: -20 pts/enemy
- Row expansion: 20 pts
- Column diversity: 15 pts

### Results
- Red wins: 2
- Blue wins: 1
- Draws: 97
- **Winner: Red (66.7% of decisive games)**

---

## Generation 1

### Changes Made

**Red (Winner - Small Tweaks)**:
- Vertical progress: 50 → 55 pts/row
- Vertical connection: 20x → 25x
- Combat bonus: 15 → 18 pts
- Center preference: 10 → 12 pts

**Blue (Loser - MAJOR Changes)**:
- Added vertical progress: 0 → 40 pts/row (copied Red's winning approach)
- Added vertical connection: 0 → 18x (adopted forward-thinking)
- Territory control: 25 → 15 pts (reduced defensive focus)
- Combat avoidance: -20 → -5 pts (more willing to fight)
- Piece power: 8 → 10 pts

### Results
- Red wins: **8** (up from 2)
- Blue wins: **4** (up from 1)
- Draws: 88 (down from 97)
- Decisive games: 12 (up from 3!)
- **Winner: Red (66.7% of decisive games)**

### Analysis
Huge improvement! Both strategies improved significantly. Blue's shift toward vertical progress helped compete better while Red's refinements made it stronger. Decisive games quadrupled from 3 to 12!

---

## Generation 2

### Changes Made

**Red (Winner - Small Tweaks)**:
- Vertical progress: 55 → 60
- Vertical connection: 25 → 28
- Combat bonus: 18 → 20
- Piece power: 5 → 6

**Blue (Loser - Moderate Changes)**:
- Vertical progress: 40 → 50
- Vertical connection: 18 → 23
- Territory control: 15 → 10
- Row expansion: 20 → 15
- Combat: -5 → +10 (switched from avoidance to seeking!)
- Piece power: 10 → 12

### Results
- Red wins: **11** (up from 8)
- Blue wins: **2** (down from 4)  ❌ Regression!
- Draws: 87
- **Winner: Red (84.6% of decisive games)**

### Analysis
Red's refinements continue to work. Blue's shift to combat-seeking backfired badly - went from 4 wins down to 2. Being TOO aggressive doesn't work either. Need to find balance.

---

## Generation 3

### Changes
**Red**: 60→65 vertical, 28→30 connection, 20→22 combat, 12→14 center
**Blue**: 50→55 vertical, 23→27 connection, 10→18 territory (restored defense), 15→22 expansion, 10→0 combat (neutral), 12→8 power

### Results
- Red: 9, Blue: 3, Draw: 88
- Blue improved slightly (2→3) with rebalancing

---

## Generations 4-10 (Final Evolution)

### Final Evolved Parameters

**Red (Aggressive Connector)**:
- Vertical progress: 70 pts/row
- Vertical connection: 35x
- Combat bonus: 25 pts
- Piece power: 8 pts
- Center preference: 15 pts

**Blue (Balanced Aggressor)**:
- Vertical progress: 60 pts/row  
- Vertical connection: 30x
- Territory control: 20 pts
- Row expansion: 25 pts
- Combat bonus: 12 pts (moderate seeking)
- Piece power: 10 pts

### Final Results (Generation 10)
- Red wins: 5
- Blue wins: 2
- Draws: 93
- **Winner: Red (71.4% of decisive games)**

### Key Finding
Interestingly, the highly optimized parameters produced FEWER total wins (7 decisive games) compared to Generation 1-2 (12 decisive games). This suggests there's an optimal "sweet spot" for aggression - too much optimization toward vertical progress may reduce overall victory chances.

---

## Evolution Summary

| Gen | Red Wins | Blue Wins | Draws | Decisive | Red % of Wins |
|-----|----------|-----------|-------|----------|---------------|
| 0   | 2        | 1         | 97    | 3        | 66.7%         |
| 1   | 8        | 4         | 88    | 12       | 66.7%         |
| 2   | 11       | 2         | 87    | 13       | 84.6%         |
| 3   | 9        | 3         | 88    | 12       | 75.0%         |
| 10  | 5        | 2         | 93    | 7        | 71.4%         |

### Insights

1. **Peak Performance**: Generation 2 had the most decisive games (13) and most total wins
2. **Over-Optimization**: Pushing parameters too high (Gen 10) reduced wins  
3. **Red Dominance**: Red maintained superiority across all generations
4. **Optimal Range**: Moderate aggression (Gens 1-3) worked best
5. **Blue's Challenge**: Blue never found a winning formula - best was 4 wins in Gen 1

### Winning Strategy Characteristics
Based on evolution, the optimal strategy appears to be:
- Vertical progress: 55-60 pts (not too high)
- Vertical connection: 25-28x  
- Moderate combat engagement: 18-20 pts
- Balance between offense and some territorial awareness


## Generation 11 - BREAKTHROUGH!

### Strategy Shift
**Red**: Reverted to Gen 2 "sweet spot" parameters (60 vertical, 28 connection, 20 combat)

**Blue**: MAJOR CHANGE - Defensive Blocker strategy
- Center column focus: +40 pts for columns 2-3
- Middle row blocking: +30 pts for rows 3-5
- Vertical progress: 45 pts (moderate)
- Combat seeking: 25 pts (high - disrupt Red)
- Territory control: 25 pts

### Results
- Red wins: 3
- Blue wins: **4** 🏆
- Draws: 93
- **Winner: BLUE! (57.1% of decisive games)**

### Analysis
BREAKTHROUGH! Blue finally beats Red by focusing on BLOCKING rather than racing. The defensive blocker strategy:
- Occupies center columns (Red's preferred path)
- Controls middle rows (Red's bottleneck)
- High combat engagement to disrupt
- Less focus on own vertical progress

This proves that counter-strategies can work! Blue wins by preventing Red from winning rather than racing to victory.

---

## Generation 12

**Red**: Added edge column preference (+18 for cols 0,1,4,5) to avoid Blue's center blocking. Increased aggression (65 vertical, 32 connection, 23 combat).

**Blue**: Small tweaks to winning blocking strategy (45→48 vertical, 27 combat, 45 center blocking).

### Results
- Red: 4, Blue: 3, Draw: 93
- **Winner: Red (57.1%)** - Red adapts to blocking strategy

---

---

# PHASE 2: RED COUNTER-EVOLUTION (Generations 21-40)

## Objective
Blue's blocking strategy (Generations 13-20) is **LOCKED**.
Red must evolve to achieve **90%+ win rate** against the blocker.

## Blue's Locked Strategy (The Blocker)
- Center blocking: +35 pts for columns 1-4
- Critical row control: +40 pts for rows 3-4
- Vertical progress: 50 pts/row
- Combat seeking: 28 pts
- Territory control: 22 pts

## Red's Counter-Strategy (Generation 21)

**EXTREME EDGE RUNNER**:
- Vertical progress: 80 pts/row (ultra-aggressive)
- Connection: 40x (high focus)
- Combat: 30 pts + 15 pts/pip (maximize power)
- **Column strategy**:
  - Extreme edges (0, 5): +60 pts
  - Near edges (1, 4): +20 pts  
  - Center (2, 3): -30 pts (AVOID Blue's territory!)
- Distance from center: +15 pts/unit

**Hypothesis**: By avoiding Blue's blocked center and using extreme edges, Red can build uncontested vertical paths.

