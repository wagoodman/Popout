import math

PLAYER1 = 0
PLAYER2 = 1

cache = None

# This is used to simply lookup all scores for row/col/diag disc placements
# in order to score the board.
def buildScoreCache(size):
    global cache
    cache = []

    for boardValue in xrange( 0x1 << size ):
        score = 0
        consecutiveBits = 0
        # determine the score for a single player
        for index in xrange(size):
            mask = 0x1 << index
            if boardValue & mask:
                consecutiveBits += 1
            else:
                if consecutiveBits:
                    if consecutiveBits >=4:
                        consecutiveBits = 10
                    score += math.pow(10, consecutiveBits-1)
                consecutiveBits = 0

        # end of the loop, there may still be a count of consecutive bits. Check...
        if consecutiveBits:
            score += math.pow(10, consecutiveBits-1)

        cache.append(score)

    #for idx in range(len(cache)):
    #    print "%-10s" % str(bin(idx)), cache[idx]
    


#         z y x
#       z y x a
#     z y x a b
#   z y x a b
# 2 y x a b
# 1 x a b
# 0 3 4  <-- los
def getLDiagLOS(board):
    size = len(board)
    elements = (size-4)
    los = [0]*(elements*2+1)

    # Mid (0 idx)
    for idx in xrange(size):
        row = idx
        col = idx
        rowBit = 0x1 << row

        los[0] |= board[col] & rowBit

    # left of mid
    for elIdx in xrange(1,elements+1):
        elOff = elIdx
        for idx in xrange(size):
            row = idx + elOff
            col = idx
            rowBit = 0x1 << row

            if row < size and col < size:
                if board[col] & rowBit:
                    los[elIdx] |= 0x1 << idx

    # Right of mid
    for elIdx in xrange(elements+1, (elements*2)+1):
        elOff = elIdx - elements
        for idx in xrange(size):
            row = idx
            col = idx + elOff
            rowBit = 0x1 << row

            if row < size and col < size:
                if board[col] & rowBit:
                    los[elIdx] |= 0x1 << idx

    return los

# x y z
# a x y z
# b a x y z
#   b a x y z
#     b a x y 2
#       b a x 1
#         4 3 0 <-- los
def getRDiagLOS(board):
    size = len(board)
    elements = (size-4)
    los = [0]*(elements*2+1)

    # Mid (0 idx)
    for idx in xrange(size):
        row = idx
        col = size - idx - 1
        rowBit = 0x1 << row

        los[0] |= board[col] & rowBit

    # Right of mid
    for elIdx in xrange(1,elements+1):
        elOff = elIdx
        for idx in xrange(size):
            row = idx + elOff
            col = size - idx - 1
            rowBit = 0x1 << row

            if row < size and col < size:
                if board[col] & rowBit:
                    los[elIdx] |= 0x1 << idx

    # Left of mid
    for elIdx in xrange(elements+1, (elements*2)+1):
        elOff = elIdx - elements
        for idx in xrange(size):
            row = idx
            col = (size - idx - 1) - elOff
            rowBit = 0x1 << row

            if row < size and col < size:
                if board[col] & rowBit:
                    los[elIdx] |= 0x1 << idx

    return los

def getHorizLOS(board):
    size = len(board)
    los = [0]*size
    for row in xrange(size):
        rowBit = 0x1 << row
        for col in xrange(size):
            if board[col] & rowBit:
                los[row] |= 0x1 << col
    return los
        
def getLOSScore(lineOfSightElements):
    return sum( cache[element] for element in lineOfSightElements )





