from fastapi import HTTPException

from starlette.responses import JSONResponse

from enums.order import Order


def return_response_sorted_bans(bans, sort: str, order: Order, limit: int, offset: int):
    headers = {"X-Total-Count": str(len(bans))}

    # check if bans contains sort attribute
    if sort is not None and len(bans) > 0:
        if sort not in bans[0]:
            raise HTTPException(status_code=400, detail="Invalid sort attribute")

    if sort is not None:
        bans = sorted(bans, key=lambda x: x[sort], reverse=order == Order.desc)
    if limit is not None:
        bans = bans[offset:offset + limit]
    return JSONResponse(content=bans, headers=headers)
