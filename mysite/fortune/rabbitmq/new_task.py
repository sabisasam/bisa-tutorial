# RabbitMQ tutorial - part 2 - work queues
# Producer, sends message.
import pika
import sys


# Establish connection with RabbitMQ server (broker on given machine (here: localhost)).
# (Connect to a broker on a different machine by specifying its name or IP address here.)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Make sure that queue exists (like "get or create", queue_declare is idempotent).
# Show existing queues and how many messages are in them with '$ rabbitmqctl list_queues'.
# 'durable=True' means the queue will be saved even if RabbitMQ server stops.
channel.queue_declare(queue='task_queue', durable=True)

# Get or set message (specify message through '$ python new_task.py your_message').
message = ' '.join(sys.argv[1:]) or "Hello World!"
# Sending message.
channel.basic_publish(exchange='', # Allows to specify to which queue the message should go.
                                   # '' identifies default exchange (name of it), routes
                                   # messages to queue specified by routing_key if it exists.
                      routing_key='task_queue', # Queue name.
                      body=message, # Message.
                      properties=pika.BasicProperties(
                        delivery_mode = 2, # Make message persistent (save it to disk;
                                           # (not lost if RabbitMQ server stops).
                      ))
print(" [x] Sent %r" % message)

# Close connection.
# Make sure that network buffers were flushed and message was actually delivered to RabbitMQ.
connection.close()
