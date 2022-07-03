from backend.auth import check_mongo_user, sign_jwt
from dbs.mongoclient import aiomongo
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from models import ODM
from models.api_models import UserLoginSchema

router = APIRouter(prefix="/user")


@router.post("/login")
async def user_login(user: UserLoginSchema):
    if found_user := await check_mongo_user(user):
        return await sign_jwt(str(found_user.id), found_user.username, found_user.email)
    return JSONResponse(status_code=403, content={"error": "Forbidden"})


@router.post("/signup")
async def create_user(user: ODM.UserSchema):

    already_existing_email = await ODM.UserSchema.find_one({"email": user.email})
    already_existing_username = await ODM.UserSchema.find_one(
        {"username": user.username}
    )

    if already_existing_email or already_existing_username:
        return JSONResponse(
            status_code=400,
            content={
                "Error": f"An user with this {'email' if already_existing_email else 'username'} already exists"
            },
        )

    new_user = await user.save()
    return await sign_jwt(str(new_user.id), new_user.username, new_user.email)
