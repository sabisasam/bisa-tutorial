# producer, sends message
import pika
import sys


# establish connection with RabbitMQ server (broker on given machine (here: localhost))
# (connect to a broker on a different machine by specifying its name or IP address here)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# make sure that queue exists (like "get or create", queue_declare is idempotent)
# show existing queues and how many messages are in them with $ rabbitmqctl list_queues
# durable=True means the queue will be saved even if RabbitMQ server stops
channel.queue_declare(queue='task_queue', durable=True)

# get or create message (specify message through $ python new_task.py your_message)
message = ' '.join(sys.argv[1:]) or "Hello World!"
# sending message
channel.basic_publish(exchange='', # allows to specify to which queue the message should go
                                   # '' identifies a default exchange
                      routing_key='task_queue', # queue name
                      body=message, # message
                      properties=pika.BasicProperties(
                        delivery_mode = 2, # make message persistent (save it to disk)
                                           # (not lost if RabbitMQ server stops)
                      ))
print(" [x] Sent %r" % message)

# close connection
# (make sure that network buffers were flushed and message was actually delivered to RabbitMQ)
connection.close()
