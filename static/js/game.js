/**
 * Main Game Controller
 * Handles game logic, user interaction, and state management
 */

let gameState = null;
let selectedPiece = null;
let currentGameMode = null;

// Initialize game when DOM loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing game...');
    initializeRenderer();
    setupEventListeners();
});

function setupEventListeners() {
    const canvas = document.getElementById('game-canvas');

    // Mouse move for hover preview
    canvas.addEventListener('mousemove', handleMouseMove);

    // Click to place piece
    canvas.addEventListener('click', handleCanvasClick);

    // Right-click to deselect
    canvas.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        selectedPiece = null;
        updateDisplay();
    });
}

function handleMouseMove(e) {
    if (!renderer || !gameState) return;

    const cell = renderer.getCellFromCoords(e.clientX, e.clientY);
    if (cell && selectedPiece) {
        // Redraw board with highlight
        renderer.drawBoard(gameState.board);
        const color = gameState.current_player === 'R' ? renderer.colors.redNeon : renderer.colors.blueNeon;
        renderer.highlightCell(cell.col, cell.row, color);
    }
}

function handleCanvasClick(e) {
    if (!renderer || !gameState) return;
    if (gameState.game_over) return;

    const cell = renderer.getCellFromCoords(e.clientX, e.clientY);
    if (!cell) return;

    console.log(`Clicked cell: (${cell.row}, ${cell.col})`);

    // Get selected piece index (defaults to 0 if none selected)
    const pieceIndex = window.getSelectedPieceIndex ? window.getSelectedPieceIndex() : 0;

    // Send placement to server with selected piece index
    socket.emit('place_piece', {
        row: cell.row,
        col: cell.col,
        piece_index: pieceIndex
    });
}

function handleGameStarted(data) {
    console.log('Game started with data:', data);
    gameState = data;
    currentGameMode = data.mode || 'human_vs_human';

    updateGameState(data);
    addStatusMessage('Game started!');
    addStatusMessage('Click any cell on the board to place a piece');
    addStatusMessage('Red player starts');
}

function updateGameState(data) {
    gameState = data;

    // Update board visualization
    if (renderer && data.board) {
        renderer.drawBoard(data.board);
    }

    // Update UI elements
    updateTurnIndicator(data.current_player);
    updatePieceCounts(data.red_pieces_remaining, data.blue_pieces_remaining);
    updateTurnNumber(data.turn_count);

    // Render piece pools (if function exists)
    if (window.renderPiecePools) {
        window.renderPiecePools(data);
    }

    // Check for victory
    if (data.game_over && data.winner) {
        showVictoryScreen(data.winner);
    }
}

function handlePiecePlaced(data) {
    console.log('Handling piece placement:', data);

    // Clear piece selection
    if (window.clearPieceSelection) {
        window.clearPieceSelection();
    }

    // Update game state FIRST (before animation) so piece pools reflect new current player
    if (data.game_state) {
        gameState = data.game_state;
        updateTurnIndicator(data.game_state.current_player);
        updatePieceCounts(data.game_state.red_pieces_remaining, data.game_state.blue_pieces_remaining);
        updateTurnNumber(data.game_state.turn_count);

        // Render piece pools with new current player
        if (window.renderPiecePools) {
            window.renderPiecePools(data.game_state);
        }
    }

    // Animate piece placement
    if (renderer && data.piece) {
        renderer.animatePiecePlacement(data.piece, data.col, data.row, () => {
            // After animation, redraw board with new state
            if (renderer && gameState && gameState.board) {
                renderer.drawBoard(gameState.board);
            }

            // Handle combat
            if (data.combat && data.combat.combat_occurred) {
                const combat = data.combat;
                addStatusMessage(
                    `Combat at (${data.row},${data.col}): ` +
                    `${combat.attacker_color} ${combat.attacker_roll} vs ` +
                    `${combat.defender_color} ${combat.defender_roll} - ` +
                    `${combat.winner} wins!`
                );

                // Animate dice roll
                renderer.animateDiceRoll(combat.attacker_roll, combat.defender_roll);
            } else {
                addStatusMessage(
                    `${data.piece.color} placed piece at (${data.row},${data.col})`
                );
            }

            // Check for victory
            if (gameState.game_over && gameState.winner) {
                showVictoryScreen(gameState.winner);
            }
        });
    } else {
        // Fallback if no renderer
        if (data.game_state) {
            updateGameState(data.game_state);
        }
    }

    selectedPiece = null;
}

function updateTurnIndicator(player) {
    const indicator = document.getElementById('turn-indicator');
    const text = document.getElementById('current-player-text');

    if (player === 'R') {
        text.textContent = 'RED PLAYER';
        indicator.setAttribute('data-player', 'R');
    } else {
        text.textContent = 'BLUE PLAYER';
        indicator.setAttribute('data-player', 'B');
    }

    // Trigger animation
    indicator.classList.remove('turn-transition');
    void indicator.offsetWidth; // Force reflow
    indicator.classList.add('turn-transition');
}

function updatePieceCounts(redCount, blueCount) {
    document.getElementById('red-pieces-count').textContent = redCount;
    document.getElementById('blue-pieces-count').textContent = blueCount;
}

function updateTurnNumber(turnCount) {
    document.getElementById('turn-number').textContent = turnCount;
}

function addStatusMessage(message) {
    const container = document.getElementById('status-messages');
    const messageEl = document.createElement('div');
    messageEl.className = 'status-message';
    messageEl.textContent = message;

    container.appendChild(messageEl);

    // Scroll to bottom
    container.scrollTop = container.scrollHeight;

    // Keep only last 20 messages
    while (container.children.length > 20) {
        container.removeChild(container.firstChild);
    }
}

function showVictoryScreen(winner) {
    const victoryScreen = document.getElementById('victory-screen');
    const victoryText = document.getElementById('victory-text');

    if (winner === 'R') {
        victoryText.textContent = 'RED WINS!';
        victoryText.setAttribute('data-winner', 'R');
    } else {
        victoryText.textContent = 'BLUE WINS!';
        victoryText.setAttribute('data-winner', 'B');
    }

    victoryScreen.classList.remove('hidden');
    addStatusMessage(`Game Over! ${winner === 'R' ? 'RED' : 'BLUE'} wins!`);
}

function updateDisplay() {
    if (renderer && gameState) {
        renderer.drawBoard(gameState.board);
    }
}

// Export functions for HTML inline handlers
window.handleGameStarted = handleGameStarted;
window.updateGameState = updateGameState;
window.handlePiecePlaced = handlePiecePlaced;
window.addStatusMessage = addStatusMessage;
