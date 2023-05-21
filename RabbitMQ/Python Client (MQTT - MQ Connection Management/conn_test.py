import pika
import pika.exceptions
import sys
import time
import os
import socket



credentials = pika.PlainCredentials(username = "guest", password="guest")
connection = None
channel = None

def connectMQ():
    global connection, channel
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1", port=5672 , heartbeat=60, tcp_options={'TCP_KEEPIDLE':10}))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1", port=5672))
    channel = connection.channel()
    connect_close = connection.is_closed
    connect_open = connection.is_open
    channel_close = channel.is_closed
    channel_open = channel.is_open
    print("connection is_closed ", connect_close)
    print("connection is_open ", connect_open)
    print("channel is_closed ", channel_close)
    print("channel is_open ", channel_open)


i = 1
msg = f"Message {i}"

connectMQ()



cont = input("Enter to continue")

while True:
    try:
        time.sleep(5)
        print("heartbeat")
        connection.process_data_events()
        print("heartbeat--")
    except pika.exceptions.AMQPConnectionError as e:
        print("AMQPConnectionError exception")
        connectMQ()
    except pika.exceptions.StreamLostError as e:
        print("StreamLostError exception")
        break
    except KeyboardInterrupt:
        break




'''
RCV_SIZE = 4096 * 2
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 19999))
sock.settimeout(1)

while True:
    try:
        byte_addr_pair = sock.recvfrom(RCV_SIZE)
        msg  = byte_addr_pair[0].decode("utf-8") 
        print("RCV", msg)

    except socket.timeout:
        print("sock.recvfrom error")

    except Exception as e:
        print("sock.recvfrom error222")
'''