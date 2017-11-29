import pika
import uuid


class FortuneClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response,
                                   no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    # Send request and block until associated response is received.
    def call(self, category='all'):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='fortunes_mq',
                                   properties=pika.BasicProperties(
                                        reply_to = self.callback_queue,
                                        correlation_id = self.corr_id),
                                   body=category)
        # Blocking part.
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)


fortune_client = FortuneClient()

print(" [x] Send request to RabbitMQ server to send a fortune to websocket.")
response = fortune_client.call()
print(" [.] Message from RabbitMQ server: %r" % response)
