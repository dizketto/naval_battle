from api.routers import authentication, game_api, stats
from fastapi import FastAPI

app = FastAPI(title="Naval Battle API")


app.include_router(
    game_api.router,
    tags=["Game"],
    prefix="/v1",
)

app.include_router(
    authentication.router,
    tags=["Authentication"],
    prefix="/v1",
)

app.include_router(
    stats.router,
    tags=["Stats"],
    prefix="/v1",
)
