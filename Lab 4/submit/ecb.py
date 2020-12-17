#!/usr/bin/env python3

# 50.042 FCS Lab 4: Block Cipher
# Section 4: Implementing ECB Mode
# Student: Kwa Li Ying (1003833)

from present import *
import argparse
import sys

nokeybits=80
blocksize=64


def ecb(infile,outfile,key,mode):
    readfile = open(infile, 'rb')
    writefile = open(outfile, 'wb')
    while True:
    	
    	# Read 8 byte chunks of the input file and convert to 64 bit blocks
        chunk = readfile.read(blocksize//8)
        if not chunk:
            break
        block = int.from_bytes(chunk, "big")
        
        # Do encryption/decryption
        if mode == 'e' or mode == 'E':
            block = present(block, key)
        
        else:
            block = present_inv(block, key)
        
        # Write to outfile
        chunk = block.to_bytes(blocksize//8, byteorder="big")
        writefile.write(chunk)
    
    writefile.close()

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile',help='input file')
    parser.add_argument('-o', dest='outfile',help='output file')
    parser.add_argument('-k', dest='keyfile',help='key file')
    parser.add_argument('-m', dest='mode',help='mode')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    keyfile=args.keyfile
    mode=args.mode
    
    # Check for valid arguments
    if infile == None:
        sys.exit("Error: Please specify an input file.")
    if outfile == None:
        sys.exit("Error: Please specify an output file.")
    if mode == None:
        sys.exit("Error: Please specify mode.")
    valid_modes = ['e', 'E', 'd', 'D']
    if mode not in valid_modes:
        sys.exit("Error: Invalid cipher mode. Mode must be e/d/E/D")
    if keyfile == None:
        sys.exit("Error: Please specify a file that contains the key written in hex.")
        
    # Parse key, has to be written in hex and 80bit
    file = open(keyfile, 'r')
    key_string = file.read()
    key_string = key_string[:-1]
    try:
        key = int(key_string, 16)
        if not 0 <= key <= 0xFFFFFFFFFFFFFFFFFFFF:
            sys.exit("Error: Key must be between 0x00000000000000000000 and 0xFFFFFFFFFFFFFFFFFFFF.")
    except ValueError:
        sys.exit("Error: Key must be a number.")
    
    # Carry out encryption/decryption
    ecb(infile, outfile, key, mode)



