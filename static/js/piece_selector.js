/**
 * Piece Selection UI
 * Handles rendering and selecting pieces from player hands
 */

let selectedPieceIndex = null;

function renderPiecePools(gameState) {
    if (!gameState) return;

    // Only render pieces for human players
    const currentPlayer = gameState.current_player;

    // Render red pieces (always show for human vs human, or if red is current player in human vs AI)
    renderPlayerPieces('R', gameState.red_pieces, currentPlayer === 'R');

    // Render blue pieces (always show for human vs human, or if blue is current player in human vs AI)
    renderPlayerPieces('B', gameState.blue_pieces, currentPlayer === 'B');
}

function renderPlayerPieces(color, pieces, isCurrentPlayer) {
    const poolId = color === 'R' ? 'red-pieces-pool' : 'blue-pieces-pool';
    const pool = document.getElementById(poolId);
    if (!pool) return;

    // Clear existing pieces
    pool.innerHTML = '';

    // Render each piece
    pieces.forEach((piece, index) => {
        const pieceElement = createPieceElement(piece, index, color, isCurrentPlayer);
        pool.appendChild(pieceElement);
    });
}

function createPieceElement(piece, index, color, isCurrentPlayer) {
    const pieceDiv = document.createElement('div');
    pieceDiv.className = 'hand-piece';
    pieceDiv.dataset.pieceIndex = index;
    pieceDiv.dataset.color = color;

    // Add selection state
    if (isCurrentPlayer && selectedPieceIndex === index) {
        pieceDiv.classList.add('selected');
    }

    // Disable if not current player
    if (!isCurrentPlayer) {
        pieceDiv.classList.add('disabled');
    }

    // Create 3x3 grid for pips
    const grid = document.createElement('div');
    grid.className = 'piece-grid';

    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
            const pip = document.createElement('div');
            pip.className = 'piece-pip';

            // Check if this position has a pip
            if (piece.pips[row][col] === color) {
                pip.classList.add('pip-filled');
                pip.classList.add(color === 'R' ? 'pip-red' : 'pip-blue');
            } else {
                pip.classList.add('pip-empty');
            }

            grid.appendChild(pip);
        }
    }

    pieceDiv.appendChild(grid);

    // Add power indicator
    const powerLabel = document.createElement('div');
    powerLabel.className = 'piece-power';
    powerLabel.textContent = `PWR: ${piece.power}`;
    pieceDiv.appendChild(powerLabel);

    // Add click handler for selection (only if current player)
    if (isCurrentPlayer) {
        pieceDiv.addEventListener('click', () => selectPiece(index, color));
    }

    return pieceDiv;
}

function selectPiece(index, color) {
    // Only allow selection if it's this color's turn
    if (!gameState || gameState.current_player !== color) {
        return;
    }

    // Update selection
    selectedPieceIndex = index;

    // Re-render to show selection
    renderPiecePools(gameState);

    // Update status
    addStatusMessage(`Selected piece ${index + 1} (Power: ${gameState[color === 'R' ? 'red_pieces' : 'blue_pieces'][index].power})`);
}

function getSelectedPieceIndex() {
    return selectedPieceIndex !== null ? selectedPieceIndex : 0;
}

function clearPieceSelection() {
    selectedPieceIndex = null;
}

// Export functions for use in other modules
window.renderPiecePools = renderPiecePools;
window.getSelectedPieceIndex = getSelectedPieceIndex;
window.clearPieceSelection = clearPieceSelection;
window.selectPiece = selectPiece;
