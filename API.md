# Borderline Game API Documentation

## Overview

The Borderline game engine provides a clean JSON-based API for external clients (GUIs, AI engines, replay systems). This API separates game logic from presentation, making it easy to:

- Build different frontends (web, desktop, mobile)
- Create AI players that compete against each other
- Record and replay games
- Test game mechanics
- Develop visualizations and "skins"

## Architecture

```
┌─────────────────────────────────────┐
│   Game Engine (BorderlineGPT)      │
│   - Authoritative game state        │
│   - Move validation & execution     │
│   - Combat resolution               │
│   - Victory conditions              │
│   - Serialization                   │
└─────────────────┬───────────────────┘
                  │
          ┌───────┴───────┐
          │   JSON API    │
          └───────┬───────┘
                  │
     ┌────────────┼────────────┐
     │            │            │
┌────▼───┐  ┌────▼───┐  ┌────▼───┐
│ Web    │  │ CLI    │  │ AI     │
│ GUI    │  │ Viewer │  │ Engine │
└────────┘  └────────┘  └────────┘
```

## Core API Methods

### 1. `execute_move(move_json)` - Execute a move

Execute a player's move and get the complete result.

**Input Format:**
```json
{
  "player": "R",
  "piece_index": 0,
  "position": [0, 3],
  "rotation": 0
}
```

**Fields:**
- `player`: `"R"` or `"B"` - Which player is making the move
- `piece_index`: `0-15` - Index of the piece in the player's hand
- `position`: `[row, col]` - Where to place the piece (row 0-7, col 0-7)
- `rotation`: `0-3` - Number of 90-degree clockwise rotations

**Output Format:**
```json
{
  "valid": true,
  "reason": null,
  "events": [
    {
      "type": "piece_placed",
      "player": "R",
      "row": 0,
      "col": 3,
      "piece": {...}
    },
    {
      "type": "combat",
      "combat_data": {...}
    },
    {
      "type": "piece_removed",
      "reason": "combat_loss",
      "row": 1,
      "col": 3,
      "piece": {...}
    }
  ],
  "game_state": {...},
  "game_over": false,
  "winner": null
}
```

**Fields:**
- `valid`: `true/false` - Whether the move was legal
- `reason`: Error message if invalid, `null` if valid
- `events`: List of events that occurred (placement, combat, removals)
- `game_state`: Complete game state after the move
- `game_over`: `true/false` - Whether the game has ended
- `winner`: `"R"/"B"/null` - Winner if game is over

**Example:**
```python
game = BorderlineGPT()

# Red player places first piece
move = {
    "player": "R",
    "piece_index": 0,
    "position": [0, 3],
    "rotation": 0
}

result = game.execute_move(move)
if result['valid']:
    print(f"Move executed! Turn {result['game_state']['turn']}")
    for event in result['events']:
        print(f"  Event: {event['type']}")
else:
    print(f"Invalid move: {result['reason']}")
```

### 2. `get_game_state()` - Get current game state

Get the complete current state of the game.

**Output Format:**
```json
{
  "game_id": "20250124_143022",
  "turn": 5,
  "current_player": "R",
  "game_over": false,
  "winner": null,
  "board": [
    [null, null, {...}, null, ...],
    [null, {...}, null, {...}, ...],
    ...
  ],
  "players": {
    "R": {
      "name": "Red Player",
      "pieces_remaining": [{...}, {...}, ...],
      "pieces_on_board": 3
    },
    "B": {
      "name": "Blue Player",
      "pieces_remaining": [{...}, {...}, ...],
      "pieces_on_board": 2
    }
  }
}
```

**Fields:**
- `game_id`: Unique identifier for this game session
- `turn`: Current turn number
- `current_player`: `"R"` or `"B"` - Whose turn it is
- `game_over`: Whether the game has ended
- `winner`: Winner if game is over
- `board`: 8x8 grid, each cell is either `null` or a piece object
- `players`: Information about both players

**Piece Object Format:**
```json
{
  "player_color": "R",
  "pips": [
    ["_", "R", "_"],
    ["_", "R", "_"],
    ["_", "R", "_"]
  ],
  "power": 3
}
```

### 3. `get_valid_moves(player_color=None)` - Get all valid moves

Get all legal moves for a player (useful for AI development).

**Parameters:**
- `player_color`: Optional, defaults to current player

