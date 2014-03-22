#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-19
#
# AES (american encryption standard)
# 128-bit block size
# key lengths of 128 bit, 192 bit or 256 bit

import sys

### utils ###
def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def DEBUG_print_box(box, name):
    print "DEBUG - print %s:"%name
    for row in range(16):
        for col in range(16):
            print "%#x " % box[row][col],
        print ""
    print "/DEBUG"




class AES:
    def __init__(self, inputkey):
        ## blocksize
        self._blocksize = 128

        ## key schedule
        if inputkey > 0xffffffffffffffffffffffffffffffffffffffffffffffff:
            ## 256 bit - bigger than 192 bit
            self._rounds = 14

        elif inputkey <= 0xffffffffffffffffffffffffffffffff:
            ## 128 bit - smaller or equal than 128 bit
            self._rounds = 10
        else:
            ## 192 bit - bigger than 128 bit and smaller than 256 bit
            self._rounds = 12

        ## TODO
        self._inputkey = inputkey  
#        self._init_keys(inputkey)

        ## S-box
        self._sbox = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
                      [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
                      [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
                      [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
                      [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
                      [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
                      [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
                      [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
                      [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
                      [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
                      [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
                      [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
                      [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
                      [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
                      [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
                      [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]

#        DEBUG_print_box(self._sbox, "sbox")  
        self._sbox_inv = self._invert_sbox(self._sbox)
#        DEBUG_print_box(self._sbox_inv, "sbox_inv")  

        ## diffusion layer
        self._shift_rows = [0,5,10,15,4,9,14,3,8,13,2,7,12,1,6,11]
        self._shift_rows_inv = [self._shift_rows.index(idx) for idx in range(len(self._shift_rows))]

        self._mix_columns__const_matrix = [[2,3,1,1],
                                           [1,2,3,1],
                                           [1,1,2,3],
                                           [3,1,1,2]]
        # TODO invert _mix_columns__const_matrix  

    ## utilities
    def _invert_sbox(self, box):
        box_inv = []
        for val in range(len(box)*len(box[0])):
            row = 0
            col = 0
            for row in range(len(box)):
                try:
                    col = box[row].index(val)
                    break
                except ValueError:
                    next
            ## invert row, col and value
            val_inv = row
            val_inv = (val_inv<<4)|col
            row_inv = val&0xf
            col_inv = (val<<4)&0xf
            if 0 == col_inv: box_inv.append([])
            box_inv[row_inv].append(val_inv)
        return box_inv

    def _hexlst_getnth(self, hexlst, nth):
        ## return the nth 8-bit number, contained in the hex list (a number)
        ## where nth is an index, starting with 0
        return ((hexlst >> (self._blocksize - (nth+1)*8)) & 0xff)

    def _hexlst_append(self, hexlst, val):
        ## appends an 8-bit hex val to a hex list (a number) of such values
        ## and returns it
        return ((hexlst << 8)|val)

    def _sbox_get(self, idx):
        ## splits an 8-bit hex into two 4-bit, the col and row sbox index
        col = (idx & 0xf)
        row = (idx >> 4) & 0xf
        return self._sbox[row][col]

# TODO apply key schedule, and NOT just _inputkey
    def _add_round_key(self, state):
        ## add a round key
        # TODO
        return self._inputkey ^ state   

    def _substitution_layer__sub_bytes(self, state):
        ## substitution per 8-bit values
        hexlst = 0x0
        for idx in range(self._blocksize/8):
            hexlst = self._hexlst_append(hexlst, self._sbox_get(self._hexlst_getnth(state, idx)))
        return hexlst


    def _diffusion_layer__shift_rows(self, state):
        # TODO put into matrix, shift rows according to AES shift_rows
        # TODO finde elegant solution...
        
        return state

    def _diffusion_layer__mix_column(self, state):
        ## major diffusion element
        
        return state

    def encrypt(self, plaintext):
        
        plaintext = "abc"    
        
        ## init
#        blocklen = len(plaintext) # TODO rm  
        state = int(plaintext.encode('hex'),16) & 0xffffffffffffffffffffffffffffffff

        ## add round key
#        state = self._add_round_key(state)        
        
        for rnd in range(self._rounds):
            print "rnd %d"%rnd   

            state = self._substitution_layer__sub_bytes(state)
            print "%#x"%state   

#            state = self._diffusion_layer__shift_rows(state) 

#            state = self._diffusion_layer__mix_column() 

#            state = self._add_round_key(state)
        die("STOP")
        

    def decrypt(self, ciphertext):
        pass


### main ###
def main():
    blocksize = 128

    ## init some raw input key
    inputkey = 0xffffffffffffffff
    print "initial key:"
    print "%#x\n" % inputkey

    ## init the algorithm
    aes = AES(inputkey)

    ## init some input text
    plaintext = "jack and jill went up the hill to fetch a pail of water"
    print "plaintext:"
    print "%s\n" % plaintext

    ciphertext = []
    blocktext = ""
    for idx in range(len(plaintext)-1):
        blocktext += plaintext[idx]
        if idx % (blocksize/8) == 0:
            ciphertext.append(aes.encrypt(blocktext))
            blocktext = ""
    blocktext += plaintext[idx+1]
    ciphertext.append(aes.encrypt(blocktext))

    ## print result
    print "encrypted:"
    for item in ciphertext:
        print "%#x"%item,
    print "\n"

    ## decrypt
    decryptedtext = ""
    for block in ciphertext:
        decryptedtext += aes.decrypt(block)

    ## print result
    print "decrypted:"
    print "%s\n" % decryptedtext

### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
