# Borderline Replay System

## Overview

The Borderline replay system allows you to **replay any game saved from non-GUI mode step-by-step in the GUI**. This demonstrates the power of the API architecture - games played in terminal mode can be perfectly visualized in the web interface.

## Architecture

```
┌──────────────────┐
│  Non-GUI Game    │
│  (Terminal/CLI)  │
└────────┬─────────┘
         │
         │ game.export_game()
         ▼
    ┌────────────┐
    │  JSON File │
    └────┬───────┘
         │
         │ BorderlineGPT.replay_game()
         ▼
┌────────────────────┐
│  GUI Replay Mode   │
│  (Web Browser)     │
│  • Step forward    │
│  • Step back       │
│  • Jump to move    │
│  • Auto-play       │
└────────────────────┘
```

## Quick Start

### 1. Create a Game in Non-GUI Mode

```python
from borderline_gpt import BorderlineGPT

# Play game (AI vs AI, Human vs AI, etc.)
game = BorderlineGPT()

# ... play the game ...

# Save when done (automatically saves to previous_games/ folder)
game.export_game('my_game.json')
```

The game is now automatically saved in `previous_games/my_game.json`!

### 2. Replay in GUI (Two Methods)

#### Method A: Using the GUI Controls (Recommended)

**Start the server:**
```bash
python3 gui_server.py
```

**Open browser:**
1. Go to `http://localhost:5000`
2. Click **"REPLAY MODE"** button
3. Upload your replay file:
   - Click **"📁 Upload Replay"** button, OR
   - Drag & drop your `.json` file into the drop zone

**Control playback:**
- Click **⏮️** to jump to first move
- Click **◀️** to go to previous move (or press **Left Arrow**)
- Click **▶️** to play/pause (or press **Spacebar**)
- Click **▶️** to go to next move (or press **Right Arrow**)
- Click **⏭️** to jump to last move
- Drag the slider to jump to any specific move
- Click speed buttons (0.5x, 1x, 2x, 4x) to change playback speed

**Keyboard Shortcuts:**
- **Left Arrow**: Previous move
- **Right Arrow**: Next move
- **Home**: First move
- **End**: Last move
- **Spacebar**: Play/Pause

#### Method B: Using Console Commands

**Open browser console (F12) and load replay:**
```javascript
socket.emit('load_replay', {filename: 'my_game.json'});
```

**Step through the game:**
```javascript
// Next move
socket.emit('replay_step_forward');

// Previous move
socket.emit('replay_step_back');

// Jump to specific move
socket.emit('replay_goto', {move_number: 10});

// Auto-play
socket.emit('replay_play');

// Pause
socket.emit('replay_pause');
```

## API Reference

### Server Events (emit from client)

#### `load_replay`
Load a game from JSON file (stored on server)

**Parameters:**
```javascript
{
  filename: 'replay_test.json'  // File in project root or previous_games/
}
```

**Response:** `replay_loaded` event

---

#### `load_replay_data`
Load a game from JSON data (for file uploads from browser)

**Parameters:**
```javascript
{
  game_data: {
    game_id: '...',
    timestamp: '...',
    players: {...},
    move_history: [...],
    final_state: {...}
  }
}
```

**Response:** `replay_loaded` event

---

#### `replay_step_forward`
Execute the next move in the replay

**Parameters:** None

**Response:** `replay_step` event with move details

---

#### `replay_step_back`
Go back one move

**Parameters:** None

**Response:** `replay_step_back` event

**Note:** Recreates game state from beginning to ensure accuracy

---

#### `replay_goto`
Jump to a specific move number

**Parameters:**
```javascript
{
  move_number: 10  // 1-indexed (1 = first move)
}
```

**Response:** `replay_goto` event

---

#### `replay_play`
Start auto-playing through the replay

**Parameters:** None

**Response:** `replay_playing` event

**Note:** Client should call `replay_step_forward` on a timer

---

#### `replay_pause`
Pause auto-play

**Parameters:** None

**Response:** `replay_paused` event

---

#### `get_replay_state`
Get current replay status

**Parameters:** None

**Response:** `replay_state` event

---

