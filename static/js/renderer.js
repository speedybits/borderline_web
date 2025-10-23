/**
 * Canvas Renderer with TRON Aesthetics
 * Handles all drawing operations with glowing effects
 */

class BoardRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.cellSize = 80;
        this.boardWidth = 6;
        this.boardHeight = 8;
        this.pipSize = 24;
        this.pipGap = 2;

        // TRON Colors
        this.colors = {
            background: '#0a0a0a',
            grid: '#1a1a2e',
            redNeon: '#ff0055',
            blueNeon: '#00d4ff',
            greenAccent: '#00ff88',
            amber: '#ffaa00'
        };

        this.board = null;
    }

    clear() {
        this.ctx.fillStyle = this.colors.background;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }

    drawBoard(boardData) {
        this.board = boardData;
        this.clear();
        this.drawGrid();
        this.drawPieces(boardData);
    }

    drawGrid() {
        this.ctx.strokeStyle = this.colors.grid;
        this.ctx.lineWidth = 2;

        // Vertical lines
        for (let col = 0; col <= this.boardWidth; col++) {
            const x = col * this.cellSize;
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.boardHeight * this.cellSize);
            this.ctx.stroke();
        }

        // Horizontal lines
        for (let row = 0; row <= this.boardHeight; row++) {
            const y = row * this.cellSize;
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.boardWidth * this.cellSize, y);
            this.ctx.stroke();
        }
    }

    drawPieces(boardData) {
        if (!boardData || !boardData.grid) return;

        for (let row = 0; row < this.boardHeight; row++) {
            for (let col = 0; col < this.boardWidth; col++) {
                const piece = boardData.grid[row][col];
                if (piece) {
                    this.drawPiece(piece, col, row);
                }
            }
        }
    }

    drawPiece(piece, col, row) {
        const x = col * this.cellSize;
        const y = row * this.cellSize;
        const color = piece.color === 'R' ? this.colors.redNeon : this.colors.blueNeon;

        // Draw 3x3 pip grid
        for (let pipRow = 0; pipRow < 3; pipRow++) {
            for (let pipCol = 0; pipCol < 3; pipCol++) {
                const pipValue = piece.pips[pipRow][pipCol];
                if (pipValue === piece.color) {
                    const pipX = x + pipCol * (this.pipSize + this.pipGap) + 10;
                    const pipY = y + pipRow * (this.pipSize + this.pipGap) + 10;
                    this.drawPip(pipX, pipY, color);
                }
            }
        }

        // Draw power level
        this.drawPowerLevel(x + 4, y + 4, piece.power, color);
    }

    drawPip(x, y, color) {
        const radius = this.pipSize / 2;
        const centerX = x + radius;
        const centerY = y + radius;

        // Outer glow
        this.ctx.shadowColor = color;
        this.ctx.shadowBlur = 15;

        // Pip circle
        this.ctx.fillStyle = color;
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
        this.ctx.fill();

        // Inner highlight
        this.ctx.shadowBlur = 0;
        this.ctx.fillStyle = '#ffffff';
        this.ctx.beginPath();
        this.ctx.arc(centerX - 3, centerY - 3, 4, 0, Math.PI * 2);
        this.ctx.fill();
    }

    drawPowerLevel(x, y, power, color) {
        this.ctx.shadowColor = this.colors.amber;
        this.ctx.shadowBlur = 5;
        this.ctx.fillStyle = this.colors.amber;
        this.ctx.font = 'bold 14px Orbitron';
        this.ctx.fillText(power.toString(), x, y + 12);
        this.ctx.shadowBlur = 0;
    }

    highlightCell(col, row, color) {
        const x = col * this.cellSize;
        const y = row * this.cellSize;

        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = 3;
        this.ctx.shadowColor = color;
        this.ctx.shadowBlur = 15;

        this.ctx.strokeRect(x + 2, y + 2, this.cellSize - 4, this.cellSize - 4);

        this.ctx.shadowBlur = 0;
    }

    getCellFromCoords(mouseX, mouseY) {
        const rect = this.canvas.getBoundingClientRect();
        const x = mouseX - rect.left;
        const y = mouseY - rect.top;

        const col = Math.floor(x / this.cellSize);
        const row = Math.floor(y / this.cellSize);

        if (col >= 0 && col < this.boardWidth && row >= 0 && row < this.boardHeight) {
            return { row, col };
        }

        return null;
    }

    animateDiceRoll(attackerRoll, defenderRoll) {
        const attackerDice = document.getElementById('attacker-dice');
        const defenderDice = document.getElementById('defender-dice');
        const diceZone = document.getElementById('dice-zone');

        // Show dice zone
        diceZone.classList.remove('hidden');

        // Reset dice
        attackerDice.querySelector('.dice-value').textContent = '?';
        defenderDice.querySelector('.dice-value').textContent = '?';
        attackerDice.classList.add('tumbling');
        defenderDice.classList.add('tumbling');

        // Tumble for 1 second
        setTimeout(() => {
            attackerDice.classList.remove('tumbling');
            defenderDice.classList.remove('tumbling');
            attackerDice.querySelector('.dice-value').textContent = attackerRoll;
            defenderDice.querySelector('.dice-value').textContent = defenderRoll;

            // Hide after 2 seconds
            setTimeout(() => {
                diceZone.classList.add('hidden');
            }, 2000);
        }, 1000);
    }
}

// Global renderer instance
let renderer;

function initializeRenderer() {
    renderer = new BoardRenderer('game-canvas');
    console.log('Renderer initialized');
}
