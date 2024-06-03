from typing import List, Annotated

from fastapi import APIRouter, Header, Response
from starlette.responses import JSONResponse

from dependencies import query_db
from enums.order import Order
from models.fail import Fail
from utils.check import check_jails

router = APIRouter(
    prefix="/fails",
    tags=["fails"],
    responses={404: {"description": "Not found"}},
)


@router.get("",
            response_model=List[Fail],
            responses={
                200: {
                    "description": "List of fails",
                    "headers": {
                        "X-Total-Count": {
                            "description": "The total number of fails",
                            "schema": {
                                "type": "integer"
                            }
                        }
                    }
                }
            }
            )
async def read_fails(sort: str = None, order: Order = None, limit: int = None, offset: int = 0):
    fails = query_db("select jail, ip, timeoffail, match from fails")
    return return_response_sorted_fails(fails, sort, order, limit, offset)



@router.get("/{jail}",
            response_model=List[Fail],
            responses={
                200: {
                    "description": "List of fails",
                    "headers": {
                        "X-Total-Count": {
                            "description": "The total number of fails",
                            "schema": {
                                "type": "integer"
                            }
                        }
                    }
                }
            }
            )
async def read_fails_by_jail(jail: str, sort: str = None, order: Order = None, limit: int = None, offset: int = 0):
    check_jails(jail)
    fails = query_db(f"select jail, ip, timeoffail, match from fails where jail = '{jail}'")
    return return_response_sorted_fails(fails, sort, order, limit, offset)


def return_response_sorted_fails(fails, sort: str, order: Order, limit: int, offset: int):
    headers = {"X-Total-Count": str(len(fails))}
    if sort is not None:
        if order is None:
            order = Order.asc
        fails.sort(key=lambda x: x[sort], reverse=order == Order.desc)
    if limit is not None:
        fails = fails[offset:offset + limit]
    return JSONResponse(content=fails, headers=headers)
