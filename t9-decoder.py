#!/usr/bin/env python3

# [Description]
#       Very basic T9 en-/decoder (also called the phone key cipher)

# [Usage]
#       1) run from command line

# [Author]
#       @crackcat

import argparse
import re

# keymap
keymap = {
        '1': ',.?!1',
        '2': 'abc2',
        '3': 'def3',
        '4': 'ghi4',
        '5': 'jkl5',
        '6': 'mno6',
        '7': 'pqrs7',
        '8': 'tuv8',
        '9': 'wxyz9',
        '0': ' 0',
}

class fc:
        blue = '\033[96m'
        green = '\033[92m'
        yellow = '\033[93m'
        red = '\033[91m'
        end = '\033[0m'
        bold = '\033[1m'
        pink   = '\x1b[1;35m'

def tel_encode(plaintext, delimiter):
        invalid = 0
        print(f'{fc.blue}[>]{fc.pink} Plaintext: {fc.end}{plaintext}{fc.end}')
        print(f'{fc.blue}[>]{fc.pink} Cipher: {fc.end}', end='')
        notFirst = False
        for char in plaintext:
                valid=False
                for key, value in keymap.items():
                        if valid:
                                continue
                        pos = value.find(char)
                        if pos > -1:
                                print(f'{delimiter if notFirst else ""}{fc.green}{key*(pos+1)}{fc.end}', end='')
                                valid=True
                if not valid:
                        invalid += 1
                        print(f'{delimiter if notFirst else ""}{fc.red}{char}{fc.end}', end='')
                notFirst=True

        if invalid == len(plaintext):
                invalid = -1
        return invalid


def tel_decode(cipher,delimiter):
        invalid = 0

        # remove leading and trailing delimiters
        cipher = cipher.strip(delimiter)

        print(f'{fc.blue}[>]{fc.pink} Cipher: {fc.end}{cipher}')
        print(f'{fc.blue}[>]{fc.pink} Plaintext: {fc.end}', end='')

        if delimiter == '':
                print()
                print(f'{fc.red}[!] Error:{fc.end} Decoding with empty delimiter not supported.',end='')

        # decode delimited cipher
        else:
                # remove repeated delimiters
                cipher = re.sub(f'{delimiter}+', delimiter, cipher)
                for num in cipher.split(delimiter):
                        valid=False
                        # validate format ('111', not '112')
                        if num.count(num[0]) == len(num):
                                for key, value in keymap.items():
                                        # check key existence and max length
                                        if num[0] == key and len(num) <= len(value):
                                                print(f'{fc.green}{value[len(num)-1]}{fc.end}', end='')
                                                valid=True
                        if not valid:
                                invalid += 1
                                print(f'{fc.red}{num}{fc.end}', end='')
                if invalid == len(cipher.split(delimiter)):
                        invalid = -1
        return invalid

keymap_string=f'''

{fc.blue}\t{"1":^7}{"2":^7}{"3":^7}{fc.green}
\t{keymap["1"]:^7}{keymap["2"]:^7}{keymap["3"]:^7}
{fc.blue}\t{"4":^7}{"5":^7}{"6":^7}{fc.green}
\t{keymap["4"]:^7}{keymap["5"]:^7}{keymap["6"]:^7}
{fc.blue}\t{"7":^7}{"8":^7}{"9":^7}{fc.green}
\t{keymap["7"]:^7}{keymap["8"]:^7}{keymap["9"]:^7}
{fc.blue}\t{" "*7}{"0":^7}{" "*7}{fc.green}
\t{" "*7}{keymap["0"]:^7}{" "*7}{fc.end}
'''

def main(args):
        print(f'{fc.blue}[+]{fc.end} Using this keymap: {keymap_string}')
        if args.delimiter == '':
                print(f'{fc.yellow}[!] Warning:{fc.end} Using an empty delimiter. Cipher might not be reversable')
        else:
                print(f'{fc.blue}[+]{fc.end} Using "{args.delimiter}" as delimiter.')

        invalid = 0
        if args.decode:
                invalid = tel_decode(args.input, args.delimiter)
        elif args.encode:
                invalid = tel_encode(args.input.lower(), args.delimiter)
        else:
                print(f'{fc.yellow}[!] Warning:{fc.end} No option specified. Nothing to be done.')
                return

        print()
        if invalid > 0:
                print(f'{fc.yellow}[!] {fc.red}Failed{fc.end} on {invalid} character{"s" if (invalid > 1) else "." (Check format and delimiter?)')
        if invalid < 0:
                print(f'{fc.red}[!] Error:{fc.end} Invalid input. Check format and delimiter.')
        print(f'{fc.blue}[>]{fc.pink} Done.{fc.end} [{fc.yellow}Keep in mind{fc.end}: uppercase cipher == lower cipher]')


banner='''
 Basic T9 decoder. @crackcat

'''

if __name__ == '__main__':
        print(banner)
        parser = argparse.ArgumentParser(description='description')
        parser.add_argument('input', help='string to encode or decode')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-d', '--decode', action='store_true', help='decode the input')
        group.add_argument('-e', '--encode', action='store_true', help='encode the input')
        parser.add_argument('-s', '--delimiter', default=' ', help='provide a delimiter to distinguish repeatedy presses (default space)')
        args = parser.parse_args()
        main(args)
