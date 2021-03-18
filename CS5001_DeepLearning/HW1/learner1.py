#!/usr/bin/env python3
from random import uniform 


'''
PSEUDOCODE:
PROCEDURE Incremental_Linear_Learner
GIVEN:
    E[0..n] : examples, each a <x, y> pair
    eta : the learning rate
LOCAL:
    w[0,1] : weights
    Randomize w[0], w[1].
    REPEAT 5000 times
    FOR k := 0 to n DO                        // go through examples
        Compute yCap ( from w[0], w[1] and E[k] ) 
        delta :=  Ex[k].y - yCap
        FOR each weight w[i]
            w[i] := w[i]  +  eta * delta * E[k].x[i] 
     return w[]

'''

def output(eta, it, w0, w1, error):
    outfile = open('learner1output.txt', 'w')
    print("CS-5001: HW#1\nProgrammer: Mark Anderson\n\nTRAINING\nUsing Learning Rate eta = %f\nUsing %d iterations.\n\nOUTPUT:\nw0 = %d\nw1 = %d\n\nVALIDATION\nSum-of-Squares Error = %d" % (eta,it,w0,w1,error))#file=outfile)

def read(filename='chocodata.txt'):
    inData = [] 
    with open(filename) as f:
        for line in f.readlines():
            x, y= line.split()
            x, y = int(x), int(y)
            inData.append((x,y))
    return inData

def SSE(weights, validationData):
    error = 0.0
    for entry in validationData:
        x_input = entry[0]
        yCap = weights[0] + (x_input * weights[1])
        error += (entry[1] - yCap) ** 2
    return error 

def main():
    inputData = read()
    validationData = read('chocovalid.txt')
    eta = float(0.00001)
    iterations = 10000
    w = [uniform(0,100), uniform(0,100)]
    for i in range(iterations):
        for k, entry in enumerate(inputData):
            x_input = entry[0]
            y_output = entry[1]
            #Computing yCap
            yCap = w[0] + (w[1] * x_input)
            #Compute the Delta
            delta = (y_output - yCap)
            update = eta * delta
            #update Weights
            w[0] = w[0] + update
            w[1] = w[1] + update * x_input
            #print("W: (%f, %f)" % (w[0], w[1]))

    error = SSE(w, validationData)
    output(eta, iterations, w[0], w[1], error)
    
if __name__ == "__main__":
    main()
