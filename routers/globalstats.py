import json
from datetime import datetime
from typing import List, Union, Dict

from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from database.jail_stats import Database
from dependencies import query_db, send_command
from enums.order import Order
from enums.unit_date import UnitDate
from models.ban import Ban, BanGroupByFields
from utils.common import return_response_sorted_bans
from utils.convert import convert_query_to_ban_model, convert_stats_formatted, aggregate_stats

router = APIRouter(
    prefix="/globalstats",
    tags=["globalstats"],
    responses={404: {"description": "Not found"}},
)

db = Database()

# get formated stats for a specific jail
@router.get("")
async def global_stats_formatted(end_date: str = "today", unit: UnitDate = "day", interval: int = 7):
    if end_date == "today":
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # check if date format is correct
    try:
        datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, should be YYYY-MM-DD")

    # get all jails
    jails = send_command("status")
    jail_list = jails[1][1].split(", ")
    formatted_stats = {}
    for jail in jail_list:
        stats = db.get_history_by_jail(jail, end_date, unit, interval)
        formatted_stats[jail] = convert_stats_formatted(stats)
    formatted_stats = aggregate_stats(formatted_stats)

    if formatted_stats is None:
        raise HTTPException(status_code=404, detail="Stats not found")
    return formatted_stats
