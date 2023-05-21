import pika
import sys
import time
import os
import threading

credentials = pika.PlainCredentials(username = "guest", password="guest")
connection = None
channel = None
mtx = threading.Lock()

def connectMQ():
    global connection, channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1", port=5672 , heartbeat=60))
    channel = connection.channel()

def reconnect():
    connectMQ()


def do_heartbeat():
    while True:
        time.sleep(30)
        print("heartbeat response")
        mtx.acquire()
        connection.process_data_events()
        mtx.release()
        
index = 0    
def sample_pub():
    global index
    ex = 'sample_ex'
    key = ['rk_A', 'rk_B']
    msg = 'Hello World'
    #print("Send message to exchange ...[%d]"%index)
    mtx.acquire()
    for n in range(2):
        try:
            channel.basic_publish(ex, key[n], msg.encode())
        except pika.exceptions.AMQPConnectionError as e:             
            print("[%d] Connection is closed [pika.exceptions.AMQPConnectionError]"%(n))
            reconnect()
            print("==== resend ====")
            channel.basic_publish(ex, key[n], msg.encode())
    mtx.release()

connectMQ()

t = threading.Thread(target=do_heartbeat, args=())
t.start()

while True:
    sample_pub()
    index += 1
    time.sleep(0.01)

print("Test end")
