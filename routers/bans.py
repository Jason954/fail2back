import json
from typing import List

from fastapi import APIRouter

from dependencies import send_command, query_db
from models.ban import Ban
from models.ip import Ip

router = APIRouter(
    prefix="/bans",
    tags=["bans"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[Ip])
async def read_bans():
    banned = send_command("banned")
    if banned is not None and len(banned):
        ip_list = []
        for service in banned:
            for service_name, ip_addresses in service.items():
                ip_list.extend(ip_addresses)
        banned_return = ip_list
    else:
        banned_return = []
    return [Ip(ip=ip) for ip in banned_return]


@router.get("/all")
async def read_bans():
    result = query_db("select jail, ip, timeofban, data from bans")
    ban_list = []
    for item in result:
        item = dict(item)
        item["data"] = json.loads(item["data"])
        ban_list.append(item)
    bans = [Ban(**item) for item in ban_list]
    return bans
#
#
# @router.get("/{service}")
# async def read_bans():
#     banned = send_command("banned")
#     if banned is not None and len(banned):
#         ip_list = []
#         for service in banned:
#             for service_name, ip_addresses in service.items():
#                 ip_list.extend(ip_addresses)
#         banned_return = ip_list
#     else:
#         banned_return = []
#     return banned_return
