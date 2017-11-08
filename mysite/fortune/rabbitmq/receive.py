# consumer, receives messages
import pika


# establish connection with RabbitMQ server (broker on given machine (here: localhost))
# (connect to a broker on a different machine by specifying its name or IP address here)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# make sure that queue exists (like "get or create", queue_declare is idempotent)
# show existing queues and how many messages are in them with $ rabbitmqctl list_queues
channel.queue_declare(queue='hello')

# gets called when a message is received
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# specify which function should receive messages from which queue
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True) # turn off message acknowledgments
                                   # messages will be lost if worker dies, including
                                   # all messages that were dispatched to this worker

# enter never-ending loop that waits for data and runs callbacks whenever necessary
print(' [*] Waiting for messages. To exit press CTRL+C (Unix) or CTRL+BREAK (Windows).')
channel.start_consuming()
