# Borderline Game - Complete API Summary

## Overview

The Borderline game engine now features a comprehensive, chess-engine-style JSON API that completely separates game logic from presentation. This enables multiple frontends, AI development, replay systems, and dynamic piece management.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              BorderlineGPT Game Engine                  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Core Game Logic (Authoritative)          │  │
│  │  • Board state                                   │  │
│  │  • Placement validation                          │  │
│  │  • Combat resolution                             │  │
│  │  • Victory conditions                            │  │
│  │  • Piece disconnection                           │  │
│  └──────────────────────────────────────────────────┘  │
│                          ▲                              │
│                          │                              │
│  ┌──────────────────────┴───────────────────────────┐  │
│  │              JSON API Layer                      │  │
│  │  • execute_move()                                │  │
│  │  • get_game_state()                              │  │
│  │  • get_valid_moves()                             │  │
│  │  • export_game() / replay_game()                 │  │
│  │  • Piece Management (6 methods)                  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          │ JSON
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
    ┌───▼────┐       ┌────▼───┐       ┌────▼────┐
    │  Web   │       │  CLI   │       │   AI    │
    │  GUI   │       │ Viewer │       │ Engine  │
    └────────┘       └────────┘       └─────────┘
```

## API Categories

### 1. Core Game API

#### execute_move(move_json)
**Purpose:** Execute a player's move

**Input:**
```json
{
  "player": "R",
  "piece_index": 0,
  "position": [row, col],
  "rotation": 0-3
}
```

**Output:**
```json
{
  "valid": true,
  "reason": null,
  "events": [...],
  "game_state": {...},
  "game_over": false,
  "winner": null
}
```

**Use cases:**
- Human player moves via GUI
- AI player moves
- Replay system
- Testing

---

#### get_game_state()
**Purpose:** Get complete current game state

**Output:**
```json
{
  "game_id": "20251024_143022",
  "turn": 5,
  "current_player": "R",
  "game_over": false,
  "winner": null,
  "board": [[...], ...],
  "board_dimensions": {"height": 8, "width": 6},
  "players": {
    "R": {
      "name": "Red Player",
      "pieces_remaining": [...],
      "pieces_on_board": 3
    },
    "B": {...}
  }
}
```

**Use cases:**
- Render game board
- AI decision making
- Save game state
- Debug/analysis

---

#### get_valid_moves(player_color)
**Purpose:** Get all legal moves for current player

**Output:**
```json
[
  {"player": "R", "piece_index": 0, "position": [0,3], "rotation": 0},
  {"player": "R", "piece_index": 0, "position": [0,4], "rotation": 0},
  ...
]
```

**Use cases:**
- AI move generation
- Hint system
- UI validation
- Testing

---

#### export_game(filename)
**Purpose:** Save complete game to JSON file

**Output File:**
```json
{
  "game_id": "20251024_143022",
  "timestamp": "2025-01-24T14:30:22.123456",
  "players": {"R": "Red AI", "B": "Blue AI"},
  "move_history": [...],
  "final_state": {...},
  "game_over": true,
  "winner": "R"
}
```

**Use cases:**
- Save/load games
- Replay analysis
- Bug reports
- Tournaments

---

#### replay_game(filename)
**Purpose:** Load and replay game from file

**Returns:** BorderlineGPT instance with game restored

**Use cases:**
- Replay viewer
- Game analysis
- Testing
- Learning from games

---

#### get_move_history()
**Purpose:** Get all moves made in game

**Output:**
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

---

### 2. Piece Management API

#### add_piece_to_hand(player_color, piece_or_json)
**Purpose:** Dynamically add piece to player's hand

**Example:**
```python
piece_json = {
    'player_color': 'R',
    'pips': [['R','_','_'], ['_','R','_'], ['_','_','R']]
}
result = game.add_piece_to_hand('R', piece_json)
```

**Use cases:**
- Gift pieces during gameplay
- Special abilities
- Undo functionality
- Custom game modes

---

#### remove_piece_from_hand(player_color, piece_index)
**Purpose:** Remove piece from hand without placing

**Example:**
```python
result = game.remove_piece_from_hand('R', 0)
```

**Use cases:**
- Penalty mechanics
- Trading pieces
- Sacrifice abilities
- Discard mechanics

---

#### gift_random_piece(player_color)
**Purpose:** Gift random piece from standard set

**Example:**
```python
result = game.gift_random_piece('R')
print(f"Gifted {result['piece']['power']}-power piece")
```

**Use cases:**
- Periodic rewards
- Random events
- Balance mechanics

---

#### create_custom_piece(player_color, pip_positions)
**Purpose:** Create piece with custom pip pattern

**Example:**
```python
# Create L-shape
result = game.create_custom_piece('R', [
    [0,0], [1,0], [1,1], [2,0]
])
```

**Use cases:**
- Special pieces
- Expansion content
- Community mods
- Testing

---

#### gift_custom_piece_to_hand(player_color, pip_positions)
**Purpose:** Create and add custom piece in one call

**Example:**
```python
# Gift super piece (9 pips)
result = game.gift_custom_piece_to_hand('R', [
    [0,0], [0,1], [0,2],
    [1,0], [1,1], [1,2],
    [2,0], [2,1], [2,2]
])
```

**Use cases:**
- Power-ups
- Achievement rewards
- Boss drops

---

#### swap_pieces_between_players(red_index, blue_index)
**Purpose:** Trade pieces between players

**Example:**
```python
result = game.swap_pieces_between_players(0, 0)
```

**Use cases:**
- Trading mechanics
- Diplomacy
- Strategic exchanges

---

## Event System

All game actions produce events that frontends can use for animation and feedback:

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
    "attackers": [...],
    "defenders": [...]
  }
}
```

