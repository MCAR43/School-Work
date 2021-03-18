#!/usr/bin/env python3
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


class Wriggler:
    def __init__(self, head, tail, id, length):
        self.head = head
        self.tail = tail
        self.id = id
        self.length = length

class State:
    def __init__(self, newState=None, filename=None):
        if filename is not None:
            with open(filename) as data:
                #EVERY STATE DOES NOT NEED THIS INFORMATION CHANGE LATER FOR OPTIMIZATION
                self.cols = int(data.read(2).strip())
                self.rows = int(data.read(2).strip())
                self.numWrigglers = int(data.read(2).strip())
                #END
                self.board = [[0 for i in range(self.rows)] for k in range(self.cols)]
                for i, line in enumerate(data):
                    line = line.replace(" ","").strip()
                    for k, char in enumerate(line):
                        self.board[i][k] = char
                self.wrigglers = self.findWrigglers()
        else:
            self.cols = newState.cols
            self.rows = newState.rows
            self.numWrigglers = newState.numWrigglers
            self.board = newState.board

    def printState(self):
        for char in self.board:
            print(*char, sep=" ")

    def findWrigglers(self):
        wrigglerDict = {}
        for i in range(0,self.numWrigglers):
            headLoc = ([(ix, iy) for ix, row in enumerate(self.board) for iy, i in enumerate(row) if i in POSSIBLE_HEAD_CHARS][i])
            tailRow, tailCol, wrigglerID, length = self.follow(headLoc, 0)
            tailLoc = (tailRow, tailCol)
            wrigglerDict[wrigglerID] = Wriggler(headLoc, tailLoc, wrigglerID, length)
        return wrigglerDict

    def follow(self, loc, length):
        length = length + 1
        row, col = loc[0], loc[1]
        currentChar = self.board[row][col]
        possibleTails = [str(i) for i in range(self.numWrigglers)]
        if currentChar in possibleTails:
            return row, col, int(currentChar), length

        try: row += ROW_HEAD_DIRECTIONS[currentChar]
        except KeyError: row += 0

        try: col += COL_HEAD_DIRECTIONS[currentChar]
        except KeyError: col += 0

        return self.follow((row,col), length)

    def move(self, wrigglerID, ):


def move(state, head=False, tail=False, wrigglerID=0, rowMod=0, colMod=0):
    if head:
        row, col = state.wrigglers[wrigglerID].head
    else: #is tail
        row, col = state.wrigglers[wrigglerID].tail

    for segment in range(0,state.wrigglers[wrigglerID].length):
        
    


def main():
    initState = State(filename="puzzle1.txt")
    initState.printState()
    move(initState, head=False, colMod=1)
    initState.printState()
    print(initState.wrigglers[0].length)

if __name__ == '__main__':
    main()
