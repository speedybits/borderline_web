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

