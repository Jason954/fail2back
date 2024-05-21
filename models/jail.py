from typing import Optional

from pydantic import BaseModel

from models.action import Action
from models.filter import Filter


class Jail(BaseModel):
    name: str
    filter: Optional[Filter] = None
    actions: Optional[Action] = None

