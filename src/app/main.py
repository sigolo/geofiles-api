import uuid
import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from .api import monitor, files
from .db.db_engine import engine, database
from .db.db_models import metadata
from .utils.logs import RestLogger

LogInstance = RestLogger.instance
RestLogger.init_logger()
metadata.create_all(engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_request_id_process_time_header(request: Request, call_next):
    request_id = str(uuid.uuid4()) if "X-Request-ID" not in request.headers else request.headers["X-Request-ID"]
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id
    LogInstance.request_id = request_id
    LogInstance.log_http_response(formatted_process_time, response.status_code)
    return response


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(monitor.router, prefix="/monitor", tags=["monitoring"])
app.include_router(files.router, prefix="/files", tags=["files"])
