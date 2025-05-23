from fastapi import APIRouter
from app.web.v1.users import users_router
from app.web.v1.products import products_router
from app.web.v1.websockets import websockets_router
from app.web.v1.images import images_router

app_v1 = APIRouter(prefix="/v1")
app_v1.include_router(users_router)
app_v1.include_router(products_router)
app_v1.include_router(websockets_router)
app_v1.include_router(images_router)
