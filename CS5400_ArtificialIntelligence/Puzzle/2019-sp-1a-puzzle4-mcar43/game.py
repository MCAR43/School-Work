#!/usr/bin/env python3
from copy import deepcopy, copy
from colorama import Fore, Back, Style
import sys
from collections import defaultdict
POSSIBLE_HEAD_CHARS = ['U', 'D', 'L', 'R']
ROW_HEAD_DIRECTIONS = {
    'U': -1,
    'D': 1,
    '^': -1,
    'v': 1
}
COL_HEAD_DIRECTIONS = {
    'L': -1,
    'R': 1,
    '<': -1,
    '>': 1
}

HEAD_DIR = {
    (0,-1): 'R',
    (0,1): 'L',
    (-1,0): 'D',
    (1,0): 'U',
}

DIRECTIONS = {
    (0,-1): '<',
     (0,1): '>',
    (-1,0): '^',
     (1,0): 'v',
}


COLORS = ['black']
BOARD_SYMBOLS = ['e','x']

#Represents each 'Segment' of a wriggler in a doubly linked list
class Node:
    def __init__(self, character, row, col):
        self.character = character
        self.row = row
        self.col = col
        self.nextSegment = None
        self.prevSegment = None

    def display(self):
        print(self.prevSegment, "<-- Prev -- Char: ", self.character, " Loc: ", (self.row, self.col), " -- Next -->", self.nextSegment)


#Data structure to represent a wriggler, implemented with a doubly linked list
class Wriggler:
    def __init__(self):
        self.head = None

    #insert at back
    def insert(self, node):
        if self.head is None:
            self.head = node
            return
        else:
            current = self.head
            while current.nextSegment:
                current = current.nextSegment
                #overwrite duplicate positional entries
                if node.row == current.row and node.col == current.col:
                    current.character = node.character
                    return

            node.prevSegment = current
            current.nextSegment = node
            return


    #insert at front
    def emplace(self, node):
        if self.head is None:
            self.head = node
        else:
            self.head.prevSegment = node
            node.nextSegment = self.head
            node.prevSegment = None
            self.head = node

    def display(self):
        current = self.head
        while current:
            current.display()
            current = current.nextSegment

        return


    def getTail(self):
        current = self.head
        while(current.nextSegment):
            current = current.nextSegment

        return current


    def remove(self, node):
        if self.head is None:
            return
        current = self.head
        while current:
            if self.head.row == node.row and self.head.col == node.col:
                self.head = self.head.nextSegment
                self.head.prevSegment = None

            if current.row == node.row and current.col == node.col:
                current.prevSegment.nextSegment = current.nextSegment
                current.nextSegment.prevSegment = current.prevSegment

            current = current.nextSegment



