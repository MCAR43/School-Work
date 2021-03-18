#!/usr/bin/env python3
from collections import defaultdict
from collections import Counter

#QUESTION_FOUR
def perm_mult(L1, L2, L3=[]):
    if not L2:
        return L3
    L3.append(L1[L2[:1][0] - 1])
    return(perm_mult(L1, L2[1:], L3))


def cycle_not(L1, val=0, cyc = [], final = [[]]):
    if len(cyc) == len(L1):
        flat_list = [item for sublist in final for item in sublist]
        final.append(list(set(cyc) - set(flat_list)))
        return final[1:]
    if L1[val] in cyc:
        val = min(set(L1) - set(cyc))
        val = L1.index(val)
        flat_list = [item for sublist in final for item in sublist]
        final.append(list(set(cyc) - set(flat_list)))
        cyc.append(L1[val])
    else:
        cyc.append(L1[val])
    return cycle_not(L1, cyc[-1] - 1, cyc)

def list_not(cyc):
    new = defaultdict(int)
    while cyc:
        sublist = cyc.pop(0)
        for i in range(len(sublist)):
            try:
                new[sublist[i]] = sublist[i + 1]
            except IndexError:
                new[sublist[i]] = sublist[0]
    for key in sorted(new):
        cyc.append(new[key])
    return cyc





def degree(poly):
    try:
        return max(idx for idx, i in enumerate(poly) if idx)
    except ValueError:
        return 0

def add(P1, P2):
    newSize = max(degree(P1), degree(P2))
    P3 = [0 for i in range(newSize)]

    for i in range(0, degree(P2)):
        P3[i] = P2[i]
    for i in range(0, degree(P1)):
        P3[i] += P1[i]
    return P3

def sub(P1,P2):
    P2 = [i * -1 for i in P2]
    return add(P1, P2)

def mult(P1, P2):
    P3 = [0 for i in range(degree(P1) + degree(P2) + 1)]
    for i, ix in enumerate(P1):
        for k, kx in enumerate(P2):
            P3[i + k] += ix * kx
    return P3

def division(dividend, divisor):
    remainder = dividend[::-1]
    divisor = divisor[::-1]
    remainderDegree = degree(remainder)
    quotient = [0 for i in range(remainderDegree)]
    newDivisor = quotient
    divisorDegree = degree(divisor)

    if divisorDegree < 0: return False

    while remainderDegree >= divisorDegree and remainder:
        print(remainder)
        print(divisor)
        step = remainderDegree - divisorDegree
        zeroes = [0 for _ in range(step)]
        
        
        newDivisor = zeroes + [remainder[-1] / divisor[-1]]
        quotient = add(newDivisor, quotient)
        remainder = sub(remainder, mult(newDivisor, divisor))
        remainderDegree = degree(remainder)
        divisorDegree = degree(divisor)

    return quotient, remainder

def poly_gcd(P1, P2):
    if not P2:
        return P1
    else:
        P1, P2 = division(P1, P2)
        poly_gcd(P1, P2)

def main():
    L1 = [5,-10,3,-5,2,-1,20,1,-2,-1,10]
    L2 = [10,-5,6,-10,1,-2,10,1,-1,-5,5]

    POLY_ONE = [-42, 0, -12, 1]
    POLY_TWO = [-3, 1, 0, 0]
    
    print(division(POLY_ONE, POLY_TWO))
    
    
    #print(poly_gcd(L1, L2))



if __name__ == "__main__":
    main()
