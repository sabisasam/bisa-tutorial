import json

from channels import Group
from .models import Question


# connected to websocket.connect
def ws_connect(message):
	print("ws_connect")
	# add to the management group
	Group("management").add(message.reply_channel)
	# accept the connection request
	message.reply_channel.send({"accept": True})


# connected to websocket.disconnect
def ws_disconnect(message):
	print("ws_disconnect")
	# remove from management group
	Group("management").discard(message.reply_channel)
