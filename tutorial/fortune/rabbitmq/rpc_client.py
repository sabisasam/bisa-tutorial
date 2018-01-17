# RabbitMQ tutorial - part 6 - remote procedure call (RPC)
# Client, sends request, waits for reply.
import pika
import uuid


class FibonacciRpcClient(object):
    # If an instance of 'FibonacciRpcClient' gets created, this function will
    # be executed.
    def __init__(self):
        # Establish connection with RabbitMQ server (broker on given machine (here: localhost)).
        # (Connect to a broker on a different machine by specifying its name or IP address here.)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # Create a fresh, empty callback queue for replies.
        # If no name for queue is specified (like here) the server will choose a random name.
        # 'exclusive=True' means the queue will be deleted if the consumer disconnects.
        # In order to receive a response the client needs to send the callback queue address
        # with the request.
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue  # Get the random queue name.

        # Specify which function should receive messages from which queue.
        # (Subscribing to the callback queue so that we can receive RPC responses.)
        self.channel.basic_consume(self.on_response,
                                   no_ack=True,
                                   # Turn off message acknowledgments.
                                   # Messages will be lost if worker dies, including
                                   # all messages that were dispatched to this worker.
                                   queue=self.callback_queue)

    # Declaring a callback for 'basic_consume'.
    # This function will be executed on every response message to the callback
    # queue.
    def on_response(self, ch, method, props, body):
        # Check if the 'correlation_id' of the message matches the value from
        # the request.
        if self.corr_id == props.correlation_id:
            # If it matches, the function saves the response in 'self.response' which breaks
            # the consuming loop of the function 'call'.
            self.response = body

    # This function sends an RPC request and blocks until the answer is
    # received.
    def call(self, n):
        self.response = None  # Delete older response.
        # Generate and save a unique 'correlation_id' number.
        self.corr_id = str(uuid.uuid4())
        # Sending request message to exchange.
        self.channel.basic_publish(exchange='',  # Default exchange, routes messages to queue specified
                                   # by routing_key if it exists.
                                   routing_key='rpc_queue',  # Queue name.
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
                                       # 'reply_to' and 'correlation_id'.
                                       reply_to=self.callback_queue,  # Commonly used to name a
                                       # callback queue.
                                       # (There will be only one
                                       # callback queue created
                                       # per client. This queue
                                       # will receive all those
                                       # responses belonging to
                                       # the client's requests.)
                                       correlation_id=self.corr_id),  # Useful to correlate RPC
                                   # responses with requests.
                                   # (Will be set to a unique
                                   # value for every request so
                                   # we will be able to match a
                                   # response with a request.)
                                   # (Messages with an unknown
                                   # correlation_id don't belong
                                   # to our requests and will be
                                   # discarded.)
                                   body=str(n))  # Message.
        # Wait until data sent to callback queue is accepted by function
        # 'on_response'.
        while self.response is None:
            self.connection.process_data_events()
        # Return result, converted to an integer.
        return int(self.response)


# Create an instance of class 'FibonacciRpcClient' (directly when the
# client starts up).
fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
# Request 30. fibonacci number.
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)