**Output:** List of valid move objects
```json
[
  {
    "player": "R",
    "piece_index": 0,
    "position": [0, 3],
    "rotation": 0
  },
  {
    "player": "R",
    "piece_index": 0,
    "position": [0, 4],
    "rotation": 0
  },
  ...
]
```

**Example:**
```python
valid_moves = game.get_valid_moves()
print(f"Player has {len(valid_moves)} valid moves")

# AI can choose one
import random
move = random.choice(valid_moves)
result = game.execute_move(move)
```

### 4. `export_game(filename=None)` - Save game to file

Export the complete game (state + move history) to a JSON file.

**Parameters:**
- `filename`: Optional, defaults to `game_{game_id}.json`

**Returns:** Filename where game was saved

**Example:**
```python
filename = game.export_game()
print(f"Game saved to {filename}")
```

**Output File Format:**
```json
{
  "game_id": "20250124_143022",
  "timestamp": "2025-01-24T14:30:22.123456",
  "players": {
    "R": "Red AI",
    "B": "Blue AI"
  },
  "move_history": [
    {
      "player": "R",
      "piece_index": 0,
      "position": [0, 3],
      "rotation": 0,
      "timestamp": "2025-01-24T14:30:25.123456",
      "turn": 0
    },
    ...
  ],
  "final_state": {...},
  "game_over": true,
  "winner": "R"
}
```

### 5. `replay_game(filename)` - Load and replay game

Load a saved game and replay all moves.

**Parameters:**
- `filename`: Path to saved game JSON file

**Returns:** BorderlineGPT instance with game state restored

**Example:**
```python
game = BorderlineGPT.replay_game("game_20250124_143022.json")
print(f"Replayed {game.turn_count} turns")
print(f"Winner: {game.winner.color if game.winner else 'None'}")
```

### 6. `get_move_history()` - Get move history

Get the complete list of moves made in the game.

**Returns:** List of move objects with timestamps

```json
[
  {
    "player": "R",
    "piece_index": 0,
    "position": [0, 3],
    "rotation": 0,
    "timestamp": "2025-01-24T14:30:25.123456",
    "turn": 0
  },
  ...
]
```

## Piece Management API

Dynamic piece manipulation for advanced game modes, special abilities, and variant rules.

### 7. `add_piece_to_hand(player_color, piece_or_json)` - Add piece to player

Add a piece to a player's hand dynamically.

**Parameters:**
- `player_color`: `"R"` or `"B"`
- `piece_or_json`: Either a GamePiece object or JSON dict

**Returns:**
```json
{
  "success": true,
  "piece_index": 16,
  "piece": {...},
  "message": "Piece added to R player hand at index 16"
}
```

**Use cases:**
- Gift pieces during gameplay
- Special abilities that grant pieces
- Undo functionality
- Custom game modes with dynamic pieces

**Example:**
```python
# Gift a piece from JSON
piece_json = {
    'player_color': 'R',
    'pips': [
        ['R', '_', '_'],
        ['_', 'R', '_'],
        ['_', '_', 'R']
    ]
}

result = game.add_piece_to_hand('R', piece_json)
print(f"Added piece at index {result['piece_index']}")
```

### 8. `remove_piece_from_hand(player_color, piece_index)` - Remove piece from player

Remove a piece from a player's hand without placing it on the board.

**Parameters:**
- `player_color`: `"R"` or `"B"`
- `piece_index`: Index of piece to remove

**Returns:**
```json
{
  "success": true,
  "piece": {...},
  "message": "Piece removed from R player hand"
}
```

**Use cases:**
- Penalty mechanics (lose a piece)
- Trade pieces between players
- Special abilities that consume pieces
- Discard mechanics

**Example:**
```python
# Remove player's first piece
result = game.remove_piece_from_hand('R', 0)
if result['success']:
    print(f"Removed piece with power {result['piece']['power']}")
```

### 9. `gift_random_piece(player_color)` - Gift random piece

Gift a random piece from the standard set to a player.

**Parameters:**
- `player_color`: `"R"` or `"B"`

**Returns:**
```json
{
  "success": true,
  "piece": {...},
  "piece_index": 16,
  "message": "Random piece gifted to R player"
}
```

**Example:**
```python
# Gift random piece to red player
result = game.gift_random_piece('R')
print(f"Gifted {result['piece']['power']}-power piece")
```

### 10. `create_custom_piece(player_color, pip_positions)` - Create custom piece

Create a custom piece by specifying pip positions.

**Parameters:**
- `player_color`: `"R"` or `"B"`
- `pip_positions`: List of `[row, col]` positions (0-2) where pips should be placed

