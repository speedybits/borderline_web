# Borderline GPT

## Overview

Borderline GPT is a strategic ASCII-based board game for two AI players (Red and Blue). Players compete to create a contiguous connection of their colored PIPs across the entire length of the board while engaging in dice-based combat when their pieces come into contact.

## Game Setup

- **Board Size**: 6 squares wide × 8 squares long (48 total squares)
- **Players**: Two AI-controlled players (Red and Blue)
- **Starting Pieces**: Each player begins with 15 randomly generated pieces
- **Objective**: Create a contiguous connection across the board's 8-square length

## Game Board

Each empty square on the board is represented as a 3×3 ASCII grid:

```
 ____
|_|_|_|
|_|_|_|
|_|_|_|
```

The complete board displays all 48 squares in a 6×8 arrangement.

## Game Pieces

Each game piece consists of 9 PIPs arranged in a 3×3 grid. PIPs can be either:
- **Filled**: Marked with the player's letter ('R' for Red, 'B' for Blue)
- **Empty**: Marked with underscore ('_')

### Piece Generation Rules:
- **Center PIP**: Always filled with the player's color
- **Row Distribution**: Each piece must have at least one PIP in each of the 3 rows of the 3×3 grid
- **PIP Count Probability**: 
  - 80% chance: Exactly 3 PIPs (minimum required)
  - 20% chance: 4-9 PIPs with additional random placement
- **Examples**:

Blue piece with 3 filled PIPs:
```
 ____
|_|_|B|
|_|B|_|
|B|_|_|
```

Red piece with 4 filled PIPs:
```
 ____
|R|_|R|
|_|R|_|
|_|R|_|
```

## Game Rules

### Rule 0: Turn Structure
Players alternate turns, placing one piece per turn. Before placing, a piece may be rotated 90°, 180°, or 270° clockwise around its center PIP to provide more placement options.

### Rule 1: Starting Row Placement
- **Red Player**: Can always place pieces in the top row (row 0)
- **Blue Player**: Can always place pieces in the bottom row (row 7)
- Pieces placed in the starting row do not require adjacency to existing pieces
- **First piece requirement**: Each player's first piece MUST be placed in their starting row

### Rule 2: Adjacency Requirement
For pieces placed outside the starting row, they must be placed adjacent to an existing piece of the same color, with at least one PIP of the new piece touching a PIP of the existing piece.

**Adjacent means**: Horizontally or vertically neighboring squares (not diagonal)

**PIP Contact Rules**:
- The touching PIPs must be on the edges where squares meet
- PIPs are orthogonally adjacent when they align across the boundary between two pieces
- When pieces are placed vertically (one above/below the other), the top edge of the lower piece must align with the bottom edge of the upper piece
- When pieces are placed horizontally (side-by-side), the left edge of the right piece must align with the right edge of the left piece
- At least one filled PIP on the touching edge of the new piece must align with a filled PIP on the touching edge of the existing piece

**Visual Examples**:

Two pieces placed vertically:
```
|R|_|_|
|_|R|_|
|R|_|_|  ← Bottom edge of upper piece
─────────  (boundary)
|R|_|R|  ← Top edge of lower piece (PIP at column 0 touches!)
|_|R|_|
|R|_|_|
```

Two pieces placed horizontally:
```
|R|_|_|| | |R|
|_|R|R||R|R| |  ← PIPs touch at the boundary (middle row)
|R|_|_|| | |R|
```

**Invalid Placement Example**:
```
|R|_|_|
|_|R|_|
|_|_|R|  ← Bottom edge has PIP at column 2
─────────  (boundary)
|R|_|_|  ← Top edge has PIP at column 0 (NO alignment - invalid!)
|_|R|_|
|_|_|R|
```

### Rule 3: Victory Condition
A player wins by creating a contiguous connection of their colored PIPs spanning the entire board length (from row 0 to row 7). The connection must be unbroken and consist only of the winning player's PIPs.

### Rule 4: Out of Pieces
If a player has no pieces remaining, they skip their turn.

### Rule 5: Game End
The game ends when both players have no pieces left to place, or when a player achieves victory.

