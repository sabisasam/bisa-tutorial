# consumer, receives messages
import pika
import time


# establish connection with RabbitMQ server (broker on given machine (here: localhost))
# (connect to a broker on a different machine by specifying its name or IP address here)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# make sure that queue exists (like "get or create", queue_declare is idempotent)
# show existing queues and how many messages are in them with $ rabbitmqctl list_queues
# durable=True means the queue will be saved even if RabbitMQ server stops
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C (Unix) or CTRL+BREAK (Windows).')

# gets called when a message is received
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.')) # fake a second of work for every dot in the message
    print(" [x] Done")
    # send acknowledgment that message had been received and processed
    ch.basic_ack(delivery_tag = method.delivery_tag)

# tell RabbitMQ not to give more than one message to a worker at a time
# RabbitMQ will dispatch the message to the next worker that is not still busy
# (a worker is busy until it has processed and acknowledged its currently assigned message)
# default behaviour: RabbitMQ sends each message to next consumer in sequence (round-robin)
channel.basic_qos(prefetch_count=1)
# specify which function should receive messages from which queue
# default: message achnowledgments are turned on (important: don't forget basic_ack!)
channel.basic_consume(callback,
                      queue='task_queue')

# enter never-ending loop that waits for data and runs callbacks whenever necessary
channel.start_consuming()
