# RabbitMQ tutorial - part 2 - work queues
# Consumer, receives messages.
import pika
import time


# Establish connection with RabbitMQ server (broker on given machine (here: localhost)).
# (Connect to a broker on a different machine by specifying its name or IP address here.)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

# Make sure that queue exists (like "get or create", queue_declare is idempotent).
# Show existing queues and how many messages are in them with '$ rabbitmqctl list_queues'.
# 'durable=True' means the queue will be saved even if RabbitMQ server stops.
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C (Unix) or CTRL+BREAK (Windows).')

# Declaring a callback for 'basic_consume'.
# Gets called when a message is received.


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # Fake a second of work for every dot in the message.
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # Send acknowledgment that message had been received and processed.
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Tell RabbitMQ not to give more than one message to a worker at a time.
# RabbitMQ will dispatch the message to the next worker that is not still busy.
# A worker is busy until it has processed and acknowledged its currently assigned message.
# (Default behaviour: sends each message to next consumer in sequence (round-robin).)
channel.basic_qos(prefetch_count=1)
# Specify which function should receive messages from which queue (subscribing to queue).
# Default: message achnowledgments are turned on (important: don't forget
# basic_ack!).
channel.basic_consume(callback,
                      queue='task_queue')

# Enter never-ending loop that waits for data and runs callbacks whenever
# necessary.
channel.start_consuming()
