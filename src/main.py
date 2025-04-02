from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine
import models
from routers import locker, organization, service_request, log, qr_gen
from dotenv import load_dotenv
import os
# from mqtt.client import connect_mqtt
# import asyncio
# from hbmqtt.broker import Broker

# # Broker configuration dictionary
# config = {
#     'listeners': {
#         'default': {
#             'type': 'tcp',
#             'bind': '0.0.0.0:1883'  # Bind to all interfaces on port 1883
#         }
#     },
#     'sys_interval': 10,
#     'topic-check': {
#         'enabled': False
#     }
# }

# broker = Broker(config)

# async def start_broker():
#     await broker.start()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(start_broker())
# loop.run_forever()

# load_dotenv()
# broker = os.getenv("MQTT_BROKER")
# if not broker:
#     raise Exception("MQTT_BROKER not found in environment variables")
# port = int(os.getenv("MQTT_PORT"))
# if not port:
#     raise Exception("MQTT_PORT not found in environment variables")

# connect_mqtt(broker, port)

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    engine.dispose()

app = FastAPI(title="Locker Service API", lifespan=lifespan)

app.include_router(locker.router)
app.include_router(log.router)
app.include_router(organization.router)
app.include_router(service_request.router)
app.include_router(qr_gen.router)


@app.get("/")
def root():
    return {"message": "Service API is running"}
