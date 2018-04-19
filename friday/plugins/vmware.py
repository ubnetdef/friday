from mattermost_bot.bot import listen_to
from mattermost_bot import settings
from pyVmomi import vim
from friday.libs.vmware import VMwareAPI

def on_init():
	# Attempt to ping the vmware server
	api = VMwareAPI()
	api.disconnect()


@listen_to('!vmsearch (.*)')
def vmsearch(message, path):
	api = VMwareAPI()
	res = api.search(path)

	# Iterate things inside the folder
	output = []
	if type(res) is None:
		output.append("No results found.")
	elif type(res) is vim.Folder:
		for item in res.childEntity:
			if type(item) is None:
				continue
			elif type(item) is vim.Folder:
				itemtype = "Folder"
				extra = ""
			else:
				itemtype = "VM"
				extra = " Online" if item.summary.runtime.powerState else " Offline"
				extra = "- {} - {}".format(item.config.uuid, extra)

			output.append("* {}: {}{}".format(itemtype, item.name, extra))
	else:
		extra = "Online" if res.summary.runtime.powerState else "Offline"
		output.append("* VM: {} - {} - {}".format(res.name, res.config.uuid, extra))

	output.insert(0, 'Found {} results'.format(len(output)))
	api.disconnect()

	message.reply('\n'.join(output))


@listen_to('!vmstatus (.*)')
def vmstatus(message, path):
	pass


@listen_to('!vmcreate (.*)')
def vmsearch(message, args):
	pass


@listen_to('!vmboot (.*)')
def vmboot(message, args):
	pass


@listen_to('!vmshutdown (.*)')
def vmshutdown(message, args):
	pass