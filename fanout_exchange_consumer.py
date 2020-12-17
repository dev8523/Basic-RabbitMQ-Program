import pika

# Connect to RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declare the exchange in case it doesn't already exist
channel.exchange_declare(exchange='messages', exchange_type='fanout')

# declare a queue which gets deleted whenever the consumer process ends
# let RabbitMQ automatically assign the queue unused name
new_queue = channel.queue_declare(queue='', exclusive=True)
queue_name = new_queue.method.queue

# bind the newly created queue to the exchange
channel.queue_bind(exchange='messages', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C ')

# define the callback function
def callback(ch, method, properties, text):
    print(" [x] %r" % text)

# wait on messages to come into the queue
channel.basic_consume(on_message_callback=callback, queue=queue_name, auto_ack=True)

channel.start_consuming()
