#!/usr/bin/env python3

# 50.042 FCS Lab 6 Diffie-Hellman Key Exchange
# Year 2020
# Student: Kwa Li Ying (1003833)

import math
import time
import primes
import dhke


def baby_step(alpha,beta,p,fname):
    # Calculate m = sqrt(size of group) = sqrt(p)
    m = math.ceil(math.sqrt(p))
    # Generate values of xb for 0 to m-1 and write to fname
    file = open(fname, 'w')
    for xb in range(m):
        value = primes.square_multiply(alpha, xb, p)
        value = primes.square_multiply((value * beta), 1, p)
        file.write(str(value) + "\n")
    file.close()
    
def giant_step(alpha,p,fname):
    # Calculate m = sqrt(size of group) = sqrt(p)
    m = math.ceil(math.sqrt(p))
    # Generate values of xg for 0 to m-1 and write to fname
    file = open(fname, 'w')
    for xg in range(m):
        power = m * xg
        value = primes.square_multiply(alpha, power, p)
        file.write(str(value) + "\n")
    file.close()

def baby_giant(alpha,beta,p):
    baby_fname = "baby.txt"
    giant_fname = "giant.txt"
    # Calculate m = sqrt(size of group) = sqrt(p)
    m = math.ceil(math.sqrt(p))
    # Execute baby step and write list to first file
    baby_step(alpha, beta, p, baby_fname)
    # Execute giant step and write list to second file
    giant_step(alpha, p, giant_fname)
    # Check the lists and see if there is a match
    baby_file = open(baby_fname, 'r')
    baby_values = baby_file.read().split('\n')[:-1]
    giant_file = open(giant_fname, 'r')
    giant_values = giant_file.read().split('\n')[:-1]
    xb = m - 1
    xg = m - 1
    for i in range(m):
        for j in range(m):
            if baby_values[i] == giant_values[j]:
                xb = i
                xg = j
                break
    x = xg*m - xb
    return x

if __name__=="__main__":
    """
    test 1
    My private key is:  264
    Test other private key is:  7265
    
    """
    p=17851
    alpha=17511
    A=2945
    B=11844
    sharedkey=1671
    a=baby_giant(alpha,A,p)
    b=baby_giant(alpha,B,p)
    guesskey1=primes.square_multiply(A,b,p)
    guesskey2=primes.square_multiply(B,a,p)
    print('a = {}, b = {}'.format(a,b))
    print('Guess key 1:',guesskey1)
    print('Guess key 2:',guesskey2)
    print('Actual shared key :',sharedkey)
    print("\n")
    
    
    # Section 6
    n = 16
    print("Section 6: Generating {}-bit shared key".format(n))
    p, alpha = dhke.dhke_setup(n)
    a = dhke.gen_priv_key(p)
    b = dhke.gen_priv_key(p)
    A = dhke.get_pub_key(alpha, a, p)
    B = dhke.get_pub_key(alpha, b, p)
    sharedKeyA = dhke.get_shared_key(B, a, p)
    sharedKeyB = dhke.get_shared_key(A, b, p)
    print("Shared key generated =", sharedKeyA)
    print("Confirm shared key generated =", sharedKeyB)
    print("\n")
    
    print("Calculating shared key (with public key A) using baby giant...")
    start1 = time.time()
    guess_a = baby_giant(alpha, A, p)
    guesskey1 = primes.square_multiply(B, a, p)
    end1 = time.time()
    print('Guess key 1:',guesskey1)
    print('Time taken: {}'.format(end1-start1))
    print("\n")
    
    print("Calculating shared key (with public key B) using baby giant...")
    start2 = time.time()
    guess_a = baby_giant(alpha, A, p)
    guesskey2 = primes.square_multiply(A, b, p)
    end2 = time.time()
    print('Guess key 2:',guesskey2)
    print('Time taken: {}s'.format(end2-start2))
