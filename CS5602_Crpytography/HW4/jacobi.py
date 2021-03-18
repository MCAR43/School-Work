#!/usr/bin/env python3
import math
from collections import defaultdict
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

#calculate the prime factors for any given number using integer division
def prime_factors(n):
    pFac = defaultdict(int)
    factor = 2
    while n > 1:
        while n % factor == 0:
            pFac[factor] += 1
            n //= factor
        factor += 1

    return dict(pFac)


def jacobi(a, n):
    #grab the prime factors of the denominator
    pFacs = prime_factors(n)
    symbol = 1
    #for each prime factor and prime factor exponent pair calculate the product of their
    #legendre symbols
    for key, val in pFacs.items():
        #multiple the resulting symbol for that prime factor
        symbol *= legendre_symbol(a, key)
        #raise the result of that symbol to the corresponding power of the prime factor
        symbol = symbol**val
    return symbol


#Tests the jacobi symbols from a = 1..10 and p = 1.60 where p is an odd integer
def testJacobi():
    for a in range(1, 10):
        for p in range(1, 60):
            if p % 2 == 1:
                if gcd(a,p) == 1:
                    print("Jacobi (%d | %d): %d" % (a, p, jacobi(a,p)))
                else:
                    print("Jacobi (%d | %d): %d" % (a, p, 0))


def main():
    testJacobi() 

if __name__ == "__main__":
    main()

