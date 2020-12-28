#=======================================#
#  Fuzzing script for Buffer Everflows  #
#=======================================#
#
# Usage:
#        1) Change ip, port and command to fuzz
#        2) Run the command
#
# Depending on the reaction of the command on the overflow
# a modification of the "try" block might be necessary!
#
#=======================================#

#!/usr/bin/env python3

import socket
import sys
import time

ip       = '10.10.01.01'
port     = 1337
cmd      = 'commando'
timeout  = 5               # seconds
stride   = 100             # bytes
buffer   = 'C' * stride

class fc:
        cyan = '\033[96m'
        green = '\033[92m'
        orange = '\033[93m'
        red = '\033[91m'
        end = '\033[0m'
        bold = '\033[1m'


print(f'Fuzzing [{fc.cyan}{cmd}{fc.end}] at [{fc.cyan}{ip}{fc.end}:{fc.cyan}{port}{fc.end}] (Timeout set to: {fc.cyan}{timeout}s{fc.end})')

while True:
        try:
                print(f'Attempting [{fc.bold}{len(buffer):5d}{fc.end}] bytes ...')

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.settimeout(timeout)

                message = cmd + ' ' + buffer
                s.send(message.encode('utf-8'))

                s.recv(1024)

                s.close()

                buffer = buffer + 'C' * stride
                time.sleep(1)

        except Exception as e:
                print(f'Fuzzing crashed at {fc.bold}{len(buffer)}{fc.end} bytes.')
                print(f'\tErr: {fc.orange}{e}{fc.end}')
                sys.exit(0)

        except KeyboardInterrupt:
                print(f'{fc.red}Aborted by user.{fc.end}')
                sys.exit(0)
