#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import binascii
from operator import xor


def stringToBits(message):
    str = ''
    for letter in message:
        #rint(bin(ord(letter)))
        binary = bin(ord(letter))
        str += binary[2:]

    return str

def convertData(bitStringA, bitStringB):
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
        intMessage = int(message[i:i+8], 2)
        str += chr(intMessage)
        
    return str
    
def string_bin(string):
    return ''.join(format(ord(c), 'b') for c in string)

def bin_string(binary):
    bingen = (binary[i:i+7] for i in range(0, len(binary), 7))
    return ''.join(chr(eval('0b'+n)) for n in bingen)

def main():
    outfile = open(sys.argv[4], "w", encoding="utf-8")
    key = open(sys.argv[1], "r").readlines()[int(sys.argv[2])]
    key = key[4:len(key) - 1]
    encrypted = open(sys.argv[3], "r").read()

    encrypted = bin(int.from_bytes(encrypted.encode(), sys.byteorder))
    encrypted = encrypted[2:]
    print(encrypted)
    '''
    xorString = xor(int(key,2), int(encrypted,2))
    print('{0:b}'.format(xorString))
    translated = (''.join(chr(int(xorString[i:i+8], 2)) for i in range(0, len(xorString), 8)))
    outfile.write(translated)
    '''
    
    
    
    

    
    

    


if __name__ == '__main__':
    main()