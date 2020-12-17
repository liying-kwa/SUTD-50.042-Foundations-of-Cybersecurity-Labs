#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Part II: Shift Cipher for binary input
# Student: Kwa Li Ying (1003833)

# Import libraries
import sys
import argparse

# Shift Cipher function
def shift_cipher_binary(filein, fileout, key, mode):
    # open file handles to both files
    fin_b = open(filein, mode='rb')
    fout_b = open(fileout, mode='wb')
    
    # encrypt plaintext
    if mode == 'e' or mode == 'E':
        # read in file into plaintext as bytes
        plaintext = fin_b.read()
        
        # convert to bytearray for easier shifting
        plaintext_list = bytearray(plaintext)
        
        # carry out shifting
        ciphertext_list = []
        for p in plaintext_list:
            c = (p + key) % 256
            ciphertext_list.append(c)
        
        # write to output file
        ciphertext = bytearray(ciphertext_list)
        fout_b.write(ciphertext)
    
    # decrypt ciphertext
    else:
        # read in file into ciphertext as a bytes
        ciphertext = fin_b.read()
        
        # convert to bytearray for easier shifting
        ciphertext_list = bytearray(ciphertext)
        
        # carry out shifting
        plaintext_list = []
        for c in ciphertext_list:
            p = (c - key) % 256
            plaintext_list.append(p)
        
        # write to output file
        plaintext = bytearray(plaintext_list)
        fout_b.write(plaintext)
        
    # close all file streams
    fin_b.close()
    fout_b.close()

# Main function
if __name__=="__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein',help='input file')
    parser.add_argument('-o', dest='fileout', help='output file')
    parser.add_argument('-k', dest='key', help='key value')
    parser.add_argument('-m', dest='mode', help='e (encrypt) or d (decrypt)')

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = args.key
    mode = args.mode
    
    # check for valid arguments
    if filein == None:
        sys.exit("Error: Please specify an input file.")
    if fileout == None:
        sys.exit("Error: Please specify an output file.")
    try:
        key = int(key)
        if not 0 <= key <= 255:
            sys.exit("Error: Key must be between 0 and 255.")
    except ValueError:
        sys.exit("Error: Key must be a number.")
    valid_modes = ['e', 'E', 'd', 'D']
    if mode not in valid_modes:
        sys.exit("Error: Invalid cipher mode. Mode must be e/d/E/D")

    # encrypt/decrypt and output result
    shift_cipher_binary(filein, fileout, key, mode)

    # all done