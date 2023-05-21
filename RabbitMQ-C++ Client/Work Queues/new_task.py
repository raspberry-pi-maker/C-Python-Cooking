#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.150.128'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

for x in range(10):
    message = "Hello World! [%d]"%(x)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
        ))
    print(" [x] Sent %r" % message)
connection.close()