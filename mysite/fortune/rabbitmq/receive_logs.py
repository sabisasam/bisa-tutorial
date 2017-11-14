# RabbitMQ tutorial - part 3 - publish/subscribe
# Consumer, receives messages.
import pika


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

# Create a fresh, empty queue when the consumer connects to RabbitMQ.
# If no name for queue is specified (like here) the server will choose a random name.
# 'exclusive=True' means the queue will be deleted if the consumer disconnects.
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue # Get the random queue name.

# Create binding (bind exchange and queue).
channel.queue_bind(exchange='logs', # Exchange which receives the messages.
                   queue=queue_name) # Queue to which the exchange should append messages.
print(' [*] Waiting for logs. To exit press CTRL+C (Unix) or CTRL+BREAK (Windows).')

# Gets called when a message is received.
def callback(ch, method, properties, body):
    print(" [x] %r" % body)

# Specify which function should receive messages from which queue.
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True) # Turn off message acknowledgments.
                                   # Messages will be lost if worker dies, including
                                   # all messages that were dispatched to this worker.

# Enter never-ending loop that waits for data and runs callbacks whenever necessary.
channel.start_consuming()
