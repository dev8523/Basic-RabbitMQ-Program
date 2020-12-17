import pika
import sys

# Connect to RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Create a new fanout exchange called messages
channel.exchange_declare(exchange='topic_messages', exchange_type='topic')

# specify the message routing key and body
routing_key = sys.argv[1] if len(sys.argv) >= 2 else 'big.red.truck'
msg = ' '.join(sys.argv[2:]) or 'Hello From Producer...'

# send the message routing key and body
channel.basic_publish(exchange='topic_messages',
                      routing_key=routing_key, body=msg)

print(" [x] Sent %r:%r" % (routing_key, msg))

# Close the connection
connection.close()
