from enum import Enum

from pydantic import BaseModel

from models.ban_info import BanInfo


# define all groupby field authorized for the query
class FailGroupByFields(str, Enum):
    JAIL = "jail"
    IP = "ip"


class Fail(BaseModel):
    jail: str
    ip: str
    timeoffail: int
    match: str
