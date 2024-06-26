from typing import List, Optional

from pydantic import BaseModel

from models.ip import Ip


class Stats(BaseModel):
    currently_banned: int
    banned: int
    ip_list: Optional[List[Ip]] = None
