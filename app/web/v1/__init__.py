from fastapi import APIRouter
from app.web.v1.user import user_router
from app.web.v1.products import product_router
from app.web.v1.websocket import websocket_router
from app.web.v1.image import image_router

app_v1 = APIRouter(prefix="/v1")
app_v1.include_router(user_router)
app_v1.include_router(product_router)
app_v1.include_router(websocket_router)
app_v1.include_router(image_router)
