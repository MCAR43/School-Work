#!/usr/bin/env python3
import math

def primesInRange(lower, upper):
    primes=[]
    for num in range(lower, upper + 1):
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                break
        else:
            primes.append(num)

    return primes

def congruency(primes, b, n):
    for number in primes:
        if (number - b) % n != 0:
            primes.remove(number)

    return primes


def egcd(a,b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def main():

    lowerBounds = [1000000, 10000000]
    upperBounds = [2000000, 11000000]
    #Length P11: 46062
    #Length P13: 45981
    #Length P21: 40547
    #Length P23: 40638
    P11 = congruency(primesInRange(lowerBounds[0], upperBounds[0]), 1, 4)
    print("Finished P11")
    #P13 = congruency(primesInRange(lowerBounds[0], upperBounds[0]), 3, 4)
    print("Finished P13")
    P21 = congruency(primesInRange(lowerBounds[1], upperBounds[1]), 1, 4)
    print("Finished P21")
    #P23 = congruency(primesInRange(lowerBounds[1], upperBounds[1]), 3, 4)
    print("Finished P23")

#    print("Length P11: %d\nLength P13: %d\nLength P21: %d\nLength P23: %d\n" % (len(P11), len(P13), len(P21), len(P23)))
    
    #Here is my barebones implementation for proving that each number in P11 U P21 can be expressed as the sum of 2 squres
    #I started off attempting this problem by computing a couple of these numbers by hand, and they worked for each hand calculation, and I knew that if I had a list of all the prime numbers from [2, UPPERBOUND] then in that list would be 2 primes that sum up to a number in P11 U P21.  
    #However As I started calculating these
    PU = P11 + P21    
    PU = sorted(PU, reverse=True)
    #print(PU[:20])
    primes = primesInRange(2,upperBounds[1])
    print(primes)
    tally = 0
    for prime in PU[:20]:
        for a in primes:
            for b in primes:
                if a**2 + b**2 == prime:
                    tally += 1
                    print("Success")
                    print(a**2 + b**2)
    
    
    print(len(PU))
    print(tally)

if __name__ == "__main__":
    main()
            
            
    
