from flask import Flask, render_template, jsonify, request, session
from chess_game import ChessGame
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store games in memory (in production, use a database)
games = {}

@app.route('/')
def index():
    """Serve the main chess page."""
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    """Start a new chess game."""
    game_id = secrets.token_hex(8)
    games[game_id] = ChessGame()
    session['game_id'] = game_id
    
    return jsonify({
        'success': True,
        'game_id': game_id,
        'board': games[game_id].board.tolist(),
        'current_turn': games[game_id].current_turn
    })

@app.route('/get_board', methods=['GET'])
def get_board():
    """Get current board state."""
    game_id = session.get('game_id')
    
    if not game_id or game_id not in games:
        return jsonify({'success': False, 'error': 'No active game'})
    
    game = games[game_id]
    return jsonify({
        'success': True,
        'board': game.board.tolist(),
        'current_turn': game.current_turn
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    """Make a chess move."""
    game_id = session.get('game_id')
    
    if not game_id or game_id not in games:
        return jsonify({'success': False, 'error': 'No active game'})
    
    data = request.json
    from_row = data['from_row']
    from_col = data['from_col']
    to_row = data['to_row']
    to_col = data['to_col']
    
    game = games[game_id]
    success, message = game.makeMove(from_row, from_col, to_row, to_col)
    
    return jsonify({
        'success': success,
        'message': message,
        'board': game.board.tolist(),
        'current_turn': game.current_turn
    })

if __name__ == '__main__':
    app.run(debug=True)