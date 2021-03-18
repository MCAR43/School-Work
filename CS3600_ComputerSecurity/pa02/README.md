# Programming assignment 2 (pa02) -- Binary One Time Pad

1. A python3 script named and executed as follows `$ ./bin_otp_key_gen.py keyfile.sec` should output a utf-8 unix delimited text file of 500 numbered OTP keys, 1-per-line, with each key 2048 characters (bits) long. 
Each line should have a 3-digit number with leading 0s, starting with 001, followed by a single space, and a 2048bit key.
For example:

    keyfile.sec would have 

    `001 1010101101010101010...
    002 1010101001010100101...
    .
    .
    .
    500 1010101001010100111...
    `

    The general format is:

    `$ ./bin_otp_key_gen.py <keyfiletowrite>`

2. A python3 script named and executed (for example) as follows `$ ./bin_otp.py keyfile.sec 3 inputfile.txt outputfile.txt` should turn the text in inputfile.txt into a bitstring, XOR it with the 3rd key in the keyfile.sec, translate back to readable utf-8 text, and write the converted data to outputfile.txt. 
Thus, the script should work symmetrically, encrypting or decrypting.
The encrypted message may look like ASCII junk. 
Input parameters could be named any valid filename, and the general format is: 

    `$ ./bin_otp.py <keyfile> <keynum> <inputfile> <outputfile>`

## What to submit
* You could have testing files like messages and keys in the repository, but just the two python scripts are necessary.

## General notes:
* Write this from scratch (without for example using a OTP library, or book code). Python standard library is ok.
* Read the syllabus procedures about file format and code running environment.
* The scripts are expected to run in an up-to-date Kali install, in python3.

## Additions:
* The message length will always be the exact length of the key in binary, so you don't have to pad or un-pad the message. 
