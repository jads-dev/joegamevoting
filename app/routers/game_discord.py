from os import name
from fastapi import Depends, APIRouter

from app.models.game_discord import get_game, get_game_platforms, pitch_game, get_game_pitches
from app.routers.auth import User, get_userid, get_optional_current_user
from pydantic import BaseModel, constr


class ParamsVote(BaseModel):
    upvote: bool
    poll: int = 0


class ParamsPitch(BaseModel):
    pitch: constr(max_length=2000)


router = APIRouter()


@router.get("/game_discord/{id}")
async def _get_game(id: int, user_id: int = Depends(get_userid)):
    game_data = get_game(id, user_id)
    if not game_data:
        return {"id": 0, "name": "Unmapped game", "summary": "Game needs to be mapped by Nodja :(", "release_date": None}
    else:
        return game_data


@router.get("/game_discord/{id}/pitches")
async def _get_game_pitches(id: int):
    return get_game_pitches(game_id=id)


@router.post("/game_discord/{id}/pitch")
async def _pitch_game(id: int, params: ParamsPitch, current_user: User = Depends(get_optional_current_user)):
    if current_user["can_vote"]:
        pitch_game(id, current_user["user_id"], params.pitch)


@router.get("/game_discord/platforms/{id}")
async def _get_game_platforms(id: int):
    return get_game_platforms(id)