### piece_removed
```json
{
  "type": "piece_removed",
  "reason": "combat_loss" | "disconnected",
  "row": 1,
  "col": 3,
  "piece": {...}
}
```

## Complete Use Case Examples

### Example 1: Simple AI

```python
from borderline_gpt import BorderlineGPT
import random

game = BorderlineGPT()

while not game.game_over:
    # Get valid moves
    valid_moves = game.get_valid_moves()
    if not valid_moves:
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

    if result['game_over']:
        print(f"Winner: {result['winner']}")
        break

# Save game
game.export_game("my_game.json")
```

### Example 2: Custom Frontend

```python
# Initialize game
game = BorderlineGPT()

# Main game loop
while not game.game_over:
    # Get and render state
    state = game.get_game_state()
    render_board(state['board'])
    render_players(state['players'])

    # Get user input
    piece_idx, row, col, rotation = get_user_input()

    # Build move
    move = {
        'player': state['current_player'],
        'piece_index': piece_idx,
        'position': [row, col],
        'rotation': rotation
    }

    # Execute
    result = game.execute_move(move)

    if not result['valid']:
        show_error(result['reason'])
    else:
        # Animate events
        for event in result['events']:
            animate_event(event)
```

### Example 3: Game Mode - Piece Generator

```python
def piece_generator_mode(gift_interval=3):
    game = BorderlineGPT()

    while not game.game_over:
        # Play turn
        valid_moves = game.get_valid_moves()
        move = choose_move(valid_moves)
        result = game.execute_move(move)

        if result['valid']:
            # Gift pieces periodically
            if result['game_state']['turn'] % gift_interval == 0:
                for player in ['R', 'B']:
                    gift_result = game.gift_random_piece(player)
                    print(f"Gifted {gift_result['piece']['power']}-power piece to {player}")

        if result['game_over']:
            break

    return result['winner']
```

### Example 4: Sacrifice Mechanic

```python
def sacrifice_for_power(game, player, indices):
    """Sacrifice multiple pieces for one super piece"""

    # Remove pieces and sum power
    total_power = 0
    for idx in sorted(indices, reverse=True):
        result = game.remove_piece_from_hand(player, idx)
        total_power += result['piece']['power']

    # Create super piece based on sacrificed power
    if total_power >= 15:
        # 9-pip block
        pips = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    elif total_power >= 10:
        # X-shape
        pips = [[0,0],[0,2],[1,1],[2,0],[2,2]]
    else:
        # T-shape
        pips = [[0,0],[0,2],[1,1],[2,1]]

    result = game.gift_custom_piece_to_hand(player, pips)
    return result

# Usage
result = sacrifice_for_power(game, 'R', [0, 1, 2])
print(f"Created {result['piece']['power']}-power super piece!")
```

## Benefits

### 1. Separation of Concerns
- Game logic completely separate from presentation
- GUI is pure presentation layer
- Easy to test in isolation

### 2. Multiple Frontends
- Web GUI (current)
- CLI viewer
- Desktop app
- Mobile app
- VR interface
- All use same API

### 3. AI Development
- Standard interface like chess engines
- Easy to implement new AIs
- AI vs AI tournaments
- Performance benchmarking

### 4. Replay System
- Games saved as human-readable JSON
- Can be committed to git
- Replay viewer
- Analysis tools
- Bug reproduction

### 5. Extensibility
- Add new piece types easily
- Custom game modes
- Special abilities
- Expansion content
- Community mods

### 6. Testing
- Easy to write automated tests
- Deterministic replay
- Edge case testing
- Balance analysis

### 7. Version Control
- Game files are text (JSON)
- Diff friendly
- Tournament results tracked
- Balance history

## Files

| File | Purpose | Lines |
|------|---------|-------|
| borderline_gpt.py | Game engine + API | ~2300 |
| gui_server.py | Web GUI server | ~420 |
| API.md | API documentation | ~920 |
| api_example.py | API demonstration | ~155 |
| piece_management_example.py | Piece management demos | ~360 |

## Testing

All API methods tested and working:

```bash
✓ execute_move() - Move execution
✓ get_game_state() - State retrieval
✓ get_valid_moves() - Move generation
✓ export_game() - Game saving
✓ replay_game() - Game loading
✓ get_move_history() - History access
✓ add_piece_to_hand() - Dynamic piece addition
✓ remove_piece_from_hand() - Piece removal
✓ gift_random_piece() - Random gifting
✓ create_custom_piece() - Custom pieces
✓ gift_custom_piece_to_hand() - Gift custom
✓ swap_pieces_between_players() - Trading
```

## Future Enhancements

Possible additions:

1. **Undo/Redo API**
   - Rewind to any previous turn
   - Branch exploration

2. **Analysis API**
   - Evaluate position strength
   - Suggest best moves
   - What-if scenarios

3. **Tournament API**
   - Run multiple games
   - Collect statistics
   - Rankings/ELO

4. **Network Protocol**
   - Client-server architecture
   - Online multiplayer
   - Spectator mode

5. **Advanced Piece Management**
   - Piece evolution/upgrades
   - Temporary pieces (expire after N turns)
   - Piece fusion (combine for new piece)

6. **Rule Variants**
   - Different board sizes
   - Alternative victory conditions
   - House rules support

## Conclusion

The Borderline game now has a production-ready API that:

✅ Separates game logic from presentation
✅ Supports multiple frontends
✅ Enables easy AI development
✅ Provides replay/analysis capabilities
✅ Allows dynamic piece management
✅ Is fully tested and documented
✅ Is extensible for future features

The architecture follows chess engine best practices and provides a solid foundation for growth, expansion, and community content.
