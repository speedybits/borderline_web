# Borderline

A strategic board game with AI opponents and a stunning TRON-inspired GUI.

## Overview

Borderline is a two-player strategy game played on an 8×6 grid where players place 3×3 pip pieces to create a contiguous path from their home row to the opponent's home row. Features combat mechanics with dice rolls and multiple AI strategies.

## Features

### Game Modes
- **Human vs Human**: Two players on the same device
- **Human vs AI**: Play against intelligent AI opponents
- **AI vs AI**: Watch AI strategies battle each other
- **Random Player**: Test strategies against random moves

### AI Strategies
- **Aggressive**: Forward-pushing offensive strategy (71% win rate vs random)
- **Defensive**: Territory control and blocking
- **Random**: Completely random legal moves

### Graphics Modes
- **ASCII Terminal**: Classic command-line interface
- **TRON GUI**: Web-based graphical interface with glowing neon aesthetics

## Installation

### Requirements
```bash
pip install flask flask-socketio python-socketio
```

No additional dependencies required for terminal mode.

## Usage

### Terminal Mode (ASCII)

**AI vs AI (default)**:
```bash
python3 borderline_gpt.py
```

**Human vs AI**:
```bash
python3 borderline_gpt.py --human_vs_ai
```
You play as Blue, AI plays as Red.

**AI vs Random**:
```bash
python3 borderline_gpt.py --blue_random
```
Watch Red AI demolish random Blue moves.

### GUI Mode (TRON Edition)

**Launch web server**:
```bash
python3 borderline_gpt.py --gui
```

Then open your browser to:
```
http://localhost:5000
```

**GUI Features**:
- Neon red (#ff0055) and cyan (#00d4ff) glowing pieces
- Semi-reflective black background
- Animated dice rolling with 3D tumbling
- Power levels displayed on pieces
- Turn indicator with pulsing glow
- Victory screen with animations
- Real-time game updates via Socket.IO
- Mouse-based piece placement
- Combat log with color-coded messages

**Supported Browsers**:
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## Game Rules

### Board
- 8 columns × 6 rows grid
- Red starts at bottom row (row 0)
- Blue starts at top row (row 5)

### Pieces
- Each player has 16 pieces
- Each piece is a 3×3 grid of pips
- Pieces can have 1-9 pips active
- Piece power = number of active pips

### Placement
- Pieces must connect to existing pieces (or home row for first move)
- Connection can be orthogonal or diagonal (corner-to-corner only)
- No overlap allowed

### Combat
- Occurs when pieces are adjacent after placement
- Both players roll 1d6
- Higher roll wins (attacker wins ties)
- Losing piece is converted to winner's color

### Victory
- Create a contiguous path of pips from your home row to opponent's home row
- Path must be connected orthogonally (up/down/left/right)

### Draw Conditions
- Both players run out of pieces
- Both players have no valid moves (stalemate)
- Turn limit reached (10,000 turns)

## File Structure

```
borderline/
├── borderline_gpt.py          # Main game logic and AI
├── gui_server.py               # Flask web server
├── optimize_vs_random.py       # Strategy benchmarking
├── templates/
│   └── index.html             # Web GUI interface
├── static/
│   ├── css/
│   │   ├── main.css           # Base styles
│   │   └── tron.css           # TRON aesthetic
│   └── js/
│       ├── game.js            # Game controller
│       ├── renderer.js        # Canvas rendering
│       └── socket_handler.js  # Real-time communication
├── GUI_VERSION.md             # GUI design specification
└── README.md                  # This file
```

## Development

### Strategy Development
AI strategies are defined in the `AIPlayer.evaluate_move()` method in `borderline_gpt.py`.

Key evaluation factors:
- **Forward Progress**: Distance toward opponent's home row
- **Connection Strength**: Number of pips connected to existing pieces
- **Path Continuity**: Maintaining contiguous vertical paths
- **Battle Opportunity**: Strategic combat positioning
- **Piece Efficiency**: Managing remaining pieces

### Testing Strategies
```bash
python3 optimize_vs_random.py
```

Runs 100-game benchmark of current strategy against random opponent.

### GUI Customization
Edit CSS files in `static/css/`:
- `main.css`: Layout and structure
- `tron.css`: Colors, glows, and animations

Color palette defined in `tron.css`:
```css
--bg-black: #0a0a0a
--grid-line: #1a1a2e
--red-neon: #ff0055
--blue-neon: #00d4ff
--green-accent: #00ff88
--amber: #ffaa00
```

## Performance

### Strategy Win Rates (vs Random, 100 games)
- **Aggressive (GEN 30)**: 71% overall, 95.9% decisive
- Average game length: 234 turns
- Draw rate: 26% (legitimate stalemates)

### GUI Performance
- 60 FPS canvas rendering
- <50ms real-time update latency
- Supports concurrent games via Socket.IO

## Credits

Game design and implementation by Mike with Claude Code.

TRON visual aesthetic inspired by the classic 1982 film.

## License

This project is for educational and entertainment purposes.

## Future Enhancements

See `GUI_VERSION.md` for planned features:
- Phase 2: Enhanced visuals and animations
- Phase 3: Advanced animations (piece movement, combat effects)
- Phase 4: AI integration improvements
- Phase 5: Sound effects, drag-and-drop, mobile support

Planned features:
- Tournament mode
- Replay system
- Strategy editor
- Online multiplayer
- Achievement system
- Custom piece designs

---

**Enjoy playing Borderline!** 🎮

For bugs or feature requests, please create an issue in the repository.
