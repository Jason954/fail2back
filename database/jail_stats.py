import os
import sqlite3
from datetime import datetime, timedelta

from fastapi import HTTPException


class Database:
    acceptable_units = ["hour", "day", "week", "month", "year"]

    def __init__(self):
        self.db_name = os.environ["DB_STATS_PATH"]
        # check if db_name is not empty
        if self.db_name == "":
            # set the default db_name
            self.db_name = "jail_stats.db"
        self.init_db()

    def init_db(self):
        print("Trying to initialize the database")
        # create a connection to the database
        conn = sqlite3.connect(self.db_name)
        # create a cursor object
        c = conn.cursor()
        # create the jail_stats table
        c.execute('''CREATE TABLE IF NOT EXISTS jail_stats
                     (jail text, date datetime, concern varchar(100), value int)''')
        # commit the changes
        conn.commit()
        # close the connection
        conn.close()
        print("Database initialized at " + self.db_name)

    def insert(self, jail, date, concern, value):
        # create a connection to the database
        conn = sqlite3.connect(self.db_name)
        # create a cursor object
        c = conn.cursor()
        # insert the values into the jail_stats table
        c.execute("INSERT INTO jail_stats VALUES (?, ?, ?, ?)", (jail, date, concern, value))
        # commit the changes
        conn.commit()
        # close the connection
        conn.close()
        print("Values inserted into the database")

    def get_stats(self, jail):
        # create a connection to the database
        conn = sqlite3.connect(self.db_name)
        # create a cursor object
        c = conn.cursor()
        # get the stats from the jail_stats table
        c.execute("SELECT * FROM jail_stats WHERE jail=?", (jail,))
        # fetch the result
        result = c.fetchall()
        # close the connection
        conn.close()
        return result

    def get_history_by_jail(self, jail, end_date, unit, interval):
        global date_format
        if unit not in self.acceptable_units:
            # throw bad request error
            raise HTTPException(status_code=400, detail="Invalid unit")

            # Convert end_date to datetime object
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        # Calculate start_date
        if unit == "hour":
            start_date = end_date - timedelta(hours=interval)
            date_format = "%Y-%m-%d %H"
        elif unit == "day":
            start_date = end_date - timedelta(days=interval)
            date_format = "%Y-%m-%d"
        elif unit == "week":
            start_date = end_date - timedelta(weeks=interval)
            date_format = "%Y-%W"
        elif unit == "month":
            start_date = end_date - timedelta(days=30 * interval)
            date_format = "%Y-%m"
        elif unit == "year":
            start_date = end_date - timedelta(days=365 * interval)  # approximate
            date_format = "%Y"

        # create a connection to the database
        conn = sqlite3.connect(self.db_name)
        # create a cursor object
        c = conn.cursor()
        # get the stats from the jail_stats table
        c.execute(f"SELECT jail, strftime('{date_format}', date), concern, MAX(value) FROM jail_stats WHERE jail=? AND date BETWEEN ? AND ? GROUP BY jail, strftime('{date_format}', date), concern", (jail, start_date, end_date))
        result = c.fetchall()
        # close the connection
        conn.close()

        return result

    def get_history(self, end_date, unit, interval):
        global date_format
        if unit not in self.acceptable_units:
            # throw bad request error
            raise HTTPException(status_code=400, detail="Invalid unit")

            # Convert end_date to datetime object
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        # Calculate start_date
        date_format, start_date = self.define_date_format_start_date(unit, interval, end_date)
        # create a connection to the database
        conn = sqlite3.connect(self.db_name)
        # create a cursor object
        c = conn.cursor()
        # get the stats from the jail_stats table
        c.execute(f"SELECT strftime('{date_format}', date), concern, MAX(value) FROM jail_stats WHERE date BETWEEN ? AND ? GROUP BY strftime('{date_format}', date), concern", (start_date, end_date))
        result = c.fetchall()
        # close the connection
        conn.close()

        return result

    def define_date_format_start_date(self, unit, interval, end_date):
        start_date = None
        format_date = None
        if unit == "hour":
            start_date = end_date - timedelta(hours=interval)
            format_date = "%Y-%m-%d %H"
        elif unit == "day":
            start_date = end_date - timedelta(days=interval)
            format_date = "%Y-%m-%d"
        elif unit == "week":
            start_date = end_date - timedelta(weeks=interval)
            format_date = "%Y-%W"
        elif unit == "month":
            start_date = end_date - timedelta(days=30 * interval)
            format_date = "%Y-%m"
        elif unit == "year":
            start_date = end_date - timedelta(days=365 * interval)  # approximate
            format_date = "%Y"

        return format_date, start_date

