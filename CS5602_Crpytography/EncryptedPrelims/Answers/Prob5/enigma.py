#!/usr/bin/env python3
import string
"""           MINI-ENIGMA SIMULATOR

This program simulates a reduced complexity Enigma machine. The

reduced complexity comes from reducing the number of rotor disks that

can be used as well as the number of reflectors. This program was

written in Python 2.7 on April 24, 2019. All plaintexts and ciphertexts

use only the capital letters A..Z. The actions do not perfectly

simulate the actions of the Enigma machine, because we have omitted extra

shifts. The idea is to provide a simulation that is Enigma-like."""




# Each rotor disk is represented as a permutation of A..Z

rotorDisks = [ "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "VZBRGITYUPSDNHLXAWMJQOFECK"]



# Each reflector is represented as a permutation of A..Z

reflectors = ["YRUHQSLDPXNGOKMIEBFZCWVJAT", "FVPJIAOYEDRZXWGCTKUQSBNMHL"]



def refl(inChar,reflector):

    # inChar is the input character, reflector is one of the two reflectors

    # outChar is the output character


    inChar = inChar.upper() # make sure we work with capital letters
    #print(inChar)
    #print(string.ascii_uppercase.index(inChar))
    #print(reflector[7])
    return reflector[string.ascii_uppercase.index(inChar)] # Applying the permutation to inChar



def rDisk(inChar,disk,shift,direction):

    # inChar is the input character, disk is one of the four rotorDisks,

    # shift is how much the disk is shifted. For example, let's use

    # disk 1 as our target disk. If the shift is 0, A goes to E, B goes to

    # K, etc. We assume that shifts are shifts to the right, shift = 1

    # EKMFLGDQVZNTOWYHXUSPAIBRCJ becomes JEKMFLGDQVZNTOWYHXUSPAIBRC and

    # for shift 2 it becomes CJEKMFLGDQVZNTOWYHXUSPAIBR, etc.

    # Enigma used the rotors in two directions. In the forward direction,

    # which we denote by 0, it used the permutation like the reflectors

    # did. In the reverse direction, which we denote by 1, it used the

    # inverse permutation.


    inChar = inChar.upper() # make sure we work with capital letters

    shift = shift%26 # make sure that shifts are proper

    perm = disk[-shift:]+disk[:-shift]

    invperm = ''

    for c in string.ascii_uppercase:
        invperm += string.ascii_uppercase[perm.index(c)]
    
    if direction == 0:

        return perm[string.ascii_uppercase.index(inChar)] # Applying the permutation to inChar

    else:
        return invperm[string.ascii_uppercase.index(inChar)] # Applying the inverse permutation
                

def mEnigma(text,disk1num,shift1,disk2num,shift2,reflectornum):

    # To encrypt something we need to select two out of four disks, pick

    # a shift for each disk, as well as a reflector. We then run the message

    # through the shifted disks in the forward direction in order, then

    # through the reflector and then back through the disks in the reverse

    # direction. After each letter, disk1 is shifted by 1. For every 26

    # letters disk2 is shifted by 1.

    global rotorDisks,reflectors

    text = text.upper() # Make sure we are working with capital letters

    disk1 = rotorDisks[disk1num]

    disk2 = rotorDisks[disk2num]

    reflector = reflectors[reflectornum]

    ostr = ''

    for c in text:

        c = rDisk(c,disk1,shift1,0)

        c = rDisk(c,disk2,shift2,0)

        c = refl(c,reflector)

        c = rDisk(c,disk2,shift2,1)

        ostr += rDisk(c,disk1,shift1,1)

        shift1 += 1

        if shift1 == 26: # disk2 shifts every 26 disk1 shifts

            shift2 += 1

            shift2 = shift2%26

        shift1 = shift1%26

    return ostr


def main():
    raw_file = ""
    with open('enigmaInput.txt', 'r') as f:
        char = f.read(1)
        while char:
            raw_file+=char
            char = f.read(1)
    
    # (2, 17, 9, 21, 1)
    '''
    with open('decrypt.txt', 'w') as out:
        for ref in range(2):
            for disk1 in range(4):
                for shift1 in range(25):
                    for disk2 in range(4): 
                        for shift2 in range(25):
                                #print("(%d, %d, %d, %d, %d)" % (disk1, shift1, disk2, shift2, ref), end="")
                                #print(" = %s" % mEnigma(raw_file, disk1, shift1, disk2, shift2, ref))
                                print("(%d, %d, %d, %d, %d)" % (disk1, shift1, disk2, shift2, ref), end="", file=out)
                                print(" = %s" % mEnigma(raw_file, disk1, shift1, disk2, shift2, ref), file=out)
    '''
    with open('fullDecrypt.txt', 'w') as out:
        print(mEnigma(raw_file, 2, 17, 0, 21, 1), file=out)



if __name__ == "__main__":
    main()    



















