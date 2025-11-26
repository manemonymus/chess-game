import numpy as np
#initialising board
rows=8
cols=8
board=np.full((rows,cols),'__',dtype=object)


#check if move is legal
def isValidPawnMove(board, from_row, from_col, to_row, to_col, piece):
    colour=piece[0]
    if colour=='w':
        direction = -1 #row decreases since white moves up
    else:
        direction = 1 #black row goes down


    #moving 1 square
    if to_col == from_col and to_row == from_row + direction:  #check if the pos pawn is going to is empty
        return board[to_row][to_col]=='__'
    
    #moving 2 squares
    if to_col == from_col and to_row == from_row + (direction * 2):
        if colour=='w':
            starting_row=6
        else:
            starting_row=1
        if from_row == starting_row: 

            #both squares need to be empty
            return (board[from_row + direction][to_col] =='__' and 
                    board[to_row][to_col]=='__')
        
    # for captures (diagonal)
    if abs(to_col - from_col)==1 and to_row == from_row + direction:
        target = board[to_row][to_col]

        #should have enemy there
        return (target !='__' and target[0] != colour)
    return False

def isValidKnightMove(board, from_row, from_col, to_row, to_col, piece):
    colour = piece[0]
    row_diff=abs(to_row-from_row)
    col_diff=abs(to_col-from_col)

    is_L_shape=(row_diff==2 and col_diff==1) or (row_diff==1 and col_diff==2)

    if not is_L_shape:
        return False
    
    target=board[to_row][to_col]

    #check if target has own piece
    if target!="__" and target[0]==colour:
        return False
    return True

def isValidBishopMove(board, from_row, from_col, to_row, to_col, piece):
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

    # Check all squares between start and end
    while True:
        current_row += row_direction
        current_col += col_direction
        
        # Stop before checking the destination square
        if current_row == to_row and current_col == to_col:
            break
        
        # Check if this square is blocked
        if board[current_row][current_col] != "__":
            return False
    
    # Check destination square
    target = board[to_row][to_col]
    if target != "__" and target[0] == colour:
        return False
    
    return True

def isValidRookMove(board, from_row, from_col, to_row, to_col, piece):
    colour=piece[0]

    row_change=abs(to_row-from_row)
    col_change=abs(to_col-from_col)

    change=max(row_change,col_change)

    if row_change>0 and col_change>0:   #must move in straight line
        return False
    if row_change==0 and col_change==0:
        return False
    
    #determine direction
    if to_row>from_row:
        row_direction=1
    else:
        row_direction=-1

    if to_col>from_col:
        col_direction=1
    else:
        col_direction=-1

    current_row=from_row
    current_col=from_col

    #check path
    while True:
        if change==row_change:
            current_row+=row_direction
        else:
            current_col+=col_direction


        if current_row==to_row and current_col==to_col:
            break

        if board[current_row][current_col]!="__":
            return False
        
    #check destination
    target=board[to_row][to_col]

    if target !="__" and target[0]==colour:
        return False
    
    return True


def isValidQueenMove(board, from_row, from_col, to_row, to_col, piece): #queen is the same as rook and bishop combined
    return (isValidBishopMove(board, from_row, from_col, to_row, to_col, piece) or 
            isValidRookMove(board, from_row, from_col, to_row, to_col, piece))  


def isValidKingMove(board, from_row, from_col, to_row, to_col, piece):
    colour = piece[0]

    row_diff=abs(to_row-from_row)
    col_diff=abs(to_col-from_col)

    if row_diff >1 or col_diff >1:  # Must move exactly 1 square
        return False
    if row_diff==0 and col_diff==0: # Must actually move
        return False
    
    # Check destination
    target=board[to_row][to_col]

    if target !="__" and target[0]==colour:
        return False
    
    #  Check if king would be moving into check 
    enemy_colour = 'b' if colour == 'w' else 'w'
    
    # Temporarily make the move to check
    old_piece = board[to_row][to_col]
    board[to_row][to_col] = piece
    board[from_row][from_col] = '__'
    
    # Is the destination square under attack?
    under_attack = isSquareUnderAttack(board, to_row, to_col, enemy_colour)
    
    # Undo the temporary move
    board[from_row][from_col] = piece
    board[to_row][to_col] = old_piece
    
    if under_attack:
        return False
    
    return True

