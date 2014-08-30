import sys
import math
import time
import board
import search 

def speakHAL(isMoveValid):
    if isMoveValid:
        print ("I'm sorry, Dave. I'm afraid I can't let you do that... Please input a valid move.")
    return isMoveValid

def cleanInput(move):

    if (move[0].lower() == "q"):
        print ("Game Abandoned.\n=====================================\n")
        sys.exit()
    
    if len(move) >= 2:     
        if (move[0].lower() == "d" or move[0].lower() == "p"):
            if (move[1].isdigit()):
                return str(move[0]+str(int(move[1])-1))
    return move

def validDim(size):
    if size and size.isdigit() and int(size) >= 4:
            return True
    return False


print "POPOUT... kinda like connect 4"
# ======================================================================
# INIT GAME
"""
searchOption = ""
depth = ""
playerOption = ""
while searchOption.lower() != "m" and searchOption.lower() != "a":
    searchOption = raw_input("Specify type of AI search [minimax=m, alpha-beta=a]: ")

if searchOption.lower() == "m":
    useAlphaBeta = False
else:
    useAlphaBeta = True

while not depth.isdigit() :
    depth = raw_input("Maximum search depth: ")

while playerOption.lower() != "h" and playerOption.lower() != "c":
    playerOption = raw_input("Specify who gets the first move [human=h, computer=c]: ")

size = None

while not validDim(size):
    height = raw_input("Specify Board Size >4: ")



"""
useAlphaBeta = False
depth = 5
playerOption = "h"
size = 6

board.buildScoreCache(size)

# ======================================================================
# START GAME

move = ""
boardInstance = board.Board(math.fabs(int(size)), ["X", "O"])
humanTurn = True
humanTurnMessage = "Enter your move [Operation=d,p][Column=1-"+str(boardInstance.width)+"]: "
if playerOption.lower() == "c":
    humanTurn = False

print boardInstance
while move.lower() != "q" and not boardInstance.isEndGame() :

    if humanTurn == True:
        humanTurn = False

        move = cleanInput(raw_input(humanTurnMessage))
        while speakHAL( not boardInstance.doMove(0, move) ) :
            move = cleanInput(raw_input(humanTurnMessage))

        print boardInstance
 
    else:
        s = time.time()
        humanTurn = True
        print "\nHAL is thinking about his next move... "
        score ,move = search.minimax(boardInstance, int(0), int(depth), int(-1*(sys.maxsize-2)), int((sys.maxsize-2)), useAlphaBeta)
        print "HAL's Move: "+str(move[0])+str(int(move[1])+1)+ "\t With Score: " + str(score)
        boardInstance.doMove(1, move)
        print "Your turn... puney human.\n"
        print boardInstance
        print time.time() - s, "seconds"
        print search.count, "Hypothetical Moves"
        search.count = 0
    

print "Thank you for a very enjoyable game, Dave."

