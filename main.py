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