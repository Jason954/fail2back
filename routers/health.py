from fastapi import APIRouter

from dependencies import send_command, query_db

router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)

@router.get("/back")
async def health_check_back():
    return "pong"


@router.get("/ban")
async def health_check_ban():
    return send_command("ping")
