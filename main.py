from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from mongoengine import connect

from fastapi.middleware.cors import CORSMiddleware

import json
from chatentry import ChatEntry 
app = FastAPI()
connected_users = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static", html=True, check_dir=False), name="static")
MONGODB_URI = "mongodb://localhost:27017/chat_app"
connect(host=MONGODB_URI)

@app.get("/")
def read_html():
    return FileResponse("static/index.html", media_type="text/html")


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: str, websocket: WebSocket):
    await websocket.accept()

    connected_users[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            new_entry = ChatEntry(timestamp = datetime.utcnow(), user = user_id, message = data)
            new_entry.save()
            for user, user_ws in connected_users.items():
                if user != user_id:
                    await user_ws.send_text(data)
    except:
        del connected_users[user_id]
        await websocket.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)