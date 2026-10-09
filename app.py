
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="WebSocket Messaging System",
    description="messaging using FastAPI WebSockets"
)

 
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()

@app.websocket("/ws")
async def websocket_connection(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()

            username = data.get("username")
            message = data.get("message")

            if not isinstance(username, str) or not username.strip():
                await websocket.send_json({
                    "error": "A valid username is required"
                })
                continue

            if not isinstance(message, str) or not message.strip():
                await websocket.send_json({
                    "error": "A valid message is required"
                })
                continue

            if message.strip().lower() == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "message": "pong"
                })
                continue

            current_time = datetime.now().strftime("%H:%M:%S")

            await websocket.send_json({
                "type": "message",
                "username": username.strip(),
                "message": message.strip(),
                "time": current_time
            })

    except WebSocketDisconnect:
        print("Client disconnected")
