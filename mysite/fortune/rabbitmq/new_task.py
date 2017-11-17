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

# Get or set message (specify message through '$ python new_task.py <your_message>').
message = ' '.join(sys.argv[1:]) or "Hello World!"
# Sending message.
channel.basic_publish(exchange='', # Allows to specify to which queue the message should go.
                                   # '' identifies default exchange (name of it), routes
                                   # messages to queue specified by routing_key if it exists.
                      routing_key='task_queue', # Queue name.
                      body=message, # Message.
                      properties=pika.BasicProperties( # Message properties.
                                                       # The AMQP 0-9-1 protocol predefines
                                                       # a set of 14 properties that go with
                                                       # a message. Most of them are rarely
                                                       # used, with the exception of
                                                       # 'delivery_mode', 'content_type'
                                                       # (used to describe the mime-type of
                                                       # the encoding), 'reply_to' (commonly
                                                       # used to name a callback queue) and
                                                       # 'correlation_id' (useful to correlate
                                                       # RPC responses with requests.).
                        delivery_mode = 2, # Make message persistent (save it to disk;
                                           # (not lost if RabbitMQ server stops).
                                           # Any other value makes message transient.
                      ))
print(" [x] Sent %r" % message)

# Close connection.
# Make sure that network buffers were flushed and message was actually delivered to RabbitMQ.
connection.close()
