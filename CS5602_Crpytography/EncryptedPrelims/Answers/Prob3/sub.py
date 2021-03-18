#!/usr/bin/env python3
from collections import defaultdict, Counter
def_freq = {
        'A': .0812,
        'B': .0149,
        'C': .0271,
        'D': .0432,
        'E': .1202,
        'F': .0230,
        'G': .0203,
        'H': .0592,
        'I': .0731,
        'J': .0010,
        'K': .0069,
        'L': .0398,
        'M': .0261,
        'N': .0695,
        'O': .0768,
        'P': .0182,
        'Q': .0011,
        'R': .0602,
        'S': .0628,
        'T': .0910,
        'U': .0288,
        'V': .0111,
        'W': .0209,
        'X': .0017,
        'Y': .0211,
        'Z': .0007
}

def_freq = sorted(def_freq, key=def_freq.get, reverse=True)


def decrypt(ciphertext):
    encoding = defaultdict(str)
    
    freq = defaultdict(float)
    cipherSize = 0
    for letter in ciphertext.strip('\n'):
        cipherSize+=1
        try:
            freq[letter] += 1
        except KeyError:
            freq[letter] = 1

    for key,val in freq.items():
        freq[key] = val / cipherSize 
       
    
    freq = sorted(freq, key=freq.get, reverse=True)
    for i, letter in enumerate(freq):
        encoding[letter] = def_freq[i]
    
    return encoding    

def main():
    ciphertext = """53$$%305))6*;4826)4$.)4$);806*;48%8@60))85;;]8*;:$*8%83(88)5
*%;46(;88*96*?;8)*$(;485);5*%2:*$(;4956*2(5*-4)8@8*;4069285)
;)6%8)4$$;1($9;48081;8:8$1;48%85;4)485%528806*81($9;48;(88;4
($?34;48)4$;161;:188;$?;"""

    enc = decrypt(ciphertext)
    for letter in ciphertext:
        print(enc[letter], end="")

if __name__ == "__main__":
    main()
