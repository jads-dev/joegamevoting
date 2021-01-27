import asyncio

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .discordbot import bot
from .models.game import calc_votes
from .routers import auth, game
from .routers.socketio import socket_app


app = FastAPI()


origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(game.router, prefix="/api", tags=["game"])

app.mount("/", socket_app)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.start("***REMOVED***"))
    await calc_votes()
