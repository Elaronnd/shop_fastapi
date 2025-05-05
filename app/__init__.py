from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.web.login import login_router
from app.db import first_start

@asynccontextmanager
async def lifespan(app: FastAPI):
    await first_start()
    yield

app = FastAPI(docs_url='/', lifespan=lifespan)
app.include_router(login_router)
