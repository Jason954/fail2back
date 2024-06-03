import json
from typing import List

from fastapi import APIRouter
from starlette.responses import JSONResponse

from dependencies import query_db
from enums.order import Order
from models.ban import Ban
from utils.common import return_response_sorted_bans
from utils.convert import convert_query_to_ban_model

router = APIRouter(
    prefix="/globalbans",
    tags=["globalbans"],
    responses={404: {"description": "Not found"}},
)


@router.get("",
            response_model=List[Ban],
            responses={
                200: {
                    "description": "List of globalbans",
                    "headers": {
                        "X-Total-Count": {
                            "description": "The total number of globalbans",
                            "schema": {
                                "type": "integer"
                            }
                        }
                    }
                }
            })
async def read_bans(sort: str = None, order: Order = None, limit: int = None, offset: int = 0):
    result = query_db("select jail, ip, timeofban, data from bans")
    ban_list = convert_query_to_ban_model(result)
    return return_response_sorted_bans(ban_list, sort, order, limit, offset)


@router.get("/{jail}",
            response_model=List[Ban],
            responses={
                200: {
                    "description": "List of globalbans",
                    "headers": {
                        "X-Total-Count": {
                            "description": "The total number of globalbans",
                            "schema": {
                                "type": "integer"
                            }
                        }
                    }
                }
            }
            )
async def read_bans_by_jail(jail: str, sort: str = None, order: Order = None, limit: int = None, offset: int = 0):
    result = query_db(f"select jail, ip, timeofban, data from bans where jail = '{jail}'")
    ban_list = convert_query_to_ban_model(result)
    return return_response_sorted_bans(ban_list, sort, order, limit, offset)

