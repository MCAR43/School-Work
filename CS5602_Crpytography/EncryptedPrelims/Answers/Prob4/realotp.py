#!/usr/bin/env python3
import glob
key = []
raw_prelim = []
decrypt = []
with open("otp.txt", 'r') as f:
    for char in f.readlines():
        char = char.strip('\n')
        key.append(int(char))





'''
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
'''

with open('ANDERSONprob4a.bin', 'rb') as f:
    fir = []
    dec = []
    byte = f.read(1)
    while byte:
        fir.append(byte)
        byte = f.read(1)

with open('ANDERSONprob4b.bin', 'rb') as f:
    sec = []
    dec = []
    byte = f.read(1)
    while byte:
        sec.append(byte)
        byte = f.read(1)



for i in range(0,len(sec)):
    res = int.from_bytes(fir[i], byteorder="little") ^ int.from_bytes(sec[i], byteorder="little")
    dec.append(res)


for char in dec:
    print(chr(char), end="")

'''

for i in range(0, len(key)):
    res = key[i] ^ int.from_bytes(raw[i], byteorder="little")
    dec.append(res)


for char in dec:
    print(chr(char), end="")
'''


#problm 5 stuff
'''
with open('ANDERSONProb4File3.bin', 'rb') as f:
    first = []
    byte = f.read(1)
    while byte:
        first.append(byte)
        byte = f.read(1)

with open('ANDERSONProb4File4.bin', 'rb') as sec:
    second = []
    byte = sec.read(1)
    while byte:
        second.append(byte)
        byte = sec.read(1)



print(len(first))
print(len(second))

for i in range(0, len(first)):
    res = int.from_bytes(first[i], byteorder="little") ^ int.from_bytes(second[i], byteorder="little")
    decrypt.append((res))


for char in decrypt:
    print(char)
'''
