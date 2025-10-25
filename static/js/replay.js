/**
 * Replay Mode Controller
 * Handles replay playback, keyboard shortcuts, file upload, and drag & drop
 */

class ReplayController {
    constructor() {
        this.isPlaying = false;
        this.currentMove = 0;
        this.totalMoves = 0;
        this.playbackSpeed = 1; // 1x speed by default
        this.playbackInterval = null;
        this.replayLoaded = false;

        this.initializeEventListeners();
        this.initializeKeyboardShortcuts();
        this.initializeDragAndDrop();
    }

    initializeEventListeners() {
        console.log('Initializing replay event listeners...');

        // Playback controls
        document.getElementById('first-move-btn').addEventListener('click', () => this.firstMove());
        document.getElementById('prev-move-btn').addEventListener('click', () => this.previousMove());
        document.getElementById('play-pause-btn').addEventListener('click', () => this.togglePlayPause());
        document.getElementById('next-move-btn').addEventListener('click', () => this.nextMove());
        document.getElementById('last-move-btn').addEventListener('click', () => this.lastMove());

        // Slider
        document.getElementById('replay-slider').addEventListener('input', (e) => {
            this.gotoMove(parseInt(e.target.value));
        });

        // Speed controls
        document.querySelectorAll('.speed-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setSpeed(parseFloat(e.target.dataset.speed));
                // Update active state
                document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
            });
        });

        // File upload
        const fileInput = document.getElementById('replay-file-input');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                console.log('File selected:', e.target.files[0]);
                this.handleFileUpload(e.target.files[0]);
            });
            console.log('File input listener attached');
        } else {
            console.error('Could not find replay-file-input element');
        }

        // Socket events for replay - wait for socket to be initialized
        if (typeof socket !== 'undefined' && socket) {
            this.attachSocketListeners();
        } else {
            console.log('Socket not ready, will attach listeners when socket connects');
            // Retry after a short delay
            setTimeout(() => {
                if (typeof socket !== 'undefined' && socket) {
                    this.attachSocketListeners();
                } else {
                    console.error('Socket still not available');
                }
            }, 500);
        }
    }

    attachSocketListeners() {
        console.log('Attaching socket listeners for replay...');
        socket.on('replay_loaded', (data) => this.onReplayLoaded(data));
        socket.on('replay_step', (data) => this.onReplayStep(data));
        socket.on('replay_step_back', (data) => this.onReplayStepBack(data));
        socket.on('replay_goto', (data) => this.onReplayGoto(data));
        socket.on('replay_playing', (data) => this.onReplayPlaying(data));
        socket.on('replay_paused', (data) => this.onReplayPaused(data));
        socket.on('replay_error', (data) => this.onReplayError(data));
        console.log('Socket listeners attached');
    }

    initializeKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Only handle shortcuts when replay controls are visible
            if (document.getElementById('replay-controls').classList.contains('hidden')) {
                return;
            }

            // Prevent default for shortcuts we're using
            const shortcutKeys = ['ArrowLeft', 'ArrowRight', 'Home', 'End', ' '];
            if (shortcutKeys.includes(e.key)) {
                e.preventDefault();
            }

            switch(e.key) {
                case 'ArrowLeft':
                    this.previousMove();
                    break;
                case 'ArrowRight':
                    this.nextMove();
                    break;
                case 'Home':
                    this.firstMove();
                    break;
                case 'End':
                    this.lastMove();
                    break;
                case ' ': // Spacebar
                    this.togglePlayPause();
                    break;
            }
        });
    }

    initializeDragAndDrop() {
        const dropZone = document.getElementById('drop-zone');

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });

        dropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileUpload(files[0]);
            }
        });
    }

    handleFileUpload(file) {
        if (!file) {
            console.log('No file provided');
            return;
        }

        console.log('Processing file:', file.name);

        if (!file.name.endsWith('.json')) {
            this.showError('Please upload a .json file');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const gameData = JSON.parse(e.target.result);
                console.log('Parsed game data:', gameData);

                // Check if socket is available
                if (typeof socket === 'undefined' || !socket) {
                    this.showError('Connection not ready. Please refresh the page.');
                    return;
                }

                // Send to server to load replay
                socket.emit('load_replay_data', { game_data: gameData });

                console.log('Uploaded replay file:', file.name);
            } catch (error) {
                console.error('Error parsing JSON:', error);
                this.showError('Invalid JSON file: ' + error.message);
            }
        };
        reader.onerror = (error) => {
            console.error('Error reading file:', error);
            this.showError('Failed to read file');
        };
        reader.readAsText(file);
    }

    // Playback control methods
    firstMove() {
        if (!this.replayLoaded) return;
        this.gotoMove(0);
    }

    previousMove() {
        if (!this.replayLoaded) return;
        socket.emit('replay_step_back');
    }

    nextMove() {
        if (!this.replayLoaded) return;
        socket.emit('replay_step_forward');
    }

    lastMove() {
        if (!this.replayLoaded) return;
        this.gotoMove(this.totalMoves);
    }

    gotoMove(moveNumber) {
        if (!this.replayLoaded) return;
        socket.emit('replay_goto', { move_number: moveNumber });
    }

    togglePlayPause() {
        if (!this.replayLoaded) return;

        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    play() {
        if (this.isPlaying) return;

        this.isPlaying = true;
        socket.emit('replay_play');

        // Update UI
        document.getElementById('play-pause-btn').textContent = '⏸️';
        document.getElementById('play-pause-btn').title = 'Pause (Space)';

        // Start auto-stepping
        const baseDelay = 1000; // 1 second base
        const delay = baseDelay / this.playbackSpeed;

        this.playbackInterval = setInterval(() => {
            if (this.currentMove >= this.totalMoves) {
                this.pause();
            } else {
                this.nextMove();
            }
        }, delay);
    }

    pause() {
        if (!this.isPlaying) return;

        this.isPlaying = false;
        socket.emit('replay_pause');

        // Update UI
        document.getElementById('play-pause-btn').textContent = '▶️';
        document.getElementById('play-pause-btn').title = 'Play (Space)';

        // Stop auto-stepping
        if (this.playbackInterval) {
            clearInterval(this.playbackInterval);
            this.playbackInterval = null;
        }
    }

    setSpeed(speed) {
        this.playbackSpeed = speed;

        // If playing, restart with new speed
        if (this.isPlaying) {
            this.pause();
            this.play();
        }
    }

    // Socket event handlers
    onReplayLoaded(data) {
        console.log('Replay loaded:', data);

        this.replayLoaded = true;
        this.currentMove = 0;
        this.totalMoves = data.total_moves;

        // Hide upload section, show playback controls
        console.log('Hiding upload section, showing playback section...');
        const uploadSection = document.getElementById('replay-upload-section');
        const playbackSection = document.getElementById('replay-playback-section');

        if (uploadSection) {
            uploadSection.classList.add('hidden');
            console.log('Upload section hidden:', uploadSection.classList.contains('hidden'));
        } else {
            console.error('Could not find replay-upload-section');
        }

        if (playbackSection) {
            playbackSection.classList.remove('hidden');
            console.log('Playback section visible:', !playbackSection.classList.contains('hidden'));
        } else {
            console.error('Could not find replay-playback-section');
        }

        // Update UI
        document.getElementById('total-moves').textContent = this.totalMoves;
        document.getElementById('current-move').textContent = 0;
        document.getElementById('replay-slider').max = this.totalMoves;
        document.getElementById('replay-slider').value = 0;

        // Render the initial game state
        if (data.game_state && typeof updateGameState === 'function') {
            console.log('Rendering initial game state...');
            updateGameState(data.game_state);
        } else {
            console.warn('updateGameState function not available or no game_state data');
        }

        this.showMessage(`Replay loaded: ${this.totalMoves} moves`);

        // Visual feedback - removed alert, just log
        console.log(`✅ Replay loaded: ${this.totalMoves} moves ready`);
    }

    onReplayStep(data) {
        console.log('Replay step:', data);

        this.currentMove = data.move_number;

        // Update UI
        document.getElementById('current-move').textContent = this.currentMove;
        document.getElementById('replay-slider').value = this.currentMove;

        // Update game state visualization
        if (data.game_state && typeof updateGameState === 'function') {
            updateGameState(data.game_state);
        }
    }

    onReplayStepBack(data) {
        console.log('Replay step back:', data);

        this.currentMove = data.move_number;

        // Update UI
        document.getElementById('current-move').textContent = this.currentMove;
        document.getElementById('replay-slider').value = this.currentMove;

        // Update game state visualization
        if (data.game_state && typeof updateGameState === 'function') {
            updateGameState(data.game_state);
        }
    }

    onReplayGoto(data) {
        console.log('Replay goto:', data);

        this.currentMove = data.move_number;

        // Update UI
        document.getElementById('current-move').textContent = this.currentMove;
        document.getElementById('replay-slider').value = this.currentMove;

        // Update game state visualization
        if (data.game_state && typeof updateGameState === 'function') {
            updateGameState(data.game_state);
        }
    }

    onReplayPlaying(data) {
        console.log('Replay playing');
        this.isPlaying = true;
    }

    onReplayPaused(data) {
        console.log('Replay paused');
        this.isPlaying = false;
    }

    onReplayError(data) {
        console.error('Replay error:', data.message);
        this.showError(data.message);

        // If we hit the end, pause
        if (data.message.includes('end')) {
            this.pause();
        }
    }

    showMessage(message) {
        // Use the existing status message system
        if (typeof addStatusMessage === 'function') {
            addStatusMessage(message);
        }
        console.log(message);
    }

    showError(message) {
        alert('Replay Error: ' + message);
        console.error(message);
    }
}

// Initialize replay controller when page loads
let replayController;

window.addEventListener('load', () => {
    replayController = new ReplayController();
    console.log('Replay controller initialized');
});