**Returns:**
```json
{
  "success": true,
  "piece": {...},
  "message": "Custom piece created with 5 pips"
}
```

**Rules:**
- Center pip `[1,1]` must always be filled
- Positions must be within 0-2 range
- Can create any shape with 1-9 pips

**Example:**
```python
# Create custom L-shape
result = game.create_custom_piece('R', [
    [0, 0],
    [1, 0],
    [1, 1],
    [2, 0]
])

if result['success']:
    print(f"Created L-shape with power {result['piece']['power']}")
```

### 11. `gift_custom_piece_to_hand(player_color, pip_positions)` - Create and gift custom piece

Combines create_custom_piece + add_piece_to_hand in one call.

**Parameters:**
- `player_color`: `"R"` or `"B"`
- `pip_positions`: List of `[row, col]` positions

**Returns:**
```json
{
  "success": true,
  "piece": {...},
  "piece_index": 16,
  "message": "Custom piece added to R player hand"
}
```

**Example:**
```python
# Create and gift super piece (9 pips - full block)
result = game.gift_custom_piece_to_hand('R', [
    [0,0], [0,1], [0,2],
    [1,0], [1,1], [1,2],
    [2,0], [2,1], [2,2]
])
print(f"Gifted 9-pip super piece!")
```

### 12. `swap_pieces_between_players(red_piece_index, blue_piece_index)` - Swap pieces

Trade pieces between players (changes colors automatically).

**Parameters:**
- `red_piece_index`: Index in red player's hand
- `blue_piece_index`: Index in blue player's hand

**Returns:**
```json
{
  "success": true,
  "red_gave": {...},
  "blue_gave": {...},
  "message": "Pieces swapped between players"
}
```

**Example:**
```python
# Swap pieces between players
result = game.swap_pieces_between_players(0, 0)
print("Pieces traded and colors swapped!")

## Event Types

The `events` list in move results can contain:

### piece_placed
```json
{
  "type": "piece_placed",
  "player": "R",
  "row": 0,
  "col": 3,
  "piece": {...}
}
```

### combat
```json
{
  "type": "combat",
  "combat_data": {
    "attacker_color": "R",
    "defender_color": "B",
    "attacker_power": 5,
    "defender_power": 3,
    "winner": "R",
    "attackers": [{...}],
    "defenders": [{...}]
  }
}
```

### piece_removed
```json
{
  "type": "piece_removed",
  "reason": "combat_loss",
  "row": 1,
  "col": 3,
  "piece": {...}
}
```

Reasons can be:
- `"combat_loss"` - Lost in combat
- `"disconnected"` - Disconnected from home row after combat

## Complete Example: AI vs AI

```python
from borderline_gpt import BorderlineGPT
import random

# Create game
game = BorderlineGPT()

# Simple AI: choose random valid move
while not game.game_over and game.turn_count < 100:
    # Get valid moves for current player
    valid_moves = game.get_valid_moves()

    if not valid_moves:
        print(f"No valid moves for {game.current_player.color}")
        break

    # Choose random move
    move = random.choice(valid_moves)

    # Execute move
    result = game.execute_move(move)

    if result['valid']:
        print(f"Turn {result['game_state']['turn']}: {move['player']} played")

        # Show events
        for event in result['events']:
            if event['type'] == 'combat':
                print(f"  Combat! {event['combat_data']['winner']} wins")
            elif event['type'] == 'piece_removed':
                print(f"  Piece removed: {event['reason']}")

    if result['game_over']:
        print(f"\nGame Over! Winner: {result['winner']}")
        break

# Save game
filename = game.export_game()
print(f"\nGame saved to {filename}")
```

## Creating a Custom AI

To create your own AI engine:

1. **Query valid moves:**
```python
valid_moves = game.get_valid_moves()
```

2. **Analyze game state:**
```python
state = game.get_game_state()
# Analyze board, pieces remaining, etc.
```

3. **Choose and execute move:**
```python
# Your AI logic here
best_move = my_ai_choose_move(state, valid_moves)
result = game.execute_move(best_move)
```

4. **Handle results:**
```python
if result['valid']:
    # Process events (combat, removals, etc.)
    for event in result['events']:
        # Update your AI's internal state
        pass
