#!/usr/bin/env python3
#Mark Anderson
#CS3600
#Homework 1

#imports
import sys
import time
from sys import argv
import re
import wordPatterns
import simpleSubCipher
import string



#CONSTANTS
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .'
englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33,
                     'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41,
                     'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98,
                     'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}


def blankMap():
    map = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [],
           'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
           'Y': [], 'Z': []}

    return map

def frequencyAnalysis(message):
    tempDict = {}
    tempKey = blankMap()
    counter = 0
    for letter in message:
        key = letter.upper()
        if key in ALPHABET:
            try:
                tempDict[key] += 1
            except KeyError:
                tempDict[key] = 1

    for key in tempDict:
        tempDict[key] = (tempDict[key] / len(message))

    for letter in ALPHABET:
        if letter not in tempDict.keys():
            tempDict[letter] = 0


    sortedList = sorted(tempDict, key=tempDict.get, reverse=True)

    for key in englishLetterFreq:
        tempKey[key].append(sortedList[counter])
        counter+=1

    return tempKey

def generateKey(mapping):
    newKey = ''
    for letter in ALPHABET:
        if len(mapping[letter]) == 1:
            newKey+=mapping[letter][0]
        else:
            newKey+='_'


    return newKey

def translateText(message, key):
    stringKey = generateKey(key)
    print(stringKey)
    return simpleSubCipher.decryptMessage(stringKey, message)

def wordPattern(word):
    index = 0
    pattern = ""
    letterMap = {}
    for letter in word:
        if letter.upper() in ALPHABET:
            upper = letter.upper()
            if upper not in letterMap:
                letterMap[upper] = index
                pattern += str(letterMap[upper]) + "."
                index += 1
            else:
                pattern += str(letterMap[upper]) + "."

        #unelegant way of slicing off trailing period
    return pattern[:-1]

def intersect(keyA, keyB, remove):
    intersectedDict = blankMap()
    for letter in ALPHABET:
        upper = letter.upper()
        if keyA[upper] == []:
            intersectedDict[upper] = keyB[upper]
        elif keyB[upper] == []:
            intersectedDict[upper] = keyA[upper]
        else:
            for item in keyA[upper]:
                if item in keyB[upper]:
                    intersectedDict[upper].append(item)

    return intersectedDict

def mappingFromPattern(cipherword):
    map = blankMap()
    pattern = wordPattern(cipherword)
    try:
        potentialWords = wordPatterns.allPatterns[pattern]
    except KeyError:
        potentialWords = None

    if potentialWords is None:
        return map

    for word in potentialWords:
        map = createMap(map, cipherword, word)

    return map

def createMap(map, cipherword, potentialword):
    for i in range(0, len(cipherword)):
        cipherIndex = cipherword[i].upper()
        if potentialword[i] not in map[cipherIndex]:
            map[cipherIndex].append(potentialword[i])

    return map

def removeSolvedLetters(key):
    loopAgain = True
    while loopAgain:
        loopAgain = False
        singleMappedLetters = []
        for letter in ALPHABET:
            letter = letter.upper()
            if len(key[letter]) == 1:
                singleMappedLetters.append(key[letter][0])


        for cipherLetter in ALPHABET:
            for solved in singleMappedLetters:
                if len(key[cipherLetter]) != 1 and solved in key[cipherLetter]:
                    key[cipherLetter].remove(solved)
                    if len(key[cipherLetter]) == 1:
                        loopAgain = True

    return key

def checkIfSolved(solutionKey):
    for key in solutionKey:
        if solutionKey[key] == []:
            return False

    return True

def addToFinalKey(bestFit, mapping):
    for key in mapping:
        if len(mapping[key]) == 1:
            bestFit[key] = mapping[key]

    return bestFit


def solvePeriod(message, mapping):
    for i in range(len(message) - 1, 0, -1):
        if message[i] == ':' and message[i+1:i+3] == '//':
            mapping['H'][0] = message[i - 4]
            mapping['T'][0] = message[i - 3]
            mapping['P'][0] = message[i - 1]
            mapping['W'][0] = message[i + 1]
            return mapping




        


def main():
    #initiate input and output
    intersectedMapping = blankMap()
    solvedMap = blankMap()
    infile = open(argv[1], "r")
    outfile = open(argv[2], "w")
    message = infile.read()
    counter = 0

    #do initial frequency analysis, depending on the length of the ciphertext this could yeild a ~70% match
    #initKey is the initial frequency, we can assume that space is solved
    initKey = frequencyAnalysis(message)
    initKey = solvePeriod(message, initKey)
    regexPattern = '^[^{:s}{:s}{:s}{:s}]*$'.format(spaceMapping.upper(), spaceMapping.lower(), periodMapping.upper(), periodMapping.lower())
    #print(regexPattern)


    for word in re.split(spaceMapping, message, flags=re.IGNORECASE):
        counter+=1
        #reset the known period and space
        intersectedMapping[initKey['.'][0]] = '.'
        intersectedMapping[initKey[' '][0]] = ' '
        #use regex to only create word patterns for cipherwords in the alphabet and exclude digraphs because word patterns from digraphs aren't useful
        #numbers are also excluded because we won't be encrypting numbers
        if bool(re.match('^[a-zA-Z. ]{4,}$', word)):
            if bool(re.match(regexPattern, word)):

                print("Word: %s" % word)
                print(solvedMap)

                #newline characters can cause issues on certain words
                potentialMapping = mappingFromPattern(word.strip('\n'))
                intersectedMapping = intersect(intersectedMapping, potentialMapping, (spaceMapping + periodMapping))
                intersectedMapping = removeSolvedLetters(intersectedMapping)
                solvedMap = addToFinalKey(solvedMap, intersectedMapping)

                if(checkIfSolved(solvedMap)):
                    break


    decrypted = translateText(message, solvedMap)
    print(decrypted)
    outfile.write(decrypted)


    

if __name__ == '__main__':
    main()
