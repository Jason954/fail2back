from fastapi import FastAPI
from routers import bans, status, jails, globalbans, health

# import routers
app = FastAPI()

app.include_router(health.router)
app.include_router(bans.router)
app.include_router(status.router)
app.include_router(jails.router)
app.include_router(globalbans.router)
