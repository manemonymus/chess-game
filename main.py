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
    
    return True


    


    


        

    



        






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


            
    
        if piece[0] != current_turn:  # piece[0] is 'w' or 'b'
            if current_turn =='w':
                print("It's white's turn!")
            else:
                print("It's Black's turn!")
            
            continue

        board[to_row][to_col] = piece
        board[from_row][from_col] = '__'
        if current_turn == 'w':
            current_turn = 'b'
        else:
            current_turn = 'w'  
        
        
    printBoard(board)

