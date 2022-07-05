import asyncio
import json
import typing as t

from api.const import ALLOCATON, SHIP_DATA, TRUNKS, Shooting
from backend.game_utils import trace_ship
from bson import ObjectId
from dbs.redis_client import redis
from models import ODM
from models.game_models import GameStage, ShipUnitData


def get_point(x: int, y: int, trunk: t.List[t.List[t.Any]]) -> t.List[int]:
    for coord in trunk:
        if [x, y] == coord[0:2]:
            return coord
    return None


def remove_unit(full_ship: t.List[int], point: t.List[int]) -> None:
    try:
        full_ship.remove(point)
    except ValueError:
        pass


def destroy(fleet: t.List[t.List[t.Any]], ship: ShipUnitData) -> None:
    for i in (-1, 1):
        remove_unit(
            fleet, [ship.center_x, ship.center_y + i]
        ) if ship.vertical else remove_unit(fleet, [ship.center_x + i, ship.center_y])


def remove_defeated_players(
    player: str, game_data: t.Dict[t.Any, t.Any]
) -> t.Dict[t.Any, t.Any]:
    if (not game_data[player][SHIP_DATA]) and player in game_data["players_left"]:
        game_data["players_left"].remove(player)


def check_shot(
    x: int, y: int, game_data: t.Dict[t.Any, t.Any], username: str
) -> t.Dict[str, t.Any]:
    shot_outcome = {}
    for player in filter(lambda x: x != username, game_data["players_left"]):
        player_ships_data = game_data[player]
        if [x, y] not in player_ships_data[SHIP_DATA]:
            shot_outcome.update({player: {"damage": Shooting.MISSED.name}})
        else:
            shot_outcome.update({player: {"damage": Shooting.HIT.name}})
            player_ships_data[SHIP_DATA].remove([x, y])

        if center_coords := get_point(x, y, player_ships_data[TRUNKS]):
            c_x, c_y, vert = center_coords
            full_ship = ShipUnitData(
                center_x=c_x,
                center_y=c_y,
                vertical=vert,
            )

            shot_outcome.update(
                {
                    player: {
                        "damage": Shooting.DESTROYED.name,
                        "boat": list(trace_ship(full_ship)),
                    }
                }
            )
            player_ships_data[TRUNKS].remove(center_coords)
            destroy(player_ships_data[SHIP_DATA], full_ship)

        remove_defeated_players(player, game_data)
    return shot_outcome


async def update_game_data_board(
    user_data: t.Dict[t.Any, t.Any],
    ship_data: ShipUnitData,
    game_data: t.Dict[t.Any, t.Any],
) -> t.Set[t.Tuple[int, int]]:

    username = user_data["username"]
    ship_coords = trace_ship(ship_data)
    game_data[username][SHIP_DATA].extend(list(ship_coords))
    game_data[username][TRUNKS].append(
        [ship_data.center_x, ship_data.center_y, ship_data.vertical]
    )
    game_data[username][ALLOCATON] -= 1

    if game_data[username][ALLOCATON] == 0:
        game_data["players_ready"].append(username)

    if set(game_data.get("players_left")) == set(game_data["players_ready"]):
        game_data["stage"] = GameStage.READY

    await redis.hset(user_data["game_id"], "gameboard", json.dumps(game_data))
    return ship_coords


async def close_game(game_id: str, winner: str) -> None:
    current_game: ODM.Game = await ODM.Game.find_one({"_id": ObjectId(game_id)})
    current_game.status = ODM.GameStatus.OVER
    current_game.winner = winner
    winning_user: ODM.UserSchema = await ODM.UserSchema.find_one({"username": winner})
    winning_user.score += 1
    save_tasks = [current_game.save(), winning_user.save()]
    await asyncio.gather(*save_tasks)


async def game_over_tasks(
    result: t.Dict[t.Any, t.Any],
    user_data: t.Dict[str, t.Any],
    game_data: t.Dict[t.Any, t.Any],
) -> None:
    username = user_data["username"]
    result.update({"winner": username, "message": "you won this game"})
    tasks = [
        redis.hset(user_data["game_id"], "gameboard", json.dumps(game_data)),
        close_game(user_data["game_id"], username),
    ]
    await asyncio.gather(*tasks)
