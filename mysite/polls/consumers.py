from channels import Group


# connected to websocket.connect
def ws_add(message):
	# accept the connection
	message.reply_channel.send({"accept": True})
	# add to the chat group
	Group("chat").add(message.reply_channel)


# connected to websocket.receive
def ws_message(message):
	Group("chat").send({
		"text": "[user] %s" % message.content['text'],
	})


# connected to websocket.disconnect
def ws_disconnect(message):
	Group("chat").discard(message.reply_channel)
