import sys
count = 0
def minimax(board, curdepth, maxdepth, alpha, beta, useAlphaBeta):
    global count
    count += 1
    if (curdepth+1)%2 == 0:
        myDisc = "X"
    elif (curdepth+1)%2 != 0:
        myDisc = "O"
    
    if board.validEndGame() or int(curdepth) >= maxdepth:
        return  board.getBoardScore(myDisc), board.getMoves(myDisc)[0]

    bestMove = None
    bestScore = int(-1*(sys.maxsize-2))

    for move in board.getMoves(myDisc):
        board.doMove(move, myDisc)
        score, _ = minimax(board, curdepth+1, maxdepth, -beta, max(int(alpha), bestScore), useAlphaBeta)
        board.undoMove(move, myDisc)

        score = -score
        
        if score > bestScore:
            bestScore = score
            bestMove = move

            if useAlphaBeta:
                if bestScore >= beta:
                    return bestScore, bestMove

    return bestScore, bestMove
        
