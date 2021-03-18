#!/usr/bin/env python3
import glob
#prelim = open("noFormatPrelim.hex", 'rb').read()
final = ""
for prelim in glob.glob("*.bin"):
    with open(prelim, 'rb') as f:
        characters = f.readlines()
        for line in characters:
            if line is not "":
                final+=hex(int(line)).split('x')[-1]

print(final)


'''
for files in glob.glob("*.bin"):
    with open(files,'latin-1') as f:
        arr = bytearray(f.read())
        print(arr)
        
        #decrypted = [chr(ord(a)) ^ chr(ord(b)) for (a,b) in zip(arr, key)]
        #print(decrypted)

'''
