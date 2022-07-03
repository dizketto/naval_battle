import typing as t
from enum import Enum

from api.const import GameStatusError
from bson import ObjectId
from models import ODM


def extract_game_info(game: ODM.Game):
    return {
        "created_by": game.created_by.username,
        "game_settings": game.settings.dict(),
        "game_status": ODM.GameStatus(game.status).name,
        "game_id": str(game.id),
        "total_player_slots": game.settings.players_number,
        "player_slots_left": game.settings.players_number - len(game.players),
        "players": game.players,
    }


async def get_game_viability(user_data: t.Dict[t.Any, t.Any]) -> GameStatusError:
    game_created: ODM.Game = await ODM.Game.find_one(
        {"_id": ObjectId(user_data["game_id"])}
    )
    if not game_created:
        return GameStatusError.NOT_EXISTING

    if game_created.status == ODM.GameStatus.WAITING:
        return GameStatusError.NOT_STARTED

    if game_created.status == ODM.GameStatus.OVER:
        return GameStatusError.NOT_PLAYABLE

    return GameStatusError.NO_ERROR
