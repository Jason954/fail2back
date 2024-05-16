from typing import Union

from fastapi import FastAPI, Response

from routers import bans
from routers import jails
# import routers
app = FastAPI()

app.include_router(bans.router)
app.include_router(jails.router)



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
