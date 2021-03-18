#!/usr/bin/env python3
import string
from collections import defaultdict

encoding = {} 
decode = []
shifted = []
with open('File354.bin', 'rb') as f:
    for i in range(26):
        byte = f.read(1)
        print(ord(byte))
        encoding[int.from_bytes(byte, byteorder="little")] = string.ascii_uppercase[i] 


print(encoding)
'''
with open('File765-2.bin', 'rb') as full:
    byte = full.read(1)
    while byte:
        try:
            decode.append(encoding[int.from_bytes(byte, byteorder="little")])
            byte = full.read(1)
        except KeyError:
            print("Key: %d" % ord(byte))


for char in decode:
    print(char, end="")

'''

with open('File354.bin', 'rb') as f:
    orig = []
    char = f.read(1)
    while char:
        orig.append(char)
        char = f.read(1)

for char in orig:
    print(encoding[int.from_bytes(char, byteorder="little")], end="")


'''
inv_encoding = {v: k for k, v in encoding.items()}
for byte in orig:
    newChar = ((ord(byte) + 3) % 26) + 65
    print(chr(inv_encoding[chr(newChar)]), end="")
'''
