from enum import Enum
from typing import List

from pydantic import BaseModel


class GameStage(int, Enum):
    PREPARING = 0
    READY = 1
    OVER = 2


class GameData(BaseModel):
    stage: GameStage
    players_ready: List[str]
    board_width: int
    board_height: int
    players_left: List[str]
    next_turn: str


class ShipUnitData(BaseModel):
    center_x: int
    center_y: int
    vertical: bool
