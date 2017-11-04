from channels.generic.websockets import WebsocketDemultiplexer

from .binding import CategoryBinding


# belongs to Fortune Page - Websocket
class Demultiplexer(WebsocketDemultiplexer):

	consumers = {
		"fortune": CategoryBinding.consumer,
	}

	def connection_groups(self):
		return ["fortune-ws"]