```

## Creating a Custom Frontend

To create a GUI or visualizer:

1. **Initialize game:**
```python
game = BorderlineGPT()
```

2. **Display initial state:**
```python
state = game.get_game_state()
# Render board, pieces, etc.
```

3. **Handle user input:**
```python
# User selects piece, position, rotation
move = {
    "player": state['current_player'],
    "piece_index": selected_piece_idx,
    "position": [clicked_row, clicked_col],
    "rotation": rotation_count
}
```

4. **Execute and update display:**
```python
result = game.execute_move(move)

if not result['valid']:
    # Show error to user
    show_error(result['reason'])
else:
    # Update display with new state
    render_board(result['game_state'])

    # Animate events
    for event in result['events']:
        if event['type'] == 'piece_placed':
            animate_placement(event)
        elif event['type'] == 'combat':
            animate_combat(event)
```

## Testing the API

Simple test script:

```python
from borderline_gpt import BorderlineGPT

# Create game
game = BorderlineGPT()

# Test 1: Get initial state
state = game.get_game_state()
assert state['turn'] == 0
assert state['current_player'] == 'R'
print("✓ Initial state correct")

# Test 2: Get valid moves
moves = game.get_valid_moves()
assert len(moves) > 0
print(f"✓ Found {len(moves)} valid moves")

# Test 3: Execute valid move
result = game.execute_move(moves[0])
assert result['valid'] == True
print("✓ Valid move executed")

# Test 4: Try invalid move
invalid_move = {
    "player": "B",  # Wrong player
    "piece_index": 0,
    "position": [0, 0],
    "rotation": 0
}
result = game.execute_move(invalid_move)
assert result['valid'] == False
print("✓ Invalid move rejected")

# Test 5: Export and replay
filename = game.export_game("test_game.json")
replayed_game = BorderlineGPT.replay_game(filename)
assert replayed_game.turn_count == game.turn_count
print("✓ Export and replay works")

print("\nAll tests passed!")
```

## Advanced Examples: Piece Management

### Example 1: Gift Random Piece Every 5 Turns

```python
from borderline_gpt import BorderlineGPT
import random

game = BorderlineGPT()

turn_count = 0
while not game.game_over and turn_count < 50:
    # Play turn
    valid_moves = game.get_valid_moves()
    if valid_moves:
        move = random.choice(valid_moves)
        result = game.execute_move(move)

        if result['valid']:
            turn_count += 1

            # Gift random piece every 5 turns
            if turn_count % 5 == 0:
                current_player = result['game_state']['current_player']
                gift_result = game.gift_random_piece(current_player)
                print(f"Turn {turn_count}: Gifted piece to {current_player}!")
                print(f"  Power: {gift_result['piece']['power']}")

print(f"Game ended after {turn_count} turns")
```

### Example 2: Custom Power Piece as Reward

```python
# When player captures territory, grant powerful piece
def grant_power_piece(game, player_color, power_level):
    """Grant custom piece based on power level"""

    if power_level == 1:
        # Single pip (weakest)
        pip_positions = [[1, 1]]
    elif power_level == 2:
        # Line of 3
        pip_positions = [[0, 1], [1, 1], [2, 1]]
    elif power_level == 3:
        # Plus shape (5 pips)
        pip_positions = [[0, 1], [1, 0], [1, 1], [1, 2], [2, 1]]
    else:
        # Full 9-pip super piece
        pip_positions = [
            [0, 0], [0, 1], [0, 2],
            [1, 0], [1, 1], [1, 2],
            [2, 0], [2, 1], [2, 2]
        ]

    result = game.gift_custom_piece_to_hand(player_color, pip_positions)
    return result

# Usage
game = BorderlineGPT()
result = grant_power_piece(game, 'R', 4)  # Grant super piece
print(f"Granted super piece with {result['piece']['power']} power!")
```

### Example 3: Piece Trading Mechanic

```python
# Trade weakest pieces between players every 10 turns
def trade_weakest_pieces(game):
    """Find and trade the weakest piece from each player"""

    red_pieces = game.get_game_state()['players']['R']['pieces_remaining']
    blue_pieces = game.get_game_state()['players']['B']['pieces_remaining']

    if not red_pieces or not blue_pieces:
        return {'success': False, 'message': 'No pieces to trade'}

    # Find weakest pieces
    red_weakest_idx = min(range(len(red_pieces)),
                          key=lambda i: red_pieces[i]['power'])
    blue_weakest_idx = min(range(len(blue_pieces)),
                           key=lambda i: blue_pieces[i]['power'])

    # Swap them
    result = game.swap_pieces_between_players(red_weakest_idx, blue_weakest_idx)
    return result

