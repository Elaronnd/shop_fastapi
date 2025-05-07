from fastapi import APIRouter, Depends, status, HTTPException
from app.utils.jwt_user import get_current_user
from app.validation.pydantic_classes import UserData

websocket_router = APIRouter()


@websocket_router.websocket("/chat")
async def chat(current_user: UserData = Depends(get_current_user)):
    ...



