#!/usr/bin/env python3

#======================================#
#  Script for finding bad characters   #
#======================================#
#
# Usage:
#       *1) Send the complete bytearray (exploit.py)
#        2) Copy the hex dump of the ESP into a file
#        3) Use cut (e.g. cut -d ' ' -f1,...) to get only the hex values block
#        4) Insert the hex values in the "dump" variable
#        5) Specify how many columns the hex dump has with "cols" (either 8 or 16 from Immunity Debugger)
#        6) Run the script - this should print out all bad characters
#    *) If a bytearray with some bad characters already excluded is sent, specify these bad characters in "expectedbad"
#
#    Here all hex values follow the format 00-FF (no prefix)
#
#======================================#

import sys

expectedbad = ['00']
cols  = 16

# get the hex dump with cut -d ' ' -f 2,3,... after copying everything from Immunity

dump = """
# <INSERT HEX DUMP STARTING FROM ESP HERE>
"""

# format hex dump
dump = dump.replace('\n', '').strip().split()

# create hey array
h = [f'{x:02X}' for x in range(0,256)]

# unify expected bad characters
expectedbad = [b.upper() for b in expectedbad]
# remove known bad chars
h = list(filter(lambda x: x.upper() not in expectedbad, h))

class fc:
        cyan    = '\033[96m'
        green   = '\033[92m'
        orange  = '\033[93m'
        red     = '\033[91m'
        redbg   = '\33[41m'
        end     = '\033[0m'
        bold    = '\033[1m'

print(f'Attempting to find {fc.redbg}bad{fc.end} characters.')

# check length of lists
if len(dump) < len(h):
        print(f'The hex dump is shorter than the crafted hex array. Copied everything? ({fc.red}Aborting{fc.end})')
        sys.exit(1)

rows  = int(len(h) / cols)
last  = len(h) % cols
badchars = []

for r in range(0,rows):
        for x in range(r*cols,r*cols+cols):
                if h[x].upper() != dump[x].upper():
                        badchars.append(h[x])
                        print(f'{fc.redbg}{h[x]}{fc.end} {fc.green}{dump[x]}{fc.end}  ', end='')
                else:
                        print(f'{fc.cyan}{h[x]}{fc.end} {" ":2s}  ', end='')
        print()

for i in range(rows*cols,rows*cols+last):
        if h[i].upper() != dump[i].upper():
                badchars.append(h[i])
                print(f'{fc.redbg}{h[i]}{fc.end} {fc.green}{dump[i]}{fc.end}  ', end='')
        else:
                print(f'{fc.cyan}{h[i]}{fc.end} {" ":2s}  ', end='')

print()
print(f'{fc.green}Matching complete.{fc.end}')
print(f'Known bad characters: {fc.orange}{expectedbad}{fc.end}')
print(f'Found bad characters: {fc.orange}{badchars}{fc.end}')
