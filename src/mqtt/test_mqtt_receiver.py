import paho.mqtt.client as mqtt

broker_address = "192.168.43.48"  # Replace with your Raspberry Pi's IP
topic = "locker/append_log"

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message

client.connect(broker_address, 1883, 60)
client.subscribe(topic)

print("Listening for messages...")
client.loop_forever()
