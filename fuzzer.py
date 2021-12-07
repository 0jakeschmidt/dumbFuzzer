#!/usr/bin/env python
##fuzzer
import sys
import random as random
import os
import subprocess



#change to 33, 127 to keep in ascii range
MIN_BYTE_VALUE = 33
MAX_BYTE_VALUE = 127
#Take two args 
PROGRAM_IN = False
#1.seed
#2.itterations to run 
############################################remove this######################
if len(sys.argv) == 4:
    program = sys.argv[3]
    PROGRAM_IN = True


#############################################################################

# start with an empty string 
# every 500 itterations we add 10 bytes to it 
# 13% chance of a byte getting randomly changed
# print output

def ran13percent():
    n = random.randrange(100)
    if n<13:
        return True

def append10():
    charcs =''
    for x in range(0,10):
        charcs+=chr(random.randrange(MIN_BYTE_VALUE,MAX_BYTE_VALUE))
    return charcs

def changeTorandByte():
        return chr(random.randrange(MIN_BYTE_VALUE,MAX_BYTE_VALUE))

def genFuzzing(seedStart,itterations):
    holdingSeed = list(seedStart)
    for i in range(0,itterations):
        if i % 500 == 0:
            holdingSeed+=list(append10())
            #print(i)
        for x in range(0,len(holdingSeed)):
            if ran13percent():
                holdingSeed[x] = changeTorandByte()

        if PROGRAM_IN:
            p = subprocess.Popen(program, 
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding= 'utf8')
            stdout, stderr = p.communicate(input="".join(holdingSeed))
        
            if p.returncode == -11:
                print('SEGFAULT')
                print('the trigger was = ',"".join(holdingSeed))
                print(p.returncode )
        else:
            print("".join(holdingSeed))
            #sys.stderr.write(str(i)+'\n')
        #sys.stdout.flush()

if len(sys.argv) >=3:
    seed =sys.argv[1]
    itterations =int(sys.argv[2])
else: 
    print('Lacking arguments')
    sys.exit() 

random.seed(seed)



genFuzzing('',itterations)