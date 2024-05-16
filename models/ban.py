from typing import Optional

from pydantic import BaseModel

from models.ban_info import BanInfo
from models.ip import Ip


class Ban(BaseModel):
    jail: str
    ip: str
    timeofban: int
    data: BanInfo

