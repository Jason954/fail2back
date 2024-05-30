from typing import List

from fastapi import APIRouter

from dependencies import send_command
from enums.order import Order
from models.action import Action
from models.jail import Jail
from utils.check import check_jails, check_ip, check_int
from utils.convert import convert_json_to_jail

router = APIRouter(
    prefix="/jails",
    tags=["jails"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[Jail])
async def read_jails(order: Order = None, limit: int = None, offset: int = 0):
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

    if Order is not None:
        jails.sort(key=lambda x: x.name, reverse=order == Order.desc)

    if limit is not None:
        # limit the jails
        jails = jails[offset:offset + limit]
    return jails


# ban a specific ip address in a jail
@router.post("/{jail}/ban")
async def ban_ip_jail(jail: str, ip: str):
    # check if the jail exists and the ip is valid
    check_jails(jail)
    check_ip(ip)

    result = send_command(f"set {jail} banip {ip}")
    return result


# unban a specific ip address in a jail
@router.post("/{jail}/unban")
async def unban_ip_jail(jail: str, ip: str):
    # check if the jail exists and the ip is valid
    check_jails(jail)
    check_ip(ip)

    result = send_command(f"set {jail} unbanip {ip}")
    return result


# get jail bantime
@router.get("/{jail}/bantime")
async def get_bantime(jail: str):
    # check if the jail exists
    check_jails(jail)

    result = send_command(f"get {jail} bantime")
    return result


# set jail bantime
@router.post("/{jail}/bantime/{time}")
async def set_bantime(jail: str, time: int):
    # check if the jail exists and the ip is valid
    check_jails(jail)
    check_int(time)

    result = send_command(f"set {jail} bantime {time}")
    return result


# get jail maxretry
@router.get("/{jail}/maxretry")
async def get_maxretry(jail: str):
    # check if the jail exists
    check_jails(jail)

    result = send_command(f"get {jail} maxretry")
    return result


# set jail maxretry
@router.post("/{jail}/maxretry/{maxretry}")
async def set_maxretry(jail: str, maxretry: int):
    # check if the jail exists and maxretry is valid
    check_jails(jail)
    check_int(maxretry)

    result = send_command(f"set {jail} maxretry {maxretry}")
    return result


# get jail maxmatches
@router.get("/{jail}/maxmatches")
async def get_maxmatches(jail: str):
    # check if the jail exists
    check_jails(jail)

    result = send_command(f"get {jail} maxmatches")
    return result


# set jail maxmatches
@router.post("/{jail}/maxmatches/{maxmatches}")
async def set_maxmatches(jail: str, maxmatches: int):
    # check if the jail exists and maxmatches is valid
    check_jails(jail)
    check_int(maxmatches)

    result = send_command(f"set {jail} maxmatches {maxmatches}")
    return result


# get jail maxlines
@router.get("/{jail}/maxlines")
async def get_maxlines(jail: str):
    # check if the jail exists
    check_jails(jail)

    result = send_command(f"get {jail} maxlines")
    return result


# set jail maxlines
@router.post("/{jail}/maxlines/{maxlines}")
async def set_maxlines(jail: str, maxlines: int):
    # check if the jail exists and maxlines is valid
    check_jails(jail)
    check_int(maxlines)

    result = send_command(f"set {jail} maxlines {maxlines}")
    return result


# get jails actions
@router.get("/{jail}/actions", response_model=List[Action])
async def get_actions(jail: str):
    # check if the jail exists
    check_jails(jail)
    result = send_command(f"get {jail} actions")
    actions = []
    # check if the result is not empty
    if result[0] is not None:
        # split the actions into a list
        for action in result:
            # create a new action object
            action_entity = Action(name=action)
            actions.append(action_entity)
    return actions


# set jail addignoreip
@router.post("/{jail}/addignoreip/{ip}")
async def add_ignore_ip(jail: str, ip: str):
    # check if the jail exists and the ip is valid
    check_jails(jail)
    check_ip(ip)

    result = send_command(f"set {jail} addignoreip {ip}")
    return result


# get jail ignoreip
@router.get("/{jail}/ignoreip")
async def get_ignore_ip(jail: str):
    # check if the jail exists
    check_jails(jail)

    result = send_command(f"get {jail} ignoreip")
    return result


# set jail delignoreip
@router.post("/{jail}/delignoreip/{ip}")
async def del_ignore_ip(jail: str, ip: str):
    # check if the jail exists and the ip is valid
    check_jails(jail)
    check_ip(ip)

    result = send_command(f"set {jail} delignoreip {ip}")
    return result
