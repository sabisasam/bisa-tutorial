# producer, sends message
import pika


# establish connection with RabbitMQ server (broker on given machine (here: localhost))
# (connect to a broker on a different machine by specifying its name or IP address here)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# make sure that queue exists (like "get or create", queue_declare is idempotent)
# show existing queues and how many messages are in them with $ rabbitmqctl list_queues
channel.queue_declare(queue='hello')

# sending message
channel.basic_publish(exchange='', # allows to specify to which queue the message should go
								   # '' identifies a default exchange
                      routing_key='hello', # queue name
                      body='Hello World!') # message
print(" [x] Sent 'Hello World!'")

# close connection
# (make sure that network buffers were flushed and message was actually delivered to RabbitMQ)
connection.close()
