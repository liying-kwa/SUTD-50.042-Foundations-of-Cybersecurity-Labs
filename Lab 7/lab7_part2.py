#!/usr/bin/env python3


# 50.042 FCS Lab 7 RSA
# Year 2020
# Student: Kwa Li Ying (1003833)
# Part III


import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_PSS


def generate_RSA(bits=1024):
    key = RSA.generate(bits)
    priv_key = key.exportKey("PEM")
    pub_key = key.publickey().exportKey("PEM")
    return priv_key, pub_key
    
def encrypt_RSA(public_key_file, message):
    pub_key = open(public_key_file,'r').read()
    rsa_pub_key = RSA.importKey(pub_key)
    oaep = PKCS1_OAEP.new(rsa_pub_key)
    ciphertext = oaep.encrypt(message.encode())
    return ciphertext
    
def decrypt_RSA(private_key_file, cipher):
    priv_key = open(private_key_file,'r').read()
    rsa_priv_key = RSA.importKey(priv_key)
    oaep = PKCS1_OAEP.new(rsa_priv_key)
    message = oaep.decrypt(cipher)
    return message
    
def sign_data(private_key_file, data):
    priv_key = open(private_key_file,'r').read()
    rsa_priv_key = RSA.importKey(priv_key)
    h = SHA256.new()
    h.update(data.encode())
    signer = PKCS1_PSS.new(rsa_priv_key)
    signature = signer.sign(h)
    # Return signature in base 64 string
    return base64.encodebytes(signature)
    
def verify_sign(public_key_file, sign, data):
    pub_key = open(public_key_file,'r').read()
    rsa_pub_key = RSA.importKey(pub_key)
    h = SHA256.new()
    h.update(data.encode())
    verifier = PKCS1_PSS.new(rsa_pub_key)
    try:
        verifier.verify(h, sign)
        return True
    except (ValueError, TypeError):
        return False
    return False
    
    
if __name__=="__main__":

    # PART III: Implementing RSA with Padding
    print("Part III------------\n")
    
    # Generate keys
    print("Generating RSA key-pair and storing in private.pem and public.pem\n")
    priv_key, pub_key = generate_RSA(1024)
    with open("private.pem", 'wb') as priv_key_file:
        priv_key_file.write(priv_key)
    with open("public.pem", 'wb') as pub_key_file:
        pub_key_file.write(pub_key)
    
    # Encrypt using public key
    print("Friend encrypts message.txt using public.pem")
    public_key_file = "public.pem"
    plaintext = open("message.txt", 'r').read()
    ciphertext = encrypt_RSA(public_key_file, plaintext)
    print("MESSAGE:", plaintext)
    print("CIPHERTEXT:", ciphertext)
    print("\n")
    
    # Decrypt using private key
    print("I decrypt ciphertext using private.pem")
    private_key_file = "private.pem"
    message = decrypt_RSA(private_key_file, ciphertext)
    print("DECRYPTED MESSAGE:", message)
    print("\n")
    
    # Sign data using private key
    print("I sign message.txt using private.pem")
    data = open("message.txt", 'r').read()
    signature = sign_data(private_key_file, data)
    print("SIGNATURE:", signature)
    print("\n")
    
    # Verify digital signature
    print("My friend is verifying that the signature sent matches the data signed again")
    verified = verify_sign(public_key_file, signature, data)
    print("VERIFIED:", verified)
    print("\n")
    
    
    
