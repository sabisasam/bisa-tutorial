"""
Command for sending fortune to websocket using RabbitMQ.
"""
import json
import pika
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Class for sending instruction to send a fortune.
    """
    help = 'Send instruction to send a fortune (optionally of given category).'

    def add_arguments(self, parser):
        """
        Add argument 'category' to the parser.
        """
        parser.add_argument('-c', '--category', type=str,
                            dest='category', default='',
                            help='Specify a category for the fortune.' + \
                                 ' (Default: all categories)')

    def handle(self, *args, **options):
        """
        Sending instruction to send a fortune.
        """
        self.stdout.write('Start sending instruction.')

        # Connect to broker on different machine by specifying its name or IP address here.
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs',
                                 exchange_type='fanout')

        # Set category.
        category = options['category']
        if not category:
            category = ''
            self.stdout.write(self.style.WARNING(
                'The fortune will be of no specific category.'))

        message = json.dumps({ 'category': category })
        channel.basic_publish(exchange='logs',
                              routing_key='',
                              body=message)

        connection.close()

        self.stdout.write(self.style.SUCCESS(
            'Successfully sent instruction.'))
