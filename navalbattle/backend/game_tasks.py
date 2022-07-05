import asyncio
import json
import random

from celery import Celery
from dbs.redis_client import redis
from models import ODM
from models.game_models import GameData, GameStage

celery = Celery("tasks", broker="amqp://guest:guest@rabbitmq:5672")


async def load_game_data(game_data: ODM.Game, game_id):
    random.shuffle(game_data.players)
    game_data = GameData(
        stage=GameStage.PREPARING,
        players_ready=[],
        board_width=game_data.settings.board_width,
        board_height=game_data.settings.board_height,
        players_left=game_data.players,
        next_turn=game_data.players[0],
    )

    result = await redis.hset(game_id, "gameboard", game_data.json())
    return result


@celery.task
def prepare_game(game_data):
    _game = ODM.Game(**game_data)
    print(_game)

    _result = asyncio.get_event_loop().run_until_complete(
        load_game_data(_game, str(game_data.get("id")))
    )
