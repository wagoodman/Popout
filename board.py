import copy
import math

class Queue:
    """
    A Queue class to be used in combination with state space
    search. The enqueue method adds new elements to the end. The
    dequeue method removes elements from the front.
    """
    def __init__(self, size):
        self.queue = []

    def __str__(self):
        result = "Queue contains " + str(len(self.queue)) + " items: "
        for item in self.queue:
            result += str(item) + " "
        return result

    def __len__(self):
        return len(self.queue)

    def enqueue(self, disc):
        self.queue.append(disc)

    def dequeue(self):
        if not self.empty():
            return self.queue.pop(0)
        else:
            raise RunTimeError

    def removeTop(self):
        if not self.empty():
            return self.queue.pop(len(self.queue)-1)
        else:
            raise RunTimeError

    def enqueueFront(self, disc):
        self.queue.insert(0,disc)

    def contains(self, disc):
        try:
            index = self.queue.index(disc)
            return True
        except ValueError:
            return False

        return False

    def empty(self):
        return len(self.queue) == 0


class Board():
    """
    A Board class represents a connect 4 board, where each column contains a Queue.
    Using the push method adds new elements to the top of the board. The pop method
    removes elements from the bottom of the board.
    """
    def __init__(self, w, h):
        self.height = int(h)
        self.width = int(w)
        self.col = [Queue(self.height) for col in range(self.width)]
        
    def __str__(self):
        retstr = ""
        for r in range(self.width):
            retstr += str(r+1) + " "
        retstr += "\n"
        for row in range(self.height-1,-1,-1):  #heigher rows       = high numbers
            for col in range(self.width):       #more left columns  = lower numbers
                if (len(self.col[col].queue) > row):
                    retstr += str(self.col[col].queue[row]) + " "
                else:
                    retstr += "_ "
            retstr += " \n"
        return retstr

    #DROP value into column
    def push(self, col, value):
        if self.validMove("d"+str(col), value):
            self.col[col].enqueue(value[0])
            return True
        return False

    #POP value from column
    def pop(self, col, value):
        if self.validMove("p"+str(col), value):
            self.col[col].dequeue()
            return True
        return False

    #UNDO DROP value into column
    def undoPush(self, col, value):
        self.col[col].removeTop()


    #UNDO POP value from column
    def undoPop(self, col, value):
        self.col[col].enqueueFront(value)


    #Generates ALL possible moves
    def getMoves(self, value):
        q = Queue(self.width*2)
        for drop in range(self.width):
            move = "d"+str(drop)
            if self.validMove(move, value):
                q.enqueue(move)
        for pop in range(self.width):
            move = "p"+str(pop)
            if self.validMove(move, value):
                q.enqueue(move)
        return q.queue

    #determines if move is valid in context of board
    def validMove(self, move, value):
        if len(move) < 2:
            return False
        
        if move[1].isdigit():
            col = int(move[1])
            if col < self.width and col >=0:
                if move[0].lower() == "d":
                    if len(self.col[col]) < self.height:
                        return True
                if len(self.col[col]) > 0:
                    if move[0].lower() == "p" and (self.col[col].queue[0] == value[0]):
                        return True
        return False

    #commits move to self, not on new board!
    def doMove(self,move,value):
        
        if len(move) < 2:
            return False
        
        if not move[1].isdigit():
            return False

        col = int(move[1])

        if (move[0].lower() == "p"):
            return self.pop(col, value[0])
        elif (move[0].lower() == "d"):
            return self.push(col,value[0])
        else:
            return False
        
        return True

    #commits move to self, not on new board!
    def undoMove(self,move,value):
        
        if len(move) < 2:
            return False
        
        if not move[1].isdigit():
            return False

        col = int(move[1])

        if (move[0].lower() == "p"):
            return self.undoPop(col, value[0])
        elif (move[0].lower() == "d"):
            return self.undoPush(col,value[0])
        else:
            return False
        
        return True
        
    #Returns the value of the disc in row,col
    def getValue(self,row,col):
        if str(col).isdigit() and str(row).isdigit():
            col = int(col)
            row = int(row)
        else:
            return "*"
        if col < self.width and row < self.height and row >= 0 and col >= 0:
            if (len(self.col[col].queue) > row):
                return str(self.col[col].queue[row])
            else:
                return "_"
        return "*"
    
    #given a grid location, returns a Queue with the values in the given direction (length 4)
    def getFourSpace(self,row,col,spacenum):
        space = Queue(4)
        base = self.getValue(row,col)
        if base == "*" or base == "_":
            return space
                             #--------------------------
                             #   spacenum   direction
                             #   --------   ---------
        if spacenum == 0:
            (dx,dy) = (0,1)  #   0          UP
        elif spacenum == 1:
            (dx,dy) = (1,1)  #   1          UP-RIGHT
        elif spacenum == 2:
            (dx,dy) = (1,0)  #   2          RIGHT
        elif spacenum == 3:
            (dx,dy) = (1,-1) #   3          DOWN-RIGHT
        elif spacenum == 4:
            (dx,dy) = (0,-1) #   4          DOWN
        elif spacenum == 5:
            (dx,dy) = (-1,-1)#   5          DOWN-LEFT
        elif spacenum == 6:
            (dx,dy) = (-1,0) #   6          LEFT
        elif spacenum == 7:
            (dx,dy) = (-1,1) #   7          UP-LEFT
                             #--------------------------

        count = 0
        while count < 4:
            newValue = self.getValue(row+(dy*count),col+(dx*count))
            if newValue != "*" :
                space.enqueue(newValue)
            else:
                return space
            count += 1
        return space

    def getCellScore(self, count):
        if count == 0:
            return 0
        if count == 1:
            return 1
        if count == 2:
            return 100
        if count == 3:
            return 10000
        if count == 4:
            return 1000000

    def getSpaceScore(self,row,col,myDisc,otherDisc):
        score = 0
        for spacenum in range(8):
            space = self.getFourSpace(row,col,spacenum)
            #print (space)
            if ( len(space.queue) == 4 ):
                if ( not space.contains(otherDisc) ):
                    myDiscCount = 0
                    for cell in range(4):
                        if space.queue[cell] == myDisc:
                            myDiscCount += 1
                        else:
                            score += self.getCellScore(myDiscCount) #if break in middle
                            myDiscCount = 0
                    score += self.getCellScore(myDiscCount) #get final count
        return score
    


    def getBoardScore(self, myDiscType):
        discTypes = ["X","O"]
        discScores = [0,0]
        printScores = False

        for discIndex in range(len(discTypes)):     #repeat operation for each disc
            thisDisc = discTypes[discIndex%2]
            otherDisc = discTypes[(discIndex+1)%2]
            for col in range(self.width):               #for all board cols
                for row in range(self.height):          #for all board rows
                    cell = self.getValue(row,col)           #get cell value and score
                    if cell == "_":
                        break
                    elif cell == thisDisc:
                        discScores[discIndex] += self.getSpaceScore(row,col,thisDisc,otherDisc)
                        
        if myDiscType == discTypes[0]:
            if (printScores):
                print (str(myDiscType) + ": " + str(discScores[0] - discScores[1]))
            return discScores[0] - discScores[1]

        if (printScores):
            print (str(myDiscType) + ": " + str(discScores[1] - discScores[0]))
       
        return discScores[1] - discScores[0]





















    


    #determins if there is a winner
    def validEndGame(self):
     
        #check for win in any column
        #print ("COL")
        for col in self.col:
            if len(col.queue) >=4:
                X = 0
                O = 0
                for item in range(len(col.queue)):
                    if col.queue[item] == "X":
                        O = 0
                        X += 1

                    elif col.queue[item] == "O":
                        X = 0
                        O += 1

                    if X >= 4:
                        return True#, "X"
                    if O >= 4:
                        return True#, "O"
        

        
        #check for win in any row...
        #print ("Row")
        for row in range(self.height):
            X = 0
            O = 0
            for col in range(self.width):
                if int(len(self.col[col].queue)) > row:
                    if self.col[col].queue[row] == "X":
                        O = 0
                        X += 1

                    elif self.col[col].queue[row] == "O":
                        X = 0
                        O += 1

                    if X >= 4:
                        return True#, "X"
                    if O >= 4:
                        return True#, "O"
                else:
                    X = 0
                    O = 0

   
    
        #check for win in any upper/right diagonal...
        #print ("UR 1")
        for row in range(self.height-1, -1, -1):
            col = 0
            currow = row
            X = 0
            O = 0
            while len(self.col[col].queue) >= (currow+1) and col < self.width and currow < self.height and col >= 0 and currow >= 0:
                #print (str(currow) + "," + str(col)+" : "+str(self.col[col].queue[currow]))
                if self.col[col].queue[currow] == "X":
                    O = 0
                    X += 1
                    
                elif self.col[col].queue[currow] == "O":
                    X = 0
                    O += 1
                    
                if X >= 4:
                    return True#, "X"
                if O >= 4:
                    return True#, "O"
                
                col += 1
                currow += 1
                if not (col < self.width and currow < self.height and col >= 0 and currow >= 0):
                    break
            #print ("X: "+ str(X)+ "  O: " +str(O))
            
        #print ("UR 2")   
        for col in range(self.width-1):
            row = 0
            curcol = col
            X = 0
            O = 0
            while len(self.col[curcol].queue) >= (row+1) and curcol < self.width and row < self.height and curcol >= 0 and row >= 0:
                #print (str(row) + "," + str(curcol)+" : "+str(self.col[curcol].queue[row]))
                if self.col[curcol].queue[row] == "X":
                    O = 0
                    X += 1
                    
                elif self.col[curcol].queue[row] == "O":
                    X = 0
                    O += 1
                    
                if X >= 4:
                    return True#, "X"
                if O >= 4:
                    return True#, "O"
                
                curcol += 1
                row += 1
                if not (curcol < self.width and row < self.height and curcol >= 0 and row >= 0):
                    break
            #print ("X: "+ str(X)+ "  O: " +str(O))

            
        
        #check for win in any upper/left diagonal...
        #print ("UL 1")
        for row in range(self.height-1, -1, -1):
            col = self.width-1
            currow = row
            X = 0
            O = 0
            while len(self.col[col].queue) >= (currow+1)  and col < self.width and currow < self.height and col >= 0 and currow >= 0:
                #print (str(currow) + "," + str(col)+" : "+str(self.col[col].queue[currow]))
                if self.col[col].queue[currow] == "X":
                    O = 0
                    X += 1
                    
                elif self.col[col].queue[currow] == "O":
                    X = 0
                    O += 1
                    
                if X >= 4:
                    return True#, "X"
                if O >= 4:
                    return True#, "O"
                
                col -= 1
                currow += 1
                if not (col < self.width and currow < self.height and col >= 0 and currow >= 0):
                    break


            
        #print ("UL 2")   
        for col in range(self.width-1, -1, -1):
            row = 0
            curcol = col
            X = 0
            O = 0
            while len(self.col[curcol].queue) >= (row+1)  and curcol < self.width and row < self.height and curcol >= 0 and row >= 0:
                #print (str(row) + "," + str(curcol)+" : "+str(self.col[curcol].queue[row]))
                if self.col[curcol].queue[row] == "X":
                    O = 0
                    X += 1
                    
                elif self.col[curcol].queue[row] == "O":
                    X = 0
                    O += 1
                    
                if X >= 4:
                    return True#, "X"
                if O >= 4:
                    return True#, "O"
                
                curcol -= 1
                row += 1
                if not (curcol < self.width and row < self.height and curcol >= 0 and row >= 0):
                    break

        
        return False
   

       
