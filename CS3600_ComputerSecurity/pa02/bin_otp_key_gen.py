#!/usr/bin/python3
import secrets
import string
import sys
try:
    outfile = open(sys.argv[1], "w")
except IndexError:
    outfile = open("keyfile.sec", "w")

def genKey():
    byteString = ""
    for i in range(0,256):
        character = secrets.choice(string.ascii_letters)
        character = bin(ord(character))
        character = character[0] + character[2:] 
        byteString+=character
        print(character)
    return byteString

for i in range(0,500):
    outfile.write('%03d' % i + " " + genKey() + "\n")
