from typing import List

from fastapi import APIRouter

from dependencies import query_db
from enums.order import Order
from models.fail import Fail
from utils.check import check_jails

router = APIRouter(
    prefix="/fails",
    tags=["fails"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[Fail])
async def read_fails(sort: str = None, order: Order = None, limit: int = None, offset: int = 0):
    fails = query_db("select jail, ip, timeoffail, match from fails")

    if sort is not None:
        if order is None:
            order = Order.asc
        fails.sort(key=lambda x: x[sort], reverse=order == Order.desc)
    if limit is not None:
        fails = fails[offset:offset + limit]

    fails = [Fail(**item) for item in fails]
    return fails

@router.get("/{jail}", response_model=List[Fail])
async def read_fails_by_jail(jail: str, sort: str = None, order: Order = None, limit: int = None, offset: int = 0):
    check_jails(jail)

    result = query_db(f"select jail, ip, timeoffail, match from fails where jail = '{jail}'")

    if sort is not None:
        if order is None:
            order = Order.asc
        fails.sort(key=lambda x: x[sort], reverse=order == Order.desc)
    if limit is not None:
        fails = fails[offset:offset + limit]


    return [Fail(**item) for item in result]
