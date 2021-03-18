#!/usr/bin/env python3
import secrets
import sys
try:
    outfile = open(sys.argv[1], "w")
except IndexError:
    outfile = open("keyfile.sec", "w")

def genKey():
    byteString = ""
    for i in range(0,2048):
        byteString += (str(secrets.randbelow(2)))
    return byteString

for i in range(0,500):
    outfile.write('%03d' % i + " " + genKey() + "\n")
