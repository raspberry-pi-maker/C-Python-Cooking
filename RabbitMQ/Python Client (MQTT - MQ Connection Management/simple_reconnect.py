import pika
import sys
import time
import os

credentials = pika.PlainCredentials(username = "guest", password="guest")
connection = None
channel = None

def connectMQ():
    global connection, channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1", port=5672 , heartbeat=60))
    channel = connection.channel()

def reconnect():
    connectMQ()
    
index = 0
def sample_pub():
    global index
    ex = 'sample_ex'
    key = ['rk_A', 'rk_B']
    msg = 'Hello World'
    print("Send message to exchange ...[%d]"%index)
    for n in range(2):
        try:
            channel.basic_publish(ex, key[n], msg.encode())
        except pika.exceptions.AMQPConnectionError as e:             
            print("[%d] Connection is closed [pika.exceptions.AMQPConnectionError]"%(n))
            reconnect()
            print("==== resend ====")
            channel.basic_publish(ex, key[n], msg.encode())


connectMQ()
print("Wait for disconnection ...")
time.sleep(4 * 60)    #After 4 minutes, the connection might be broken.

while True:
    sample_pub()
    time.sleep(5)
    if index == 2: break
    index += 1

print("Test end")
