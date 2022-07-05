from enum import Enum
from typing import List, Optional

from bson.objectid import ObjectId
from dbs.mongoclient import aiomongo
from odmantic import Field, Model, Reference
from pydantic import BaseModel, EmailStr, Extra
from pydantic import Field as pydField


class MongoInterface:
    @classmethod
    async def find_one(cls, search_query: dict):
        return await aiomongo.find_one(cls, search_query)

    async def save(self):
        return await aiomongo.save(self)


class UserSchema(Model, MongoInterface):
    fullname: str
    email: EmailStr
    password: str
    username: str
    score: int = Field(0)

    class Config:
        collection = "user"
        schema_extra = {
            "example": {
                "fullname": "Usagi Yojimbo",
                "email": "usagi@yojimbo.net",
                "username": "uyojimbo",
                "password": "weakpassword",
            }
        }


class GameStatus(int, Enum):
    WAITING = 0
    STARTED = 1
    OVER = 2


class GameSettings(BaseModel):
    players_number: int = pydField(le=4, gt=1)
    board_width: int = pydField(le=10, ge=4)
    board_height: int = pydField(le=10, ge=4)

    class Config:
        schema_extra = {
            "example": {"board_width": "4", "board_height": "4", "players_number": "2"}
        }


class Game(Model, MongoInterface):
    settings: GameSettings
    created_by: UserSchema = Reference()
    winner: Optional[str]
    status: GameStatus
    players: List[str]

    class Config:
        collection = "games"
