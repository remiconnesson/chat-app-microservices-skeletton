import os
import asyncio
from fastapi import FastAPI, WebSocket, Cookie, Depends, WebSocketDisconnect
from jose import jwt
import redis

r = redis.Redis(host='redis', port=6379)

JWT_SECRET = os.environ.get('JWT_SECRET')
assert JWT_SECRET is not None, "Please set JWT_SECRET"

#
# WEBSOCKET MANAGER
#
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        # we make a copy to avoid iterating over a list that might be modified
        # during iteration.
        for connection in self.active_connections[:]:
            try:
                await connection.send_text(message)
            except RunTimeError as error:
                # this can happen if a websocket is closed during iteration.
                print(error)

manager = ConnectionManager()

# 
# BROADCAST TO WEBSOCKETS
#
def broadcast_chat_messages_from_redis(message_from_redis):
    async def async_wrapper ():
        await manager.broadcast(message_from_redis["data"].decode())
    asyncio.run(async_wrapper())

broadcaster = r.pubsub(ignore_subscribe_messages=True)
broadcaster.subscribe(**{'chat': broadcast_chat_messages_from_redis})

thread = broadcaster.run_in_thread(sleep_time=0.005, daemon=True)

#
# RECEIVE FROM WEBSOCKETS
# 
app = FastAPI()

async def auth_token(
    websocket: WebSocket,
    session: str | None = Cookie(default=None),
):
    if session is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    session = jwt.decode(session, JWT_SECRET)
    return session

@app.websocket("/")
async def websocket_endpoint(
    websocket: WebSocket,
    session: str = Depends(auth_token)
):
    client_id = session["id"]
    await manager.connect(websocket)
    try:
        while True:
            message_from_websocket = await websocket.receive_text()
            r.publish("chat", client_id + " says " + message_from_websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
