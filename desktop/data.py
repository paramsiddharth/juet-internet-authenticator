from datetime import datetime

# App metadata
app_name = 'JUET Internet Authenticator'
config_file = '.juetrc'
external_attrib = {
	'Icons': '<a href=\'https://icons8.com\'>Icons8</a>'
}
app_info = f'''\
<b>{app_name}</b> lets you login/logout of the JUET Internet \
authentication system seamlessly.<br />
<br />
{
	'<br/>'.join([f'{thing} from {entity}.' for thing, entity in external_attrib.items()])
}<br />
© Param Siddhharth 2022-{datetime.now().year}'''

# System-specific
test_url = 'https://www.google.com'
desk_url = 'http://10.10.10.1:8090/'
class routes:
	login = 'login.xml'
	logout = 'logout.xml'
	home = 'httpclient.html'