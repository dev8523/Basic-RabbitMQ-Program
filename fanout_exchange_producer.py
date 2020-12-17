import pika
import sys

# Connect to RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Create a new fanout exchange called messages
channel.exchange_declare(exchange='messages', exchange_type='fanout')

# Send a new message to the exchange
msg = ' '.join(sys.argv[1:]) or "info: RabbitMQ is cool!"
channel.basic_publish(exchange='messages', routing_key='', body=msg)

print(" [x] Sent %r " % msg)

# Close the connection
connection.close()
