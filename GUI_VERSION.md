# Borderline GUI Version - Design Document

## Overview
A web-based GUI implementation of Borderline with TRON-inspired neon aesthetics, featuring glowing Red and Blue graphics on a semi-reflective black background with mouse control and animated dice rolling.

## Technology Stack

### Backend
- **Flask**: Lightweight Python web framework
- **Flask-SocketIO**: Real-time bidirectional communication for game updates
- **Existing Game Logic**: Reuse `borderline_gpt.py` classes (Board, Piece, Player, etc.)

### Frontend
- **HTML5 Canvas**: For rendering the game board and pieces with custom graphics
- **Socket.IO (client)**: Real-time updates from server
- **CSS3**: Styling, animations, and TRON aesthetic
- **Vanilla JavaScript**: Game rendering, mouse interaction, animations

## Visual Design Specifications

### Color Palette (TRON-Inspired)
```
Background:     #0a0a0a (near-black with subtle reflection)
Grid Lines:     #1a1a2e (dark blue-gray, subtle)
Red Player:     #ff0055 (neon magenta-red)
Red Glow:       #ff0055 with blur
Blue Player:    #00d4ff (cyan-blue)
Blue Glow:      #00d4ff with blur
Neutral/UI:     #00ff88 (neon green accents)
Text:           #e0e0e0 (light gray)
Power Display:  #ffaa00 (amber)
```

### Board Layout
```
┌─────────────────────────────────────────────────────┐
│  BORDERLINE                    [Turn: RED PLAYER]   │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────┐  ┌───────────────┐  ┌─────────┐      │
│  │         │  │               │  │         │      │
│  │   RED   │  │     8×6       │  │  BLUE   │      │
│  │ PIECES  │  │     BOARD     │  │ PIECES  │      │
│  │         │  │               │  │         │      │
│  │  [16]   │  │   (24 cells)  │  │  [16]   │      │
│  │         │  │               │  │         │      │
│  │ ┌───┐   │  │               │  │  ┌───┐  │      │
│  │ │PWR│   │  │               │  │  │PWR│  │      │
│  │ │ 7 │   │  │               │  │  │ 3 │  │      │
│  │ └───┘   │  │               │  │  └───┘  │      │
│  │         │  │               │  │         │      │
│  └─────────┘  └───────────────┘  └─────────┘      │
│                                                      │
│  ┌──────────────────────────────────────────┐      │
│  │  DICE ROLL ZONE                          │      │
│  │  [Animated dice appear here during combat]      │
│  └──────────────────────────────────────────┘      │
│                                                      │
│  [Status Messages / Combat Log]                     │
└─────────────────────────────────────────────────────┘
```

## Detailed Component Specifications

### 1. Game Board (8×6 grid)
- **Cell Size**: 80×80 pixels (suitable for 3×3 pip display)
- **Grid Lines**: 2px glowing lines in grid color
- **Background**: Semi-reflective black with subtle gradient
- **Hover Effect**: Cell highlights with current player's color (low opacity)
- **Valid Placement Indicators**: Subtle pulsing glow on valid cells

### 2. Piece Representation (3×3 pip grid per piece)
- **Empty Pip**: Dark circle with faint outline
- **Red Pip**: Glowing red circle with outer glow effect
- **Blue Pip**: Glowing cyan circle with outer glow effect
- **Glow Effect**: CSS `box-shadow` with multiple layers:
  ```css
  box-shadow:
    0 0 10px currentColor,
    0 0 20px currentColor,
    0 0 30px currentColor,
    inset 0 0 10px currentColor;
  ```
- **Power Level Display**: Small number in upper-left corner (amber color, 12px font)

### 3. Piece Pools (Left and Right Sidebars)
- **Layout**: Vertical stack of available pieces
- **Interaction**: Click to select, drag to board
- **Selected State**: Bright glow, slightly enlarged (scale 1.1)
- **Piece Count**: Large number showing remaining pieces
- **Preview**: Hover shows piece details

