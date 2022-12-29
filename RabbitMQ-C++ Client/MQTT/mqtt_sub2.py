import paho.mqtt.client as mqtt
import sys

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    if rc:
        print("connect failed rc: " + str(rc))
        sys.exit()
    else:    
        print("connected ")
    # Start subscribe, with QoS level 0
    mqttc.subscribe(topic)

def on_message(client, obj, msg):
    print("RCV topic[" + msg.topic + "] qos[" + str(msg.qos) + "]  patload[" + str(msg.payload) + "]") 

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " QOS:" + str(granted_qos))

topic = "topicA/topicB"
mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Parse CLOUDMQTT_URL (or fallback to localhost)
mqttc.connect("192.168.150.128", 1883)

# Continue the network loop, exit when an error occurs
mqttc.loop_forever()
