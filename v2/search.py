import sys
count = 0
def minimax(board, curdepth, maxdepth, alpha, beta, useAlphaBeta):
    global count
    count += 1
    if (curdepth+1)%2 == 0:
        player = 0
    elif (curdepth+1)%2 != 0:
        player = 1
    
    if board.isEndGame() or int(curdepth) >= maxdepth:
        return  board.getBoardScore(player), board.getPossibleMoves(player)[0]

    bestMove = None
    bestScore = int(-1*(sys.maxsize-2))

    for move in board.getPossibleMoves(player):
        board.doMove(player, move)

        score, _ = minimax(board, curdepth+1, maxdepth, -beta, max(int(alpha), bestScore), useAlphaBeta)
        board.undoMove(player, move)

        score = -score
        
        
        if score > bestScore:
            bestScore = score
            bestMove = move

            if useAlphaBeta:
                if bestScore >= beta:
                    return bestScore, bestMove

    return bestScore, bestMove
        
