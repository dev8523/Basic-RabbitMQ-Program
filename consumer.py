import pika

# Connect to RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare the queue in case it doesn't already exist
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print("[x] Received %r" % body)


channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True
)

print('[*] Waiting for messages to exit press CTRL+C')

channel.start_consuming()
