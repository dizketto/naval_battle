import typing as t
from pydantic import BaseModel, EmailStr


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {"email": "usagi@yojimbo.net", "password": "weakpassword"}
        }
