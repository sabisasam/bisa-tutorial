# RabbitMQ tutorial - part 1 - "Hello world!"
# Consumer, receives messages.
import pika


# Establish connection with RabbitMQ server (broker on given machine (here: localhost)).
# (Connect to a broker on a different machine by specifying its name or IP address here.)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

# Make sure that queue exists (like "get or create", queue_declare is idempotent).
# Show existing queues and how many messages are in them with '$
# rabbitmqctl list_queues'.
channel.queue_declare(queue='hello')

# Declaring a callback for 'basic_consume'.
# Gets called when a message is received.


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


# Specify which function should receive messages from which queue
# (subscribing to queue).
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)  # Turn off message acknowledgments.
# Messages will be lost if worker dies, including
# all messages that were dispatched to this worker.

# Enter never-ending loop that waits for data and runs callbacks whenever
# necessary.
print(' [*] Waiting for messages. To exit press CTRL+C (Unix) or CTRL+BREAK (Windows).')
channel.start_consuming()
