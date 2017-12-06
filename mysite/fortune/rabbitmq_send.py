# Usage: type in the command $ python rabbitmq_send.py <category>
import pika
import sys


# (Connect to a broker on a different machine by specifying its name or IP address here.)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

category = ' '.join(sys.argv[1:]) or "all"
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=category)
print(" [x] Sent category %r" % category)

connection.close()
