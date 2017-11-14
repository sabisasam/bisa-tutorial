# RabbitMQ tutorial - part 3 - publish/subscribe
# Producer, sends message.
import pika
import sys


# Establish connection with RabbitMQ server (broker on given machine (here: localhost)).
# (Connect to a broker on a different machine by specifying its name or IP address here.)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Deklare exchange.
# Receives messages from producers and pushes them to queues.
# Must know exactly what to do with a received message (e.g. discard it or append it
# to particular queue or many queues), those rules are defined by the exchange type.
# (Available exchange types: 'direct', 'topic', 'headers' and 'fanout'.)
channel.exchange_declare(exchange='logs', # Define name of exchange.
                         exchange_type='fanout') # This type broadcasts all received
                                                 # messages to all queues it knows.

# Get or set message (specify message through '$ python emit_log.py your_log').
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
# Sending message to exchange.
channel.basic_publish(exchange='logs', # Specify which exchange will get the message.
                      routing_key='', # This value is ignored for fanout exchanges.
                      body=message) # Message.
print(" [x] Sent %r" % message)

# Close connection.
# Make sure that network buffers were flushed and message was actually delivered to RabbitMQ.
connection.close()
