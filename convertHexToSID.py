#!/usr/bin/env python3
# https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-azod/ecc7dfba-77e1-4e03-ab99-114b349c7164

import sys
import binascii
import struct

def convertHexToSID(hexsid):
	print(f'[+]  In: {hexsid}')
	bytesid = binascii.unhexlify(hexsid)

	revision = bytesid[0]
	numberOfDashes = bytesid[1]
	identifierAuthority = int.from_bytes(bytesid[2:8], 'big')

	bytesid = bytesid[8:]

	subAuthorities=''
	for i in range(numberOfDashes):
		value = int.from_bytes(bytesid[:4], 'little')
		bytesid = bytesid[4:]
		subAuthorities += f'-{value}'

	sid = f'S-{revision}-{identifierAuthority}{subAuthorities}'

	print(f'[+] Out: {sid}')
	return 0

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print(f'[!] Usage: {sys.argv[0]} 0x0105000000000005150000005b7bb0f398aa2245ad4a1ca401020000')
		sys.exit(1)
	try:
		if sys.argv[1].startswith('0x'):
			sys.argv[1] = sys.argv[1][2:]
		sys.exit(convertHexToSID(sys.argv[1]))
	except Exception as e:
		print(f'[!] Failed conversion with: {e}')
		sys.exit(1)
