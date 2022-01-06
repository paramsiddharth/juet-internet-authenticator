from sys import stderr
from time import sleep
from http.client import HTTPConnection
import requests as req

from data import test_url, desk_url, routes
from auth import get_username, get_password

__all__ = [
	'is_connected',
	'disconnect'
]

def remove_prefix(url):
	prefixes = ('https://', 'http://')
	for prefix in prefixes:
		if url.startswith(prefix):
			url = url[len(prefix):]
	return url

def is_connected():
	url = remove_prefix(test_url)
	try:
		c = HTTPConnection(url)
		c.request('HEAD', '/')
		status = c.getresponse().status
		c.close()
		if 200 <= status <= 299:
			return True
	except Exception as e:
		print(e.args, file=stderr)
	return False

def disconnect():
	try:
		username = get_username()
		if username is None:
			raise Exception('Username not provided')

		url = desk_url + routes.logout
		resp = req.post(url, data={
			'mode': 193,
			'producttype': 0,
			'username': username
		})
		i = 5
		while is_connected() and i > 0:
			sleep(0.4)
			i -= 1
		if resp.ok and not is_connected():
			return True
	except Exception as e:
		print(e.args, file=stderr)
	return False

def connect():
	try:
		username, password = get_username(), get_password()
		if username is None:
			raise Exception('Username not provided')
		if password is None:
			raise Exception('Password not provided')

		url = desk_url + routes.login
		resp = req.post(url, data={
			'mode': 191,
			'producttype': 0,
			'username': get_username(),
			'password': get_password()
		})
		if resp.ok and is_connected():
			return True
		raise Exception('Invalid credentials')
	except Exception as e:
		print(e.args, file=stderr)
	return False