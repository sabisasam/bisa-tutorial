from channels import Group
from channels.generic.websockets import WebsocketDemultiplexer

from .binding import CategoryBinding


# belongs to Fortune Page - Websocket
class Demultiplexer(WebsocketDemultiplexer):

	consumers = {
		"fortune": CategoryBinding.consumer,
	}

	def connection_groups(self):
		return ["fortune-ws"]


# belongs to Fortune Page - RabbitMQ
def ws_connect(message):
    # add to the fortunes-mq group
    Group("fortunes-mq").add(message.reply_channel)
    # create instance of FortuneServer
    message.reply_channel.send({"accept": True})


# belongs to Fortune Page - RabbitMQ
def ws_disconnect(message):
    # remove from fortunes-mq group
    Group("fortunes-mq").discard(message.reply_channel)
