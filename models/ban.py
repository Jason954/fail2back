from enum import Enum

from pydantic import BaseModel

from models.ban_info import BanInfo


# define all groupby field authorized for the query
class BanGroupByFields(str, Enum):
    JAIL = "jail"
    IP = "ip"


class Ban(BaseModel):
    jail: str
    ip: str
    timeofban: int
    data: BanInfo

