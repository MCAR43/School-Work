#!/usr/bin/env python3
from random import uniform, seed
from math import exp
class Network:
    def __init__(self, inputLayer, hiddenLayer, outputLayer):
        self.input = []
        self.net = []
        self.input_length = inputLayer
        self.hidden_length = hiddenLayer
        self.output_length = outputLayer
    
    def randomize(self, seedVal):
        seed(seedVal)
        hidden_layer = [{'weights':[round(uniform(-1,1),3) for i in range(self.input_length + 1)]} for i in range(self.hidden_length)]
        self.net.append(hidden_layer)
        output_layer = [{'weights':[round(uniform(-1,1),3) for i in range(self.hidden_length + 1)]} for i in range(self.output_length)]
        self.net.append(output_layer)
        return self.net
        

def read(filename='hw3data.txt'):
    dataPointList = []
    with open(filename) as f:
        for line in f.readlines():
            x, y, plane = line.split()
            dataPointList.append([int(x),int(y),int(plane)])
    return dataPointList

def feedForward(net, row):
    for layer in net:
        newIn = []
        for neuron in layer:
            ac = activate(neuron['weights'], row)
            neuron['output'] = fw_sigmoid(ac)
            newIn.append(neuron['output'])
    return newIn

def fw_sigmoid(x):
    return 1 / (1 + exp(-x))

def bk_sigmoid(dA, x):
    sig = fw_sigmoid(x)
    return dA * sig * (1-sig)

def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights)):
        activation += weights[i] * inputs[i]

    return fw_sigmoid(activation)

def output(eta, it, network, SSE):
    outfile = open('classifieroutput.txt', 'w')
    print("CS-5001: HW#3\nProgrammer: Mark Anderson")
    print("\nTraining\nUsing Learning rate eta = %f\nUsing %d iterations." % (eta, it))
    print("\nOutput:\nInput Units:")
    for line in network[:-1]:
        for neuron in line:
            x,y,z = neuron['weights']
            print("%f\t%f\t%f" % (x,y,z))
    v,w,x,y,z = network[-1][0]['weights']
    print("Output Unit:\n%f %f %f %f %f" % (v,w,x,y,z))
    print("VALIDATION:")
    print("Sum-of-Squares Error = Did Not finish..")

def SSE(weights, validData):
    error = 0.0
    valiData = read('hw3valid.txt')
    for entry in valiData:
        x_input = entry[0]


def main():
    eta = 0.00001
    iterations = 1000
    seed(100)
    data = read()
    dataNet = Network(2,4,1)
    dataNet.randomize(10)
    print(data[0])
    #fw_prop(dataNet.net, data[0])
    output(eta,iterations, dataNet.net, 1)


if __name__ == "__main__":
    main()
