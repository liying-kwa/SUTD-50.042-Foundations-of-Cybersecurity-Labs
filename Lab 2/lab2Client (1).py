#!/usr/bin/python3
# -*- coding: utf-8 -*-
# DA+Nils 2018
# Andrei + Z.TANG + Bowen + Saket, 2020

"""
Lab2: Breaking Ciphers

Pwntool client for python3

Install: see install.sh

Documentation: https://python3-pwntools.readthedocs.io/en/latest/
"""


from pwn import remote

# pass two bytestrings to this function
def XOR(a, b):
    r = b''
    for x, y in zip(a, b):
        r += (x ^ y).to_bytes(1, 'big')
    return r


def sol1():
    conn.send("1")  # select challenge 1
    challenge = conn.recv()
    print("Question 1:\n")
    print(challenge)
    # decrypt the challenge here
    solution = answerone
    conn.send(solution)
    message = conn.recv()
    if b'Congratulations' in message:
        print(message)


def sol2():
    conn.send("2")  # select challenge 2
    challenge = conn.recv()
    print("\nQuestion 2:\n")
    challenge = challenge.decode("UTF-8")
    print(challenge)
    challenge = bytearray.fromhex(challenge)

    # some all zero mask.
    # TODO: find the magic mask!
    
    message = XOR(challenge, mask)
    conn.send(message)
    message = conn.recv()
    if b'points' in message:
        print(message)


if __name__ == "__main__":

    # NOTE: UPPERCASE names for constants is a (nice) Python convention
    URL = "35.198.199.82"
    PORT = 4455

    conn = remote(URL, PORT)
    receive1 = conn.recv()
    print(receive1.decode("UTF-8"))

    sol1()
    sol2()
    conn.close()