def isSquareUnderAttack(board,row,col,attacking_colour):
    """
    Check if a square is under attack by pieces of a given color.

    Returns:
        True if any piece of attacking_color can attack (row, col)
    """

    # check every square on board
    for r in range(8):
        for c in range(8):
            piece=board[r][c]

            if piece=="__" or piece[0]!=attacking_colour:
                continue

            piece_type=piece[1]


            #pawn attack differently than they move
            if piece_type=='p':
                if attacking_colour=='w':
                    # white pawns attack diagonally upward
                    if r-1==row and abs(col-c)==1:
                        return True
                
                else:
                    # black pawns attack diagonally downwards
                    if r+1==row and abs(col-c)==1:
                        return True
            
            #for other pieces we can just use their respective functions
            elif piece_type=='n':
                if isValidKnightMove(board,r,c,row,col,piece):
                    return True
                
            elif piece_type=='b':
                if isValidBishopMove(board,r,c,row,col,piece):
                    return True
            
            elif piece_type=='r':
                if isValidRookMove(board,r,c,row,col,piece):
                    return True
            
            elif piece_type=='q':
                if isValidQueenMove(board,r,c,row,col,piece):
                    return True
                
            elif piece_type=='k':
                if isValidKingMove(board,r,c,row,col,piece):
                    return True
    return False


def findKing(board, colour):
    """
    Find the position of the king for a given color.
    """
    for r in range(8):
        for c in range(8):
            if board[r][c] == colour + 'k':
                return (r, c)
                
def isKingInCheck(board,colour):

    """
    Check if the king of a given color is currently in check.
    
    """
    krow,kcol=findKing(board,colour)

    enemy_colour=""
    if colour=='w':
        enemy_colour='b'
    else:
        enemy_colour='w'
    
    return isSquareUnderAttack(board,krow,kcol,enemy_colour)

def hasLegalMoves(board,colour):
    #check if player has legal moves left
    for from_row in range(8):
        for from_col in range(8):
            piece=board[from_row][from_col]

            if piece=='__' or piece[0]!=colour:
                continue


            piece_type=piece[1]

            for to_row in range(8):
                for to_col in range(8):
                    #check if move is valid for certain piece type
                    isValid=False

                    if piece_type == 'p':
                        is_valid = isValidPawnMove(board, from_row, from_col, to_row, to_col, piece)
                    elif piece_type == 'n':
                        is_valid = isValidKnightMove(board, from_row, from_col, to_row, to_col, piece)
                    elif piece_type == 'b':
                        is_valid = isValidBishopMove(board, from_row, from_col, to_row, to_col, piece)
                    elif piece_type == 'r':
                        is_valid = isValidRookMove(board, from_row, from_col, to_row, to_col, piece)
                    elif piece_type == 'q':
                        is_valid = isValidQueenMove(board, from_row, from_col, to_row, to_col, piece)
                    elif piece_type == 'k':
                        is_valid = isValidKingMove(board, from_row, from_col, to_row, to_col, piece)

                    if not is_valid:
                        continue    #this moves doesnt work for this piece


                    #if move is valid for a piece,does it leave the king in check

                    #make move temporarily
                    captured=board[to_row][to_col]
                    board[to_row][to_col]=piece
                    board[from_row][from_col]=="__"

                    #check if king is still in check
                    kingInCheck=isKingInCheck(board,colour)

                    # Undo the move
                    board[from_row][from_col] = piece
                    board[to_row][to_col] = captured

                    if not kingInCheck:
                        return True #found legal move
    return False

                    





    



    


        

    



        






def printBoard(board):
    print("\n   a   b   c   d   e   f   g   h")
    for row in range(rows):
        print(8-row, end=" ")
        for col in range(cols):
            piece = board[row][col]
            print(f" {piece} ", end="")
        print()
    print()

