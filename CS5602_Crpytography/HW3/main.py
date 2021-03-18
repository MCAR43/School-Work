#!/usr/bin/env python3
from collections import defaultdict, OrderedDict
from random import randint, shuffle
def cycle_not(L1, val, cyc, final):
    if len(cyc) == len(L1):
        flat_list = [item for sublist in final for item in sublist]
        final.append(list([item for item in cyc if item not in flat_list]))
        return final[1:]
    if L1[val] in cyc:
        val = min([item for item in L1 if item not in cyc])
        val = L1.index(val)
        flat_list = [item for sublist in final for item in sublist]
        final.append(list([item for item in cyc if item not in flat_list]))
        cyc.append(L1[val])
    else:
        cyc.append(L1[val])
    return cycle_not(L1, cyc[-1] - 1, cyc, final)

def list_not(cyc):
    if 0 in cyc:
        print("Invalid Permutation")
        return None

    new = defaultdict(int)
    list_not = []
    #We want to loop through the entirety of the cycle notation permutation
    while cyc:
        #Pop off the first 'cycle' from the cycle notation list frmo the left side
        # Ex: (3 2 4 1) (5 6)
        # at iteration 0 sublist = (3 2 4 1) and cyc = (5 6)
        sublist = cyc.pop(0)
        #Loop through the entirety of the sublist
        for i in range(len(sublist)):
            
            #We start with the first element in the cycle, and add it do a dictionary corresponding to its value and the next element in the cycle
            # Ex:
            # 3 -> 2
            # 2 -> 4
            # 4 -> 1
            # when we try to index into what comes after 1 in the sublist, we will throw an index error, and at that point we add the first item in the sublist to the corresponding element in the dict
            # So for the above permutation, after looping through the entirety of the first sublist our permutation will look like ethis
            #   1 2 3 4 5 6
            #   3 4 2 1 _ _
            try:
                new[sublist[i]] = sublist[i + 1]
            except IndexError:
                new[sublist[i]] = sublist[0]

    #This just converts the dictionary into a list in the order of the elements inserted
    for key, val in sorted(new.items()):
        list_not.append(val)
    return list_not

def findNext(perm, val):
    for subl in perm:
        for i in range(0, len(subl)):
            if subl[i] == val:
                try:
                    val = subl[i + 1]
                except IndexError:
                    val = subl[0]
                
                return val
    return 0
    
def cycle_mult(P1, P2):
    mult = []
    submult = []
    flat_list = [item for sublist in P2 for item in sublist]
    nextVal = flat_list[0]
    while flat_list:
        val = findNext(P1, nextVal)
        if val in submult:
            mult.append(submult)
            submult = [min(flat_list)]
        else:
            submult.append(val)
        nextVal = findNext(P2, submult[-1])
        flat_list.remove(submult[-1])
        
    mult.append(submult)
    return mult

def generate_test_cases():
    numPassed = 0
    numCases = 5
    for i in range(numCases):
        #Generates an ordered list of size [25,100] 
        testPerm = list(range(1, randint(5,10)))
        #Shuffles the list generated in order to achieve a "random" permutation
        shuffle(testPerm)

        print("Case %d:" % i)
        print("Original Permutation: %s" % str(testPerm))
        #converts the randomly shuffled list to cycle notation
        cycle = cycle_not(testPerm, 0, [], [[]])
        print("Cycle Notation: %s" % str(cycle))
        #converts the list back into its original notation
        listNot = list_not(cycle)
        print("List Notation: %s" % str(listNot))
        #if value returned from list_not equals the value of the original testPermutation
        # List -> cycle -> list works correctly
        
        if listNot == testPerm:
            print("Case %d passes" % i)
            numPassed += 1
        else:
            print("Case %d fails" % i)
    print("Passed: %d -- Failed: %d" % (numPassed, numCases - numPassed))
    
def cyc_mult_test():
    numCases = 5
    numPassed = 0
    for i in range(numCases):
        print("Case %d: " % i)
        length = randint(5,10)
        perm_one = list(range(1,length))
        perm_two = list(range(1,length))
        shuffle(perm_one)
        shuffle(perm_two)
        perm_one_cycle = cycle_not(perm_one, 0, [], [[]])
        perm_two_cycle = cycle_not(perm_two, 0, [], [[]])
        print("Cycle_one: %s" % str(perm_one_cycle))
        print("Cycle_two: %s" % str(perm_two_cycle))
        cycle_m = cycle_mult(perm_one_cycle, perm_two_cycle)
        print("Cycle Multiplication Result: %s" % str(cycle_m))
        list_m = permMult(perm_one, perm_two)
        print("Multiplication Result of given Multiplication Function: %s" % str(list_m))
        cycle_m_list = list_not(cycle_m)
        print("Converted List notation of My Function: %s" % str(cycle_m_list))

        if cycle_m_list == list_m:
            print("Case %d PASSES" % i)
            numPassed += 1
        else:
            print("Case %d FAILS" % i)

        print()
        
    print("Passed: %d -- Failed: %d" % (numPassed, numCases - numPassed))

def permMult(P1, P2):
    if (0 in P1) != (0 in P2):
        return "Base error"
    if len(P1) != len(P2):
        return "Len error"
    if 0 not in P1:
        base = 1
        P1 = [0] + P1
        P2 = [0] + P2
    else:
        base = 0
    pout = [ P1[P2[i]] for i in range(len(P1))]
    return pout[base:]

def main():
    generate_test_cases()
    L1 = [[6,5,2,7,3,4,8,1]]
    L2 = [[5,2,4,6,8,1], [7,3]]
    #cyc_mult_test()
    #print(cycle_mult(L1, L2))


if __name__ == "__main__":
    main()
