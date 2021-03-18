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
        movement, output = state.getValid(wIndex)
        for action in movement:
            #Generate the new State corresponding to the action
            newVertex = Vertex(state.move(*action), output.pop(0), vertex.depth + 1)
            #append to the list
            
            #add a weight to the current state to determine the next best search
            #This weight value represents the likelihood of the next state being the correct choice
            newVertex.weight = heuristic(newVertex)
            generated.append(newVertex) 

    return generated


def GBFGS(graph, root):
    #deque to represent the current frontier
    frontier = deque()
    frontier.append(root)
    #Ordered Dict to keep track of insertion of solutions with their evaluation and frontier nodes
    solution = OrderedDict()
    while(frontier):
        current = frontier.pop()
        print("Evaluating: ", (current.ident), end="")
        print("--> [")
        [print(item.weight, end=" ", sep=", ") for item in frontier]
        print("]\n")
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
        frontier = sorted(frontier, key=lambda x: x.weight)
        solution[current.ident] = [item.ident for item in frontier]
    
    return False    

#the heuristic values the position of the 0 wriggler the most, and wants all other wrigglers away from the goal state
def heuristic(vert):
    weight = 0
    #Loop through all of the wrigglers in the specified vertex
    for wIndex in range(vert.state.numWrigglers):
        #Compute the manhattan distance of the Specified wriggler and the goal state (we want non 0 wrigglers to be farther away)
        wrigglerWeight = mDistance(vert.state.wrigglers[wIndex], vert.state.rows, vert.state.cols)
        
        #For all wriggler IDs except 0 (the wriggler we want in the goal) add up the manhattan distance, for wriggler 0, multipy it because
        #the 0 wriggler position matters the most
        if wIndex is not 0:
            weight += wrigglerWeight
        else:
            weight *= wrigglerWeight

    return weight + vert.depth 

#function to compute the manhattan distance of a wriggler
def mDistance(wriggler, gRow, gCol):
    head = wriggler.head
    tail = wriggler.getTail()
    headDist = (gRow - head.row) + (gCol - head.col)
    tailDist = (gRow - tail.row) + (gCol - tail.col)
    return max(headDist, tailDist)

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
                graphTrace, graph = GBFGS(graph, graph.vertices[0])
                parsedSolution = parseSolution(graphTrace)
                outputSolution(parsedSolution, graph, fileNumber) 
            else:
                print("Puzzle File Does Not Exist")
    else:
        print("No Input file Specified")

if __name__ == "__main__":
    main()
