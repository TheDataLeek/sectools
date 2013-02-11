#!/usr/bin/env python

""" Arguments:
        -h = Display help and exit
        -m = Message for encryption
        -k = Key for encryption
        -o = Operation (encrypt or decrypt)
        -f = File for encryption
    XOR means eXclusive OR, hence the acronym XOR
    XOR works by converting the bytes to binary, stacking them on top of the key and following
     the procedure 1+1=0, 0+0=0, 1+0=1, for example:
        110101100101  take the last column, 1 up here
        010100010110  0 down here
        ------------
        100001110011  you get 1 as a result
    This procedure is used for every byte which results in low-level encryption but secure enough for trivial communication
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
    if opts.filename != None and opts.operation == encrypt:
        encrypted_string = encrypt(opts.message, opts.key, opts.operation, opts.filename)
    elif opts.filename != None and opts.operation == decrypt:
        encrypted_string = decrypt(opts.message, opts.key, opts.operation, opts.filename)
    else:
        encrypted_string = xor_function(opts.message, opts.key, opts.operation)
    print encrypted_string


def encrypt(message, key, operation, filename):
    file_open        = open(filename, mode = 'r')
    opts.message     = file_open.read()
    file_open.close()
    encrypted_string = xor_function(message, key, operation)
    file_open        = open(filename + '.enc', mode = 'w')
    file_open.write(encrypted_string)
    file_open.close()
    return encrypted_string


def decrypt(message, key, operation, filename):
    file_open        = open(filename, mode = 'r')
    opts.message     = file_open.read()
    file_open.close()
    encrypted_string = xor_function(message, key, operation)
    file_open        = open(filename[0:-8] + '.txt', mode = 'w')
    file_open.write(encrypted_string)
    file_open.close()
    return encrypted_string


def xor_function(string, key, operation):
    str_list = []
    key_list = []
    if operation == 'encrypt':
        for byte in string:
            str_list.append(ord(byte))
    if operation == 'decrypt':
        m_list = string.split(' ')
        for item in m_list:
            str_list.append(int(item))
    for byte in key:
        key_list.append(ord(byte))
    xor_list = []
    digit = 0
    for item in str_list:
        xor_list.append(str(item ^ key_list[digit]))
        key_list.append(key_list[digit])
        digit += 1
    function_list = []
    if operation == 'decrypt':
        for item in xor_list:
            function_list.append(chr(int(item)))
        xored_string = ''.join(function_list)
    else:
        function_list = xor_list
        xored_string = ' '.join(function_list)
    return xored_string


def get_args():
    """ This is just to allow argument handling for more experienced users,
         but manual input is also accepted
    """
    global opts
    global args
    parser = optparse.OptionParser(usage = 'UsageL %prog <options>', version = 'Version 1.0')
    parser.add_option('-o', '--operation'    , action='store', type='string', default=None, help='(E)ncrpyt or (D)ecrypt the message')
    parser.add_option('-m', '--message'      , action='store', type='string', default=None, help='The message to encrypt/decrypt')
    parser.add_option('-k', '--key'          , action='store', type='string', default=None, help='The keyword')
    parser.add_option('-f', '--filename'     , action='store', type='string', default=None, help='Name of the file')
    opts, args = parser.parse_args()

    if opts.operation == None:
        opts.operation = raw_input('(E)ncrypt or (D)ecrypt the message: ')
    if opts.operation.lower() in ['encrypt', 'e']:
        opts.operation = 'encrypt'
    elif opts.operation.lower() in ['decrypt', 'd']:
        opts.operation = 'decrypt'
    if opts.filename == None and opts.message == None:
        opts.message = raw_input('Enter message: ')
    if opts.key == None:
        opts.key = raw_input('Enter key: ')
    print opts
    return opts

if __name__ == "__main__":
    sys.exit(main())
