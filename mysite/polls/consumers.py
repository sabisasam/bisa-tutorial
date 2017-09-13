import json

from channels import Group


# connected to websocket.connect
def ws_connect(message):
	# add to the management group
	Group("management").add(message.reply_channel)
	# accept the connection request
	message.reply_channel.send({"accept": True})

# connected to websocket.receive
def ws_receive(message):
	Group("management").send({
		'text': json.dumps({
			'question': message.question,
			'question_text': message.question.question_text
		})
	})

# connected to websocket.disconnect
def ws_disconnect(message):
	Group("management").discard(message.reply_channel)