### Client Events (listen on client)

#### `replay_loaded`
Fired when replay successfully loads

```javascript
{
  success: true,
  total_moves: 20,
  game_state: {...},
  message: 'Loaded replay with 20 moves'
}
```

---

#### `replay_step`
Fired when a move is executed

```javascript
{
  move_number: 5,          // Current move (1-indexed)
  total_moves: 20,         // Total moves in replay
  move: {...},             // Move JSON
  row: 0,
  col: 3,
  piece: {...},            // Placed piece
  combat: {...},           // Combat data (if any)
  removed_pieces: [...],   // Removed pieces (if any)
  game_state: {...},       // Complete state after move
  game_over: false,
  winner: null
}
```

---

#### `replay_step_back`
Fired when stepping backward

```javascript
{
  move_number: 4,
  total_moves: 20,
  game_state: {...}
}
```

---

#### `replay_goto`
Fired when jumping to a move

```javascript
{
  move_number: 10,
  total_moves: 20,
  game_state: {...}
}
```

---

#### `replay_playing`
Fired when auto-play starts

```javascript
{
  is_playing: true
}
```

---

#### `replay_paused`
Fired when auto-play pauses

```javascript
{
  is_playing: false
}
```

---

#### `replay_state`
Response to `get_replay_state`

```javascript
{
  loaded: true,
  current_move: 5,
  total_moves: 20,
  is_playing: false
}
```

---

#### `replay_error`
Fired when an error occurs

```javascript
{
  message: 'Already at end of replay'
}
```

---

## Example: Full Replay Client

```javascript
// Connect to server
const socket = io();

// Load replay
socket.emit('load_replay', {filename: 'my_game.json'});

// Listen for load complete
socket.on('replay_loaded', (data) => {
  console.log(`Loaded ${data.total_moves} moves`);
  renderBoard(data.game_state);
});

// Listen for steps
socket.on('replay_step', (data) => {
  console.log(`Move ${data.move_number}/${data.total_moves}`);

  // Render the move
  renderMove(data.row, data.col, data.piece);

  // Show combat if any
  if (data.combat) {
    showCombat(data.combat);
  }

  // Remove pieces if any
  data.removed_pieces.forEach(p => {
    removePiece(p.row, p.col);
  });

  // Update board
  renderBoard(data.game_state);

  // Check for game end
  if (data.game_over) {
    showVictory(data.winner);
  }
});

// Auto-play example
function autoPlay(delayMs = 1000) {
  socket.emit('replay_play');

  const interval = setInterval(() => {
    socket.emit('replay_step_forward');
  }, delayMs);

  // Stop at end
  socket.on('replay_error', (data) => {
    if (data.message.includes('end')) {
      clearInterval(interval);
      socket.emit('replay_pause');
    }
  });
}

// Start auto-play at 1 second per move
autoPlay(1000);
```

## Use Cases

### 1. **Game Analysis**
Review games to understand what happened, analyze strategies, find mistakes

### 2. **Teaching/Learning**
Show new players how games unfold, demonstrate strategies

### 3. **Bug Reports**
Reproduce and debug issues by replaying exact game states

### 4. **Tournament Review**
Analyze tournament games, create highlight reels

### 5. **Content Creation**
Record commentary over replays, create tutorial videos

### 6. **AI Development**
Review AI decision-making, debug AI behavior

## Example: Create and Replay a Game

```python
#!/usr/bin/env python3
from borderline_gpt import BorderlineGPT
import random

# 1. Play a game in terminal mode
print("Playing game in terminal...")
game = BorderlineGPT()

while not game.game_over and game.turn_count < 30:
    valid_moves = game.get_valid_moves()
    if not valid_moves:
        break

    move = random.choice(valid_moves)
    result = game.execute_move(move)

    if result['valid']:
        print(f"Turn {game.turn_count}: {move['player']} played")

# 2. Save the game
filename = game.export_game('tutorial_game.json')
print(f"\nGame saved to: {filename}")
print(f"Turns: {game.turn_count}")

# 3. Now replay in GUI:
#    - Start: python3 gui_server.py
#    - Browser: http://localhost:5000
#    - Console: socket.emit('load_replay', {filename: 'tutorial_game.json'});
#    - Step through with: socket.emit('replay_step_forward');

print("\nReady for GUI replay!")
```

