import json
import base64
from os import path, remove
from pathlib import Path
from shutil import rmtree

from data import config_file as c_file

__all__ = [
	'get_username',
	'get_password'
]

def get_config_file():
	user_dir = path.expanduser('~')
	return path.join(user_dir, c_file)

def get_config():
	conf_file = get_config_file()
	try:
		with open(conf_file, 'r', encoding='utf-8') as f:
			conf = json.load(f)
		return conf
	except:
		return None

def get_username():
	conf = get_config()
	if conf is None:
		return None
	return conf.get('username')

def get_password():
	conf = get_config()
	if conf is None:
		return None
	pw_encoded = conf.get('password')
	if pw_encoded is None:
		return None
	return base64.b64decode(pw_encoded.encode('utf-8')).decode('utf-8')

def set_credentials(username, password):
	conf = {
		'username': username,
		'password': base64.b64encode(password.encode('utf-8')).decode('utf-8')
	}
	conf_file = get_config_file()
	try:
		with open(conf_file, 'w', encoding='utf-8') as f:
			json.dump(conf, f)
		return True
	except:
		return False

def flush_credentials():
	conf = get_config_file()
	if Path(conf).exists():
		try:
			if Path(conf).is_dir():
				rmtree(conf)
			else:
				remove(conf)
		except:
			return False
		return True
	else:
		return True