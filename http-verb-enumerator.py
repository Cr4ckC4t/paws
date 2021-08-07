#!/usr/bin/env python3

# Just a very very small script that checks what an OPTIONS request on a target returns.
#
# USAGE: ./http-verb-enumerator.py
#  - it will prompt for the target and port

import http.client

class fc:
        cyan = '\033[96m'
        green = '\033[92m'
        orange = '\033[93m'
        purple = '\033[35m'
        red = '\033[91m'
        end = '\033[0m'
        bold = '\033[1m'

def main():
        host = input(f"{fc.cyan}Host/IP{fc.end}  : ")
        port = input(f"{fc.cyan}Port{fc.end}     : ")
        print()

        try:
                print(f"{fc.orange}> Connecting ... {fc.end}")
                con = http.client.HTTPConnection(host, port)
                con.request("OPTIONS", "/")
                response = con.getresponse()
                print(f"{fc.green}> Enabled methods{fc.end} : {fc.cyan}{response.getheader('allow')}{fc.end}")
                con.close()
        except ConnectionRefusedError:
                print(f"{fc.red}> Connection to target failed!{fc.end}")
        except Exception as e:
                print(f"{fc.red}> Exception caught{fc.end} : {e}")


if __name__ == "__main__":
        banner = """
\tPython3 HTTP Verb Enumerator

 > Attempts to use the OPTION method to find out other available http verbs.

"""
        print(f"{fc.purple}{banner}{fc.end}")
        main()
