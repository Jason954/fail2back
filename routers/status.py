import json
from typing import List

from fastapi import APIRouter, HTTPException

from dependencies import send_command, query_db
from models.ban import Ban
from models.ip import Ip
from models.jail import Jail
from utils.check import check_ip
from utils.convert import convert_json_to_jail

router = APIRouter(
    prefix="/status",
    tags=["status"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{jail}")
async def read_status_jail(jail: str):
    jail_return = send_command(f"status {jail}")
    if jail_return is None:
        # return exception if jail does not exist
        raise HTTPException(status_code=404, detail="Jail not found")
    # format the output
    jail = convert_json_to_jail(jail, jail_return)
    return jail
