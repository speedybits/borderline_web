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
Players alternate turns, placing one piece per turn.

### Rule 1: Initial Placement
- **Red Player**: Must place first piece in the top row (row 0) if no Red pieces exist there
- **Blue Player**: Must place first piece in the bottom row (row 7) if no Blue pieces exist there

### Rule 2: Adjacency Requirement
After the initial piece, all subsequent pieces must be placed adjacent to an existing piece of the same color, with at least one PIP of the new piece touching a PIP of the existing piece.

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

### Rule 6: Combat System
When a newly placed piece has PIPs adjacent to enemy PIPs:
1. Each player rolls a 6-sided die
2. The player with the higher roll wins
3. The losing piece is removed from the board and returned to its owner's hand
4. In case of ties, the attacking player (who just placed the piece) loses

## Strategic Elements

### AI Decision Making
The AI players evaluate moves based on:
- **Victory potential**: Moves that create or extend winning connections
- **Blocking**: Preventing opponent victories
- **Territory control**: Securing strategic board positions
- **Piece efficiency**: Maximizing the value of pieces with more PIPs
- **Combat considerations**: Risk/reward of engaging in combat

### Key Strategic Concepts
- **Connection building**: Creating long chains of connected PIPs
- **Territorial control**: Dominating key areas of the board
- **Combat timing**: Knowing when to engage in risky battles
- **Resource management**: Efficiently using limited pieces
- **Defensive play**: Blocking opponent progress while advancing your own

## Implementation Details

The game is implemented in Python with:
- Object-oriented design (GameBoard, GamePiece, AIPlayer classes)
- Flood-fill algorithms for victory detection
- Strategic AI with move evaluation
- Real-time ASCII display
- Comprehensive rule enforcement

## Running the Game

Execute the Python script to watch two AI players compete:

```bash
python3 borderline_gpt.py
```

The game displays the board state after each turn, showing piece placements, combat results, and strategic decisions made by both AI players.

## Display Format

Below the main game board, all remaining pieces (not yet placed on the board) are displayed in two rows:
- **Red Player Row**: Shows all Red player's remaining pieces in their hand
- **Blue Player Row**: Shows all Blue player's remaining pieces in their hand

Each piece is displayed with its full 3×3 PIP pattern with clear spacing between pieces to avoid visual confusion. This allows players to see what pieces are available for future placement and provides strategic visibility into remaining resources and piece variety.






