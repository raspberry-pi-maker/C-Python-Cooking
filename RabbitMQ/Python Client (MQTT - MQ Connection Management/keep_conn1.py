import pika
import sys
import time
import os
import threading

credentials = pika.PlainCredentials(username = "guest", password="guest")
connection = None
channel = None

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
        connection.process_data_events()
        
connectMQ()

t = threading.Thread(target=do_heartbeat, args=())
t.start()

while True:
    time.sleep(1)

print("Test end")
