#!/usr/bin/env python3
from collections import Counter, defaultdict 
import glob
def readByteFile(filename):
    raw_file = []
    with open(filename, 'rb') as bytefile:
        byte = bytefile.read(1)
        while byte:
            raw_file.append(int.from_bytes(byte, byteorder="little"))
            byte = bytefile.read(1)
    return raw_file
    
    
def main():
    for filename in glob.glob('testaro.txt'):
        charFreq = defaultdict(int)
        digramFreq = defaultdict(int)
        trigramFreq = defaultdict(int)
        raw = readByteFile(filename)
        for char in raw:
            try:
                charFreq[char] += 1
            except KeyError:
                charFreq[char] = 1


        for i in range(len(raw) - 1):
            digram = "".join(str(raw[i]) + "." + str(raw[i+1]))
            try:
                digramFreq[digram] += 1
            except KeyError:
                digramFreq[digram] = 1
        
        for i in range(len(raw) - 2):
            trigram = "".join(str(raw[i]) + "." + str(raw[i+1]) + "." + str(raw[i+2]))
            try:
                trigramFreq[trigram] += 1
            except KeyError:
                trigramFreq[trigram] = 1

        c = Counter(charFreq)
        for key, value in c.most_common(26):
            print("ord(%d) count(%d)" % (key, value))

        dig = Counter(digramFreq)
        for key, value in dig.most_common(10):
            key = key.split('.')
            print("ord(%s) ord(%s) count(%d)" % (key[0], key[1], value))
        
        trig = Counter(trigramFreq)
        for key, value in trig.most_common(10):
            key = key.split('.')
            print("ord(%s) ord(%s) ord(%s) count(%d)" % (key[0], key[1], key[2], value))

if __name__ == "__main__":
    main()

