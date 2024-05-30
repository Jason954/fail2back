from fastapi import FastAPI
from routers import bans, status, jails, globalbans, health, stats
from database import jail_stats
# import routers
app = FastAPI()

# Database setup
jail_stats.Database()

app.include_router(health.router)
app.include_router(bans.router)
app.include_router(status.router)
app.include_router(jails.router)
app.include_router(globalbans.router)
app.include_router(stats.router)
