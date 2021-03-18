#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

def xor(bitStringA, bitStringB):
    bits = ''
    if(len(bitStringA) == len(bitStringB)):
        for i in range(0,len(bitStringA)):
            if bitStringA[i] != bitStringB[i]:
                bits += '1'
            else:
                bits += '0'
    else:
        print("UNEQUAL LENGTH OF BINARY STRING")
        exit()
    return bits

def binToString(message):
    str = ''
    for i in range(0,len(message), 8):
        byte = message[i:i+8]
        intMessage = int(byte, 2)
        str += chr(intMessage)
        
    return str

def convert(key, encrypted):
    encrypted = bin(int.from_bytes(encrypted, 'big'))
    #srtip the 'b' from the binary string
    if (len(encrypted)) != 2048:
        encrypted = encrypted[0] + encrypted[2:]

    encrypted = bytearray(encrypted, 'utf-8')
    return (binToString(xor(key, encrypted)))



def main():
    #Set-up input and output
    outfile = open(sys.argv[4], "wb")
    key = open(sys.argv[1], "rb").readlines()[int(sys.argv[2])]
    key = key[4:len(key) - 1]
    encrypted = open(sys.argv[3], "rb").read()

    toWrite = convert(key, encrypted)
    outfile.write(bytearray(toWrite, 'utf-8'))

if __name__ == '__main__':
    main()