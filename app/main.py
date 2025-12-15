from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database.database import init_db
from app.endpoints.metrics import metrics_router
from app.endpoints.measurement import measurement_router

init_db()

app = FastAPI()

app.include_router(metrics_router)
app.include_router(measurement_router)

EXCEPTIONS_TO_IGNORE = (
    ValueError,
    KeyError,
)

@app.exception_handler(Exception)
async def catch_all_exception_handler(request: Request, exc: Exception):
    import logging

    if isinstance(exc, EXCEPTIONS_TO_IGNORE):
        raise exc

    logging.error(f"Unhandled Server Error: {request.url} - {exc}")

    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected server error occurred.", "error_code": "INTERNAL_SERVER_ERROR"},
    )

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
