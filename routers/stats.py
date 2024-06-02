from datetime import datetime

from fastapi import APIRouter, HTTPException

from database.jail_stats import Database
from enums.unit_date import UnitDate
from utils.check import check_jails
from utils.convert import convert_stats_formatted

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    responses={404: {"description": "Not found"}},
)

db = Database()


@router.get("/{jail}")
async def read_stats_jail(jail: str):
    check_jails(jail)
    stats = db.get_stats(jail)
    if stats is None:
        raise HTTPException(status_code=404, detail="Stats not found")
    return stats


# get formated stats for a specific jail
@router.get("/history/{jail}/formatted")
async def read_stats_jail_formatted(jail: str, end_date: str = "today", unit: UnitDate = "day", interval: int = 7):
    if end_date == "today":
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(end_date)
    # check if date format is correct
    try:
        datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, should be YYYY-MM-DD")
    stats = db.get_history_by_jail(jail, end_date, unit, interval)

    if stats is None:
        raise HTTPException(status_code=404, detail="Stats not found")
    formatted_stats = convert_stats_formatted(stats)
    return formatted_stats


# get formated stats for the last 24 hours
@router.get("/history/recent")
async def read_all_history_stats_recent():
    stats = db.get_history(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "hour", 24)

    return stats

    if stats is None:
        raise HTTPException(status_code=404, detail="Stats not found")
    formatted_stats = convert_stats_formatted(stats)
    return formatted_stats


# get formated stats for the last 24 hours
@router.get("/history/{jail}/recent")
async def read_stats_jail_recent(jail: str):
    stats = db.get_history_by_jail(jail, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "hour", 24)
    if stats is None:
        raise HTTPException(status_code=404, detail="Stats not found")
    formatted_stats = convert_stats_formatted(stats)
    return formatted_stats
