import os

import schedule
import time
from database import jail_stats
from utils import stats_calculator

db = jail_stats.Database()
calculator = stats_calculator.StatsCalculator(db)

X = int(os.getenv("SCHEDULE_INTERVAL", 1))
print(X)
print("Scheduler started, will run every " + str(X) + " minutes")

# Schedule the function to be called every X minutes
schedule.every(X).minutes.do(calculator.calculate_and_insert_stats)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
