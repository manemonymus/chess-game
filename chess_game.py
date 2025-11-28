import numpy as np

class ChessGame:
    def __init__(self):
        """Initialize a new chess game."""
        # Board setup
        self.rows = 8
        self.cols = 8
        self.board = np.full((self.rows, self.cols), '__', dtype=object)
        
        # Game state
        self.current_turn = 'w'
        
        # Castling tracking
        self.has_moved = {
            'wk': False, 'bk': False,
            'wr_a': False, 'wr_h': False,
            'br_a': False, 'br_h': False
        }
        
        # En passant tracking
        self.last_move = {
            'from': None,
            'to': None,
            'piece': None
        }
        
        # Coordinate mappings
        self.alphaMap = {
            'a': 0, 'b': 1, 'c': 2, 'd': 3,
            'e': 4, 'f': 5, 'g': 6, 'h': 7
        }
        
        self.numMap = {
            '8': 0, '7': 1, '6': 2, '5': 3,
            '4': 4, '3': 5, '2': 6, '1': 7
        }
        
        # Initialize board with pieces
        self._setup_board()
    
    def _setup_board(self):
        """Place pieces in starting positions."""
        for i in range(self.rows):
            self.board[1][i] = 'bp'
            self.board[6][i] = 'wp'
            if i == 0:
                self.board[0][i] = 'br'
                self.board[7][i] = 'wr'
            elif i == 1:
                self.board[0][i] = 'bn'
                self.board[7][i] = 'wn'
            elif i == 2:
                self.board[0][i] = 'bb'
                self.board[7][i] = 'wb'
            elif i == 3:
                self.board[0][i] = 'bq'
                self.board[7][i] = 'wq'
            elif i == 4:
                self.board[0][i] = 'bk'
                self.board[7][i] = 'wk'
            elif i == 5:
                self.board[0][i] = 'bb'
                self.board[7][i] = 'wb'
            elif i == 6:
                self.board[0][i] = 'bn'
                self.board[7][i] = 'wn'
            elif i == 7:
                self.board[0][i] = 'br'
                self.board[7][i] = 'wr'
    
    def isValidPawnMove(self, from_row, from_col, to_row, to_col, piece):
        colour = piece[0]
        if colour == 'w':
            direction = -1
        else:
            direction = 1

        # Moving 1 square
        if to_col == from_col and to_row == from_row + direction:
            return self.board[to_row][to_col] == '__'
        
        # Moving 2 squares
        if to_col == from_col and to_row == from_row + (direction * 2):
            if colour == 'w':
                starting_row = 6
            else:
                starting_row = 1
            if from_row == starting_row:
                return (self.board[from_row + direction][to_col] == '__' and 
                        self.board[to_row][to_col] == '__')
        
        # Diagonal capture
        if abs(to_col - from_col) == 1 and to_row == from_row + direction:
            target = self.board[to_row][to_col]
            if target != '__' and target[0] != colour:
                return True
            
            # En passant
            if self.last_move['piece'] is not None and self.last_move['piece'][1] == 'p':
                last_from_row, last_from_col = self.last_move['from']
                last_to_row, last_to_col = self.last_move['to']
                
                if abs(last_to_row - last_from_row) == 2:
                    if last_to_row == from_row and last_to_col == to_col:
                        return True
        
        return False

    def isValidKnightMove(self, from_row, from_col, to_row, to_col, piece):
        colour = piece[0]
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        is_L_shape = (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

        if not is_L_shape:
            return False
        
        target = self.board[to_row][to_col]
        if target != "__" and target[0] == colour:
            return False
        return True

    def isValidBishopMove(self, from_row, from_col, to_row, to_col, piece):
        colour = piece[0]
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        if row_diff != col_diff:
            return False
        
        if to_row > from_row:
            row_direction = 1
        else:
            row_direction = -1

        if to_col > from_col:
            col_direction = 1
        else:
            col_direction = -1

        current_row = from_row
        current_col = from_col

        while True:
            current_row += row_direction
            current_col += col_direction
            
            if current_row == to_row and current_col == to_col:
                break
            
            if self.board[current_row][current_col] != "__":
                return False
        
        target = self.board[to_row][to_col]
        if target != "__" and target[0] == colour:
            return False
        
        return True

    def isValidRookMove(self, from_row, from_col, to_row, to_col, piece):
        colour = piece[0]

        row_change = abs(to_row - from_row)
        col_change = abs(to_col - from_col)

        change = max(row_change, col_change)

        if row_change > 0 and col_change > 0:
            return False
        if row_change == 0 and col_change == 0:
            return False
        
        if to_row > from_row:
            row_direction = 1
        else:
            row_direction = -1

        if to_col > from_col:
            col_direction = 1
        else:
            col_direction = -1

        current_row = from_row
        current_col = from_col

        while True:
            if change == row_change:
                current_row += row_direction
            else:
                current_col += col_direction

            if current_row == to_row and current_col == to_col:
                break

            if self.board[current_row][current_col] != "__":
                return False
        
        target = self.board[to_row][to_col]

        if target != "__" and target[0] == colour:
            return False
        
        return True

    def isValidQueenMove(self, from_row, from_col, to_row, to_col, piece):
        return (self.isValidBishopMove(from_row, from_col, to_row, to_col, piece) or 
                self.isValidRookMove(from_row, from_col, to_row, to_col, piece))

    def isValidKingMove(self, from_row, from_col, to_row, to_col, piece):
        colour = piece[0]

        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        if row_diff > 1 or col_diff > 1:
            return False
        if row_diff == 0 and col_diff == 0:
            return False
        
        target = self.board[to_row][to_col]

        if target != "__" and target[0] == colour:
            return False
        
        enemy_colour = 'b' if colour == 'w' else 'w'
        
        old_piece = self.board[to_row][to_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = '__'
        
        under_attack = self.isSquareUnderAttack(to_row, to_col, enemy_colour)
        
        self.board[from_row][from_col] = piece
        self.board[to_row][to_col] = old_piece
        
        if under_attack:
            return False
        
        return True

    def isSquareUnderAttack(self, row, col, attacking_colour):
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]

                if piece == "__" or piece[0] != attacking_colour:
                    continue

                piece_type = piece[1]

                if piece_type == 'p':
                    if attacking_colour == 'w':
                        if r - 1 == row and abs(col - c) == 1:
                            return True
                    else:
                        if r + 1 == row and abs(col - c) == 1:
                            return True
                
                elif piece_type == 'n':
                    if self.isValidKnightMove(r, c, row, col, piece):
                        return True
                    
                elif piece_type == 'b':
                    if self.isValidBishopMove(r, c, row, col, piece):
                        return True
                
                elif piece_type == 'r':
                    if self.isValidRookMove(r, c, row, col, piece):
                        return True
                
                elif piece_type == 'q':
                    if self.isValidQueenMove(r, c, row, col, piece):
                        return True
                    
                elif piece_type == 'k':
                    if self.isValidKingMove(r, c, row, col, piece):
                        return True
        return False

    def findKing(self, colour):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == colour + 'k':
                    return (r, c)

    def isKingInCheck(self, colour):
        krow, kcol = self.findKing(colour)

        enemy_colour = ""
        if colour == 'w':
            enemy_colour = 'b'
        else:
            enemy_colour = 'w'
        
        return self.isSquareUnderAttack(krow, kcol, enemy_colour)

    def hasLegalMoves(self, colour):
        for from_row in range(8):
            for from_col in range(8):
                piece = self.board[from_row][from_col]

                if piece == '__' or piece[0] != colour:
                    continue

                piece_type = piece[1]

                for to_row in range(8):
                    for to_col in range(8):
                        is_valid = False

                        if piece_type == 'p':
                            is_valid = self.isValidPawnMove(from_row, from_col, to_row, to_col, piece)
                        elif piece_type == 'n':
                            is_valid = self.isValidKnightMove(from_row, from_col, to_row, to_col, piece)
                        elif piece_type == 'b':
                            is_valid = self.isValidBishopMove(from_row, from_col, to_row, to_col, piece)
                        elif piece_type == 'r':
                            is_valid = self.isValidRookMove(from_row, from_col, to_row, to_col, piece)
                        elif piece_type == 'q':
                            is_valid = self.isValidQueenMove(from_row, from_col, to_row, to_col, piece)
                        elif piece_type == 'k':
                            is_valid = self.isValidKingMove(from_row, from_col, to_row, to_col, piece)

                        if not is_valid:
                            continue

                        captured = self.board[to_row][to_col]
                        self.board[to_row][to_col] = piece
                        self.board[from_row][from_col] = '__'

                        kingInCheck = self.isKingInCheck(colour)

                        self.board[from_row][from_col] = piece
                        self.board[to_row][to_col] = captured

                        if not kingInCheck:
                            return True
        return False
    
    def getLegalMoves(self, from_row, from_col):
        """
        Get all legal moves for a piece at the given position.
        Returns list of (row, col) tuples.
        """
        piece = self.board[from_row][from_col]
        
        if piece == '__':
            return []
        
        if piece[0] != self.current_turn:
            return []
        
        legal_moves = []
        piece_type = piece[1]
        
        # Check all possible destination squares
        for to_row in range(8):
            for to_col in range(8):
                # Check if move is valid for this piece type
                is_valid = False
                
                if piece_type == 'p':
                    is_valid = self.isValidPawnMove(from_row, from_col, to_row, to_col, piece)
                elif piece_type == 'n':
                    is_valid = self.isValidKnightMove(from_row, from_col, to_row, to_col, piece)
                elif piece_type == 'b':
                    is_valid = self.isValidBishopMove(from_row, from_col, to_row, to_col, piece)
                elif piece_type == 'r':
                    is_valid = self.isValidRookMove(from_row, from_col, to_row, to_col, piece)
                elif piece_type == 'q':
                    is_valid = self.isValidQueenMove(from_row, from_col, to_row, to_col, piece)
                elif piece_type == 'k':
                    # For king, also check castling
                    is_valid = self.isValidKingMove(from_row, from_col, to_row, to_col, piece)
                    
                    # Check castling moves
                    if not is_valid and piece_type == 'k' and abs(to_col - from_col) == 2:
                        is_kingside = to_col > from_col
                        if self.canCastle(self.current_turn, is_kingside):
                            is_valid = True
                
                if not is_valid:
                    continue
                
                # Make move temporarily to check if it leaves king in check
                captured = self.board[to_row][to_col]
                self.board[to_row][to_col] = piece
                self.board[from_row][from_col] = '__'
                # Check if this leaves our king in check
                king_in_check = self.isKingInCheck(self.current_turn)
                # Undo the move
                self.board[from_row][from_col] = piece
                self.board[to_row][to_col] = captured
                # If move doesn't leave king in check then it's legal
                if not king_in_check:
                    legal_moves.append((to_row, to_col))
        
        return legal_moves

    def canCastle(self, colour, is_kingside):
        row = 7 if colour == 'w' else 0

        if self.has_moved[colour + 'k']:
            return False
        
        if is_kingside:
            if self.has_moved[colour + 'r_h']:
                return False
            
            if self.board[row][5] != '__' or self.board[row][6] != '__':
                return False
            
            enemy = 'b' if colour == 'w' else 'w'
            if (self.isSquareUnderAttack(row, 4, enemy) or
                self.isSquareUnderAttack(row, 5, enemy) or
                self.isSquareUnderAttack(row, 6, enemy)):
                return False
        else:
            if self.has_moved[colour + 'r_a']:
                return False
            
            if self.board[row][1] != '__' or self.board[row][2] != '__' or self.board[row][3] != '__':
                return False
            
            enemy = 'b' if colour == 'w' else 'w'
            if (self.isSquareUnderAttack(row, 4, enemy) or
                self.isSquareUnderAttack(row, 3, enemy) or
                self.isSquareUnderAttack(row, 2, enemy)):
                return False
        return True

    def makeMove(self, from_row, from_col, to_row, to_col):
        """
        Attempt to make a move. Returns (success, message).
        success: bool - whether the move was legal
        message: str - info about the move (e.g., "Check!", "Checkmate!")
        """
        piece = self.board[from_row][from_col]
        
        if piece == '__':
            return (False, "No piece there!")
        
        if piece[0] != self.current_turn:
            return (False, f"It's {self.current_turn}'s turn!")
        
        # Check for castling
        if piece[1] == 'k' and abs(to_col - from_col) == 2:
            is_kingside = to_col > from_col
            
            if self.canCastle(self.current_turn, is_kingside):
                # Perform castling
                self.board[to_row][to_col] = piece
                self.board[from_row][from_col] = '__'
                
                if is_kingside:
                    rook_from_col = 7
                    rook_to_col = 5
                else:
                    rook_from_col = 0
                    rook_to_col = 3
                
                rook = self.board[from_row][rook_from_col]
                self.board[from_row][rook_to_col] = rook
                self.board[from_row][rook_from_col] = '__'
                
                self.has_moved[piece[0] + 'k'] = True
                self.current_turn = 'b' if self.current_turn == 'w' else 'w'
                
                return (True, "Castled!")
            else:
                return (False, "Cannot castle!")
        
        # Validate move
        piece_type = piece[1]
        is_valid = False
        
        if piece_type == 'p':
            is_valid = self.isValidPawnMove(from_row, from_col, to_row, to_col, piece)
        elif piece_type == 'n':
            is_valid = self.isValidKnightMove(from_row, from_col, to_row, to_col, piece)
        elif piece_type == 'b':
            is_valid = self.isValidBishopMove(from_row, from_col, to_row, to_col, piece)
        elif piece_type == 'r':
            is_valid = self.isValidRookMove(from_row, from_col, to_row, to_col, piece)
        elif piece_type == 'q':
            is_valid = self.isValidQueenMove(from_row, from_col, to_row, to_col, piece)
        elif piece_type == 'k':
            is_valid = self.isValidKingMove(from_row, from_col, to_row, to_col, piece)
        
        if not is_valid:
            return (False, "Illegal move!")
        
        # Make the move temporarily
        captured_piece = self.board[to_row][to_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = '__'
        
        # Handle en passant capture
        if piece[1] == 'p' and captured_piece == '__' and from_col != to_col:
            captured_pawn_row = from_row
            self.board[captured_pawn_row][to_col] = '__'
        
        # Check if move leaves king in check
        if self.isKingInCheck(self.current_turn):
            self.board[from_row][from_col] = piece
            self.board[to_row][to_col] = captured_piece
            return (False, "That would leave your king in check!")
        
        # Move is legal - update state
        self.last_move['from'] = (from_row, from_col)
        self.last_move['to'] = (to_row, to_col)
        self.last_move['piece'] = piece
        
        if piece[1] == 'k':
            self.has_moved[piece[0] + 'k'] = True
        elif piece[1] == 'r':
            if from_col == 0:
                self.has_moved[piece[0] + 'r_a'] = True
            elif from_col == 7:
                self.has_moved[piece[0] + 'r_h'] = True
        
        # Check for pawn promotion
        promotion = None
        if piece[1] == 'p':
            if (piece[0] == 'w' and to_row == 0) or (piece[0] == 'b' and to_row == 7):
                promotion = 'q'  # Default to queen for GUI
                self.board[to_row][to_col] = piece[0] + promotion
        
        # Switch turns
        self.current_turn = 'b' if self.current_turn == 'w' else 'w'
        
        # Check game state
        message = ""
        if self.isKingInCheck(self.current_turn):
            if not self.hasLegalMoves(self.current_turn):
                winner = "WHITE" if self.current_turn == 'b' else "BLACK"
                return (True, f"CHECKMATE! {winner} WINS!")
            else:
                return (True, "CHECK!")
        elif not self.hasLegalMoves(self.current_turn):
            return (True, "STALEMATE!")
        
        return (True, message)



if __name__ == "__main__":
    from main import *  # Import  old file 