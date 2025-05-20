from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.web.v1 import app_v1
from app.db import first_start
from app.config.config import TAGS_METADATA

@asynccontextmanager
async def lifespan(app: FastAPI):
    await first_start()
    yield

app = FastAPI(docs_url='/', lifespan=lifespan, openapi_tags=TAGS_METADATA)
app.include_router(app_v1)

