# RabbitMQ tutorial - part 5 - topics
# Consumer, receives messages.
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
channel.exchange_declare(exchange='topic_logs', # Define name of exchange.
                         exchange_type='topic') # This type broadcasts a message to all
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

# Create a fresh, empty queue when the consumer connects to RabbitMQ.
# If no name for queue is specified (like here) the server will choose a random name.
# 'exclusive=True' means the queue will be deleted if the consumer disconnects.
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue # Get the random queue name.

# Get binding keys (the consumer will only get logs with a matching routing_key).
# Specify them through '$ python receive_logs_topic.py [binding_key]...' (specify multiple
# binding keys by seperating them with spaces).
# To simplify things we will assume that a binding_key will have two words:
# '<facility>.<severity>'.
# For topic exchanges, binding_keys must be a list of words, delimited by dots.
# The words can be anything, but usually they specify some features connected to the message.
# There can be as many words in the binding key as you like, up to the limit of 255 bytes.
binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

# Create binding for each given binding_key (bind exchange and queue).
for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs', # Exchange which receives the messages.
                       queue=queue_name, # Queue to which the exchange should append messages.
                       routing_key=binding_key) # Define binding key.
                                                # Its meaning depends on the exchange type.
                                                # ('topic' exchanges can do routing based on
                                                # multiple criteria which are defined here.)
print(' [*] Waiting for logs. To exit press CTRL+C (Unix) or CTRL+BREAK (Windows).')

# Declaring a callback for 'basic_consume'.
# Gets called when a message is received.
def callback(ch, method, properties, body):
    print(" [x] %r: %r" % (method.routing_key, body))

# Specify which function should receive messages from which queue (subscribing to queue).
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True) # Turn off message acknowledgments.
                                   # Messages will be lost if worker dies, including
                                   # all messages that were dispatched to this worker.

# Enter never-ending loop that waits for data and runs callbacks whenever necessary.
channel.start_consuming()
