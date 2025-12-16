import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.database import init_db, close_db
from app.endpoints.metrics import metrics_router
from app.endpoints.measurement import measurement_router

logger = logging.getLogger("api") # Use a specific logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

    await close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(metrics_router)
app.include_router(measurement_router)

EXCEPTIONS_TO_IGNORE = (
    ValueError,
    KeyError,
)

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
