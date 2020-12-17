#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Part I: Shift Cipher for printable input
# Student: Kwa Li Ying (1003833)

# Import libraries
import sys
import argparse
import string

# Shift Cipher function
def shift_cipher(filein, fileout, key, mode):
    # open file handles to both files
    fin  = open(filein, mode='r', encoding='utf-8', newline='\n')
    fout = open(fileout, mode='w', encoding='utf-8', newline='\n')
    
    # encrypt plaintext
    if mode == 'e' or mode == 'E':
        # read in file into plaintext as a str
        plaintext = fin.read()
        
        # split into chars for easier shifting
        plaintext_list = list(plaintext)
        
        # carry out shifting
        ciphertext_list = []
        for p in plaintext_list:
            p_index = string.printable.find(p)
            c_index = (p_index + key) % len(string.printable)
            c = string.printable[c_index]
            ciphertext_list.append(c)
        ciphertext = "".join(ciphertext_list)
        
        # write to output file
        fout.write(ciphertext)
    
    # decrypt ciphertext
    else:
        # read in file into ciphertext as a str
        ciphertext = fin.read()
        
        # split into chars for easier shifting
        ciphertext_list = list(ciphertext)
        
        # carry out shifting
        plaintext_list = []
        for c in ciphertext_list:
            c_index = string.printable.find(c)
            p_index = (c_index - key) % len(string.printable)
            p = string.printable[p_index]
            plaintext_list.append(p)
        plaintext = "".join(plaintext_list)
        
        # write to output file
        fout.write(plaintext)
    
    # close all file streams
    fin.close()
    fout.close()
    
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
        if not 1 <= key <= len(string.printable)-1:
            sys.exit("Error: Key must be between 1 and {}.".format(len(string.printable)-1))
    except ValueError:
        sys.exit("Error: Key must be a number.")
    valid_modes = ['e', 'E', 'd', 'D']
    if mode not in valid_modes:
        sys.exit("Error: Invalid cipher mode. Mode must be e/d/E/D")

    # encrypt/decrypt and output result
    shift_cipher(filein, fileout, key, mode)

    # all done