# Usage
game = BorderlineGPT()
# ... play some turns ...
result = trade_weakest_pieces(game)
print(f"Traded pieces: {result['message']}")
```

### Example 4: Dynamic Difficulty - Gift Pieces to Losing Player

```python
def help_losing_player(game):
    """Gift piece to player who has fewer pieces on board"""

    state = game.get_game_state()
    red_on_board = state['players']['R']['pieces_on_board']
    blue_on_board = state['players']['B']['pieces_on_board']

    # Determine who's losing
    if red_on_board < blue_on_board - 2:
        losing_player = 'R'
    elif blue_on_board < red_on_board - 2:
        losing_player = 'B'
    else:
        return None  # Game is balanced

    # Gift a powerful piece
    result = game.gift_custom_piece_to_hand(losing_player, [
        [0, 1],
        [1, 0], [1, 1], [1, 2],
        [2, 1]
    ])  # Plus shape (5 pips)

    return result

# Usage
game = BorderlineGPT()
# After some turns...
result = help_losing_player(game)
if result:
    print(f"Helped losing player with 5-pip piece!")
```

### Example 5: Special Ability - Sacrifice for Super Piece

```python
def sacrifice_for_super_piece(game, player_color, sacrifice_indices):
    """
    Remove multiple pieces from hand to create one super piece

    Args:
        sacrifice_indices: List of piece indices to sacrifice

    Returns power based on sacrificed pieces
    """
    total_power = 0

    # Remove pieces (in reverse order to maintain indices)
    for idx in sorted(sacrifice_indices, reverse=True):
        result = game.remove_piece_from_hand(player_color, idx)
        if result['success']:
            total_power += result['piece']['power']

    # Create super piece based on total power
    if total_power >= 15:
        # Full 9-pip block
        pip_positions = [
            [0, 0], [0, 1], [0, 2],
            [1, 0], [1, 1], [1, 2],
            [2, 0], [2, 1], [2, 2]
        ]
    elif total_power >= 10:
        # X-shape (5 pips)
        pip_positions = [[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]
    else:
        # T-shape (4 pips)
        pip_positions = [[0, 0], [0, 2], [1, 1], [2, 1]]

    result = game.gift_custom_piece_to_hand(player_color, pip_positions)
    result['total_power_sacrificed'] = total_power

    return result

# Usage
game = BorderlineGPT()
# Sacrifice first 3 pieces for a super piece
result = sacrifice_for_super_piece(game, 'R', [0, 1, 2])
print(f"Sacrificed {result['total_power_sacrificed']} power")
print(f"Created piece with {result['piece']['power']} power")
```

### Example 6: Game Mode - Random Piece Generator

```python
def random_piece_generator_mode(game, gift_interval=3):
    """
    Game mode where players receive random pieces periodically
    """
    import random

    turn_count = 0

    while not game.game_over and turn_count < 100:
        # Get valid moves
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            break

        # Play random move
        move = random.choice(valid_moves)
        result = game.execute_move(move)

        if result['valid']:
            turn_count += 1

            # Gift random piece at interval
            if turn_count % gift_interval == 0:
                # Gift to both players
                for player in ['R', 'B']:
                    gift_result = game.gift_random_piece(player)
                    print(f"Turn {turn_count}: {player} received "
                          f"{gift_result['piece']['power']}-power piece")

            if result['game_over']:
                break

    return {
        'winner': result['winner'] if result['game_over'] else None,
        'turns': turn_count
    }

# Usage
game = BorderlineGPT()
result = random_piece_generator_mode(game, gift_interval=3)
print(f"Game ended: Winner = {result['winner']}, Turns = {result['turns']}")
```

## Benefits of This API

1. **Separation of Concerns**: Game logic is completely separate from presentation
2. **Testability**: Easy to write automated tests
3. **AI Development**: Standard interface for creating AIs
4. **Replay System**: Games can be saved and replayed
5. **Multiple Frontends**: Same engine works with any UI
6. **Chess Engine Model**: Similar to how chess engines work (UCI protocol)
7. **Debugging**: JSON format is human-readable
8. **Version Control**: Game files can be committed to git

## Future Enhancements

Possible additions to the API:

- **Undo/Redo**: Add ability to rewind game state
- **Analysis Mode**: Query what-if scenarios without committing
- **Performance Metrics**: Track thinking time, nodes searched, etc.
- **Opening Book**: Standard starting positions
- **Tournament Mode**: Run multiple games in parallel
- **Network Protocol**: Client-server architecture for online play
