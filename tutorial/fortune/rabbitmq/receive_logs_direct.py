# RabbitMQ tutorial - part 4 - routing
# Consumer, receives messages.
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
channel.exchange_declare(exchange='direct_logs',  # Define name of exchange.
                         exchange_type='direct')  # This type broadcasts a message to all
# queues whose binding key (routing_key
# in channel.queue_bind()) exactly
# matches the routing key of the message.

# Create a fresh, empty queue when the consumer connects to RabbitMQ.
# If no name for queue is specified (like here) the server will choose a random name.
# 'exclusive=True' means the queue will be deleted if the consumer disconnects.
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue  # Get the random queue name.

# Get severities (the consumer will only get logs of this severities).
# Specify those severities through '$ python receive_logs_direct.py [info] [warning] [error]'.
# To simplify things we will assume that the severities are 'info',
# 'warning', 'error'.
severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

# Create binding for each given severity (bind exchange and queue).
for severity in severities:
    channel.queue_bind(exchange='direct_logs',  # Exchange which receives the messages.
                       queue=queue_name,
                       # Queue to which the exchange should append messages.
                       routing_key=severity)  # Define binding key.
    # Its meaning depends on the exchange type.
    # ('fanout' exchanges simply ignore this value.)
print(' [*] Waiting for logs. To exit press CTRL+C (Unix) or CTRL+BREAK (Windows).')

# Declaring a callback for 'basic_consume'.
# Gets called when a message is received.


def callback(ch, method, properties, body):
    print(" [x] %r: %r" % (method.routing_key, body))


# Specify which function should receive messages from which queue
# (subscribing to queue).
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)  # Turn off message acknowledgments.
# Messages will be lost if worker dies, including
# all messages that were dispatched to this worker.

# Enter never-ending loop that waits for data and runs callbacks whenever
# necessary.
channel.start_consuming()
