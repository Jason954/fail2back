from typing import Optional

from pydantic import BaseModel

from models.action import Action
from models.ban_info import BanInfo
from models.filter import Filter
from models.ip import Ip


class Jail(BaseModel):
    name: str
    filter: Optional[Filter] = None
    actions: Optional[Action] = None

