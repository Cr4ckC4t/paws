#!/usr/bin/env python3

import socket
import sys
import time

ip       = '10.10.84.100'
port     = 1337
cmd      = 'command'
timeout  = 5 # seconds
buffer   = 'C' * 100

while True:
        try:
                print(f'Attempting [{len(buffer)}] bytes ...')
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.settimeout(timeout)
                message = cmd + ' ' + buffer
                s.send(message.encode('utf-8'))
                s.recv(1024)
                s.close()
                time.sleep(1)
                buffer = buffer + 'C' * 100
        except Exception as e:
                print(f'Fuzzing crashed at {len(buffer)} bytes.')
                print(f'\tErr: {e}')
                sys.exit(0)
