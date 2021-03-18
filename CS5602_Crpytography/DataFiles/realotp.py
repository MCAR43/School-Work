#!/usr/bin/env python3
import glob
key = []
raw_prelim = []
decrypt = []
with open("otp.txt", 'r') as f:
    for char in f.readlines():
        char = char.strip('\n')
        key.append(int(char))


with open('File765.bin', 'rb') as f:
    raw = []
    dec = []
    byte = f.read(1)
    while byte:
        raw.append(byte)
        byte = f.read(1)

for i in range(0, len(key) - 25):
    res = key[i] ^ int.from_bytes(raw[i], byteorder="little")
    dec.append(res)


for char in dec:
    print(chr(char), end="")



