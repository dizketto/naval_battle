import asyncio
import json
import typing as t

from api.const import (
    ALLOCATION_ERROR,
    ALLOCATON,
    BOUNDARIES_ERROR,
    GAME_ERROR_TEXT,
    MAX_SHIP_UNITS,
    SHIP_DATA,
    TRUNKS,
    GameStatusError,
)
from api.utils import extract_game_info, get_game_viability
from backend.auth import JWTBearer, sign_jwt
from backend.context_lock import get_lock
from backend.game_backends import (
    check_shot,
    game_over_tasks,
    update_game_data_board,
)
from backend.game_tasks import prepare_game
from backend.game_utils import alive, is_consistent_ship, trace_ship
from dbs.redis_client import redis
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models import ODM
from models.game_models import GameStage, ShipUnitData

reusable_bearer = JWTBearer()
router = APIRouter()
simple_lock = asyncio.Lock()


@router.post("/game/create")
async def post_new_game(
    game_setting: ODM.GameSettings, user_data=Depends(reusable_bearer)
):

    hosting_user = await ODM.UserSchema.find_one(
        {"username": user_data.get("username")}
    )

    new_game = ODM.Game(
        settings=game_setting,
        status=ODM.GameStatus.WAITING,
        created_by=hosting_user,
        players=[user_data.get("username")],
    )

    game = await new_game.save()
    game_token = await sign_jwt(
        user_data["user_id"],
        user_data["username"],
        user_data["user_email"],
        {"game_id": str(game.id)},
    )
    response = {
        "game": json.loads(
            new_game.json(exclude={"winner": True, "created_by": True, "id": True})
        )
    }
    response.update(game_token)
    return JSONResponse(status_code=200, content=response)


@router.get("/game/join")
async def join_game(user_data=Depends(reusable_bearer)):
    query_games = (ODM.Game.status == ODM.GameStatus.WAITING) & (
        ODM.Game.players != user_data["username"]
    )

    async with simple_lock:
        joinable_game: ODM.Game = await ODM.Game.find_one(query_games)
        if not joinable_game:
            return JSONResponse(
                status_code=400,
                content={"game": "no joinable game found, start a new one if you wish"},
            )

        joinable_game.players.append(user_data["username"])

        if len(joinable_game.players) == joinable_game.settings.players_number:
            joinable_game.status = ODM.GameStatus.STARTED
            prepare_game.delay(json.loads(joinable_game.json()))

        game_info = extract_game_info(joinable_game)
        await joinable_game.save()
        game_token = await sign_jwt(
            user_data["user_id"],
            user_data["username"],
            user_data["user_email"],
            {"game_id": str(joinable_game.id)},
        )

    response = {"game": game_info}
    response.update(game_token)
    return JSONResponse(status_code=200, content=response)


@router.post("/game/add_ship")
async def new_ship(ship_data: ShipUnitData, user_data=Depends(reusable_bearer)):
    game_status_error = await get_game_viability(user_data)
    if game_status_error != GameStatusError.NO_ERROR:
        message = GAME_ERROR_TEXT[game_status_error]
        return JSONResponse(status_code=422, content={"error": message})

    username = user_data["username"]
    async with get_lock(f"{user_data['game_id']}-lock"):
        game_data = json.loads(await redis.hget(user_data["game_id"], "gameboard"))
        if not game_data:
            return JSONResponse(
                status_code=403,
                content={"error": "this game has probably expired"},
            )

        if username in game_data["players_ready"]:
            return JSONResponse(status_code=400, content=ALLOCATION_ERROR)

        if not username in game_data:
            game_data[username] = {
                SHIP_DATA: [],
                ALLOCATON: MAX_SHIP_UNITS,
                TRUNKS: [],
            }

        if not is_consistent_ship(username, ship_data, game_data):
            return JSONResponse(status_code=400, content=BOUNDARIES_ERROR)

        ship_coords = await update_game_data_board(user_data, ship_data, game_data)
        return JSONResponse(
            status_code=200,
            content={"game": f"ship added successfully: {ship_coords}"},
        )


@router.get("/game/shot/{x}/{y}")
async def shot(x: int, y: int, user_data=Depends(reusable_bearer)):
    game_status_error = await get_game_viability(user_data)
    if game_status_error != GameStatusError.NO_ERROR:
        message = GAME_ERROR_TEXT[game_status_error]
        return JSONResponse(status_code=400, content={"error": message})

    username = user_data["username"]
    game_data = json.loads(await redis.hget(user_data["game_id"], "gameboard"))

    if game_data["stage"] != GameStage.READY:
        return JSONResponse(
            status_code=422,
            content={"error": "this game is either in preparation or is finished"},
        )

    if not alive(username, game_data):
        return JSONResponse(
            status_code=200,
            content={"game_over": "this game is over for you, you lost."},
        )

    if game_data["next_turn"] != username:
        return JSONResponse(
            status_code=422,
            content={"error": f"not your turn, next in line: {game_data['next_turn']}"},
        )

    result = check_shot(x, y, game_data, username)

    if len(game_data["players_left"]) < 2:
        await game_over_tasks(result, user_data, game_data)
        return JSONResponse(status_code=200, content={"outcome": result})

    next_player = (game_data["players_left"].index(username) + 1) % len(
        game_data["players_left"]
    )
    game_data["next_turn"] = game_data["players_left"][next_player]
    await redis.hset(user_data["game_id"], "gameboard", json.dumps(game_data))
    return JSONResponse(status_code=200, content={"outcome": result})
