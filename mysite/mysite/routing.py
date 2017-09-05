from channels.routing import route
from polls.consumers import msg_consumer, ws_connect, ws_message, ws_disconnect


channel_routing = [
	route("chat-messages", msg_consumer),
	route("websocket.connect", ws_connect),
	route("websocket.receive", ws_message),
	route("websocket.disconnect", ws_disconnect),
]
