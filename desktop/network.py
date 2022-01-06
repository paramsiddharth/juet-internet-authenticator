from sys import stderr
from http.client import HTTPConnection
import requests as req

from data import test_url, desk_url, routes

__all__ = ['is_connected', 'disconnect']

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
		url = desk_url + routes.logout
		resp = req.post(url, data={
			'mode': 193,
			'producttype': 0,
			'username': 'XXXBXXX' # Replace this with your username
		})
		if resp.ok:
			return True
	except Exception as e:
		print(e.args, file=stderr)
	return False