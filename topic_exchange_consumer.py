import pika
import sys

# Connect to RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declare the exchange in case it doesn't already exist
channel.exchange_declare(exchange='topic_messages', exchange_type='topic')

# declare a queue which gets deleted whenever the consumer process ends
# let RabbitMQ automatically assign the queue unused name
new_queue = channel.queue_declare(queue='', exclusive=True)
queue_name = new_queue.method.queue

# get the binding keys from command line arguments
binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Add binding keys with spaces between them: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

# add the binding keys to the queue
for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_messages',
                       queue=queue_name, routing_key=binding_key)

print(' [*] Waitng for messages. To exit press CTRL+C')

# Display the message text and routing key


def callback(ch, method, properties, text):
    print(" [x] %r:%r" % (method.routing_key, text))


# start monitoring the queue
channel.basic_consume(on_message_callback=callback, queue=queue_name, auto_ack=True)


channel.start_consuming()
