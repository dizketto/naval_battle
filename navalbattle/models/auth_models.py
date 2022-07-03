from uuid import uuid4

from pydantic import UUID4, BaseModel, EmailStr, Field


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {"email": "abdulazeez@x.com", "password": "weakpassword"}
        }
