# Usage: type in the command $ python rabbitmq_send.py [category]
import json
import pika
import sys


# (Connect to a broker on a different machine by specifying its name or IP address here.)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

category = ' '.join(sys.argv[1:]) or ''
message = json.dumps({'category': category})
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
if category == '':
    print(" [x] Sent no specific category")
else:
    print(" [x] Sent category %r" % category)

connection.close()
