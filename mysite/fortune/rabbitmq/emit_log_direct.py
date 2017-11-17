# RabbitMQ tutorial - part 4 - routing
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
channel.exchange_declare(exchange='direct_logs', # Define name of exchange.
                         exchange_type='direct') # This type broadcasts a message to all
                                                 # queues whose binding key (routing_key
                                                 # in channel.queue_bind()) exactly
                                                 # matches the routing key of the message.

# Get or set severity.
# To simplify things we will assume that severity can be one of 'info', 'warning', 'error'.
severity = sys.argv[1] if len(sys.argv) > 2 else 'info'
# Get or set message (specify message through
# '$ python emit_log_direct.py <severity> <your_log>').
message = ' '.join(sys.argv[2:]) or 'Hello World!'
# Sending message to exchange.
channel.basic_publish(exchange='direct_logs', # Specify which exchange will get the message.
                      routing_key=severity, # Supply the log severity as routing key.
                                            # This way the receiving script will be able to
                                            # select the severity it wants to receive.
                      body=message) # Message.
print(" [x] Sent %r: %r" % (severity, message))

# Close connection.
# Make sure that network buffers were flushed and message was actually delivered to RabbitMQ.
connection.close()
