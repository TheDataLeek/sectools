#!/usr/bin/env python

""" Arguments:
        -h = Display help and quit
        -o = Encrypt or Decrypt
        -s = Shift of how many spaces
        -f = File for encryption
    The Caesar cipher is one of the most widely known ciphers.
    It relies on a seperate cipher alphabet for encryption/decryption.
    Example of Caesar Cipher with a shift of 7:
        a b c d e f g h i j k l m n o p q r s t u v w x y z
        h i j k l m n o p q r s t u v w x y z a b c d e f g
    According to the above alphabet, a would become h, b to i, etc.
    This cipher is as weak as the XOR cipher, if not weaker due to popularity
"""

import sys
import optparse

print '''**********************************************
Copyright (c) 2010, William Zebulon Farmer
All rights reserved.
Licensed with the BSD License.
**********************************************
      '''


def main():
    opts = get_args()
    message = get_message(opts.filename)
    if opts.operation == 'encrypt':
        final_message = shift_message(opts.filename, message, opts.shift)
    elif opts.operation == 'decrypt':
        final_message = d_shift_message(opts.filename, message, opts.shift)
    if opts.filename == None:
        print final_message


def get_message(filename):
    ''' Gets input from user and enables/disables file operations
    '''
    if filename != None:
        read_path = filename
        open_file = open(read_path, mode='r')
        message   = open_file.read()
        open_file.close()
    else:
        message   = raw_input('Enter Message: ')
    return message


def shift_message(filename, message, shift):
    ''' Uses ASCII codes to identify letter and shift it however many it was shifted
        Depending on whether or not file operations were enabled, it will also write the file
        file_det: whether to write files (value = 'y' or 'n')
        read_file: name of unqualified input file
        message: data to encrypt
        shift:   how many places to shift
    '''
    final_message = message_shift(message, shift)
    if filename != None:
        file_open = open(filename + '.enc', mode='w')
        file_open.write(final_message)
        file_open.close()
    return final_message


def d_shift_message(filename, message, shift):
    ''' Same thing as encryption, just reversed
    '''
    final_message = message_shift(message, -shift)
    if filename != None:
        file_open = open(filename[0:-4], mode='w')
        file_open.write(final_message)
        file_open.close()
    return final_message


def message_shift(message, shift):
    end_list   = []
    final_list = []
    for byte in message:
        number = (ord(byte) + shift) % 128
        end_list.append(number)
    for item in end_list:
        final_list.append(chr(item))
    final = ''.join(final_list)
    return final


def get_args():
    global opts
    global args
    parser = optparse.OptionParser(usage = 'UsageL %prog <options>', version = 'Version 1.0')
    parser.add_option('-o', '--operation'    , action = 'store', type = 'string', default = None, help = 'Encrypt or decrypt the message')
    parser.add_option('-s', '--shift'        , action = 'store', type = 'int'   , default = None, help = 'How far to shift the message')
    parser.add_option('-f', '--filename'     , action = 'store', type = 'string', default = None, help = 'This is the name of the read/write file')
    opts, args = parser.parse_args()

    if opts.operation == None:
        opts.operation = raw_input('(E)ncrypt or (D)ecrypt: ')
    if opts.operation.lower() in ['encrypt', 'e']:
        opts.operation = 'encrypt'
    elif opts.operation.lower() in ['decrypt', 'd']:
        opts.operation = 'decrypt'
    else:
        parser.print_help()   # invalid operation
        sys.exit(1)
    if opts.shift == None:
        opts.shift = int(raw_input('Enter Shift: '))
    return opts

if __name__ == "__main__":
    sys.exit(main())