### Rule 6: Piece Rotation
Pieces can be rotated before placement to maximize strategic options:
- **Rotation Options**: 0° (no rotation), 90° clockwise, 180°, or 270° clockwise
- **Center PIP**: Always remains at position [1][1] during rotation
- **Rotation Mechanics**: PIPs rotate around the center using coordinate transformation
- **Strategic Value**: Provides 4x placement options per piece, enabling better adjacency matching

**Rotation Example**:
```
Original:           90° Clockwise:
|_|B|_|             |_|_|_|
|_|B|_|      →      |_|B|B|
|_|_|B|             |B|_|_|
```

### Rule 7: Combat System
When a newly placed piece has PIPs adjacent to enemy PIPs, combat is initiated:

**Power Calculation**:
- Each piece has a **power level** = number of PIPs ÷ 2 (rounded down)
- Example: 3 PIPs = power 1, 5 PIPs = power 2, 9 PIPs = power 4

**Combat Resolution**:
1. **Attacker**: Newly placed piece rolls a 6-sided die + its power level
2. **Defenders**: All adjacent enemy pieces combine their power, roll one die + combined power
3. **Winner**: Highest total wins (attacker wins ties)
4. **Multiple Defenders**: If multiple enemy pieces are adjacent, they fight as a combined force

**Combat Outcome**:
- **If attacker loses**: Attacking piece is removed from board, converted to defender's color, and added to defender's hand
- **If defenders lose**: All defending pieces are removed from board, converted to attacker's color, and added to attacker's hand
- **Piece Conversion**: Losing pieces change color (all 'R' PIPs become 'B' or vice versa) and join the winner's hand as usable pieces

**Combat Example**:
```
Attacker (Red, 5 PIPs, power 2): Roll 4 + 2 = 6
Defender (Blue, 3 PIPs, power 1): Roll 3 + 1 = 4
Result: Red wins! Blue piece converts to Red and is added to Red's hand
```

## Strategic Elements

### AI Decision Making
The AI players evaluate moves based on:
- **Victory potential**: Moves that create or extend winning connections
- **Blocking**: Preventing opponent victories
- **Territory control**: Securing strategic board positions
- **Piece efficiency**: Maximizing the value of pieces with more PIPs
- **Combat considerations**: Risk/reward of engaging in combat (power-based calculations)
- **Rotation optimization**: Trying all 4 rotations to find optimal placement

### Key Strategic Concepts
- **Connection building**: Creating long chains of connected PIPs
- **Territorial control**: Dominating key areas of the board
- **Combat timing**: Knowing when to engage in risky battles (considering power levels)
- **Resource management**: Efficiently using limited pieces and captured pieces
- **Piece conversion**: Winning combat grows your piece count while reducing opponent's
- **Defensive play**: Blocking opponent progress while advancing your own
- **Rotation tactics**: Using rotation to create adjacency where it wouldn't otherwise exist

## Implementation Details

The game is implemented in Python with:
- Object-oriented design (GameBoard, GamePiece, AIPlayer classes)
- Piece rotation system with coordinate transformation
- Power-based combat with multiple defender support
- Piece conversion mechanics (color change and hand transfer)
- Flood-fill algorithms for victory detection
- Strategic AI with move evaluation across all rotations
- Real-time ASCII display with combat highlighting
- Comprehensive rule enforcement

## Running the Game

Execute the Python script to watch two AI players compete:

```bash
python3 borderline_gpt.py
```

The game displays the board state after each turn, showing piece placements, rotations, combat results (with power calculations), piece conversions, and strategic decisions made by both AI players.

## Display Format

Below the main game board, all remaining pieces (not yet placed on the board) are displayed in two rows:
- **Red Player Row**: Shows all Red player's remaining pieces in their hand (includes original pieces and converted captures)
- **Blue Player Row**: Shows all Blue player's remaining pieces in their hand (includes original pieces and converted captures)

Each piece is displayed with its full 3×3 PIP pattern with clear spacing between pieces to avoid visual confusion. This allows players to see what pieces are available for future placement and provides strategic visibility into remaining resources and piece variety.

**Visual Indicators**:
- **Lowercase letters** (r, b): Highlight pieces involved in combat or newly placed pieces
- **Uppercase letters** (R, B): Standard piece display
- Piece counts shown in parentheses update as pieces are placed and captured






