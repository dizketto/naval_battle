import typing as t

from api.const import BOARD_HEIGHT, BOARD_WIDTH, SHIP_DATA
from models.game_models import ShipUnitData


def trace_ship(ship: ShipUnitData) -> t.Set[t.Tuple]:
    if ship.vertical == True:
        return {
            (ship.center_x, ship.center_y - 1),
            (ship.center_x, ship.center_y),
            (ship.center_x, ship.center_y + 1),
        }
    return {
        (ship.center_x - 1, ship.center_y),
        (ship.center_x, ship.center_y),
        (ship.center_x + 1, ship.center_y),
    }


def _overlaps(new_ship: ShipUnitData, existing_ship: t.List[t.Tuple]) -> bool:
    print(existing_ship)
    existing_ship_coords = set([tuple(coord) for coord in existing_ship])
    new_ship_coords = trace_ship(new_ship)
    print(new_ship_coords)
    if new_ship_coords.intersection(existing_ship_coords):
        return True
    return False


def is_consistent_ship(
    username: str, new_ship: ShipUnitData, game_data: t.Dict[t.Any, t.Any]
) -> bool:
    consistent = False
    board_width = game_data[BOARD_WIDTH]
    board_heigth = game_data[BOARD_HEIGHT]

    if new_ship.vertical == False:
        if (1 <= new_ship.center_x < board_width - 1) and (
            0 <= new_ship.center_y < board_heigth
        ):
            consistent = True
    else:
        if (0 <= new_ship.center_x < board_width) and (
            1 <= new_ship.center_y < board_heigth - 1
        ):
            consistent = True

    if _overlaps(new_ship, game_data[username][SHIP_DATA]):
        return False

    return consistent


def alive(username: str, game_data: t.Dict[t.Any, t.Any]) -> bool:
    return username in game_data["players_left"]
