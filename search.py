import sys

def minimax(board, curdepth, maxdepth, alpha, beta, useAlphaBeta):
    
    if (curdepth+1)%2 == 0:
        myDisc = "X"
    elif (curdepth+1)%2 != 0:
        myDisc = "O"
    
    if board.validEndGame() or int(curdepth) >= maxdepth:
        return  board.getBoardScore(myDisc), board.getMoves(myDisc)[0]

    bestMove = None
    bestScore = int(-1*(sys.maxsize-2))

    for move in board.getMoves(myDisc):
        moved = board.makeBoard(move, myDisc)

        score, _ = minimax(moved, curdepth+1, maxdepth, -beta, max(int(alpha), bestScore), useAlphaBeta)

        score = -score
        
        if score > bestScore:
            bestScore = score
            bestMove = move

            if useAlphaBeta:
                if bestScore >= beta:
                    return bestScore, bestMove

    return bestScore, bestMove
        