### 4. Dice Rolling Animation
- **Container**: 200×100px box in lower-left corner
- **Animation Phases**:
  1. **Appear**: Dice fade in with scale animation
  2. **Tumble**: 3D CSS transform rotating dice (1 second)
  3. **Settle**: Dice stop and display final number with glow pulse
  4. **Fade**: After 2 seconds, dice fade out
- **Dice Design**: 3D cube with dots, glowing edges
- **Colors**: Attacker's dice in red glow, defender's in blue glow

### 5. Turn Indicator
- **Location**: Top-right of screen
- **Display**: Large text "RED PLAYER" or "BLUE PLAYER"
- **Effect**: Pulsing glow animation
- **Transition**: Smooth fade between turns

### 6. Victory Screen
- **Overlay**: Full-screen semi-transparent backdrop
- **Winner Display**: Large animated text with winner's color
- **Animation**:
  - Text flies in from off-screen
  - Glow pulses
  - Particle effects (small glowing dots) around text
- **Buttons**: "New Game" and "Rematch" with glowing borders

### 7. Combat Log / Status Messages
- **Location**: Bottom of screen, scrollable
- **Display**: Recent 5 messages
- **Format**:
  ```
  Turn 15: RED attacks BLUE at (4,2) - RED wins! (5 vs 3)
  Turn 16: BLUE places piece at (2,1)
  ```
- **Color Coding**: Action keywords in player colors

## Mouse Interaction

### Selection and Placement
1. **Select Piece**: Click on available piece in sidebar
2. **Hover Preview**: Move mouse over board, see piece preview (semi-transparent)
3. **Place Piece**: Click valid cell to place
4. **Cancel**: Right-click or click outside board to deselect

### Rotation (if implemented)
- **Mouse Wheel**: Rotate piece preview before placement
- **Keyboard**: Arrow keys for 90° rotations

### Drag and Drop (Alternative)
- **Drag**: Click and hold piece from sidebar
- **Drop**: Release over valid cell to place
- **Invalid Drop**: Piece returns to sidebar with bounce animation

## Game Flow

### Starting the Application
```bash
python3 borderline_gpt.py --gui
```

This launches Flask server on `http://localhost:5000`

### Initial Screen
- Title screen with glowing BORDERLINE logo
- Game mode selection:
  - Human vs Human
  - Human vs AI (choose difficulty)
  - AI vs AI (watch mode)
  - Load Strategy (for testing)

### Game Loop
1. **Turn Start**: Update turn indicator
2. **AI Turn**: If AI player, show "AI Thinking..." with animated dots
3. **Human Turn**:
   - Highlight available pieces
   - Enable mouse interaction
   - Show valid placement zones on hover
4. **Placement**: Animate piece moving from sidebar to board
5. **Combat**:
   - Highlight involved pieces
   - Show dice animation
   - Display result
   - Animate piece transformation (losing piece changes color)
6. **Victory Check**: If won, show victory screen
7. **Next Turn**: Switch player and repeat

## File Structure

```
borderline/
├── borderline_gpt.py          # Existing game logic (modified for GUI)
├── gui_server.py               # Flask server + SocketIO
├── static/
│   ├── css/
│   │   ├── main.css           # Base styles
│   │   ├── tron.css           # TRON aesthetic styles
│   │   └── animations.css     # Keyframe animations
│   ├── js/
│   │   ├── game.js            # Main game controller
│   │   ├── renderer.js        # Canvas rendering
│   │   ├── input.js           # Mouse/keyboard handling
│   │   ├── animations.js      # Animation helpers
│   │   └── socket_handler.js  # Socket.IO client
│   └── assets/
│       ├── sounds/            # Optional: sound effects
│       │   ├── place.wav      # Piece placement
│       │   ├── combat.wav     # Combat sound
│       │   ├── dice.wav       # Dice rolling
│       │   └── victory.wav    # Victory sound
│       └── images/
│           └── logo.png       # Optional: game logo
└── templates/
    └── index.html             # Main game page
```

## Implementation Phases

