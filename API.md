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
