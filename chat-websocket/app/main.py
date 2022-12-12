import os
from fastapi import FastAPI, WebSocket, Cookie, Depends, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from jose import jwt

JWT_SECRET = os.environ.get('JWT_SECRET')
assert JWT_SECRET is not None, "Please set JWT_SECRET"

app = FastAPI()

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
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

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
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
