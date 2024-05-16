import json
from typing import List

from fastapi import APIRouter

from dependencies import send_command
from models.ip import Ip
from models.jail import Jail
from utils.convert import convert_json_to_jail

router = APIRouter(
    prefix="/jails",
    tags=["jails"],
    responses={404: {"description": "Not found"}},
)


# @router.get("")
@router.get("", response_model=List[Jail])
async def read_jails():
    status = send_command("status")
    jails = []
    # check if number of jails is greater than 0
    if status[0] is not None and status[0][1] > 0:
        # get list of jails
        list_of_jails = status[1][1].split(", ")
        for jail in list_of_jails:
            # get the name of the jail
            jail_name = jail
            jail_info = send_command(f"status {jail_name}")
            jail_entity = convert_json_to_jail(jail_name, jail_info)
            # create a new jail object
            print(type(jail_entity))
            jails.append(jail_entity)
    return jails
