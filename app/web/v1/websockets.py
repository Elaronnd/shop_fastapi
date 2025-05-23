from asyncio import sleep
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from app.config.config import STATUS_CODE, FORBIDDEN_TAGS
from app.utils.jwt_user import get_current_user_ws
from app.validation.pydantic_classes import UserData
from app.db.queries import (
    get_product_by_id,
    get_user_by_id
)
from typing import Dict

websockets_router = APIRouter()


active_chats: Dict[str, WebSocket] = {}


@websockets_router.websocket("/chats/{id_product}")
async def chat(
        websocket: WebSocket,
        id_product: int,
        token: UserData = Depends(get_current_user_ws)
):
    await websocket.accept()

    try:
        seller_id = get_product_by_id(product_id=id_product)['user_id']
        seller = get_user_by_id(user_id=seller_id)
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))

    seller_username = seller.get("username")
    active_chats[token.username] = websocket
    notified = False

    try:
        while True:
            message = await websocket.receive_text()

            if seller_username not in active_chats:
                if notified is True:
                    notified = False
                await websocket.send_json(
                    {
                        "name": "Chat",
                        "tag": "System",
                        "message": "Seller's not in the chat"
                    }
                )
                await sleep(5)
                continue

            if notified is False:
                await websocket.send_json(
                    {
                        "name": "Chat",
                        "tag": "System",
                        "message": "Seller joined to the chat"
                    }
                )
                notified = True

            if len(message) > 1000:
                await websocket.send_json(
                    {
                        "name": "Chat",
                        "tag": "System",
                        "message": "Too big text"
                    }
                )
            elif any(tag in message.lower() for tag in FORBIDDEN_TAGS) and token.username != seller_username:
                await websocket.send_json(
                    {
                        "name": "Chat",
                        "tag": "System",
                        "message": "Please, don't try to scam"
                    }
                )
            else:
                user_chat = active_chats[seller_username]
                await user_chat.send_json(
                    {
                        "name": token.username,
                        "tag": "(Seller)" if token.username == seller_username else "(Customer)",
                        "message": message
                    }
                )

    except WebSocketDisconnect:
        del active_chats[token.username]
        await websocket.close()
