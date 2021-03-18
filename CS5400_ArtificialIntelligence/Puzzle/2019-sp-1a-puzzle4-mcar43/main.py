#!/usr/bin/env python3
from game import *
from collections import deque
from collections import OrderedDict
import time
import os
import random
start_time = time.time()


def generate(vertex):
    #state of the current vertex
    state = vertex.state
    #List of states generated to be returned
    generated = []
    #loop through all the wrigglers to check for valid moves
    for wIndex in range(state.numWrigglers):
        #Get valid moves for wriggler I
        try:
            movement, output = state.getValid(wIndex)
        except TypeError:
            movement = []
            output = None
        for action in movement:
            #Generate the new State corresponding to the action
            newVertex = Vertex(state.move(*action), output.pop(0), vertex.depth + 1)
            #append to the list
            if newVertex.state.isGoalState():
                newVertex.weight = 0
                return [newVertex]
            #add a weight to the current state to determine the next best search
            #This weight value represents the likelihood of the next state being the correct choice
            newVertex.weight = heuristic(newVertex)
            generated.append(newVertex) 

    return generated


def ASTAR(graph, root):
    #deque to represent the current frontier
    frontier = deque()
    frontier.append(root)
    #Ordered Dict to keep track of insertion of solutions with their evaluation and frontier nodes
    solution = OrderedDict()
    while(frontier):
        current = frontier.pop()
        #If the Vertex we're evaluating is the goal state, add it to the solution and return
        if current.state.isGoalState():
            solution[current.ident] = [item.ident for item in frontier]
            return solution, graph
        
        #If the current vertex is not visited, generate states corresponding to the possible moves
        if not current.visited:
            current.vistited = True
            for vert in generate(current):
                if graph.addVertex(current, vert):
                    #If the state generated is unique, add it to our graph
                    frontier.append(vert)
                    

        #Sort the frontier by weight of the vertices
        frontier = sorted(frontier, key=lambda x: x.weight, reverse=True) 
        solution[current.ident] = [item.ident for item in frontier]
    return False    

#the heuristic values the position of the 0 wriggler the most, and wants all other wrigglers away from the goal state
def heuristic(vert):
    weight = mDistance(vert.state.wrigglers[0], vert.state.rows - 1, vert.state.cols - 1)
    for wIndex in reversed(range(vert.state.numWrigglers)):
        if wIndex == 0:
            mWeight = mDistance(vert.state.wrigglers[wIndex], vert.state.rows - 1, vert.state.cols - 1)
            weight *= mWeight
        else:
            mWeight = mDistance(vert.state.wrigglers[wIndex], 0, 0)
            weight += mWeight

    #A* = g(n) + h(n)
    return vert.depth + weight


#function to compute the manhattan distance of a wriggler
def mDistance(wriggler, gRow, gCol):
    head = wriggler.head
    tail = wriggler.getTail()
    headDist = (gRow - head.row) + (gCol - head.col)
    tailDist = (gRow - tail.row) + (gCol - tail.col)
    return min(abs(headDist), abs(tailDist))
def outputSolution(solu, graph, infile):
    outFile = "solution" + str(infile) + ".txt"
    with open(outFile, 'w') as output:
        for item in solu[::-1]:
            for character in graph.vertices[item].action:
                print(character, end=" ", file=output)
            print(file=output)

        graph.displayState(solu[0], output)
        print(time.time() - start_time, file=output)
        print(len(solu) - 1, file=output)

def parseSolution(trace):
    solution = []
    solution.append(trace.popitem()[0])
    for key, value in reversed(trace.items()):
        if solution[-1] not in value:
            solution.append(prevKey)
        prevKey = key
    solution.append(0)
    return solution

def main():
    fileNumber = 0
    if len(sys.argv) > 1:
        for infile in sys.argv[1:]:
            if os.path.isfile(infile):
                fileNumber += 1
                sourceState = State(filename=infile)
                graph = Graph(Vertex(sourceState))
                graphTrace, graph = ASTAR(graph, graph.vertices[0])
                parsedSolution = parseSolution(graphTrace)
                outputSolution(parsedSolution, graph, fileNumber) 
            else:
                print("Puzzle File Does Not Exist")
    else:
        print("No Input file Specified")

if __name__ == "__main__":
    main()
