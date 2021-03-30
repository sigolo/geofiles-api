from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api import monitor, items
from .db.db_engine import engine, database
from .db.db_models import metadata

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


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(monitor.router, prefix="/monitor", tags=["monitoring"])
app.include_router(items.router, prefix="/items", tags=["items"])