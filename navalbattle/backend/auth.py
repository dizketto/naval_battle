import asyncio
import functools
import time
import typing as t

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import ODM
from models.auth_models import UserLoginSchema


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            valid, payload = await self.verify_jwt(credentials.credentials)
            if not valid:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return payload
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    async def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = await decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid, payload


async def check_mongo_user(data: UserLoginSchema):
    found_user = await ODM.UserSchema.find_one({"email": data.email})
    print(found_user)
    if found_user and found_user.password == data.password:
        return found_user
    return None


def get_jwt_info():
    def wrapping(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            jwt_info = {"secret": "awesome_secret", "algorithm": "HS256"}
            return await func(jwt_info, *args, **kwargs)

        return wrapper

    return wrapping


@get_jwt_info()
async def sign_jwt(
    jwt_info: t.Dict[str, str],
    user_id: str,
    username: str,
    user_email: str,
    payload: dict = dict(),
) -> t.Dict[str, str]:
    payload.update(
        {
            "user_id": user_id,
            "username": username,
            "user_email": user_email,
            "expires": time.time() + 60000,
        }
    )
    token = jwt.encode(payload, jwt_info["secret"], algorithm=jwt_info["algorithm"])
    return token_response(token)


def token_response(token):
    return {"access_token": token}


@get_jwt_info()
async def decodeJWT(jwt_info, token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, jwt_info["secret"], algorithms=jwt_info["algorithm"]
        )
        return decoded_token if decoded_token["expires"] >= time.time() else {}
    except:
        return {}
