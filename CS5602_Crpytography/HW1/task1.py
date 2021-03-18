import random
ofile = open('otp.txt', 'w')
for i in range(0,10000):
    ofile.write(str(random.randint(0,255)) + '\n')

    
