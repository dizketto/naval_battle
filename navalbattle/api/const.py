from enum import Enum

MAX_SHIP_UNITS = 2
ALLOCATON = "allocation"
SHIP_DATA = "ship_data"
TRUNKS = "ship_trunks"
BOARD_WIDTH = "board_width"
BOARD_HEIGHT = "board_height"

BOUNDARIES_ERROR = {
    "error": "the ship center is not consistent with gameboard's boundaries "
    "or overlaps with another ship"
}

ALLOCATION_ERROR = {"error": "you already have all ships allocated"}


class GameStatusError(int, Enum):
    NO_ERROR = 0
    NOT_EXISTING = 1
    NOT_STARTED = 2
    NOT_PLAYABLE = 3


class Shooting(int, Enum):
    MISSED = 0
    HIT = 1
    DESTROYED = 2


GAME_ERROR_TEXT = {
    GameStatusError.NOT_EXISTING: "The game you want to play was not found on this server, please create or join another game.",
    GameStatusError.NOT_STARTED: "The game has not started yet, waiting for other players to join",
    GameStatusError.NOT_PLAYABLE: "The game you want to play has finished, please create or join another game",
}
