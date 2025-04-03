from ..crud import create_log
from ..database import get_db
from fastapi import Depends
import json
from ..database import SessionLocal


topic = "lockers/append_log"  # The topic to subscribe to

# Define the callback function that will handle incoming messages
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to the topic when connected
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"Message received: {msg.payload.decode()}")  
    try:
        message_data = json.loads(msg.payload.decode())
        print(f"Message data: {message_data}")
        log_data = {
            "locker_id": message_data["locker_id"],
            "actor": message_data["actor"],
            "action": message_data["action"],
            "timestamp": message_data["timestamp"]
        }
        print(f"Log data: {log_data}")
        # Create a database session directly using SessionLocal
        db = SessionLocal()
        print(f"created_log: {create_log(db, log_data)}")
    except Exception as e:
        print(f"Error processing message: {e}")