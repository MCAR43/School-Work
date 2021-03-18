#!/usr/bin/env python3
from copy import copy
from random import uniform, randint
'''
The following Functions are defined and function as follows:
degree(poly):
    - poly is the input and is a polynomial represented as a list such that the first element in the list is the highest degree represented in the polynomial
    - This function recursively loops through the list and returns the index of the first non-zero element in the list, this index reperesents the degree of the polynomial
    - If no non-zero element in poly is found than the function return 0, indicating it is either the [0] polynomial, or the list was completely empty

add(P1,P2):
    - P1, and P2 are two polynomials in list notation that are to be added together, there are no limitations on size or elements in the polynomails
    - The function creates a new polynomials represented as a list that is the size of the largest input polynomial, it then loop through all the elements of the polynomial on the LHS and assigns them to the indeces of the
      newly created polynomial.  After this it loops through the second polynomial and adds each element to the correct index in the newly created polynomial, the result of this a polynomial representing the addition
      of the 2 polynomials passed as input

sub(P1,P2):
    - This function takes in 2 polynomials that are the same requirements as the polynomials for the add() function
    - This function loops through the elements of the 2 polynomial given, and multiplies each element in the list by -1, we do this because A - B == A + (-B)

division(dividend, divisor):
    - This function takes in 2 polynomials such that the degree of the divisor is not greater than the dividend, because then the result is trivial, it also checks to make sure the first element in both polynomials is non-zero
      as instructed in the prompt

    - This function is an implementation of polynomial long division similarly to as how it would be done by hand, at each iteration it matches the highest degree that can be divided into the dividend, and then multiplies the
      result of that operation into a variable called quotient, representing the terms successfully divided through, it will then subtract the result of this from the dividend and loop again with dividend being what wasn't divided
      the function returns 2 lists representing the quotient, and the remainded

poly_gcd(a, b):
    - This function takes in two polynomials represented as lists a, b and uses the Extended Euclidean Algorithm to find the GCD of the 2 polynomials.
    - This function works on the assumption that gcd(a,b) = gcd(b,r1) = gcd(r1, r2) = gcd(r2, r3) until the remainder is 0, at that point whatever is left in the left hand side variable in the function call is the greatest common divisor
'''

def degree(poly):
    if poly:
        if poly[0] != 0:
            return len(poly) 
        else:
            return(degree(poly[1:]))
    else:
        return 0
def add(P1, P2):
    newSize = max(len(P1), len(P2))
    P3 = [0 for i in range(newSize)]
    for i in range(0, len(P1)):
        P3[i] = P1[i]
    for i in range(0, len(P2)):
        P3[i] += P2[i]
    return P3

def sub(P1,P2):
    P2 = [i * -1 for i in P2]
    return add(P1, P2)

def division(dividend, divisor):
    if not dividend or not divisor:
        print("Error")
        return False

    if degree(divisor) > degree(dividend):
        print("Cannot divide")
        return ([1],[0])

    degDivisor = degree(divisor)
    degDividend = degree(dividend)
    quotient = [] 
    counter = 0
    while(degDividend >= degDivisor and counter < 10):
        counter += 1
        newDivisor = copy(divisor)
        shiftValue = degDividend - degDivisor
        for _ in range(shiftValue): newDivisor.append(newDivisor.pop(0))
        val1 = dividend[len(dividend) - degree(dividend)]
        val2 = newDivisor[len(newDivisor) - degree(newDivisor)]
        quotient.append(round(val1 / val2, 2))
        newDivisor = [round(elem * quotient[-1], 2) for elem in newDivisor]
        dividend = sub(dividend, newDivisor)
        degDividend = degree(dividend)

    rem = dividend
    return(quotient, rem)

def poly_gcd(a, b):
    loop = True
    counter = 0
    while(loop and counter < 5):
        counter += 1
        quot, rem = division(a,b)
        if all(elem == 0 for elem in rem):
            return quot
        else:
            a = b
            b = rem

def generate_tests():
    cases = []
    degree = randint(10,25)
    cases.append([randint(1,50) for i in range(degree)])
    cases.append([randint(1,50) for i in range(degree - randint(1,7))])
    for polynomial in cases:
        for i in range(2, len(polynomial)):
            if i % randint(1,10) % 5 == 0:
                polynomial[i] = 0
    
    return cases[0], cases[1]


def main():
    testcases = 5
    for i in range(testcases):
        t1, t2 = generate_tests()
        print(division(t1,t2))
        print(poly_gcd(t1,t2))

if __name__ == "__main__":
    main()
