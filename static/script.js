let selectedSquare = null;
let currentBoard = null;
let currentTurn = 'w';

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    newGame();
    
    document.getElementById('new-game-btn').addEventListener('click', () => {
        if (confirm('Start a new game?')) {
            newGame();
        }
    });
});

async function newGame() {
    try {
        const response = await fetch('/new_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentBoard = data.board;
            currentTurn = data.current_turn;
            renderBoard();
            updateTurnDisplay();
            clearMessage();
        }
    } catch (error) {
        showMessage('Error starting new game', 'error');
    }
}

function renderBoard() {
    const boardElement = document.getElementById('chess-board');
    boardElement.innerHTML = '';
    
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.className = 'square';
            square.className += (row + col) % 2 === 0 ? ' light' : ' dark';
            square.dataset.row = row;
            square.dataset.col = col;
            
            const piece = currentBoard[row][col];
            if (piece !== '__') {
                const img = document.createElement('img');
                img.src = `/static/pieces/${piece}.png`;
                img.className = 'piece';
                img.alt = piece;
                square.appendChild(img);
            }
            
            square.addEventListener('click', () => handleSquareClick(row, col));
            boardElement.appendChild(square);
        }
    }
}

async function handleSquareClick(row, col) {
    const piece = currentBoard[row][col];
    
    if (selectedSquare) {
        // Try to make a move
        makeMove(selectedSquare.row, selectedSquare.col, row, col);
        selectedSquare = null;
        clearHighlights();
    } else if (piece !== '__' && piece[0] === currentTurn) {
        // Select a piece and show legal moves
        selectedSquare = { row, col };
        await showLegalMoves(row, col);
    }
}

async function showLegalMoves(row, col) {
    try {
        const response = await fetch('/get_legal_moves', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                from_row: row,
                from_col: col
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            clearHighlights();
            highlightSquare(row, col);
            highlightLegalMoves(data.legal_moves);
        }
    } catch (error) {
        console.error('Error getting legal moves:', error);
    }
}

function highlightLegalMoves(legalMoves) {
    const squares = document.querySelectorAll('.square');
    squares.forEach(square => {
        const row = parseInt(square.dataset.row);
        const col = parseInt(square.dataset.col);
        
        if (legalMoves.some(move => move[0] === row && move[1] === col)) {
            square.classList.add('valid-move');
        }
    });
}

async function makeMove(fromRow, fromCol, toRow, toCol) {
    try {
        const response = await fetch('/make_move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                from_row: fromRow,
                from_col: fromCol,
                to_row: toRow,
                to_col: toCol
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentBoard = data.board;
            currentTurn = data.current_turn;
            renderBoard();
            updateTurnDisplay();
            
            if (data.message) {
                if (data.message.includes('CHECKMATE')) {
                    showMessage(data.message, 'checkmate');
                } else if (data.message.includes('CHECK')) {
                    showMessage(data.message, 'check');
                } else if (data.message.includes('STALEMATE')) {
                    showMessage(data.message, 'checkmate');
                } else {
                    showMessage(data.message, 'info');
                }
            } else {
                clearMessage();
            }
        } else {
            showMessage(data.message || 'Illegal move!', 'error');
        }
    } catch (error) {
        showMessage('Error making move', 'error');
    }
}

function highlightSquare(row, col) {
    clearHighlights();
    const squares = document.querySelectorAll('.square');
    squares.forEach(square => {
        if (square.dataset.row == row && square.dataset.col == col) {
            square.classList.add('selected');
        }
    });
}

function clearHighlights() {
    document.querySelectorAll('.square').forEach(square => {
        square.classList.remove('selected', 'valid-move');
    });
}

function updateTurnDisplay() {
    const turnDisplay = document.getElementById('current-turn');
    turnDisplay.textContent = currentTurn === 'w' ? "White's Turn" : "Black's Turn";
}

function showMessage(message, type) {
    const messageElement = document.getElementById('message');
    messageElement.textContent = message;
    messageElement.className = type;
}

function clearMessage() {
    const messageElement = document.getElementById('message');
    messageElement.textContent = '';
    messageElement.className = '';
}