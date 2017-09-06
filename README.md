# django-tutorial

## Channels

mysite/settings.py got changed for use of channels.
The models Room and Message got added to polls/models.py.
They are used in polls/consumers.py which contains four functions or consumers.
The function msg_consumer in polls/consumers.py sends incoming messages to listening sockets.
The consumer ws_connect accepts connection requests.
ws_message deals with messages and ws_disconnect discards a connection.
Channel routing is contained in polls/routing.py and it maps channels to consumer functions.
