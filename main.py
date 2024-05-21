from typing import Union

from fastapi import FastAPI, Response

from routers import bans
from routers import jails
from routers import globalbans
# import routers
app = FastAPI()

app.include_router(bans.router)
app.include_router(jails.router)
app.include_router(globalbans.router)
