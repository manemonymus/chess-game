import numpy as np
#initialising board
rows=8
cols=8
board=np.full((rows,cols),'__',dtype=object)

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



