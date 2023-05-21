import pika, sys, os
import time

work_time = int(sys.argv[1])

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.150.128'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(work_time)
    print("sleep %d seconds"%(work_time))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

channel.close()    