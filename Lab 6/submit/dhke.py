#!/usr/bin/env python3

# 50.042 FCS Lab 6 Diffie-Hellman Key Exchange
# Year 2020
# Student: Kwa Li Ying (1003833)

import primes
import random

def dhke_setup(nb):
    p = primes.gen_prime_nbits(nb)
    #p = 1208925819614629174706189
    alpha = random.randint(2, p-2)
    return p, alpha

def gen_priv_key(p):
    priv_key = random.randint(2, p-2)
    return priv_key

def get_pub_key(alpha, a, p):
    pub_key = primes.square_multiply(alpha, a, p)
    return pub_key

def get_shared_key(keypub, keypriv, p):
    shared_key = primes.square_multiply(keypub, keypriv, p)
    return shared_key
    
if __name__=="__main__":
    
    p, alpha = dhke_setup(80)
    print('Generate P and alpha:')
    print('P:', p)
    print('alpha:',alpha)
    print()
    a=gen_priv_key(p)
    b=gen_priv_key(p)
    print('My private key is: ', a)
    print('Test other private key is: ', b)
    print()
    A=get_pub_key(alpha,a,p)
    B=get_pub_key(alpha,b,p)
    print('My public key is: ',A)
    print('Test other public key is: ',B)
    print()
    sharedKeyA=get_shared_key(B,a,p)
    sharedKeyB=get_shared_key(A,b,p)
    print('My shared key is: ',sharedKeyA)
    print('Test other shared key is: ',sharedKeyB)
    print('Length of key is %d bits.'%sharedKeyA.bit_length())
    