## GUI Features

The replay system now includes a full-featured GUI with:

### Visual Controls
- **Play/Pause Button**: Start and stop auto-play
- **Previous/Next Buttons**: Step through moves one at a time
- **First/Last Buttons**: Jump to the beginning or end
- **Progress Slider**: Scrub to any move in the game
- **Speed Control**: Adjust playback speed (0.5x, 1x, 2x, 4x)
- **Move Counter**: Shows current move and total moves

### File Upload
- **Upload Button**: Click to select a .json replay file
- **Drag & Drop**: Drag replay files directly into the drop zone
- **Auto-Detection**: Automatically validates and loads uploaded files

### Keyboard Shortcuts
- **←** Left Arrow: Previous move
- **→** Right Arrow: Next move
- **Home**: Jump to first move
- **End**: Jump to last move
- **Space**: Play/Pause toggle

### Move Details Display
Shows detailed information about the current move:
- Player (Red or Blue)
- Position on board
- Piece index and rotation
- Combat results (if any)

### Neon Theme
- Glowing neon borders and buttons
- Animated effects on hover
- Consistent with game's visual style
- Smooth transitions and feedback

## Benefits

✅ **Perfect Visualization** - See terminal games with full graphics
✅ **Step-by-Step Analysis** - Pause and examine any move
✅ **Time Travel** - Jump forward/backward through the game
✅ **Easy Upload** - Drag & drop replay files from anywhere
✅ **Keyboard Control** - Navigate quickly with shortcuts
✅ **Variable Speed** - Watch at your preferred pace
✅ **Verification** - Confirm game logic is working correctly
✅ **Documentation** - Create visual records of games
✅ **Education** - Teach game mechanics visually

## Implementation Details

### How Replay Works

1. **Load**: Server loads JSON file using `BorderlineGPT.replay_game()`
2. **Extract**: Pulls out move history from loaded game
3. **Fresh Start**: Creates new empty game for step-by-step replay
4. **Step Forward**: Executes one move from history using `execute_move()`
5. **Step Back**: Rebuilds game from start up to previous move
6. **Jump**: Rebuilds game from start up to target move

### Why Rebuild for Step Back?

The game engine doesn't store undo state, so to go backward:
1. Create fresh game
2. Replay all moves up to target
3. This ensures perfect accuracy

### Performance

- **Step Forward**: ~1ms (single move execution)
- **Step Back**: ~10-100ms depending on move count (rebuild)
- **Jump**: ~10-100ms depending on target move (rebuild)
- **Load**: ~50-200ms (file I/O + initial replay)

For large games (100+ moves), jumping/stepping back may have noticeable delay. This is acceptable for replay viewing.

## Future Enhancements

Possible additions to replay system:

- **Speed Control**: Variable playback speed (0.5x, 1x, 2x, 4x)
- **Bookmarks**: Mark important moments in replay
- **Annotations**: Add comments to specific moves
- **Branching**: Explore "what if" scenarios from any point
- **Comparison**: Side-by-side comparison of two games
- **Export**: Save replay as video/GIF
- **Highlights**: Auto-detect exciting moments (big combats, etc.)

## Troubleshooting

### Replay doesn't load
- Ensure JSON file exists in project root
- Check filename spelling
- Verify file is valid JSON (`BorderlineGPT.replay_game('file.json')`)

### Moves don't match original game
- This shouldn't happen! The API ensures perfect replay
- If it does, it's a bug - please report with the JSON file

### Slow replay on large games
- Expected for 100+ move games when stepping backward
- Consider adding move limit or caching intermediate states

## Conclusion

The replay system demonstrates the power of the API architecture:

**One game engine + JSON interface = Multiple ways to play and view**

Games played in any mode (terminal, GUI, AI vs AI) can be:
- Saved to JSON
- Loaded in any other mode
- Replayed perfectly
- Analyzed from any angle

This is only possible because of the clean separation between game logic and presentation!
