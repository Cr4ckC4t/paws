#!/usr/bin/env python3

# A quick and dirty script to mock different sorts of HTTP requests (in case you rather read python than the curl manual)

import socket
import sys
from urllib.parse import quote_plus as urlencode
from xml.sax.saxutils import escape as xmlescape
from base64 import b64encode

def build_http_request(host, uri, verb,
			version='HTTP/1.1',
			headers=[],
			get_params=[],
			post_params=[],
			cookies={},
			multipart=False,
			raw_post_body=None,
			):

	if len(get_params) > 0:
		uri = uri+'?'
		for param in get_params:
			uri += urlencode(param[0]) + '=' + urlencode(param[1]) + '&'
		uri = uri[:-1]

	post_body = ''
	if len(post_params) > 0:
		if not multipart:
			for param in post_params:
				post_body += urlencode(param[0]) + '=' + urlencode(param[1]) + '&'
			post_body = post_body[:-1]
		else:
			# if multipart is true
			# then post params should have the format:
			# {'name': 'header':, 'ct', 'data':}
			# default content type is "text/plain"
			post_body += f'-----------------------------9051914041544843365972754266\r\n'
			for param in post_params:
				post_body += f'Content-Disposition: form-data; name="{param["name"]}"'
				if 'header' in param:
					post_body += f'; {param["header"]}'
				post_body += '\r\n'
				post_body += f'Content-Type: {param["ct"] if "ct" in param else "text/plain"}\r\n\r\n'
				post_body += param["data"] + '\r\n'
				post_body += f'-----------------------------9051914041544843365972754266\r\n'
	elif raw_post_body:
		post_body = raw_post_body

	cookie_str = ''
	if len(cookies) > 0:
		for c in cookies:
			cookie_str += c + '=' + cookies[c] + ';'

	raw = f'{verb} {uri} {version}\r\n'
	raw += f'Host: {host}\r\n'

	if len(post_body):
		if multipart:
			headers.append('Content-Type: multipart/form-data; boundary=---------------------------9051914041544843365972754266')
		elif raw_post_body:
			pass # set content type manually
		else:
			headers.append('Content-Type: application/x-www-form-urlencoded')

	for h in headers:
		raw += h + '\r\n'
	if len(cookie_str) > 0:
		raw += f'Cookie: {cookie_str}\r\n'

	raw += f'Connection: close\r\n'
	if len(post_body) > 0:
		raw += f'Content-Length: {len(post_body)}\r\n'

	raw += f'\r\n' # headers should be terminated by \r\n\r\n

	if len(post_body)>0:
		raw += post_body

	return raw.encode('utf8')

def main(host, port):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, port))

		uri = '/pentesterlab'
		verb = 'GET'
		raw_req = build_http_request(host, uri, verb, headers=[f'Authorization: Basic {b64encode(b"key:please").decode()}'])

		print(f'[+] DEBUG OUTPUT - Raw request: \n{raw_req}')
		s.sendall(raw_req)

		print(f'[+] Waiting for a response...')
		resp = b''
		while True:
			data = s.recv(4096)
			if not data:
				break
			else:
				print(f'[+] Received {len(data)} bytes:')
				resp += data

		print(f'[+] Complete response: {resp}')
		if b'key for this' in resp:
			print(f'[!] Possible key detected in response!')

		print(f'[+] Connection closed')


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print(f'Please specify the target HOST')
		sys.exit(1)

	HOST = sys.argv[1]
	PORT = 80

	if 'http://' in HOST:
		HOST = HOST[7:-1]

	main(HOST, PORT)
