import json

from api.const import SHIP_DATA
from backend.auth import JWTBearer
from bson import ObjectId
from dbs.mongoclient import aiomongo
from dbs.redis_client import redis
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models import ODM
from models.ODM import UserSchema

router = APIRouter()
bearer = JWTBearer()


@router.get("/scores")
async def scores():
    users_list = await aiomongo.find(UserSchema, sort=UserSchema.score.desc())
    chart = enumerate(
        [{"user": user.username, "score": user.score} for user in users_list], 1
    )

    return JSONResponse(status_code=200, content={"scores": {x: y for x, y in chart}})


@router.get("/reveal")
async def reveal_map(username: str, user_data=Depends(bearer)):
    game_id = user_data.get("game_id")
    if not game_id:
        return JSONResponse(
            status_code=401, content={"error": "you don't have a game token"}
        )

    game_info = await redis.hget(game_id, "gameboard")
    if not game_info:
        return JSONResponse(
            status_code=403, content={"error": "this game has not started"}
        )

    game_info_dict = json.loads(game_info)
    if not username in game_info_dict:
        return JSONResponse(
            status_code=422,
            content={
                "error": f"{username} is not playing this game "
                "or has not added any ships"
            },
        )
    json_board = {}
    for i in range(game_info_dict["board_width"]):
        board_row = ""
        for j in range(game_info_dict["board_height"]):
            if [j, i] in game_info_dict[username][SHIP_DATA]:
                board_row += f"[{username[0]}]"
            else:
                board_row += "[ ]"

        json_board.update({i: board_row})

    return JSONResponse(status_code=200, content=json_board)
