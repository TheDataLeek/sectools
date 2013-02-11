#!/usr/bin/env python

""" See www.will-farmer.com/projects for more info on RSA
    arguments
        -h prints arguments
        -o decides operation: encrypt or decrypt
        -e is the encryption exponent (encryption and decryption)
        -p is the first prime (decryption only)
        -q is the second prime (decryption only)
        -n is the product of p and q, used for the mod of the algorithm (encryption and decryption)
        -d is the decryption exponent (decryption only)
        -f is the file name of the read/write file (encryption and decryption)
    This program, when supplied with a message (any characters, any number of them), will return a n-bit RSA encrypted message
    The program needs specific variables:
        (encryption exponent) e can be any number
        (first prime)         p must be prime
        (second prime)        q must be prime
        (product of p and q)  n
        the file name must have an extension and it must be a .txt file
    RSA works through prime numbers. As stated above, the user needs a variety of giant primes for this to be absolutely secure.
    The basic formula for encryption is: Ciphertext=Message**Encryption_Exponent or C=M**E (mod N)
    The basic formula for decryption is: Message=Ciphertext**Decryption_Exponent or M=C**D (mod N)
    The Decryption Exponent is the hardest one to calculate:
        Encryption_Exponent*Decryption_Exponent = (First_Prime-1)*(Second_Prime-1) (Mod (First_Prime*Second_Prime))
    To be secure, a key length of around 500 digits is very safe (for now)
    Example:
        p = 11
        q = 17
        e = 23
        n = 187
        d = 3680
        m = 97 (a)
        c = 97**23 (Mod N) = 58
        m = 58**3680 (Mod N) =
    the most common values for e are 3 and 17. 3 is a little less secure for encrpytion, so use 17 when possible
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
    opts = get_input()
    if opts.operation == 'encrypt':
        encrypt(opts.pq_product, opts.enc_exp, opts.filename)

    elif opts.operation == 'decrypt':
        decrypt(opts.dec_exp, opts.pq_product, opts.filename)


def encrypt(pq_product, enc_exp, filename):

    if filename != None:

        file_path = filename
        file_open = open(file_path, mode='r')
        m         = file_open.read()  # Sets m as the file
        message   = encrypt_string(m, enc_exp, pq_product)
        file_open = open(file_path + '.enc', mode='w')  # Appends .enc to indicate encrypted file
        file_open.write(message)
        file_open.close()

    else:
        m       = raw_input('Enter Message: ')
        message = encrypt_string(m, enc_exp, pq_product)
        print message


def encrypt_string(m, e, n):

    block_size = len(str(n)) - 1      # Block size is wholly dependent on n, block size =
    print 'BLOCK_SIZE =', block_size  # the length of n minus one

    num_list = []
    for byte in m:
        num_value = (ord(byte))
        num_value_zeroed = '%03d' % (num_value)  # zero-pad it to 3 digits
        num_list.append(str(num_value_zeroed))   # zero-padding ensures all ASCII characters are correctly interpreted
    num_final = ''.join(num_list)

    start    = 0
    end      = block_size
    end_list = []
    while start < len(num_final):                   # parses through the entire message based on block size
        byte = num_final[start:end]
        end_list.append(str((int(byte) ** e) % n))  # this is the actual formula C = M ** E
        start += block_size
        end   += block_size
    message = ' '.join((end_list))
    return message


def dcalc(p, q, e):
    d   = 0
    phi = (p - 1) * (q - 1)
    while (d * e) % phi != 1:  # just cycles through every number until it findes the right one
        d += 1
    return d


def decrypt(dec_exp, pq_product, filename):

    if filename != None:
        file_path  = filename
        file_open  = open(file_path, mode='r')
        m          = file_open.read()

        message    = decrypt_message(m, dec_exp, pq_product)

        file_open.close()
        new_file   = file_path[0:-8] + '.txt'
        file_write = open(new_file, mode='w')
        file_write.write(message)
        file_write.close()

    else:
        m       = raw_input('Enter Message to be Decrypted: ')
        message = decrypt_message(m, dec_exp, pq_product)
        print message


def decrypt_message(m, d, n):
    block_size = len(str(n)) - 1
    print 'BLOCK_SIZE =', block_size

    m_list = m.split(' ')  # split() takes the string
                           # seperates it into a list according to the delimiter ' '
    m_conv = []
    for item in m_list:
        m_conv.append(str((int(item) ** d) % n))  # here is the actual formula M = C ** D
    end_list = []
    for item in m_conv:
        end_list.append(chr(int(item)))
    message = ''.join(end_list)
    return message


def get_input():
    global opts
    global args
    parser = optparse.OptionParser(usage = 'UsageL %prog <options>', version = 'Version 1.0')
    parser.add_option('-o', '--operation'    , action = 'store', type = 'string', default = None, help = 'Encrypt or decrypt the message')
    parser.add_option('-e', '--enc_exp'      , action = 'store', type = 'int'   , default = None,
                                               help   = 'This is the encryption exponent, is also used for calculating d')
    parser.add_option('-p', '--first_prime'  , action = 'store', type = 'int'   , default = None, help = 'This is the first random prime')
    parser.add_option('-q', '--second_prime' , action = 'store', type = 'int'   , default = None, help = 'This is the second random prime')
    parser.add_option('-n', '--pq_product'   , action = 'store', type = 'int'   , default = None, help = 'This is the product of p and q')
    parser.add_option('-d', '--dec_exp'      , action = 'store', type = 'int'   , default = None,
                                               help   = "This is the decryption exponent, the program will supply it if you don't have one")
    parser.add_option('-f', '--filename'     , action = 'store', type = 'string', default = None, help = 'This is the name of the read/write file')
    opts, args = parser.parse_args()

    if opts.operation == None:
        opts.operation = raw_input('(E)ncrypt or (D)ecrypt? ')
    if opts.operation.lower() in ['encrypt', 'e']:
        opts.operation        = 'encrypt'
        if opts.enc_exp       == None:
            opts.enc_exp      = int(raw_input('Enter Encryption Exponent: '))
        if opts.pq_product    == None:
            opts.pq_product   = int(raw_input('Enter N, the Product of P and Q: '))
    elif opts.operation.lower() in ['decrypt', 'd']:
        opts.operation        = 'decrypt'
        if opts.first_prime   == None:
            opts.first_prime  = int(raw_input('Enter First Prime: '))
        if opts.second_prime  == None:
            opts.second_prime = int(raw_input('Enter Second Prime: '))
        if opts.enc_exp   == None:
            opts.enc_exp  = int(raw_input('Enter Encryption Exponent: '))
        opts.pq_product   = opts.first_prime * opts.second_prime
        if opts.dec_exp       == None:
            opts.dec_exp      = dcalc(opts.first_prime, opts.second_prime, opts.enc_exp)
    else:
        parser.print_help()   # invalid operation
        sys.exit(1)
    print opts
    return opts


if __name__ == "__main__":
    sys.exit(main())