class State:
    def __init__(self, newState=None, filename=None):
        if filename is not None:
            with open(filename) as data:
                try:
                    self.cols = int(data.read(2).strip())
                    self.rows = int(data.read(2).strip())
                    self.numWrigglers = int(data.read(2).strip())
                except ValueError:
                    print("Columns, rows, or number of wrigglers is invalid")
                    sys.exit()

                self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

                for row, line in enumerate(data):
                    line = line.replace(" ","").strip()
                    for col, board_symbol in enumerate(line):
                        self.board[row][col] = str(board_symbol)

                self.wrigglers = self.findWrigglers()
        else:
            self.cols = newState.cols
            self.rows = newState.rows
            self.numWrigglers = newState.numWrigglers
            self.wrigglers = newState.wrigglers
            self.board = newState.board

    def printState(self):
        for char in self.board:
            print(*char, sep=" ")

    #For the first state loop through and find all wrigglers, as well as map them to a wriggler linked list
    def findWrigglers(self):
        wrigglerDict = [Wriggler() for _ in range(self.numWrigglers)]

        #A list of Tail IDs represented as strings so the below function can recognize if it has passed a tail
        tails = [str(tailID) for tailID in range(self.numWrigglers)]

        #We know there are X number of wrigglers, so we can loop through X amount of times
        #Each time we wind a wriggler we add its tail identifier to a dictionary, and since the order the wrigglers
        #are found is never guaranteed, a dictionary allows us to still look up by the Tail ID

        for location in ([(ix, iy) for ix, row in enumerate(self.board) for iy, i in enumerate(row) if i in POSSIBLE_HEAD_CHARS]):
            temp = Wriggler()
            wriggler = self.follow(location, temp, tails)
            wrigglerDict[int(wriggler.getTail().character)] = wriggler



        return wrigglerDict

    #Recursive function to map each wriggler by following the symbols
    def follow(self, headLoc, wriggler, tails):
        #for easier reading, the row and column of the selected head is stored in shorter variables
        row, col = headLoc

        #current Character we are at in the follow() of the wriggler
        current = self.board[row][col]
        #insert the character, row, and column into the wriggler
        wriggler.insert(Node(current, row, col))

        #If we have reached ANY of the tail characters we can exit the function and return the wriggler
        #Can exit on reaching any of the characters instead of a specific is because each head will only point to one tail
        #and since we follow based on the symbols '<>^v' we always reach the tail from the head
        if current in tails:
            return wriggler

        #If the character is indicating a direction across rows, we add the corresponding value from the dictionary
        #to the current row value
        # Example:
        # current = '^'
        # ROW_HEAD_DIRECTIONS['^'] = -1 meaning the next segment is -1 rows, since the segments cannot move diagonally
        # the value will only change by one so if the rows change, the columns can stay the same
        try: row += ROW_HEAD_DIRECTIONS[current]
        except KeyError: row += 0
        try: col += COL_HEAD_DIRECTIONS[current]
        except KeyError: col += 0

        #recursively call the follow function with the updated row and column from before
        return self.follow((row, col), wriggler, tails)

    #after using the move function, redraw all wrigglers on the board to a new board
    def redrawState(self):

        #Any symbol that is not a permanent part of the board ([e, x]) will be replaced with e
        #in other words, all parts of a wriggler will be erased and then redrawn in the next step
        for row in range(0,self.rows):
            for col in range(0,self.cols):
                if self.board[row][col] not in BOARD_SYMBOLS:
                    self.board[row][col] = 'e'

        #for all of the wrigglers in the state redraw them onto the board based on their segments data
        # Segment:
        # row: 1
        # col: 1
        # char: >
        # redraws [1][1] = > and then traversing the linked list draws the next segment
        for wIndex in range(self.numWrigglers):
            current = self.wrigglers[wIndex].head
            while current.nextSegment:
                self.board[current.row][current.col] = current.character
                current = current.nextSegment
            self.board[current.row][current.col] = current.character

    #Get a list of all valid moves from the current state (head and tail)
    def getValid(self, id):
        #GOTTA BE A BETTER WAY TO DO THIS
        VALID_MOVES = []
        OUTPUT_FORMAT = []
        for start_loc in range(2):
            #For the first passthrough, search for valid moves starting from the head position
            if start_loc == 0:
                current = self.wrigglers[id].head
                direction = 1
            #Second passthrough, search for valid moves starting from the tail position
            else:
                current = self.wrigglers[id].getTail()
                direction = -1

            row, col = current.row, current.col

            #Try all 4 possible moves
            for key in DIRECTIONS:
                rowDir, colDir = key
                #The row and column of the potential next move
                nextRow, nextCol = row + rowDir, col + colDir

                #If the Row and Column are within the bounds of the matrix
                if nextRow in range(0, self.rows) and nextCol in range(0, self.cols):
                    #If the character where the potential move occurs is an empty space, the move is valid
                    if self.board[nextRow][nextCol] == 'e':
                        #Append the valid move to the list to be returned in the same format that the move function takes
                        VALID_MOVES.append([id, rowDir, colDir, direction])
                        #Generate the valid move in the format required by the graders
                        if direction > 0:
                            OUTPUT_FORMAT.append([id, 0, nextCol, nextRow])
                        else:
                            OUTPUT_FORMAT.append([id, 1, nextCol, nextRow])
        if VALID_MOVES and OUTPUT_FORMAT:
            return VALID_MOVES, OUTPUT_FORMAT
        else:
            return None

    def isGoalState(self):
        blueWriggler = self.wrigglers[0]
        head = blueWriggler.head
        tail = blueWriggler.getTail()
        if ((head.row, head.col) == (self.rows - 1, self.cols - 1) or (tail.row, tail.col) == (self.rows - 1, self.cols - 1)):
            return True

    def move(self, wrigglerID, rowDir, colDir, direction):
        #Create a new wriggler list, and a deepcopy of the current state
        #using deepcopy because the states rely on traversing a linked list, so we'll need a deepcopy of each wriggler
        #in the state
        temp = Wriggler()
        newState = deepcopy(self)

        #Direction > 0 indicates the head is moving
        if direction > 0:
            #Set the current node to the head of the wriggler selected
            currentNode = newState.wrigglers[wrigglerID].head
            #Loopcontrol is stored in a variable instead of just
            #while (currentNode.nextSegment) because if the chosen move is from the tail, we need the prev segment
            loopControl = currentNode.nextSegment
            #Insert the move into the new wriggler list
            temp.insert(Node(HEAD_DIR[(rowDir, colDir)], currentNode.row + rowDir, currentNode.col + colDir))
        #Direction < 0 indicates the tail is moving
        else:
            #Set the current node to the tail of the selected wriggler
            currentNode = newState.wrigglers[wrigglerID].getTail()
            #same as above but with prevSegment
            loopControl = currentNode.prevSegment
            #Insert the new Node into the wriggler list
            temp.insert(Node(str(wrigglerID), currentNode.row + rowDir, currentNode.col + colDir))

        #Loop until the Next/Prev Node of the current Node is None, indicating there are no more nodes left to be traversed
        while loopControl:
            #Head is chosen
            if direction > 0:
                #represents the Row, Col of the current Node
                nRow, nCol = currentNode.row, currentNode.col
                #Changes the current node to be the next segment in the wriggler
                currentNode = currentNode.nextSegment

                #Subtracts the Previous Row, and the Current Row to receive a tuple representing the direction of the next
                #node
                # Example:
                # x e e    x e e
                # 0 < L -> e 0 <
                # x e e    x e U

                # currentNode.row, currentNode.col = (1, 1)
                # nRow, nCol                       = (1, 2)
                # subtract the two to receive      = (0, -1)
                # DIRECTIONS[(0,-1)] = '<'
                # indicating the character to place in the current row/col should be '<'

                difference = ((currentNode.row - nRow), (currentNode.col - nCol))
                loopControl = currentNode.nextSegment
                temp.insert(Node(DIRECTIONS[difference], nRow, nCol))
            #Tail is chosen
            else:
                #Same as above but instead of retrieving the next row from the existing wriggler, we retrieve the next
                #row from the temporary list because we are traversing backwards
                # since we're traversing backwards we need to multiply the result of the tuple subtraction by -1 to get
                # the correct value
                nRow, nCol = temp.head.row, temp.head.col
                difference = ((currentNode.row - nRow) * direction, (currentNode.col - nCol) * direction)
                #insert the node at the front since we build the wriggler backwards
                temp.emplace(Node(DIRECTIONS[difference], currentNode.row, currentNode.col))
                currentNode = currentNode.prevSegment
                loopControl = currentNode.prevSegment

        #Same if statements as above, this block changes either the Head or the Tail character to be the correct one
        #based on which was chosen
        if direction > 0:
            temp.getTail().character = str(wrigglerID)
        else:
            headRow, headCol = difference
            headLocation = ((headRow * direction),(headCol * direction))
            temp.head.character = HEAD_DIR[headLocation]

        #Replace the wriggler in the state with the generated wriggler from our move function
        newState.wrigglers[wrigglerID] = temp
        #Redraw the state to get an accurate representation of the board (even though its not needed, it helps for debugging)
        newState.redrawState()
        return newState


