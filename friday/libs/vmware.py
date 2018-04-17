import atexit
from mattermost_bot import settings
from pyVim import connect
from pyVmomi import vim

class VMwareAPI(object):
	def __init__(self):
		# Monkey patch to disable SSL verification
		import ssl
		context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
		context.verify_mode = ssl.CERT_NONE

		# Connect
		self.connection = connect.SmartConnect(host=settings.VMWARE_HOST,
												user=settings.VMWARE_USER,
												pwd=settings.VMWARE_PASS,
												sslContext=context)

	def disconnect(self):
		connect.Disconnect(self.connection)

	def search(self, path):
		return self.connection.content.searchIndex.FindByInventoryPath(path)
