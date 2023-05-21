import pika
import sys
import time
import os
import threading
import functools

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
        #time.sleep(0.0001)
        print("heartbeat response")
        connection.add_callback_threadsafe(lambda: connection.process_data_events())    
        '''
        connection.add_callback_threadsafe(
            functools.partial(
                connection.process_data_events
            )
        )  
        '''    
        
index = 0    
def sample_pub():
    global index
    ex = 'sample_ex'
    key = ['rk_A', 'rk_B']
    msg = 'Hello World'
    #print("Send message to exchange ...[%d]"%index)
    for n in range(2):
        try:
            connection.add_callback_threadsafe(lambda: channel.basic_publish(ex, key[n], msg.encode()))    
        except pika.exceptions.AMQPConnectionError as e:             
            print("[%d] Connection is closed [pika.exceptions.AMQPConnectionError]"%(n))
            reconnect()
            print("==== resend ====")
            connection.add_callback_threadsafe(lambda: channel.basic_publish(ex, key[n], msg.encode()))    
            '''
            connection.add_callback_threadsafe(
                functools.partial(
                    channel.basic_publish,
                    exchange = ex,
                    routing_key = key[n],
                    body = msg.encode()
                )
            )  
            '''            

connectMQ()

t = threading.Thread(target=do_heartbeat, args=())
t.start()

while True:
    sample_pub()
    index += 1
    #time.sleep(0.01)

print("Test end")
