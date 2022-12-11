import os
from fastapi import FastAPI, WebSocket, Cookie, Depends
from fastapi.responses import HTMLResponse
from jose import jwt

JWT_SECRET = os.environ.get('JWT_SECRET')
assert JWT_SECRET is not None, "Please set JWT_SECRET"

app = FastAPI()

async def auth_token(
    websocket: WebSocket,
    session: str | None = Cookie(default=None),
):
    print(session)
    if session is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    session = jwt.decode(session, JWT_SECRET)
    return session

@app.websocket("/")
async def websocket_endpoint(
    websocket: WebSocket,
    session: str = Depends(auth_token)
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"{session} : Message text was: {data}")