### Phase 1: Basic Structure (MVP)
- Flask server setup
- Basic HTML/CSS layout
- Canvas rendering of board and pieces
- Simple piece placement (no drag-drop, just click)
- Turn-based play for Human vs Human

### Phase 2: Visuals
- TRON aesthetic CSS
- Glowing effects
- Piece hover previews
- Turn indicator
- Status messages

### Phase 3: Animations
- Piece placement animation
- Dice rolling animation
- Victory screen
- Smooth transitions

### Phase 4: AI Integration
- Connect to existing AI players
- "AI Thinking" indicator
- AI move visualization

### Phase 5: Polish
- Sound effects
- Drag-and-drop
- Piece rotation
- Mobile responsive design
- Settings menu (toggle animations, sound, etc.)

## Technical Implementation Details

### Flask Server (gui_server.py)
```python
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from borderline_gpt import BorderlineGPT, Board, HumanPlayer, AIPlayer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'borderline_secret'
socketio = SocketIO(app)

# Global game state
current_game = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_game')
def handle_start_game(data):
    global current_game
    mode = data['mode']
    # Initialize game based on mode
    current_game = BorderlineGPT(...)
    emit('game_state', current_game.get_state())

@socketio.on('place_piece')
def handle_place_piece(data):
    row, col, piece_config = data['row'], data['col'], data['piece']
    # Validate and place piece
    result = current_game.place_piece(row, col, piece_config)
    emit('placement_result', result, broadcast=True)

@socketio.on('get_state')
def handle_get_state():
    emit('game_state', current_game.get_state())
```

### Canvas Rendering (renderer.js)
```javascript
class BoardRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.cellSize = 80;
  }

  drawBoard(gameState) {
    this.clearCanvas();
    this.drawGrid();
    this.drawPieces(gameState.board);
    this.drawGlowEffects();
  }

  drawPiece(piece, x, y) {
    // Draw 3×3 pip grid
    for (let row = 0; row < 3; row++) {
      for (let col = 0; col < 3; col++) {
        const pip = piece.pips[row][col];
        if (pip !== '.') {
          this.drawPip(x + col * 25, y + row * 25, pip);
        }
      }
    }
    // Draw power level
    this.drawPowerLevel(x, y, piece.power);
  }

  drawPip(x, y, color) {
    const glowColor = color === 'R' ? '#ff0055' : '#00d4ff';

    // Outer glow
    this.ctx.shadowColor = glowColor;
    this.ctx.shadowBlur = 20;

    // Pip circle
    this.ctx.fillStyle = glowColor;
    this.ctx.beginPath();
    this.ctx.arc(x, y, 8, 0, Math.PI * 2);
    this.ctx.fill();

    // Inner highlight
    this.ctx.shadowBlur = 0;
    this.ctx.fillStyle = '#ffffff';
    this.ctx.beginPath();
    this.ctx.arc(x - 2, y - 2, 3, 0, Math.PI * 2);
    this.ctx.fill();
  }
}
```

### Dice Animation (animations.js)
```javascript
class DiceAnimation {
  constructor(container) {
    this.container = container;
    this.dice = null;
  }

  async roll(attackerRoll, defenderRoll) {
    // Create dice elements
    this.createDice('attacker', attackerRoll);
    this.createDice('defender', defenderRoll);

    // Tumble animation (1 second)
    await this.tumble();

    // Settle on final values
    await this.settle(attackerRoll, defenderRoll);

    // Wait and fade out
    await this.wait(2000);
    await this.fadeOut();
  }

  createDice(type, value) {
    const dice = document.createElement('div');
    dice.className = `dice dice-${type}`;
    dice.dataset.value = value;
    this.container.appendChild(dice);
    return dice;
  }

  async tumble() {
    return new Promise(resolve => {
      // CSS animation for tumbling
      const dice = this.container.querySelectorAll('.dice');
      dice.forEach(d => d.classList.add('tumbling'));
      setTimeout(resolve, 1000);
    });
  }

  async settle(attackerRoll, defenderRoll) {
    // Show final values with glow pulse
    const dice = this.container.querySelectorAll('.dice');
    dice.forEach(d => {
      d.classList.remove('tumbling');
      d.classList.add('settled');
      d.textContent = d.dataset.value;
    });
  }
}
```

