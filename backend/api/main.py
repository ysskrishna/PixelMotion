from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import asyncio
import threading

# Load config from .env file
from app.core.config import config

from app.routers.user import router as user_router
from app.core.utils import connected_websockets
from app.listeners.task_updates import task_updates_listener

# Create FastAPI instance
app = FastAPI()

# CORS middleware (for development, adjust as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/user", tags=["user"])


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return """
    <html>
    <head>
        <title>PixelMotion</title>
    </head>
    <body>
        <h1>PixelMotion</h1>
        <p>Image to Video Generator API</p>
    </body>
    </html>
    """




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)
    try:
        while True:
            await asyncio.sleep(1)  # Keep websocket connection open
    except WebSocketDisconnect:
        connected_websockets.remove(websocket)

if __name__ == '__main__':
    threading.Thread(target=task_updates_listener, daemon=True).start()
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)