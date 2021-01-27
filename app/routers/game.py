from os import name
from fastapi import Depends, APIRouter

from app.models.game import get_game_search, get_game, get_game_platforms, calc_votes, vote_game, get_game_voters, pitch_game, get_game_pitches
from app.routers.auth import User, get_userid, get_optional_current_user
from pydantic import BaseModel, constr


class ParamsVote(BaseModel):
    upvote: bool
    poll: int = 0


class ParamsPitch(BaseModel):
    pitch: constr(max_length=2000)


router = APIRouter()


@router.get("/game/search")
async def _get_games(search_term: str):
    return get_game_search(search_term)


@router.get("/game/{id}")
async def _get_game(id: int, user_id: int = Depends(get_userid)):
    return get_game(id, user_id)


@router.get("/game/{id}/voters")
async def _get_game_voters(id: int):
    return get_game_voters(poll=0, game_id=id)


@router.get("/game/{id}/pitches")
async def _get_game_pitches(id: int):
    return get_game_pitches(game_id=id)


@router.post("/game/{id}/vote")
async def _vote_game(id: int, params: ParamsVote, current_user: User = Depends(get_optional_current_user)):
    if current_user["can_vote"]:
        vote_game(params.poll, id, current_user["user_id"], params.upvote)
        await calc_votes()


@router.post("/game/{id}/pitch")
async def _pitch_game(id: int, params: ParamsPitch, current_user: User = Depends(get_optional_current_user)):
    if current_user["can_vote"]:
        pitch_game(id, current_user["user_id"], params.pitch)
        await calc_votes()


@router.get("/game/platforms/{id}")
async def _get_game_platforms(id: int):
    return get_game_platforms(id)


@router.get("/game_test")
async def test_shit():
    await calc_votes()