
from pydantic import BaseModel

from models.ban_info import BanInfo


class Ban(BaseModel):
    jail: str
    ip: str
    timeofban: int
    data: BanInfo

