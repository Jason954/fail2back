from typing import Optional

from pydantic import BaseModel

from models.stats import Stats
from models.filter import Filter


class Jail(BaseModel):
    name: str
    filter: Optional[Filter] = None
    stats: Optional[Stats] = None

