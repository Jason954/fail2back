import json
from typing import List

from fastapi import APIRouter

from dependencies import query_db
from models.ban import Ban
from utils.convert import convert_query_to_ban_model

router = APIRouter(
    prefix="/globalbans",
    tags=["globalbans"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[Ban])
async def read_bans():
    result = query_db("select jail, ip, timeofban, data from bans")
    ban_list = convert_query_to_ban_model(result)

    bans = [Ban(**item) for item in ban_list]
    return bans

@router.get("/{jail}", response_model=List[Ban])
async def read_bans(jail):
    result = query_db(f"select jail, ip, timeofban, data from bans where jail = '{jail}'")
    ban_list = convert_query_to_ban_model(result)
    bans = [Ban(**item) for item in ban_list]
    return bans
