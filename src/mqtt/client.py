from ..crud import create_log
from ..database import get_db
from fastapi import Depends
import json

topic = "lockers/append_log"  # The topic to subscribe to

# Define the callback function that will handle incoming messages
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to the topic when connected
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"Message received: {msg.payload.decode()}")  # Decode the byte message
    # Here you can process the message and call the create_log function
    # For example, if the message is in JSON format, you can parse it and create a log entry
    # Assuming the message payload is a JSON string that matches the LogCreate schema
    try:
        message_data = json.loads(msg.payload.decode())
        # Extract the necessary fields from the message data
        log_data = {
            "locker_id": message_data["locker_id"],
            "actor": message_data["actor"],
            "action": message_data["action"],
            "timestamp": message_data.get("timestamp")  # Optional field
        }
        # Call the create_log function with the extracted data
        db = Depends(get_db())
        print(f"created_log: {create_log(db, log_data)}")
    except Exception as e:
        print(f"Error processing message: {e}")