/**
 * Piece Selection UI
 * Handles rendering and selecting pieces from player hands
 */

let selectedPieceIndex = null;

function renderPiecePools(gameState) {
    console.log('renderPiecePools called with:', gameState);
    if (!gameState) {
        console.warn('No game state provided to renderPiecePools');
        return;
    }

    // Only render pieces for human players
    const currentPlayer = gameState.current_player;

    console.log('Rendering pieces - red:', gameState.red_pieces?.length, 'blue:', gameState.blue_pieces?.length);

    // Render red pieces (always show for human vs human, or if red is current player in human vs AI)
    renderPlayerPieces('R', gameState.red_pieces, currentPlayer === 'R');

    // Render blue pieces (always show for human vs human, or if blue is current player in human vs AI)
    renderPlayerPieces('B', gameState.blue_pieces, currentPlayer === 'B');
}

function renderPlayerPieces(color, pieces, isCurrentPlayer) {
    const poolId = color === 'R' ? 'red-pieces-pool' : 'blue-pieces-pool';
    const pool = document.getElementById(poolId);

    console.log(`Rendering ${color} pieces:`, { poolId, poolFound: !!pool, piecesCount: pieces?.length });

    if (!pool) {
        console.error(`Pool element not found: ${poolId}`);
        return;
    }

    if (!pieces || pieces.length === 0) {
        console.warn(`No pieces to render for ${color}`);
        pool.innerHTML = '<div style="color: white; padding: 10px;">No pieces</div>';
        return;
    }

    // Clear existing pieces
    pool.innerHTML = '';

    // Group identical pieces together
    const groupedPieces = groupPiecesByPattern(pieces);
    console.log(`${color} grouped into ${groupedPieces.length} groups`);

    // Render each unique piece with count
    groupedPieces.forEach((group, index) => {
        const pieceElement = createGroupedPieceElement(group, color, isCurrentPlayer);
        pool.appendChild(pieceElement);
        console.log(`Added ${color} piece group ${index + 1}/${groupedPieces.length}`);
    });
}

function groupPiecesByPattern(pieces) {
    const groups = [];
    const processedIndices = new Set();

    pieces.forEach((piece, index) => {
        if (processedIndices.has(index)) return;

        // Find all pieces with identical pip patterns
        const identicalIndices = [index];
        const pattern = JSON.stringify(piece.pips);

        for (let i = index + 1; i < pieces.length; i++) {
            if (!processedIndices.has(i) && JSON.stringify(pieces[i].pips) === pattern) {
                identicalIndices.push(i);
                processedIndices.add(i);
            }
        }

        processedIndices.add(index);

        groups.push({
            piece: piece,
            indices: identicalIndices,
            count: identicalIndices.length
        });
    });

    return groups;
}

function createGroupedPieceElement(group, color, isCurrentPlayer) {
    const pieceDiv = document.createElement('div');
    pieceDiv.className = 'hand-piece';

    // Store all indices that belong to this group
    pieceDiv.dataset.groupIndices = JSON.stringify(group.indices);
    pieceDiv.dataset.color = color;

    // Check if any piece in this group is selected
    const isGroupSelected = isCurrentPlayer && group.indices.includes(selectedPieceIndex);
    if (isGroupSelected) {
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
            if (group.piece.pips[row][col] === color) {
                pip.classList.add('pip-filled');
                pip.classList.add(color === 'R' ? 'pip-red' : 'pip-blue');
            } else {
                pip.classList.add('pip-empty');
            }

            grid.appendChild(pip);
        }
    }

    pieceDiv.appendChild(grid);

    // Add power and count indicator
    const infoContainer = document.createElement('div');
    infoContainer.className = 'piece-info';

    const powerLabel = document.createElement('div');
    powerLabel.className = 'piece-power';
    powerLabel.textContent = `PWR: ${group.piece.power}`;
    infoContainer.appendChild(powerLabel);

    // Add count label if more than one
    if (group.count > 1) {
        const countLabel = document.createElement('div');
        countLabel.className = 'piece-count';
        countLabel.textContent = `${group.count}x`;
        infoContainer.appendChild(countLabel);
    }

    pieceDiv.appendChild(infoContainer);

    // Add click handler for selection (only if current player)
    if (isCurrentPlayer) {
        pieceDiv.addEventListener('click', () => selectPieceFromGroup(group, color));
    }

    return pieceDiv;
}

function selectPieceFromGroup(group, color) {
    // Only allow selection if it's this color's turn
    if (!gameState || gameState.current_player !== color) {
        return;
    }

    // Select the first available piece from the group
    const firstAvailableIndex = group.indices[0];
    selectPiece(firstAvailableIndex, color);
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
