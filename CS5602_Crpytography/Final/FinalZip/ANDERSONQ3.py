#!/usr/bin/env python3
import re
import math
from collections import defaultdict, Counter

def process(message):
    nonAlpha = re.compile('[^a-z\s]')
    message = message.lower()
    message = message.replace('\n', ' ')
    message = nonAlpha.sub('', message)

    parsedList = []
    for word in message.split(' '):
        if len(word) > 2:
            parsedList.append(word)
            
    #extract tripls
    triplesList = defaultdict(int)
    for word in parsedList:

        for i in range(len(word)):
            if i + 3 > len(word):
                break
            try:
                triplesList[word[i:i+3]] += 1
            except KeyError:
                triplesList[word[i:i+3]] = 1
    
    triplesList = Counter(triplesList)
    return triplesList


def calculate(triples):
    H_P3 = 0
    total = sum(triples.values())
    for trigram, val in triples.items():
        probability = val / total * math.log((val/total), 10)
        H_P3 += probability

    print(-1*H_P3)


def main():
    infile = "infile.txt"
    message = ""
    with open(infile, 'r') as f:
        message = f.read()
    
    calculate(process(message))


if __name__ == "__main__":
    main()
