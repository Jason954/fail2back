
from enum import Enum


class UnitDate(str, Enum):
    day = "day"
    week = "week"
    month = "month"
    year = "year"
