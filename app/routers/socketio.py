import os

import socketio


from app.models import votes

origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
]


if os.environ.get("ISDOCKER", False):
    manager = socketio.AsyncRedisManager("redis://")
    sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[], client_manager=manager)
else:
    sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])

socket_app = socketio.ASGIApp(sio, static_files={"/": "app.html"})


async def send_votes():
    await sio.emit("votes", data=votes.data, namespace="/gamevotes")


@sio.event(namespace="/gamevotes")
async def connect(sid, environ):
    await sio.emit("votes", data=votes.data, namespace="/gamevotes")
