#!/usr/bin/env python3

# 50.042 FCS Lab 4: Block Cipher
# Section 4: Limitation of ECB Mode
# Student: Kwa Li Ying (1003833)

import argparse
import sys
import operator

def getInfo(headerfile):
    file = open(headerfile, mode='rb')
    info = file.read()
    return info

def extract(infile,outfile,headerfile):
    
    # Skip to after header in ciphertext (+1 for LineFeed)
    headerinfo = getInfo(headerfile)
    readfile = open(infile, mode = 'rb')
    readfile.read(len(headerinfo) + 1)
    
    # Read each character (byte) and check for the most frequent byte
    occurences = {}
    while True:
        char = readfile.read(8)
        if not char:
            break
        if char in occurences:
            occurences[char] += 1
        else:
            occurences[char] = 1
    most_frequent = max(occurences.items(), key=operator.itemgetter(1))[0]
    
    # Take the most frequent byte to be white, and the rest to be black
    writefile = open(outfile, 'w')
    writefile.write((headerinfo.decode('utf-8') + "\n"))
    readfile2 = open(infile, 'rb')
    readfile2.read(len(headerinfo) + 1)
    while True:
        char = readfile2.read(8)
        if not char:
            break
        if char == most_frequent:
            writefile.write('00000000')
        else:
            writefile.write('11111111')
    
    writefile.close()

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile',help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile',help='output PBM file')
    parser.add_argument('-hh', dest='headerfile',help='known header file')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    headerfile=args.headerfile
    
    # Check for valid arguments
    if infile == None:
        sys.exit("Error: Please specify an input file.")
    if outfile == None:
        sys.exit("Error: Please specify an output file.")
    if headerfile == None:
        sys.exit("Error: Please specify a header file.")

    print('Reading from: %s'%infile)
    print('Reading header file from: %s'%headerfile)
    print('Writing to: %s'%outfile)
    
    success=extract(infile, outfile, headerfile)

            
