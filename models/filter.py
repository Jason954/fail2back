from typing import List

from pydantic import BaseModel


class Filter(BaseModel):
    currently_failed: int
    failed: int
    file_list: List[str]
