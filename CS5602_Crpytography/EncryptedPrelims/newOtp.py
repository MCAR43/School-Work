#!/usr/bin/env python3
import glob
key = b''
prelim = ""
with open("myKey.key", 'rb') as f:
    while True:
        bit = f.read(1)
        if not bit:
            break
        
        key += bit

        
print(len(key))

'''
for toOpen in glob.glob("*.bin"):
    print("Testing Prelim: %s" % toOpen)
    with open(toOpen, 'rb') as f:
        prelim = f.read()
    print(prelim)
    #print(key)
    #decrypt = ([a ^ b for (a,b) in zip(prelim, key)])
    #print(decrypt)
'''