for i in range(rows):
    board[1][i]='bp'
    board[-2][i]='wp'
    if i==0:
        board[0][i]='br'
        board[-1][i]='wr'

    elif i==1:
        board[0][i]='bn'
        board[-1][i]='wn'
    elif i==2:
        board[0][i]='bb'
        board[-1][i]='wb'
    elif i==3:
        board[0][i]='bq'
        board[-1][i]='wq'
    elif i==4:
        board[0][i]='bk'
        board[-1][i]='wk'
    elif i==5:
        board[0][i]='bb'
        board[-1][i]='wb'
    elif i==6:
        board[0][i]='bn'
        board[-1][i]='wn'
    elif i==7:
        board[0][i]='br'
        board[-1][i]='wr'
    
printBoard(board)
alphaMap={
    'a':0,
    'b':1,
    'c':2,
    'd':3,
    'e':4,
    'f':5,
    'g':6,
    'h':7
    

}
numMap={
    '8':0,
    '7':1,
    '6':2,
    '5':3,
    '4':4,
    '3':5,
    '2':6,
    '1':7
}


# Game loop
current_turn = 'w'
while True:
    move = input("Enter your move (e.g., 'e2 e4') or 'resign': ")
    
    if move == 'resign':
        break
    
    print(f"You entered: {move}")
    if " " in move:
        moves = move.lower().split()
        initialMove = moves[0]  
        finalMove = moves[1]    
        
        from_row = numMap[initialMove[1]]  
        from_col = alphaMap[initialMove[0]]  
        
        to_row = numMap[finalMove[1]]
        to_col = alphaMap[finalMove[0]]
        
   
        piece = board[from_row][from_col]
        if piece == '__':
            print("No piece there!")
            continue

        if piece[1]=='p':#pawn
            if not isValidPawnMove(board,from_row,from_col,to_row,to_col,piece):
                print("Illegal Move!")

                continue
        elif piece[1]=='n':#knight
            if not isValidKnightMove(board,from_row,from_col,to_row,to_col,piece):
                print("Illegal Move!")

                continue
        elif piece[1]=='b': #bishop
            if not isValidBishopMove(board,from_row,from_col,to_row,to_col,piece):
                print("Illegal Move!")

                continue
        elif piece[1]=='r': #rook
            if not isValidRookMove(board,from_row,from_col,to_row,to_col,piece):
                print("Illegal Move!")

                continue
        elif piece[1]=="q": #queen
            if not isValidQueenMove(board,from_row,from_col,to_row,to_col,piece):
                print("Illegal Move!")

                continue
        elif piece[1]=='k': #king
            if not isValidKingMove(board,from_row,from_col,to_row,to_col,piece):
                print("Illegal Move!")

                continue


            
    
        if piece[0] != current_turn:  
            if current_turn =='w':
                print("It's white's turn!")
            else:
                print("It's Black's turn!")
            
            continue
        
        # note the piece at destination incase u need to undo
        captured_piece = board[to_row][to_col]

        # Make the move temporarily
        board[to_row][to_col] = piece
        board[from_row][from_col] = '__'

        # Check if this move leaves YOUR king in check
        if isKingInCheck(board, current_turn):
            # UNDO the move
            board[from_row][from_col] = piece
            board[to_row][to_col] = captured_piece
            print("Illegal move! That would leave your king in check.")
            continue  # Don't switch turns

        
        

        # Switch turns
        if current_turn == 'w':
            current_turn = 'b'
        else:
            current_turn = 'w'

        printBoard(board)

        # Check if the move puts opponent in check
        enemy_colour = 'b' if current_turn == 'w' else 'w'

        

        # Check if the player who's about to move is in check
        if isKingInCheck(board, current_turn):
            color_name = "WHITE" if current_turn == 'w' else "BLACK"
            print(f"\n*** {color_name} IS IN CHECK! ***\n")
            
            # Check for checkmate
            if not hasLegalMoves(board, current_turn):
                winner = "WHITE" if current_turn == 'b' else "BLACK"
                print(f"\n🎉 CHECKMATE! {winner} WINS! 🎉\n")
                break  
        
        else:
            # Not in check - check for stalemate
            if not hasLegalMoves(board, current_turn):
                print("\n STALEMATE! The game is a draw. \n")
                break  