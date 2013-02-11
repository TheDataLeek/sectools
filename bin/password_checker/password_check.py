#!/usr/bin/env python

'''
DEPENDENCIES == password_dictionary.txt

length_check checks the length of the password and scores it on length
letter_repeat_check determines how many repeated letters there are in your
    password, for every repeated letter it adds one (the lower the better)
frequent_password_check checks to see if the given password is included in
    the top 500 list (0 is good, 1 is not)
num_include_check checks to see how many numbers are included in the given
    password (the higher the better)

TODO:
    add argument handling - DONE
    add more checks
        look up previous programs
    weigh certain checks...
    maybe add john the ripper compatibility?
    run pep8 and pychecker
'''

import sys
import optparse


def main():
    opts                   = get_args()
    password               = opts.password
    final_score, checklist = scoring(password)
    if final_score <= 0:
        final_score = 0
    if final_score < 25:
        print 'WEAK'
    elif 25 < final_score < 50:
        print 'OK'
    elif 50 < final_score < 75:
        print 'MEDIUM'
    elif 75 < final_score < 100:
        print 'STRONG'
    elif final_score > 100:
        print 'UNBREAKABLE'
    print 'Final Score =', final_score
    print checklist


def scoring(password):
    frequency_class            = PasswordFrequency()
    pass_dict                  = frequency_class.dictionary_get()
    frequent_password_results  = frequency_class.check(password, pass_dict)

    character_class            = CharacterVariance()
    num_include_results        = character_class.num_include_check(password)
    character_variance_results = character_class.variance_check(password)

    check_class                = MajorChecks()
    length_results             = check_class.length_check(password)
    letter_repeat_results      = check_class.letter_repeat_check(password)
    consecutive_byte_results   = check_class.consecutive_bytes(password)

    checklist                  = [length_results, letter_repeat_results, consecutive_byte_results,
                                 frequent_password_results, num_include_results, character_variance_results]

    final_score                = ((length_results[2] + letter_repeat_results[2] +
                                 frequent_password_results[1] + num_include_results[2] + character_variance_results[1]
                                 + consecutive_byte_results[1]) / 6)

    return final_score, checklist


def get_args():
    global opts
    global args
    parser = optparse.OptionParser(usage = 'UsageL %prog <options>', version = 'Version 1.0')
    parser.add_option('-p', '--password', action='store', type='string', default=None, help='Password for Scoring')
    opts, args = parser.parse_args()

    if opts.password == None:
        opts.password = raw_input('Enter Password: ')

    return opts


class MajorChecks:
    '''This class defines checks that aren't in any category
    '''

    def length_check(self, password):
        '''This function checks for password length
           score = length * 2
        '''
        length = len(password)
        score  = length * 2
        if score > 100:
            score = 100
        return ['length_check', length, score]

    def letter_repeat_check(self, password):
        '''This function checks for repeated letters
           The modifier isn't very large due to how little this issue is
           score = the number of repeated letters
        '''
        letter_repeat = 0
        pass_list     = []
        for letter in password:
            if letter in pass_list:
                letter_repeat += 1
            pass_list.append(letter)
        if letter_repeat != 0:
            score = -letter_repeat
        else:
            score = 10
        return ['letter_repeat_check', letter_repeat, score]

    def consecutive_bytes(self, password):
        '''This function checks for repeated characters in a row
           This is weighted fairly heavily
           score = 10 * repeated letters
        '''
        prev_byte = ''
        score     = 10
        for byte in password:
            if prev_byte == '':
                prev_byte += byte
            elif byte == prev_byte[0]:
                prev_byte += byte
                score += 10
            else:
                prev_byte = ''
        if score == 10:
            score += 20
        else:
            score *= -1
        return ['consecutive_bytes', score]


class CharacterVariance:

    def num_include_check(self, password):
        '''This function checks to see if numbers are included in the passphrase
           It is not as important as the variance check
           score = the number of included numbers ** 2
        '''
        num_list     = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        num_includes = 0
        for letter in password:
            if letter in num_list:
                num_includes += 1
            else:
                pass
        if num_includes == 0:
            score = 0
        else:
            score = num_includes ** 2
        if score > 100:
            score = 100
        return ['number_include_check', num_includes, score]

    def variance_check(self, password):
        '''This function checks to see if there are enough of each type of character
           This is very important
           score = uppercase *3 + lowercase * 3 + numbers * 3
        '''
        num_list   = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        lower_byte = 0.0
        upper_byte = 0.0
        num_byte   = 0.0
        for byte in password:
            if byte in num_list:
                num_byte += 1
            elif byte.lower() == byte:
                lower_byte += 1
            elif byte.upper() == byte:
                upper_byte += 1
        score_upper = upper_byte * 3
        score_lower = lower_byte * 3
        score_num   = num_byte * 3
        score_tmp = score_upper + score_lower + score_num
        if score_tmp > 100:
            score = 100
        else:
            score = score_tmp
        return ['variance_check', score]


class PasswordFrequency:

    def dictionary_get(self):
        '''This function gets the frequent passwords dictionary for checking
        '''
        pass_dict_file = open('password_dictionary.txt', mode='r')
        pass_dict_str  = pass_dict_file.read()
        byte_list      = []
        pass_dict      = []
        tmp_str        = ''
        for byte in pass_dict_str:
            byte_list.append(byte)
        for item in byte_list:
            if item == ' ':
                pass_dict.append(tmp_str)
                tmp_str = ''
            else:
                tmp_str += item
        return pass_dict

    def check(self, password, pass_dict):
        '''This function checks the password against the dictionary
           score = either 100, -50, or -100
        '''
        score = 100
        if password in pass_dict:
            score = -100
        else:
            for item in pass_dict:
                if item in password:
                    score = -50
        if score > 100:
            score = 100
        return ['frequent_password_check', score]


if __name__ == "__main__":
    sys.exit(main())
