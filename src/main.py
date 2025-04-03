from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import engine
from . import models
from .routers import locker, organization, service_request, log, qr_gen
from fastapi.middleware.cors import CORSMiddleware

import paho.mqtt.client as mqtt
from .mqtt.client import on_connect, on_message

# Define the MQTT settings
broker = "152.42.220.156"  # The IP address of your MQTT broker
port = 1883  # Default MQTT port (use 8883 if SSL/TLS is enabled)

# Set up the client and assign the callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker, port, 60)

# Loop forever to listen for messages
client.loop_forever()


models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    engine.dispose()

app = FastAPI(title="Locker Service API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(locker.router)
app.include_router(log.router)
app.include_router(organization.router)
app.include_router(service_request.router)
app.include_router(qr_gen.router)


@app.get("/")
def root():
    return {"message": "Service API is running"}
