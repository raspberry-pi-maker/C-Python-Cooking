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

def sample_pub():
    ex = 'sample_ex'
    key = ['rk_A', 'rk_B']
    msg = 'Hello World'
    for n in range(2):
        channel.basic_publish(ex, key[n], msg.encode())


connectMQ()
sample_pub()

