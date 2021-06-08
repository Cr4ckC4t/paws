#!/usr/bin/env python3

# [Description]
# Ping sweeper for the use on windows and linux.
#
#	Checks if any hosts from a list of IPs are alive by pinging them. (Obviously not suited when ICMP is deactivated.)
# After gathering intel and loads of IP addresses, this tool can help to quickly filter out the reachable ones.
#
# 100 addresses (30% alive) ~ 1.5 minutes (using 5 processes)
# This script uses multiprocessing. The amount of max. parallel processes can be controlled via the "processes" variable.

# [Requires]
#       - a list of IP-addresses as input parameter

# [Usage]
#	1) run the script with a file as argument; the file contains the ip addresses to scan

# [Author]
#	@crackcat

import sys
import subprocess
import platform
from datetime import datetime as dt
from multiprocessing import Pool

pool       = None
finished   = 0
tasks      = 0
processes  = 5 # amount of max. parallel processes
alives     = 0

# change ping flag and disable colors when executed on windows
ping_cmd  = 'ping -n 1' if platform.system() == 'Windows' else 'ping -c 1'
COLORED = False if platform.system() == 'Windows' else True

class fc:
	if COLORED:
	        cyan = '\033[96m'
	        green = '\033[92m'
	        orange = '\033[93m'
	        red = '\033[91m'
	        end = '\033[0m'
	else:
		cyan=green=orange=red=end=''
    
def ping(ip):
	# use subprocess instead of os so it works in windows aswell
	p = subprocess.Popen(f'{ping_cmd} {ip}', shell=True, stdout=subprocess.PIPE)
	res = [l.decode(encoding='utf-8', errors='ignore') for l in p.stdout]
	return [ip, res]

def pong(result):
	global finished
	global tasks
	global alives

	finished += 1

	ip, lines = result
	for l in lines:
		if l.upper().count('TTL'):
			print(f'\t{fc.green}[\N{check mark}]{fc.cyan} {ip:20}{fc.end}')
			alives += 1
		else:
			percent = int(finished*100/tasks)
			print(f'\t[{fc.orange}{percent:2}%{fc.end}] scanning... \r', end='')

def main(filename):
	global pool
	global finished
	global tasks
	global alives

	ips = []
	with open(filename, 'r') as f:
		ips = f.readlines()

	ips = [ ip.strip('\n') for ip in ips ]

	tasks = len(ips)
	print(f'{fc.cyan}[+]{fc.end} Loaded {fc.cyan}{tasks}{fc.end} targets')

	start = dt.now()
	print(f'{fc.cyan}[+]{fc.end} Starting scan at: {start}')

	try:
		with Pool(processes=processes) as pool:
			pings = []
			for ip in ips:
				pings.append(pool.apply_async(ping, args=(ip,), callback=pong))

			pool.close()
			pool.join()
	except:
		print(f'\n{fc.red}[!] Aborted{fc.end}')
		sys.exit(1)

	end = dt.now()
	print(f'{fc.cyan}[+]{fc.green} Scan completed{fc.end} (took us {end-start}s)')
	print(f'{fc.cyan}[+]{fc.end} Statistics:')
	print(f'\tTotal scanned targets  : {finished}')
	print(f'\tAlive hosts (pingable) : {alives}')


if __name__ == '__main__':
	if (len(sys.argv) == 2):
		main(sys.argv[1])
	else:
		print(f'[!] Usage: {sys.argv[0]} <file with list of IPs>')
		sys.exit()
