import socketio


from app.models import votes
from app.models.game_discord import get_latest_pitches, get_random_pitches

origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
]


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
socket_app = socketio.ASGIApp(sio, static_files={"/": "app.html"})


async def send_votes():
    await sio.emit("votes", data=votes.data, namespace="/gamevotes")


@sio.event(namespace="/gamevotes")
async def connect(sid, environ):
    await sio.emit("latest_pitches", data=get_latest_pitches(), namespace="/gamevotes")
    await sio.emit("random_pitches", data=get_random_pitches(), namespace="/gamevotes")


@sio.event(namespace="/gamevotes")
async def votes_pls(sid, data):
    if data == "discordvotes":
        from app.discordbot import bot

        await sio.emit("votes_discord", data=bot.votes, namespace="/gamevotes")
    else:
        await sio.emit("votes", data=votes.data, namespace="/gamevotes")
