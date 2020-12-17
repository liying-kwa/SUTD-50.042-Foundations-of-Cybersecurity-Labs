#!/usr/bin/env python3

# 50.042 FCS Lab 6 Diffie-Hellman Key Exchange
# Year 2020
# Student: Kwa Li Ying (1003833)

import random
def square_multiply(a,x,n):
    y = 1
    x_bits = []
    # Convert x to binary in list format, starting with MSB
    x_bits = bin(x)[2:]
    for i in x_bits:
        y = (y * y) % n
        if int(i) == 1:
            y = (y * a) % n
    return y

def miller_rabin(n, k):
    # Base cases where n < 3
    if n < 6:
        if n == 2 or n == 3 or n == 5: return True
        else: return False
    # Express n in the form of (2^r)*d
    temp = n - 1
    r = 0
    while temp % 2 == 0:
        r += 1
        temp = temp // 2
    d = temp
    # WitnessLoop: Calculate b0, b1, ...
    for i in range(k):
        # Pick a random integer 'a' from 2 to n-2 inclusive
        a = random.randint(2, n-2)
        x = square_multiply(a, d, n)
        # For the first calculation of a^d mod p, +-1 is probably prime
        if x == 1 or x == n-1:
            continue
        # For subsequent calculations of a^d mod p, -1 is probably prime
        continue_WitnessLoop = False
        for j in range(r-1):
            x = square_multiply(x, 2, n)
            if x == n-1:
                continue_WitnessLoop = True
                break
        if continue_WitnessLoop == True:
            continue
        return False
    return True

def gen_prime_nbits(n):
    is_prime = False
    while is_prime == False:
        number = random.randint(2, (2**n)-1 )
        is_prime = miller_rabin(number, 2)
    return number

if __name__=="__main__":
    print('Is 561 a prime?')
    print(miller_rabin(561,2))
    print('Is 27 a prime?')
    print(miller_rabin(27,2))
    print('Is 61 a prime?')
    print(miller_rabin(61,2))

    print('Random number (100 bits):')
    print(gen_prime_nbits(100))
    print('Random number (80 bits):')
    print(gen_prime_nbits(80))
    
    print('Calculate is 3^5 mod 11 using Square and Multiply method:')
    print(square_multiply(3, 5, 11))
