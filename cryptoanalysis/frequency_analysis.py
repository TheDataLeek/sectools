#!/usr/bin/env python

import sys

freq_dict = {'a':0.0,
             'b':0.0,
             'c':0.0,
             'd':0.0,
             'e':0.0,
             'f':0.0,
             'g':0.0,
             'h':0.0,
             'i':0.0,
             'j':0.0,
             'k':0.0,
             'l':0.0,
             'm':0.0,
             'n':0.0,
             'o':0.0,
             'p':0.0,
             'q':0.0,
             'r':0.0,
             's':0.0,
             't':0.0,
             'u':0.0,
             'v':0.0,
             'w':0.0,
             'x':0.0,
             'y':0.0,
             'z':0.0}

alpha_dict = {'a':0,
              'b':0,
              'c':0,
              'd':0,
              'e':0,
              'f':0,
              'g':0,
              'h':0,
              'i':0,
              'j':0,
              'k':0,
              'l':0,
              'm':0,
              'n':0,
              'o':0,
              'p':0,
              'q':0,
              'r':0,
              's':0,
              't':0,
              'u':0,
              'v':0,
              'w':0,
              'x':0,
              'y':0,
              'z':0,}

alpha_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def main():
    text   = raw_input('Enter text to be analyzed: ')
    length = 0
    for byte in text:
        letter = byte.lower()
        if letter in alpha_list:
            length             += 1
            alpha_dict[letter] += 1.0
            freq_dict[letter]   = (alpha_dict[letter] / length) * 100
        else:
            pass

    print length
    print ''
    print alpha_dict
    print ''
    print freq_dict


if __name__=="__main__":
    sys.exit(main())
