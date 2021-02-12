import datetime

from os import name
from fastapi import Depends, APIRouter

from app.models.game_discord import (
    get_game,
    get_game_platforms,
    pitch_game,
    get_game_pitches,
    get_game_voters,
    get_latest_pitches,
    get_random_pitches,
    get_votes,
    get_voters,
    get_stats,
    get_vote_files,
    get_vote_file,
)
from app.routers.auth import User, get_userid, get_optional_current_user
from app.routers.socketio import sio
from pydantic import BaseModel, constr


class ParamsVote(BaseModel):
    upvote: bool
    poll: int = 0


class ParamsPitch(BaseModel):
    pitch: constr(max_length=2000)


router = APIRouter()


@router.get("/game_discord/random_pitches/")
async def _get_random_pitches():
    return get_random_pitches()


@router.get("/game_discord/vote_files/")
async def _get_vote_files():
    return get_vote_files()


@router.get("/game_discord/vote_file/{file}")
async def _get_vote_file(file: str):
    return get_vote_file(file)


@router.get("/game_discord/weeb_status/")
async def _weeb_status(votes: int):
    from app.discordbot import bot

    await bot.check_weeb()
    await sio.emit("votes_discord", data=bot.votes, namespace="/gamevotes")


@router.get("/game_discord/test/{votes}")
async def _test(votes: int):
    if votes > 0:
        await sio.emit("votos_time", data=datetime.datetime.now().isoformat(), namespace="/gamevotes")
    else:
        await sio.emit("votos_time", data=None, namespace="/gamevotes")
    return ""


@router.get("/game_discord/votes/")
async def _get_votes():
    return get_votes()


@router.get("/game_discord/voters/")
async def _get_voters():
    return get_voters()


@router.get("/game_discord/stats/")
async def _get_stats():
    return get_stats()


@router.get("/game_discord/{id}")
async def _get_game(id: int, user_id: int = Depends(get_userid)):
    game_data = get_game(id, user_id)

    return game_data


@router.get("/game_discord/{id}/voters")
async def _get_game_voters(id: int):
    return get_game_voters(message_id=id)


@router.get("/game_discord/{id}/pitches")
async def _get_game_pitches(id: int):
    return get_game_pitches(message_id=id)


@router.post("/game_discord/{id}/pitch")
async def _pitch_game(id: int, params: ParamsPitch, current_user: User = Depends(get_optional_current_user)):
    if current_user["can_vote"]:
        pitch_game(id, current_user["user_id"], params.pitch)
        await sio.emit("latest_pitches", data=get_latest_pitches(), namespace="/gamevotes")


@router.get("/game_discord/platforms/{id}")
async def _get_game_platforms(id: int):
    return get_game_platforms(id)
