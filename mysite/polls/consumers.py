import json

from channels import Group
from channels.generic.websockets import WebsocketDemultiplexer

from .binding import QuestionBinding
from .models import Question


# belongs to Management Page - Signals
def ws_connect(message):
    # add to the management group
    Group("management-signals").add(message.reply_channel)
    # accept the connection request
    message.reply_channel.send({"accept": True})


# belongs to Management Page - Signals
def ws_disconnect(message):
    # remove from management group
    Group("management-signals").discard(message.reply_channel)


# belongs to Management Page - Binding
class Demultiplexer(WebsocketDemultiplexer):

	consumers = {
		"management": QuestionBinding.consumer,
	}

	def connection_groups(self):
		return ["management-binding"]
