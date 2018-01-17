# RabbitMQ tutorial - part 6 - remote procedure call (RPC)
# Server, waits for request, sends reply.
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
channel.queue_declare(queue='rpc_queue')

# Declaring fibonacci function, assumes only valid positive integer input.


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

# Declaring a callback for 'basic_consume', the core of the RPC server.
# Gets called when a request message is received.


def on_request(ch, method, props, body):
    n = int(body)
    print(" [.] fib(%s)" % n)
    response = fib(n)

    # Send response message with result to exchange.
    ch.basic_publish(exchange='',  # Default exchange, routes messages to queue specified
                     # by routing_key if it exists.
                     routing_key=props.reply_to,  # Queue name.
                     # (Using callback queue given from client.)
                     properties=pika.BasicProperties(  # Message properties.
                         # The AMQP 0-9-1 protocol predefines
                         # a set of 14 properties that go with
                         # a message. Most of them are rarely
                         # used, with the exception of
                         # 'delivery_mode' (marks a message as
                         # persistent (with a value of 2) or
                         # transient (any other value)),
                         # 'content_type' (used to describe
                         # the mime-type of the encoding),
                         # 'reply_to' (commonly used to name a
                         # callback queue) and 'correlation_id'.
                         correlation_id=props.correlation_id),  # Useful to correlate RPC
                     # responses with requests.
                     # (Will be set to a unique
                                                                # value for every request so
                                                                # we will be able to match a
                                                                # response with a request.)
                                                                # (Messages with an unknown
                                                                # correlation_id don't belong
                                                                # to our requests and will be
                                                                # discarded.)
                     body=str(response))  # Message.

    # Send acknowledgment that request message had been received and processed.
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Tell RabbitMQ not to give more than one message to a server at a time.
# RabbitMQ will dispatch the message to the next server that is not still busy.
# A server is busy until it has processed and acknowledged its currently assigned message.
# (Default behaviour: sends each message to next consumer in sequence (round-robin).)
channel.basic_qos(prefetch_count=1)
# Specify which function should receive messages from which queue.
channel.basic_consume(on_request,
                      queue='rpc_queue')

print(" [x] Awaiting RPC requests")
# Enter never-ending loop that waits for data and runs callbacks whenever
# necessary.
channel.start_consuming()
