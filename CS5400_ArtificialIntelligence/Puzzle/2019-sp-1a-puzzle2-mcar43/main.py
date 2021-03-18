#!/usr/bin/env python3
from game import *
from collections import deque
from collections import OrderedDict
import time
import sys
import os
start_time = time.time()


def generate(vertex):
    #state of the current vertex
    state = vertex.state
    #List of states generated to be returned
    generated = []
    #loop through all the wrigglers to check for valid moves
    for i in range(state.numWrigglers):
        #Get valid moves for wriggler I
        movement, output = state.getValid(i)
        for action in movement:
            #Generate the new State corresponding to the action
            newVertex = Vertex(state.move(*action), output.pop(0), vertex.depth + 1)
            #append to the list
            generated.append(newVertex)

    return generated

def IDDFS(graph, depth, frontier):
    #DFS pops the first node in the frontier list

    #Solution is an orderedDict representing the actions taken to reach a certain point (exactly like how we do it in class)
    solution = OrderedDict()
    #While the frontier is not empty loop through
    #We use this to iterate instead of using depth <= limit
    #because the only nodes that will be appended to the frontier are those that are less than the depth limit
    while frontier:
        currentVertex = frontier.popleft()
        #check if the vertex we are evaluating is a goal state
        if currentVertex.state.isGoalState():
            solution[currentVertex.ident] = [item.ident for item in frontier]
            return True, solution, graph

        #generate a list of the new states that have been added, if they are not duplicates
        sublist = []
        for vert in generate(currentVertex):
            if graph.addVertex(currentVertex, vert):
                sublist.append(vert)

        #Append all items in the list of states generated if their depth is less than the depth limit
        #we reverse the list and append left to keep the order in which the states were generated
        [frontier.appendleft(item) for item in sublist[::-1] if item.depth < depth]
        #append the Evaluation and the Frontier at that evaluation to the solution,so we can backtrack
        solution[currentVertex.ident] = [item.ident for item in frontier]

    #if no solution is found, clear the graph because ID-DFTS generates from Root always
    graph.clear()
    return False, None, None

def solve(root):
    #set the initial depth to 0
    depth = 0
    found = False
    #implementing frontier as a deque
    frontier = deque()
    
    #continue generating and checking new depths until a solution is found
    while not found:
        #ID-DFTS from class says to generate from the root each time the depth is increased
        frontier.append(root)

        #Reset the data in the root node before calling
        root.connected = []
        root.depth = 0

        #Call DFTS restricted to our depth limit
        found, result, newGraph = IDDFS(Graph(root), depth, frontier)
        
        #increment the depth limit so we search to the next level
        depth += 1


    #The algorithm to find the path taken by the script to generate the goal state
    #Result is an ordered dict with the Node evaluated, and the Frontier for each iteration of IDDFS
    solution = []
    solution.append(result.popitem()[0])
    #Algorithm to implement the backtracking as shown in class to find out what Evaluation generated what state
    for key, value in reversed(result.items()):
        if solution[-1] not in value:
            solution.append(prevKey)
        prevKey = key

    solution.append(0)

    return solution, newGraph

def outputSolution(solu, graph, infile):
    outFile = "solu" + infile
    with open(outFile, 'w') as output:
        for item in solu[::-1]:
            for character in graph.vertices[item].action:
                print(character, end=" ", file=output)
            print(file=output)

        graph.displayState(solu[0], output)
        print(time.time() - start_time, file=output)
        print(len(solu), file=output)

def main():
    if len(sys.argv) > 1:
        for infile in sys.argv[1:]:
            if os.path.isfile(infile):
                sourceState = State(filename=infile)
                graph = Graph(Vertex(sourceState))
                solution, graph = solve(graph.vertices[0])
                outputSolution(solution, graph, infile)
                print("Time: %.3f" % (time.time() - start_time))
            else:
                print("Puzzle File Does Not Exist")
    else:
        print("No Input file Specified")








    




if __name__ == "__main__":
    main()
