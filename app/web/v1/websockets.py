from asyncio import sleep
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from markupsafe import escape
from app.config.config import STATUS_CODE, FORBIDDEN_TAGS
from app.utils.jwt_user import get_current_user_ws
from app.validation.pydantic_classes import UserData
from app.db.queries import (
    get_product_by_id,
    get_user_by_id
)

websockets_router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.chat_connections: dict[int, dict[str, WebSocket]] = {}

    async def connect(self, id_product: int, username: str, websocket: WebSocket):
        await websocket.accept()
        if id_product not in self.chat_connections:
            self.chat_connections[id_product] = {}
        self.chat_connections[id_product][username] = websocket

    def disconnect(self, id_product: int, username: str):
        if id_product in self.chat_connections:
            self.chat_connections[id_product].pop(username, None)
            if not self.chat_connections[id_product]:
                del self.chat_connections[id_product]

    async def send_personal_message(self, message: dict, username: str, id_product: int):
        websocket = self.chat_connections.get(id_product, {}).get(username)
        if websocket is not None:
            await websocket.send_json(message)

    async def broadcast(self, id_product: int, message: dict):
        for websocket in self.chat_connections.get(id_product, {}).values():
            await websocket.send_json(message)


manager = ConnectionManager()


@websockets_router.websocket("/chats/{id_product}")
async def chat(
        websocket: WebSocket,
        id_product: int,
        token: UserData = Depends(get_current_user_ws)
):
    await manager.connect(id_product=id_product, username=token.username, websocket=websocket)

    try:
        seller_id = get_product_by_id(product_id=id_product)['user_id']
        seller = get_user_by_id(user_id=seller_id)
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))

    seller_username = seller.get("username")
    notified = False

    try:
        while True:
            message = await websocket.receive_text()
            message = escape(message)

            seller_ws = manager.chat_connections.get(id_product, {}).get(seller_username)

            if seller_ws is None:
                if notified is True:
                    notified = False
                await websocket.send_json({
                    "name": "Chat",
                    "tag": "System",
                    "message": "Seller's not in the chat"
                })
                await sleep(5)

            elif notified is False:
                await websocket.send_json({
                    "name": "Chat",
                    "tag": "System",
                    "message": "Seller joined to the chat"
                })
                notified = True

            if len(message) > 1000:
                await websocket.send_json({
                    "name": "Chat",
                    "tag": "System",
                    "message": "Too big text"
                })

            elif any(tag in message.lower() for tag in FORBIDDEN_TAGS) and token.username != seller_username:
                await websocket.send_json({
                    "name": "Chat",
                    "tag": "System",
                    "message": "Please, don't try to scam"
                })

            else:
                await manager.broadcast(id_product, {
                    "name": token.username,
                    "tag": "(Seller)" if token.username == seller_username else "(Customer)",
                    "message": message
                })

    except WebSocketDisconnect:
        manager.disconnect(id_product=id_product, username=token.username)
        await websocket.close()
