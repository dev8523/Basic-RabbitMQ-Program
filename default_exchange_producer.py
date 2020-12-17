import pika

# Connect to RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Create a new queue called hello
channel.queue_declare(queue='hello')

# Add a message to the hello queue
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

# Close the connection
connection.close()
