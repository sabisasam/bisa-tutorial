# RabbitMQ tutorial - part 5 - topics
# Producer, sends message.
import pika
import sys


# Establish connection with RabbitMQ server (broker on given machine (here: localhost)).
# (Connect to a broker on a different machine by specifying its name or IP address here.)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

# Deklare exchange.
# Receives messages from producers and pushes them to queues.
# Must know exactly what to do with a received message (e.g. discard it or append it
# to particular queue or many queues), those rules are defined by the exchange type.
# (Available exchange types: 'direct', 'topic', 'headers' and 'fanout'.)
channel.exchange_declare(exchange='topic_logs',  # Define name of exchange.
                         exchange_type='topic')  # This type broadcasts a message to all
# queues whose binding key (routing_key
# in channel.queue_bind()) matches the
# routing key of the message. Important
# special cases for binding keys:
# '*' can substitute for exactly one word.
# '#' can substitute for zero or more words.
# (So a queue with '#' as binding key would
# receive all messages, regardless of the
# routing key - like in fanout exchange.)
# (When the special characters '*' and '#'
# aren't used in bindings, the topic exchange
# will behave just like a direct exchange.)

# Get or set routing_key.
# To simplify things we will assume that the routing keys of logs will have two words:
# '<facility>.<severity>'.
# The routing_key of messages for topic exchanges must be a list of words, delimited by dots.
# The words can be anything, but usually they specify some features connected to the message.
# There can be as many words in the routing key as you like, up to the
# limit of 255 bytes.
routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
# Get or set message (specify message through
# '$ python emit_log_topic.py <facility>.<severity> <your_log>').
message = ' '.join(sys.argv[2:]) or 'Hello World!'
# Sending message to exchange.
channel.basic_publish(exchange='topic_logs',  # Specify which exchange will get the message.
                      routing_key=routing_key,
                      # Supply given routing_key as routing key.
                      # ('topic' exchanges can do routing based on
                      # multiple criteria which are defined here.)
                      body=message)  # Message.
print(" [x] Sent %r: %r" % (routing_key, message))

# Close connection.
# Make sure that network buffers were flushed and message was actually
# delivered to RabbitMQ.
connection.close()
