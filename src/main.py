from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine
import models
from routers import locker, organization, service_request, log, qr_gen
from fastapi.middleware.cors import CORSMiddleware

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