### CSS TRON Effects (tron.css)
```css
body {
  background: #0a0a0a;
  background-image:
    radial-gradient(circle at 50% 50%, #1a1a2e 1px, transparent 1px);
  background-size: 50px 50px;
  color: #e0e0e0;
  font-family: 'Orbitron', sans-serif;
}

.board-cell {
  border: 2px solid #1a1a2e;
  transition: all 0.3s ease;
}

.board-cell:hover {
  border-color: currentColor;
  box-shadow: 0 0 20px currentColor;
}

.pip-red {
  background: #ff0055;
  box-shadow:
    0 0 10px #ff0055,
    0 0 20px #ff0055,
    0 0 30px #ff0055,
    inset 0 0 10px #ff0055;
}

.pip-blue {
  background: #00d4ff;
  box-shadow:
    0 0 10px #00d4ff,
    0 0 20px #00d4ff,
    0 0 30px #00d4ff,
    inset 0 0 10px #00d4ff;
}

.turn-indicator {
  font-size: 2em;
  text-transform: uppercase;
  animation: glow-pulse 2s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { text-shadow: 0 0 10px currentColor; }
  50% { text-shadow: 0 0 30px currentColor, 0 0 50px currentColor; }
}

.dice {
  width: 60px;
  height: 60px;
  background: #000;
  border: 2px solid currentColor;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2em;
  box-shadow: 0 0 20px currentColor;
}

.dice.tumbling {
  animation: dice-tumble 1s ease-in-out;
}

@keyframes dice-tumble {
  0% { transform: rotate(0deg) scale(1); }
  25% { transform: rotate(90deg) scale(1.2); }
  50% { transform: rotate(180deg) scale(0.8); }
  75% { transform: rotate(270deg) scale(1.2); }
  100% { transform: rotate(360deg) scale(1); }
}

.victory-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fade-in 0.5s ease;
}

.victory-text {
  font-size: 5em;
  animation: victory-appear 1s ease, glow-pulse 2s ease-in-out infinite;
}

@keyframes victory-appear {
  0% { transform: translateY(-100vh) scale(0); }
  60% { transform: translateY(0) scale(1.2); }
  100% { transform: translateY(0) scale(1); }
}
```

## Accessibility Considerations
- Keyboard navigation support (Tab, Enter, Arrow keys)
- ARIA labels for screen readers
- High contrast mode option
- Colorblind-friendly mode (change colors, add patterns)
- Text size options

## Performance Optimizations
- Canvas rendering at 60 FPS
- Debounce mouse move events
- Lazy load animations
- Minimize socket emissions
- Cache rendered pieces

## Future Enhancements
- Replay system (save/load games)
- Online multiplayer (multiple clients)
- Tournament mode
- Strategy editor (create custom AI strategies)
- Piece customization (design your own pieces)
- Leaderboard
- Achievement system
- Mobile app (React Native or Flutter)

## Testing Plan
- Unit tests for game logic (existing)
- Integration tests for Flask routes
- E2E tests with Selenium for UI
- Performance testing (FPS monitoring)
- Cross-browser testing (Chrome, Firefox, Safari, Edge)
- Mobile device testing

## Deployment
- Development: `flask run --debug`
- Production: Gunicorn + Nginx
- Docker container for easy deployment
- Environment variables for configuration

---

## Getting Started (Quick Start)

1. **Install Dependencies**:
   ```bash
   pip install flask flask-socketio python-socketio
   ```

2. **Run the Server**:
   ```bash
   python3 borderline_gpt.py --gui
   ```

3. **Open Browser**:
   Navigate to `http://localhost:5000`

4. **Play**:
   - Select game mode
   - Click pieces to select
   - Click board to place
   - Watch the TRON-style battle unfold!

---

*This document serves as the complete specification for implementing the GUI version of Borderline. Implementation should follow the phases outlined above, starting with MVP and gradually adding visual polish and features.*
