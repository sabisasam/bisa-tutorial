import pika

from channels import Group

# from .models import Fortune


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='fortunes_mq')

def send_to_websocket(fortune):
    #Group("fortunes-mq").send({
    #    'text': json.dumps({
    #        'fortune': fortune
    #    })
    #})
    return 'Sent fortune to websocket.'

def on_request(ch, method, props, body):
    print(" [.] Received request from client.")
    category = str(body)
    if category == 'all':
        print(" [.] Get fortune of no specific category.")
        fortune = 'This is a placeholder for a fortune.' # Fortune.fortune()
    else:
        print(" [.] Get fortune of category '%s'." % category)
        fortune = 'This is a placeholder for a fortune.' # Fortune.fortune(category)
    print(" [.] Send fortune to websocket.")
    response = send_to_websocket(fortune)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to, # Callback queue given from client.
                     properties=pika.BasicProperties(
                        correlation_id = props.correlation_id),
                     body=str(response))

    ch.basic_ack(delivery_tag = method.delivery_tag)
    print(" [.] Request has been processed.\n [x] Continue awaiting requests...")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request,
                      queue='fortunes_mq')

print(" [x] Awaiting requests...")
channel.start_consuming()
