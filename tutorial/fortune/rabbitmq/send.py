# RabbitMQ tutorial - part 1 - "Hello world!"
# Producer, sends message.
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

# Sending message.
channel.basic_publish(exchange='',  # Allows to specify to which queue the message should go.
                      # '' identifies default exchange (name of it), routes
                      # messages to queue specified by routing_key if it
                      # exists.
                      routing_key='hello',  # Queue name.
                      body='Hello World!')  # Message.
print(" [x] Sent 'Hello World!'")

# Close connection.
# Make sure that network buffers were flushed and message was actually
# delivered to RabbitMQ.
connection.close()
