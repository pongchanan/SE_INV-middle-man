import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()
broker = os.getenv("MQTT_BROKER")
if not broker:
    raise Exception("MQTT_BROKER not found in environment variables")
port = int(os.getenv("MQTT_PORT"))
if not port:
    raise Exception("MQTT_PORT not found in environment variables")

# Callback for when a client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected to broker with result code {rc}")
    client.subscribe("test/topic")

# Callback for when a message is received
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

def connect_mqtt(broker, port):
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(broker, port, 60)
    mqtt_client.loop_start()
    mqtt_client.subscribe("test/topic")

# Connect to the external broker
connect_mqtt(broker, port)
