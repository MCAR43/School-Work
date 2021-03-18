#!/usr/bin/env python3
import math
from p_factor import sieve
# <summary>
# Computes the gcd of 2 given integers
# @params:
#   - a,b are 2 integers
# @return:
#   - returns the GCD of the two integers a and b
def gcd(a,b):
    while b != 0:
        (a, b) = (b, a % b)
    return a


# <summary>
# Computes the quadratic residue of 2 given integers a and p
# @params:
#   - a and p are two integers with p assumed to be prime and odd
# @return:
#   - returns 1 if the two integers form a quadratic residue, or -1 if they form a quadratic
#     non-residue
#   - 0 if the two numbers are divisible
def quadratic_residue(a, p):
    if a % p == 0:
        return 0
    for x in range(0,p - 1):
        if (x ** 2) % p == a:
            return 1
    return -1


# <summary>
# Wrapper for the quad_residue function, takes in the same params and returns the legendre_symbol
def legendre_symbol(a, p):
    qR = quadratic_residue(a,p)
    return qR


# <summary>
# A function to determine if a given number is prime, loops through the range of the number
# only returning False if the number has been divided evenly, returns True otherwise
# @params:
#   - num is an integer > 2 
# @return:
#   - True/False whether or not the number is a prime
def isPrime(num):
    for i in range(2, num): 
        if num % i == 0:
            return False

    return True

# <summary>
# A function that prints the Legendre_symbol table from wikipedia to easily check whether
# the computed legendre symbols are correct
# @params:
#   - symbol_table is a 2d list corresponding to the (a | p) values respectively for the legedre symbol
def print_table(symbol_table):
    lefthandside = [i for i in range(3,128) if isPrime(i)]
    print("    ", end="")
    for elem in range(1,10):
        if elem < 10:
            print(str(elem) + "  | ", end="")
        else:
            print(str(elem) + " | ", end="")

    print()
    for i, row in enumerate(symbol_table):
        print(lefthandside[i], end="| ")
        for elem in row:
            if elem is not -1:
                print(str(elem) + "  | ", end="")
            else:
                print(str(elem) + " | ", end="")
        print()


# <summary>
# Function to compute the same test cases as given on the wikipedia to determine if the legendre_symbol is functioning
# correctly,  The given range for legendre(a | p) is a = 30, p = 127
def testLegendre():
    symbol_table = [[0 for _ in range(10)] for _ in range(30)]
    for a in range(1, 10):
        c=-1
        for p in range(3,128):
            if isPrime(p) and (p % 2 == 1):
                c+=1
                if(gcd(a,p)) == 1:
                    symbol = legendre_symbol(a,p)
                    symbol_table[c][a-1] = symbol
                else:
                    symbol_table[c][a-1] = 0
    print_table(symbol_table) 
    
def main():
    testLegendre() 

if __name__ == "__main__":
    main()


'''

def jacobi_symbol(a,n):
sign = 1
negativeValues = [3, 5]
while (a is not 0):
    while(a % 2 == 0):
        a //= 2
        if a in negativeValues:
            sign *= -1
    a, n = n, a
    if (a == 3 and n == 3):
        sign *= -1
    a %= n

if (n == 1):
    return sign
else:
    return 0


'''
