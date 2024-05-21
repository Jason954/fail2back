import json
import socket
from typing import List

from fastapi import APIRouter, HTTPException

from dependencies import send_command
from models.jail import Jail
from utils.check import check_jails, check_ip, check_int
from utils.convert import convert_json_to_jail

router = APIRouter(
    prefix="/jails",
    tags=["jails"],
    responses={404: {"description": "Not found"}},
)


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
            jails.append(jail_entity)
    return jails


# ban a specific ip address in a jail
@router.post("/{jail}/ban")
async def ban_ip(jail: str, ip: str):
    # check if the jail exists
    jails = send_command("status")
    jail_list = jails[1][1].split(", ")
    if jail not in jail_list:
        raise HTTPException(status_code=400, detail="Jail does not exist")

    # control ip address
    try:
        socket.inet_aton(ip)
    except socket.error:
        raise HTTPException(status_code=400, detail="Invalid IP address")

    result = send_command(f"set {jail} banip {ip}")
    return result


# unban a specific ip address in a jail
@router.post("/{jail}/ban/{ip}")
async def ban_ip_jail(jail: str, ip: str):
    # check if the jail exists and the ip is valid
    check_jails(jail)
    check_ip(ip)

    result = send_command(f"set {jail} banip {ip}")
    return result


# unban a specific ip address in a jail
@router.post("/{jail}/unban/{ip}")
async def unban_ip_jail(jail: str, ip: str):
    # check if the jail exists and the ip is valid
    check_jails(jail)
    check_ip(ip)

    result = send_command(f"set {jail} unbanip {ip}")
    return result


# set jail bantime
@router.post("/{jail}/bantime/{time}")
async def set_bantime(jail: str, time: int):
    # check if the jail exists and the ip is valid
    check_jails(jail)
    check_int(time)

    result = send_command(f"set {jail} bantime {time}")
    return result

# set jail maxretry
@router.post("/{jail}/maxretry/{maxretry}")
async def set_maxretry(jail: str, maxretry: int):
    # check if the jail exists and maxretry is valid
    check_jails(jail)
    check_int(maxretry)

    result = send_command(f"set {jail} maxretry {maxretry}")
    return result

# set jail maxmatches
@router.post("/{jail}/maxmatches/{maxmatches}")
async def set_maxmatches(jail: str, maxmatches: int):
    # check if the jail exists and maxmatches is valid
    check_jails(jail)
    check_int(maxmatches)

    result = send_command(f"set {jail} maxmatches {maxmatches}")
    return result

# set jail maxlines
@router.post("/{jail}/maxlines/{maxlines}")
async def set_maxlines(jail: str, maxlines: int):
    # check if the jail exists and maxlines is valid
    check_jails(jail)
    check_int(maxlines)

    result = send_command(f"set {jail} maxlines {maxlines}")
    return result
