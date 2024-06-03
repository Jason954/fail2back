import json
from typing import List

from fastapi import APIRouter
from starlette.responses import JSONResponse

from dependencies import send_command, query_db
from enums.order import Order
from models.ip import Ip
from utils.check import check_ip

router = APIRouter(
    # prefix="/bans",
    tags=["bans"],
    responses={404: {"description": "Not found"}},
)


@router.get("/bans",
            response_model=List[Ip],
            responses={
                200: {
                    "description": "List of bans",
                    "headers": {
                        "X-Total-Count": {
                            "description": "The total number of bans",
                            "schema": {
                                "type": "integer"
                            }
                        }
                    }
                }
            }
            )
async def read_bans(order: Order = None, limit: int = None, offset: int = 0):
    banned = send_command("banned")
    if banned is not None and len(banned):
        ip_list = []
        for service in banned:
            for service_name, ip_addresses in service.items():
                ip_list.extend(ip_addresses)
        banned_return = ip_list
    else:
        banned_return = []
    return return_response_sorted_bans(banned_return, order, limit, offset)


@router.get("/bans/{ip}",
            responses={
                200: {
                    "description": "List of bans",
                    "headers": {
                        "X-Total-Count": {
                            "description": "The total number of bans",
                            "schema": {
                                "type": "integer"
                            }
                        }
                    }
                }
            }
            )
async def get_jails_by_banned_ip(ip: str):
    check_ip(ip)
    banned = send_command(f"banned {ip}")
    jail_list = []
    for jail in banned:
        jail_list.extend(jail)
    return jail_list


@router.post("/unban")
async def unban(ip: str):
    if ip == "all":
        return send_command("unban --all")

    check_ip(ip)
    return send_command(f"unban {ip}")


def return_response_sorted_bans(bans, order: Order, limit: int, offset: int):
    headers = {"X-Total-Count": str(len(bans))}
    if order is not None:
        bans.sort(reverse=order == "desc")
    if limit is not None:
        bans = bans[offset:offset + limit]
    return JSONResponse(content=bans, headers=headers)
