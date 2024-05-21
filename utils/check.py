import socket

from fastapi import HTTPException

from dependencies import send_command


def check_ip(ip: str):
    # control ip address
    try:
        socket.inet_aton(ip)
    except socket.error:
        raise HTTPException(status_code=400, detail="Invalid IP address")


def check_jails(jail: str):
    # check if the jail exists
    jails = send_command("status")
    jail_list = jails[1][1].split(", ")
    if jail not in jail_list:
        raise HTTPException(status_code=400, detail="Jail does not exist")


def check_int(time: int):
    if not isinstance(time, int):
        raise HTTPException(status_code=400, detail="Invalid time")
