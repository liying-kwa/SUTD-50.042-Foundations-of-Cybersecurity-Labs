#!/usr/bin/env python3


# 50.042 FCS Lab 7 RSA
# Year 2020
# Student: Kwa Li Ying (1003833)
# Part I and II


import math
import random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

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

def encrypt_message(m, e, n):
    c = square_multiply(m, e, n)
    return c
    
def decrypt_message(c, d, n):
    m = square_multiply(c, d, n)
    return m


if __name__=="__main__":

    # PART I: RSA Without Padding
    print("Part I--------------\n")

    # Encrypt message.txt
    pub_key = open('mykey.pem.pub','r').read()
    rsa_pub_key = RSA.importKey(pub_key)
    plaintext = open('message.txt', 'r').read()
    ciphertext = []
    for char in plaintext:
        m = ord(char)
        c = encrypt_message(m, rsa_pub_key.e, rsa_pub_key.n)
        ciphertext.append(c)

    # Decrypt ciphertext to message.txt
    priv_key = open('mykey.pem.priv','r').read()
    rsa_priv_key = RSA.importKey(priv_key)
    message = ""
    for c in ciphertext:
        m = decrypt_message(c, rsa_priv_key.d, rsa_priv_key.n)
        message += chr(m)
    print("ORIGINAL MESSAGE:", plaintext)
    print("DECRYPTED MESSAGE:", message)
    
    # Create signature by exponentiating the digest
    h = SHA256.new()
    h.update(plaintext.encode())
    hash_val = h.hexdigest()
    signature = []
    for char in hash_val:
        x = ord(char)
        s = decrypt_message(x, rsa_priv_key.d, rsa_pub_key.n)
        signature.append(s)
    
    # Verify the signature
    verification = ""
    for s in signature:
        x = encrypt_message(s, rsa_pub_key.e, rsa_pub_key.n)
        verification += chr(x)
    print("ORIGINAL HASH:", hash_val)
    print("VERIFICATION:", verification)
    
    print("\n\n")
    
    
    # PART II: Protocol Attack
    print("Part II-------------\n")
    
    # RSA Encryption Protocol Attack
    m = 100
    print("Encrypting:", m, "\n")
    c = encrypt_message(m, rsa_pub_key.e, rsa_pub_key.n)
    print("Result:")
    length = math.ceil(math.log(c, 2) / 8)
    print(c.to_bytes(length, 'big'), "\n")
    s = 2
    ys = encrypt_message(s, rsa_pub_key.e, rsa_pub_key.n)
    c_prime = square_multiply(c*ys, 1, rsa_pub_key.n)
    print("Modified to:")
    length2 = math.ceil(math.log(c_prime, 2) / 8)
    print(c_prime.to_bytes(length2, 'big'), "\n")
    m_prime = decrypt_message(c_prime, rsa_priv_key.d, rsa_priv_key.n)
    print("Decrypted:", m_prime, "\n")
    
    # RSA Decryption Signature Protocol Attack
    # Generate random message s
    s = random.getrandbits(2048)
    print("s =", str(s) + "\n")
    x = encrypt_message(s, rsa_pub_key.e, rsa_pub_key.n)
    print("x =", str(x) + "\n")
    print("Sending s and x over...\n")
    x_prime = encrypt_message(s, rsa_pub_key.e, rsa_pub_key.n)
    print("Verification x' =", str(x_prime), "\n")
    
    print("\n")

    
    
    
    
    
    
