from fastapi import FastAPI
from database import Base, engine
import models
from routers import service_request

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Locker Service API")

app.include_router(service_request.router)

@app.get("/")
def root():
    return {"message": "Service API is running"}
