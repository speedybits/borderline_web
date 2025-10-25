/**
 * Socket.IO Client Handler
 * Manages real-time communication with the server
 */

let socket;

function initializeSocketConnection() {
    socket = io();

    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('connection_established', (data) => {
        console.log('Connection established:', data);
    });

    socket.on('game_started', (data) => {
        console.log('Game started:', data);
        handleGameStarted(data);
    });

    socket.on('game_state', (data) => {
        console.log('Game state received:', data);
        updateGameState(data);
    });

    socket.on('piece_pending_rotation', (data) => {
        console.log('Piece pending rotation:', data);
        handlePiecePendingRotation(data);
    });

    socket.on('piece_rotated', (data) => {
        console.log('Piece rotated:', data);
        handlePieceRotated(data);
    });

    socket.on('piece_placed', (data) => {
        console.log('Piece placed:', data);
        handlePiecePlaced(data);
    });

    socket.on('ai_thinking', (data) => {
        console.log('AI thinking:', data);
        showAIThinking(data.player);
    });

    socket.on('ai_moved', (data) => {
        console.log('AI moved:', data);
        hideAIThinking();
        handlePiecePlaced(data);
    });

    socket.on('ai_no_moves', (data) => {
        console.log('AI has no valid moves:', data);
        hideAIThinking();
        addStatusMessage(`${data.player} has no valid moves - turn skipped`);
    });

    socket.on('placement_error', (data) => {
        console.log('Placement error:', data);
        addStatusMessage(`Error: ${data.message}`);
    });

    socket.on('placement_invalid', (data) => {
        console.log('Placement invalid:', data);
        addStatusMessage(`Invalid move: ${data.message}`);
        // Player remains in rotation mode - can try different position/rotation or piece
    });

    socket.on('error', (data) => {
        console.error('Server error:', data);
        addStatusMessage(`Error: ${data.message}`);
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
    });
}

function showAIThinking(player) {
    const aiThinking = document.getElementById('ai-thinking');
    aiThinking.classList.remove('hidden');
}

function hideAIThinking() {
    const aiThinking = document.getElementById('ai-thinking');
    aiThinking.classList.add('hidden');
}
