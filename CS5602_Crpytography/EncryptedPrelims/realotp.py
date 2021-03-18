#!/usr/bin/env python3
import glob
key = []
raw_prelim = []
decrypt = []
with open("otp.txt", 'r') as f:
    for char in f.readlines():
        char = char.strip('\n')
        key.append(int(char))


for prelim in glob.glob("Prelim2Num13.bin"):
    print("Testing Prelim: %s" % prelim)
    with open(prelim, 'rb') as bytefile:
        raw_prelim = []
        decrypt = []
        byte = bytefile.read(1)
        while byte:
            raw_prelim.append(byte)
            byte = bytefile.read(1)
            

        #do XOR stuff
        for i in range(0,len(key)):
            res = key[i] ^ int.from_bytes(raw_prelim[i], byteorder="little")
            decrypt.append(chr(res))

        for char in decrypt:
            print(char, end="", sep="")
