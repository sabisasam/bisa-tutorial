from channels import include
from channels.routing import route

from chat import consumers as chat
from polls import consumers as polls


chat_websocket = [
	route("chat-messages", chat.msg_consumer),
	route("websocket.connect", chat.ws_connect, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
	route("websocket.receive", chat.ws_message),
	route("websocket.disconnect", chat.ws_disconnect),
]


polls_websocket = [
	route("websocket.connect", polls.ws_connect),
	route("websocket.receive", polls.ws_receive),
	route("websocket.disconnect", polls.ws_disconnect),
]


channel_routing = [
	include(chat_websocket, path=r'^/chat'),
	include(polls_websocket, path=r'^/management/$'),
]
