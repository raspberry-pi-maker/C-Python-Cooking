import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.150.128'))
channel = connection.channel()
channel.queue_declare(queue='hello') #If queue("Hello") does not exist, it creates the queue
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')