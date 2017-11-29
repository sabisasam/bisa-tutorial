from channels import include, route_class
from channels.routing import route

from chat import consumers as chat
from fortune import consumers as fortune
from polls import consumers as polls


chat_websocket = [
	route("chat-messages", chat.msg_consumer),
	route("websocket.connect", chat.ws_connect),
	route("websocket.receive", chat.ws_message),
	route("websocket.disconnect", chat.ws_disconnect),
]


fortune_websocket = [
	route("websocket.connect", fortune.ws_connect),
	route("websocket.disconnect", fortune.ws_disconnect),
]


polls_websocket = [
	route("websocket.connect", polls.ws_connect),
	route("websocket.disconnect", polls.ws_disconnect),
]


channel_routing = [
	include(chat_websocket, path=r'^/chat/(?P<room_name>[a-zA-Z0-9_]+)/$'),
	include(fortune_websocket, path=r'^/fortune/rabbitmq/$'),
	include(polls_websocket, path=r'^/management/signals/$'),
	route_class(fortune.Demultiplexer, path=r'/fortune/websocket/$'),
	route_class(polls.Demultiplexer, path=r'/management/binding/$')
]
