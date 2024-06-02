
from pydantic import BaseModel

from models.ban_info import BanInfo


class Fail(BaseModel):
    jail: str
    ip: str
    timeoffail: int
    match: str

