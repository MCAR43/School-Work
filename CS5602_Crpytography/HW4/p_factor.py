#!/usr/bin/env python3
import math
# <summary>
# @summary:
#  - Sieve or Eratosthenes as shown in class
# @params: n
#  - integer of which we want to calculate all primes < n
# </summary>
def sieve(n):
    if n < 2:
        return []

    s = list(range(n+1))
    s[0] = s[1] = -1
    for i in range(2, n + 1):
        if s[i] > 0:
            for k in range(2 * i, n + 1, i):
                s[k] = -1

    os = []
    for i in range(2, n+1):
        if s[i] > 0:
            os.append(i)
    return os

# <summary>
# Takes in an integer input, and calculates the prime factorization of the input factorial
# @params:
#  - n: is the integer of which we want to calculate the prime factorization of factorial (n!)
# @return:
#  - result: this is a string representation of the prime factorization of n! for example (9! = (2**7)(3**4)(5**1)(7**1))
#  - calcVal: this is the value of calculating our prime factorization of n!, in the example of 9! this is the result of
#             2^7 * 3^4 * 5^1 * 7^1, this value is used to compare to the math.factorial() value from python to ensure
#             we calculated the correct roots 
def primeFactorization(n):
    #our return values
    result = ""
    calcVal = 1
    #All primes < our input n, (our prime factors)
    primes = sieve(n)
    #A List representing the future exponents that will correspond to our prime factors
    # e.g:
    #   n = 6
    #   primes         = [2, 3, 5]
    #   primeExponents = [4, 2, 1]
    #   which corresponds to (2**4)(3**2)(5**1)
    primeExponents = [0 for _ in range(len(primes))]

    #loop through all of our prime numbers to determine their exponents
    for i, num in enumerate(primes):
        exp = 1
        #the first computed exponent determines how many times this factor shows up in n!
        first = math.floor(n / (num**exp))
        #add the exponent to the corresponding position in the exponents list
        primeExponents[i] += first
        while(exp < first):
            exp += 1
            val = math.floor(n / (num**exp))
            #add the computed value to the corresponding position in the exponents list
            primeExponents[i] += val
    
    #This is used to format the results we calculated above into the specified format in the homework
    #as well as calculating the result of n! from our factored primes to compare to math.factorial() later
    for i in range(0, len(primes)):
        calcVal *= primes[i]**primeExponents[i]
        result += "(" + str(primes[i]) + "**" + str(primeExponents[i]) + ")"

    return result, calcVal
# <summary>
# Takes in an integer input and calculatres the primeFactorization of that number factorial, then compares it to the result
# of that computation and pythons math.factorial(), prints out the number of test cases passed
# @params:
#  - maxnum: the amount of test cases / highest value integer we would like to compute the prime factorization of
def test(maxNum):
    numPassed = 0
    for i in range(1,maxNum):
        resString, resVal = primeFactorization(i)
        print("primeFactorization(%d) %s" % (i, resString))
        factorRes = math.factorial(i)
        if(factorRes == resVal):
            numPassed+=1
    print("%d out of %d cases passed" % (numPassed, maxNum - 1))

def main():
    NUM_CASES = 100
    test(NUM_CASES)   
    
if __name__ == "__main__":
    main()
