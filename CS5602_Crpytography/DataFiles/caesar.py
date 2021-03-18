#!/usr/bin/env python3
import string

encoding = {}
decode = []
shifted = []
with open('File431.bin', 'rb') as f:
    for i in range(26):
        byte = f.read(1)
        encoding[int.from_bytes(byte, byteorder="little")] = string.ascii_uppercase[i] 

with open('File431.bin', 'rb') as full:
    byte = full.read(1)
    while byte:
        decode.append(encoding[int.from_bytes(byte, byteorder="little")])
        byte = full.read(1)


for char in decode:
    print(char, end="")


inv_encoding = {v: k for k, v in encoding.items()}

for byte in decode:
    newChar = ((ord(byte) + 3) % 26) + 65
    #print(chr(newChar), end="")
    print(chr((inv_encoding[chr(newChar)])), end="")

