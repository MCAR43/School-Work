#!/usr/bin/env python3
from random import randint
import math

# @Rabin.py
#  - This program implements the Rabin encryption system on some given plaintext


def egcd(a,b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)


# #rabin(text, decrypt)
# plaintext:
#  - string that we want to decrpyt/encrypt
#
# decrypt:
#  - boolean variable to determine if we're encrypting or decrypting, False for encryption, True for decryption
#
# @returns:
#  - The result of the encryption/decryption using the Rabin encryption method
def rabin(plaintext, rabin_n, rabin_b, dec=False):
    #Variables used to determine our private and public key
    rabin_p = 8751139
    rabin_q = 8761279
    #Our private and public keypairs
    rabin_private = (rabin_p,rabin_q)
    rabin_public = (rabin_n, rabin_b)
    
    if dec:
        return(decrypt(plaintext, rabin_public, rabin_private))
    else:
        return(encrypt(plaintext, rabin_public))

def decrypt(ciphertext, public, private):
    possibleDecryptions = []
    roots = []
    N, B = public
    p, q = private
    
    ### TVALUES
    #Compute the value of T
    rabin_t = ((B**2) + 4 * ciphertext) % N
    
    ###P1
    #Compute the roots of our T value % p
    exp = ((p+1)//4) % p
    p1= (rabin_t ** exp) % p // 2

    ### P2
    #Comjpute the roots of our T value % q
    exp = ((q+1)//4) % q
    p2= (rabin_t ** exp) % q // 2 
    
    #Find the GCD of our 2 primes
    a, b = egcd(p,q)[1:]
    #Use CRT to obtain the roots of t % N
    roots.append(((a * p * p2) + (b * q * p1)) % N)
    roots.append(roots[-1] * -1)
    roots.append(((a * p * (p2*-1)) - (b * q * (p1*-1))) % N)
    roots.append(roots[-1] * -1)
    
    #Generate our possible decryptions from our values
    for root in roots:
        possibleDecryptions.append(((root - (B//2)) + ((N*-1)//2)) % N)

    


def encrypt(plaintext, public):
    ciphertext = plaintext * (plaintext + public[1]) % public[0]
    return(ciphertext)
    
    


def main():
    filename="plaintext.txt"
    keyfilename="ANDERSONQ6.key"
    
    for line in open(keyfilename, 'r').readlines():
        rabin_n, rabin_b = line[1:len(line)-2].split(',')
        
    plaintext = []
    for char in open(filename, 'rb').read():
        plaintext.append((char))
    
    cipher = []
    for char in plaintext:
        cipher.append(rabin(char, int(rabin_n), int(rabin_b), False))
        

    for block in cipher:
        print(block, end=", ")


if __name__ == "__main__":
    main()
