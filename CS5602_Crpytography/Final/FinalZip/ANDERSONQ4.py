#!/usr/bin/env python3
import ANDERSONQ4Constants as constants



def populateBoxes():
    perm = constants.DES_PERM
    NEW_SBOXES = [0 for _ in range(8)]
    for i, entry in enumerate(perm):
        NEW_SBOXES[int(entry) - 1] = (constants.S_BOX[i])
    
    return NEW_SBOXES

def main():
    SBOX = populateBoxes()
    print(SBOX)

if __name__ == "__main__":
    main()
