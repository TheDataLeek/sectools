#!/usr/bin/env python

""" Arguments:
        -h = Display help and exit
        -o = Encrypt or Decrypt
        -k = Keyword/Passphrase
        -f = File for encryption
    The vigenere cipher is very similar to the Caesar cipher but much more secure.
    This is due to the use of multiple cipher alphabets instead of just one (see Caesar cipher)
    The message is encrypted with the use of a vigenere square and a passphrase,
     the passphrase tells the individual which alphabet to use and the switch alphabets each time
    VIGENERE SQUARE:
        b c d e f g h i j k l m n o p q r s t u v w x y z a
        c d e f g h i j k l m n o p q r s t u v w x y z a b
        d e f g h i j k l m n o p q r s t u v w x y z a b c
        e f g h i j k l m n o p q r s t u v w x y z a b c d
        f g h i j k l m n o p q r s t u v w x y z a b c d e
        g h i j k l m n o p q r s t u v w x y z a b c d e f
        h i j k l m n o p q r s t u v w x y z a b c d e f g
        i j k l m n o p q r s t u v w x y z a b c d e f g h
        j k l m n o p q r s t u v w x y z a b c d e f g h i
        k l m n o p q r s t u v w x y z a b c d e f g h i j
        l m n o p q r s t u v w x y z a b c d e f g h i j k
        m n o p q r s t u v w x y z a b c d e f g h i j k l
        n o p q r s t u v w x y z a b c d e f g h i j k l m
        o p q r s t u v w x y z a b c d e f g h i j k l m n
        p q r s t u v w x y z a b c d e f g h i j k l m n o
        q r s t u v w x y z a b c d e f g h i j k l m n o p
        r s t u v w x y z a b c d e f g h i j k l m n o p q
        s t u v w x y z a b c d e f g h i j k l m n o p q r
        t u v w x y z a b c d e f g h i j k l m n o p q r s
        u v w x y z a b c d e f g h i j k l m n o p q r s t
        v w x y z a b c d e f g h i j k l m n o p q r s t u
        w x y z a b c d e f g h i j k l m n o p q r s t u v
        y z a b c d e f g h i j k l m n o p q r s t u v w x
        z a b c d e f g h i j k l m n o p q r s t u v w x y
        a b c d e f g h i j k l m n o p q r s t u v w x y z
    As you can see, this cipher is not overly complex, but will ensure security.
    If your key is as long as you message and COMPLETELY random, is is a one-time-pad
     which is unbreakable. Since there are no patterns for analysis, is is impossible to
     decrypt.
    Example, Message = hello world, key = man:
        h e l l o w o r l d
        m a n m a n m a n m
        -------------------
        s d x w n i z q x o
    The only repitition is the first 'l' of hello and the 'l' of world but that id due to
     the short key-length.
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
    opts          = get_args()
    message       = get_message(opts.filename)
    final_message = vigenere_shift(message, opts.key, opts.operation)
    if opts.operation == 'encrypt':
        encrypt_write(final_message, opts.filename)
    elif opts.operation == 'decrypt':
        decrypt_write(final_message, opts.filename)


def vigenere_shift(message, key, operation):
    key_list   = []
    letter     = 0
    ciphertext = []
    for byte in key:
        if operation == 'decrypt':
            key_list.append(-ord(byte))
        else:
            key_list.append(ord(byte))
    for byte in message:
        chr_enc = shift_message(byte, key_list[letter])
        ciphertext.append(chr_enc)
        letter += 1
        if letter  == len(key):
            letter = 0
    final_message = ''.join(ciphertext)
    return final_message


def encrypt_write(final_message, filename):
    if filename  != None:
        file_open = open(filename + '.enc', mode = 'w')
        file_open.write(final_message)
        file_open.close()
    else:
        print final_message


def decrypt_write(final_message, filename):
    if filename  != None:
        file_open = open(filename[0:-4], mode = 'w')
        file_open.write(final_message)
        file_open.close()
    else:
        print final_message


def shift_message(message, shift):
    ''' Uses ASCII codes to identify letter and shift it however many it was shifted
        Depending on whether or not file operations were enabled, it will also write the file
    '''
    end_list   = []
    end_list.append(chr((ord(message) + shift) % 128))  # mod 128 due to limits of ASCII
    final = ''.join(end_list)
    return final


def get_message(filename):
    if filename != None:
        read_file = filename
        open_file = open(read_file, mode = 'r')
        message   = open_file.read()
        open_file.close()
    else:
        message   = raw_input('Enter Message: ')
    return message


def get_args():
    global opts
    global args
    parser = optparse.OptionParser(usage = 'UsageL %prog <options>', version = 'Version 1.0')
    parser.add_option('-o', '--operation', action = 'store', type = 'string', default = None, help = 'Encrypt or decrypt the message')
    parser.add_option('-k', '--key'      , action = 'store', type = 'string', default = None, help = 'The keyword for encryption or decryption')
    parser.add_option('-f', '--filename' , action = 'store', type = 'string', default = None, help = 'This is the name of the read/write file')
    opts, args = parser.parse_args()

    if opts.operation == None:
        opts.operation = raw_input('(E)ncrypt or (D)ecrypt: ')
    if opts.operation.lower() in ['encrypt', 'e']:
        opts.operation        = 'encrypt'
    elif opts.operation.lower() in ['decrypt', 'd']:
        opts.operation        = 'decrypt'
    else:
        parser.print_help()   # invalid operation
        sys.exit(1)
    if opts.key == None:
        opts.key = raw_input('Enter Keyword: ')
    return opts


if __name__ == "__main__":
    sys.exit(main())
