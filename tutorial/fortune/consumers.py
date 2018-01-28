import json
import pika
import threading

from channels import Group
from channels.generic.websockets import WebsocketDemultiplexer

from .binding import CategoryBinding
from .models import Fortune


# belongs to Fortune Page - Websocket
class Demultiplexer(WebsocketDemultiplexer):

    consumers = {
        "fortune": CategoryBinding.consumer,
    }

    def connection_groups(self):
        return ["fortune-ws"]


# belongs to Fortune Page - RabbitMQ
def callback(ch, method, properties, body):
    category = json.loads(body)['category']
    print(" [.] Received message.")
    fortune = Fortune.fortune(category)
    Group('fortunes-mq').send({
        'text': json.dumps({'fortune': fortune})
    })
    print(
        " [.] Sent fortune of category %r to websocket.\n [x] Continue awaiting messages..." %
        category)


# belongs to Fortune Page - RabbitMQ
def rabbitmq_receive():
    # (Connect to a broker on a different machine by specifying its name or IP address here.)
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)
    channel = connection.channel()

    channel.exchange_declare(exchange='logs',
                             exchange_type='fanout')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs',
                       queue=queue_name)
    print(' [x] Waiting for messages...')

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()


# belongs to Fortune Page - RabbitMQ
class RunRabbitmqReceive(threading.Thread):
    started = False

    def run(self):
        rabbitmq_receive()


# belongs to Fortune Page - RabbitMQ
def ws_connect(message):
    Group("fortunes-mq").add(message.reply_channel)
    message.reply_channel.send({"accept": True})

    if not RunRabbitmqReceive.started:
        RunRabbitmqReceive().start()
        RunRabbitmqReceive.started = True


# belongs to Fortune Page - RabbitMQ
def ws_disconnect(message):
    Group("fortunes-mq").discard(message.reply_channel)
