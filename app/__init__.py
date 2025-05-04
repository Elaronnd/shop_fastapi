from fastapi import FastAPI
from app.web.login import login_router

app = FastAPI(docs_url='/')
app.include_router(login_router)
