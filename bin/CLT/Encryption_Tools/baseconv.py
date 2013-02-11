#!/usr/bin/env python

""" Arguments:
        -h = Display help and exit
        -i = Initial base of the number
        -b = Final base of the number
        -n = The number
    This formula works along a basic series of steps:
        Lets say you want to convert a number, n, to a base, b.
        First, divide that number by the base and the remainder goes on the right
        Divide the remainder by the base again and put the remainder 2nd from the right
        Repeat until your division = 0 and when you do, that last remainder is the left-most digit
    Example: 10, base 10, to base 2:
        10/2 = 5 (remainder of 0, number is ***0)
        5/2  = 2 (remainder of 1, number is **10)
        2/2  = 1 (remainder of 0, number is *010)
        When you get to zero, the leftmost digit is the last remainder:
        1/2  = 0 (since you have reached 0, number is 1010)
    Example: 23, base 10, to base 3:
        23/3 = 7 (remainder of 2, number is **2)
        7/3  = 2 (remainder of 1, number is *12)
        2/3  = 0 (since you have reached zero, add the remainder)
                                 (number is 212)
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
    if opts.initial_base == 10:
        final_num = decimal2base(int(opts.num), opts.base)
    if opts.initial_base != 10:
        if opts.base != 10:
            number    = int(opts.num, opts.initial_base)  # If the initial base is not 10, convert it to base ten first
            final_num = decimal2base(number, opts.base)   # then convert from 10 to another
        if opts.base == 10:
            print int(opts.num, opts.initial_base)
    if opts.base != 10:
        print final_num


def decimal2base(number, base):
    digit_list = []
    count      = -1
    while True:
        digit_list.append(number % base)  # Add the remainder to the list
        number /= base                    # the number has now been divided for the next step
        if number / base == 0:            # If the last division resulted in 0, add the last remainder and quit
            digit_list.append(number % base)
            break
    for item in digit_list:
        count += 1
        if item > 9:
            digit_list[count] = chr(96 + (item - 9))  # This is to allow for more bases beyond 10
    final_list = []                                   # It uses the ASCII dictionary to do this
    while True:
        final_list.append(str(digit_list[count]))
        count -= 1
        if count <= -1:
            break
    final_num = ''.join(final_list)
    return final_num


def get_args():
    global opts
    global args
    parser = optparse.OptionParser(usage = 'UsageL %prog <options>', version = 'Version 1.0')
    parser.add_option('-i', '--initial_base' , action = 'store', type = 'int'   , default = None, help = 'Initial base of the number')
    parser.add_option('-b', '--base'         , action = 'store', type = 'int'   , default = None, help = 'Final base to be converted to')
    parser.add_option('-n', '--num'          , action = 'store', type = 'string', default = None, help = 'The number to be converted')
    opts, args = parser.parse_args()

    if opts.initial_base == None:
        opts.initial_base = int(raw_input('Enter Initial Base: '))
    if opts.base == None:
        opts.base = int(raw_input('Enter Final Base: '))
    if opts.num == None:
        opts.num = raw_input('Enter Number: ')

    return opts

if __name__ == '__main__':
    sys.exit(main())
