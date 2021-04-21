import time
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from .api import monitor, files
from .db.db_engine import engine, database
from .db.db_models import metadata
from .utils.logs import log_http_response, log_http_request, RestLogger
from .utils.http import HTTPFactory
from .utils.env import ACCESS_TOKEN_KEY, REQUEST_ID_KEY, REQUEST_TIME_KEY


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
    request_id = HTTPFactory.set_request_id(request)
    request.state.user, new_token = await HTTPFactory.instance.check_user_credentials(request)
    start_time = time.time()
    log_http_request(request.url, request.method, request.headers,
                     request.path_params)
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    response.headers[REQUEST_TIME_KEY] = str(process_time)
    response.headers[REQUEST_ID_KEY] = request_id
    if new_token:
        response.headers[ACCESS_TOKEN_KEY] = new_token
    log_http_response(formatted_process_time, response.status_code, response.headers)
    return response


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(monitor.router, prefix="/monitor", tags=["monitoring"])
app.include_router(files.router, prefix="/files", tags=["files"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
