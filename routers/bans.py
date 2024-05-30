import json
from typing import List

from fastapi import APIRouter

from dependencies import send_command, query_db
from enums.order import Order
from models.ban import Ban
from models.ip import Ip
from models.jail import Jail
from utils.check import check_ip
from utils.convert import convert_query_to_ban_model

router = APIRouter(
    # prefix="/bans",
    tags=["bans"],
    responses={404: {"description": "Not found"}},
)


@router.get("/bans", response_model=List[Ip])
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
    if order is not None:
        banned_return.sort(reverse=order == "desc")
    if limit is not None:
        banned_return = banned_return[offset:offset + limit]

    return [Ip(ip=ip) for ip in banned_return]


@router.get("/bans/{ip}")
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
