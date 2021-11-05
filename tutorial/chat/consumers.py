from channels import Channel, Group
from channels.sessions import channel_session
from .models import Message


# connected to chat-messages
def msg_consumer(message):
	# save the model
	room = message.content['room']
	Message.objects.create(
		room=room,
		message=message.content['message'],
	)
	# broadcast to listening sockets
	Group("chat-%s" % room).send({
		"text": message.content['message'],
	})


# connected to websocket.connect
@channel_session
def ws_connect(message):
	# work out room name from path (ignore slashes)
	room = message.content['path'].strip("/")
	# save room in session and add us to the group
	message.channel_session['room'] = room
	Group("chat-%s" % room).add(message.reply_channel)
	# accept the connection request
	message.reply_channel.send({"accept": True})


# connected to websocket.receive
@channel_session
def ws_message(message):
	# stick the message onto the processing queue
	Channel("chat-messages").send({
		"room": message.channel_session['room'],
		"message": message['text'],
	})


# connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
	Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