class Board(object):
    """
    A Board class represents a connect 4 board, where each column contains a Queue.
    Using the push method adds new elements to the top of the board. The pop method
    removes elements from the bottom of the board.
    """
    # index:
    #    player 1 = 0
    #    player 2 = 1

    def __init__(self, size, disc, board=None):
        self.size = int(size)
        self.height = int(size)
        self.width = int(size)
        self.disc = (disc[0], disc[1])
        if board:
            self.board = (list(board[0]), list(board[1]))
        else:
            self.board = ([0]*self.width, [0]*self.width)

        self.topRowBit = 0x1 << (self.height - 1)




    def __str__(self):
        ret = ""
        for col in xrange(self.width):
            ret += "%d " % int(col+1)
        ret += "\n"
        for row in reversed(xrange(self.height)):
            bit = 0x1 << row
            for col in xrange(self.width):
                if self.board[PLAYER1][col] & bit:
                    ret += self.disc[PLAYER1]
                elif self.board[PLAYER2][col] & bit:
                    ret += self.disc[PLAYER2]
                else:
                    ret += "_"
                ret += " "
            ret += "\n"
        return ret

    # DROP value into column
    def push(self, player, col):
        # requires knowledge of all pieces on the board...
        boardCol = self.board[PLAYER1][col] | self.board[PLAYER2][col] 
        boardInv = ~boardCol
        # The LSB of the inverse of the board is where the next piece should be
        # placed. X-1 XOR'd with X manipulates the only the LSB, and adding 1 will 
        # extract the LSB value.
        lsbVal = (1 + (boardInv ^ (boardInv-1))) >> 1
        self.board[player][col] = self.board[player][col] | lsbVal

    # UNDO DROP value into column
    def undoPush(self, player, col):
        # requires knowledge of all pieces on the board...
        boardCol = self.board[PLAYER1][col] | self.board[PLAYER2][col] 
        boardInv = ~boardCol
        # The LSB of the inverse of the board is where the next piece should be
        # placed. X-1 XOR'd with X manipulates the only the LSB, and adding 1 will 
        # extract the LSB value.
        lsbAdjVal = (1 + (boardInv ^ (boardInv-1))) >> 2
        self.board[player][col] = self.board[player][col] & ~lsbAdjVal


    # POP value from column
    def pop(self, player, col):
        self.board[PLAYER1][col] = self.board[PLAYER1][col] >> 1
        self.board[PLAYER2][col] = self.board[PLAYER2][col] >> 1

    # UNDO POP value from column
    def undoPop(self, player, col):
        self.board[PLAYER1][col] = self.board[PLAYER1][col] << 1
        self.board[PLAYER2][col] = self.board[PLAYER2][col] << 1
        self.board[player][col] = self.board[player][col] | 0x1

    # Generates ALL possible next moves
    def getPossibleMoves(self, player):
        nextMoves = []
        for col in xrange(self.width):
            if self.board[player][col] & 0x1 == 1:
                nextMoves.append("p%d"%col)
            if (self.board[PLAYER1][col] | self.board[PLAYER2][col] ) & self.topRowBit == 0:
                nextMoves.append("d%d"%col)
        return nextMoves


    # determines if given move is valid in context of board
    def isValidMove(self, player, move):
        action = move[0]
        col = int(move[1])

        if action == 'd':
            if (self.board[PLAYER1][col] | self.board[PLAYER2][col] ) & self.topRowBit != 0:
                return False
        elif action == 'p':
            if self.board[player][col] & 0x1 == 0:
                return False
        else:
            print "Invalid Action! %s" % repr(action)
            return False

        return True

    # commits the given move to self, not on new board!
    def doMove(self, player, move):
        action = move[0]
        col = int(move[1])

        if self.isValidMove(player, move):
                
            if action == 'd':
                self.push(player, col)
            elif action == 'p':
                self.pop(player, col)
            else:
                return False

            return True

        return False

    def undoMove(self, player, move):
        action = move[0]
        col = int(move[1])

        if action == 'd':
            self.undoPush(player, col)
        elif action == 'p':
            self.undoPop(player, col)
        else:
            return False

            return True

        return False
    """
    # commits move to new board if valid, else returns original board
    def makeBoardAndMove(self, player, move):
        newBoard = Board(self.size, self.disc, self.board)
        if newBoard.doMove(player, move):
            return newBoard
        else:
            return self
    """ 
   
    def getPlayerScore(self, player):

        # my score...
        board = self.board[player]
        vert = getLOSScore(board)
        ldiag = getLOSScore( getLDiagLOS(board) )
        rdiag = getLOSScore( getRDiagLOS(board) )
        horiz = getLOSScore( getHorizLOS(board) )
        #print player, ":\n   V:", board, "\n   H:", getHorizLOS(board), "\n   L:", getLDiagLOS(board), "\n   R:",getRDiagLOS(board)
        playerScore = vert + horiz + ldiag + rdiag

        return playerScore

    def getBoardScore(self, player):
        playerScore = self.getPlayerScore(player)
        otherPlayer = (player+1)&0x1
        otherPlayerScore = self.getPlayerScore(otherPlayer)

        boardScore = playerScore - otherPlayerScore

        return boardScore

    def isEndGame(self):
        playerScore = self.getPlayerScore(0)
        otherPlayerScore = self.getPlayerScore(1)
        #print playerScore, otherPlayerScore , math.pow(10,9)
        if playerScore >= math.pow(10, 9) or otherPlayerScore >= math.pow(10,9):
            return True

        return False




def show(board):
    print board
    print "P1", board.getPossibleMoves(PLAYER1)
    print "P2", board.getPossibleMoves(PLAYER2)
    print "Score (P1)", board.getPlayerScore(PLAYER1)#, board.getBoardScore(PLAYER1)
    print "Score (P2)", board.getPlayerScore(PLAYER2)#, board.getBoardScore(PLAYER2)
    print "isEndGame", board.isEndGame()

"""
buildScoreCache(6)
b = Board(6, "X","O")



show(b)

print b.doMove(0, "d0")
print b.doMove(0, "d1")
print b.doMove(0, "d2")
print b.doMove(1, "d3")
print b.doMove(0, "d4")
print b.doMove(0, "d5")

print b.doMove(1, "d0")
print b.doMove(1, "d1")
print b.doMove(1, "d2")
print b.doMove(0, "d3")
print b.doMove(0, "d4")
print b.doMove(1, "d5")

print b.doMove(0, "d0")
print b.doMove(1, "d1")
print b.doMove(0, "d4")
print b.doMove(0, "d5")

print b.doMove(1, "d0")
print b.doMove(0, "d5")

show(b)
"""