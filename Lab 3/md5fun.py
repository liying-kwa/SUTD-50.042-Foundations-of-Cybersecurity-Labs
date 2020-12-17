#!/usr/bin/python3

# 50.042 FCS Lab 3: MD5 and Rainbow Tables
# Student: Kwa Li Ying (1003833)

# Time taken to bruteforce hash5.txt: 514.59124021s
# Time taken to rcrack hash5.txt: 16.234s
# Time taken to rcrack salted6.txt: 15.028s

import hashlib
import itertools
import random
import timeit

# MD5 Hash Function
def md5hash(m):
	hash = hashlib.md5(m.encode('utf-8')).hexdigest()
	return hash

# Brute force to crack hashes in hash5.txt
alphabets = "abcdefghijklmnopqrstuvwxyz0123456789"
file = open('hash5.txt', 'r')
filelines = file.readlines()

start = timeit.default_timer()

passwords = []
for line in filelines:
	hash = line[0:-1]
	# Brute force from last letter to first letter: aaaaa, aaaab, ..., aaaba, ...
	for broken_guess in itertools.product(alphabets, repeat=5):
		guess = ''.join(broken_guess)
		if md5hash(guess) == hash:
			passwords.append(guess)
			print(guess)
			break

stop = timeit.default_timer()
print('Brute force duration: ', stop - start)

# Section 5: Salting
file2 = open('salted6.txt', 'w')
for password in passwords:
	salted_password = password + chr(random.randint(ord('a'), ord('z')+1))
	salted_hash = md5hash(salted_password)
	file2.write(salted_hash + "\n")
file2.close()