#Represents a single vertex in the directed graph
class Vertex:
    def __init__(self, state, action = None, depth = 0, weight = 0):
        self.state = state
        self.depth = depth
        self.connected = []
        self.ident = 0
        self.weight = weight 
        self.visited = False

        #A variable to make outputting the final solution, will be implemented cleaner in the futre
        #formats the move function to match expected output of
        #[ID HEAD/TAIL ROW COL]
        #[0 1 0 1].. ETC
        if action is not None:
            self.action = action
        else:
            self.action = ""



class Graph:
    def __init__(self, root):
        self.vertices = {}
        self.vertices[0] = root

    def addVertex(self, root, vertex):
        for key in self.vertices:
            if vertex.state.board == self.vertices[key].state.board:
                return False

        vertex.ident = len(self.vertices)
        self.addEdge(root, vertex)
        self.vertices[vertex.ident] = vertex
        return True

    def display(self):
        for key in self.vertices:
            print("Manhattan: %d Depth: %d Vertex: %s -> %s" % (self.vertices[key].weight, self.vertices[key].depth, key, [ident.ident for ident in self.vertices[key].connected]))

    def addEdge(self, source, dest):
        source.connected.append(dest)

    def displayState(self, ident, filename=None):
        finalState = self.vertices[ident].state
        if filename:
            for char in finalState.board:
                print(*char, sep=" ", file=filename)
        else:
            for char in finalState.board:
                print(*char, sep=" ")

    def displayAll(self):
        for ident in self.vertices:
            print("Vertex: %d represented by:" % ident)
            self.vertices[ident].state.printState()

    def getMaxDepth(self):
        nodesAtDepth = []
        for vertex in self.vertices:
            if not self.vertices[vertex].connected:
                nodesAtDepth.append(vertex)
        return nodesAtDepth

    def clear(self):
        for vertex in range(len(self.vertices)):
            del self.vertices[vertex]




