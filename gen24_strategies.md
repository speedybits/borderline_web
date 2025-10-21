# Potential Strategies for Gen 24-40

## Current Status
- Gen 21: 50% win rate (4-4) - Extreme edge runner
- Gen 22: 71% win rate (5-2) - Same as Gen 21 (variance)
- Gen 23: RUNNING - Multi-path edge runner with row-skipping
- Target: 90%+ win rate

## If Gen 23 < 90%: Strategy Options

### Option A: Sacrifice Strategy (Gen 24-26)
**Philosophy**: Intentionally lose battles to convert Blue pieces to Red

**Key Parameters**:
- Lower combat power preference initially
- High piece count in hand bonus
- After conversion, extremely high vertical push
- Target weak Blue pieces (low pip count)
- Convert them, then use converted pieces aggressively

**Hypothesis**: More Red pieces on board = better coverage and blocking

---

### Option B: Diagonal Infiltration (Gen 27-29)
**Philosophy**: Instead of pure vertical, use diagonal paths to slip around Blue's blocking

**Key Parameters**:
- Bonus for diagonal connectivity (row+col or row-col constant)
- Still prefer edges but allow diagonal movement through less-blocked zones
- Lower vertical urgency, higher spatial coverage
- Build "lattice" structure instead of direct paths

**Hypothesis**: Blue's blocking is vertical-focused; diagonal paths might be less defended

---

### Option C: Tempo Control (Gen 30-32)
**Philosophy**: Block Blue's expansion while building own paths

**Key Parameters**:
- High bonus for placing where Blue wants to place
- Counter-blocking: occupy Blue's target rows (3-4) on edges
- Defensive positioning in Red's rows (0-2)
- Only push vertically when Blue is blocked

**Hypothesis**: If Blue can't expand, Red wins by default

---

### Option D: Piece Rotation Exploitation (Gen 33-35)
**Philosophy**: Maximize strategic use of rotation for optimal placement

**Key Parameters**:
- Bonus for placements that create multiple connection points
- Prefer pieces that can rotate to fit gaps
- Rotation-aware path planning
- Value "connector" pieces that link disconnected regions

**Hypothesis**: Better rotation usage creates more placement options and better connectivity

---

### Option E: Adaptive Aggression (Gen 36-38)
**Philosophy**: Change strategy based on board state

**Key Parameters**:
- Early game: Build safely in home territory
- Mid game: High combat to clear paths
- Late game: Sprint to victory with converted pieces
- Dynamic scoring that changes based on turn count
- Board state analysis (if ahead, consolidate; if behind, attack)

**Hypothesis**: Optimal strategy changes as game progresses

---

### Option F: Extreme Vertical Sprint (Gen 39-40)
**Philosophy**: Push vertical score to 100+ and ignore everything else

**Key Parameters**:
- Vertical progress: 100 pts/row
- Connection: 60x
- Minimal everything else
- Pure speed approach
- Ignore combat unless blocking path

**Hypothesis**: Sometimes simplicity wins - just rush as fast as possible

---

## Combination Strategies

If individual approaches don't work, combine elements:

**Gen 36-37**: Edge Runner + Sacrifice
**Gen 38-39**: Tempo Control + Diagonal
**Gen 40**: Best elements from all previous generations

---

## Analysis Approach

After each generation:
1. Record win rate and decisive game count
2. If improvement: Continue in that direction (small tweaks)
3. If regression: Try next strategy option
4. If plateau: Combine multiple approaches
5. Track which parameters correlate most with wins

---

## Target Milestones

- Gen 25: Aim for 75%+
- Gen 30: Aim for 80%+
- Gen 35: Aim for 85%+
- Gen 40: Achieve 90%+ or document why it's impossible

