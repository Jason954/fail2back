from typing import List, Optional

from pydantic import BaseModel


class BanInfo(BaseModel):
    matches: Optional[List[int]] = None
    failures: int

