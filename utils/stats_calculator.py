from datetime import datetime
from database.jail_stats import Database
from dependencies import send_command
from utils.convert import convert_command_result_to_jail_entities


class StatsCalculator:

    stats_names = ["currently_banned", "banned", "currently_failed", "failed"]

    def __init__(self, db: Database):
        self.db = db

    def calculate_and_insert_stats(self):
        status = send_command("status")
        jails = []
        current_datetime = datetime.now()
        convert_command_result_to_jail_entities(jails, status)

        for jail in jails:
            self._insert_stats(jail, current_datetime)

        return 0

    def _insert_stats(self, jail, current_datetime):
        for stat in jail.stats:
            if stat[0] in self.stats_names:
                self._insert_stat(jail.name, current_datetime, stat[0], stat[1])

        for f in jail.filter:
            print("f: ", f)
            if f[0] in self.stats_names:
                self._insert_stat(jail.name, current_datetime, f[0], f[1])

    def _insert_stat(self, jail_name, current_datetime, stat_name, stat_value):
            self.db.insert(jail_name, current_datetime, stat_name, stat_value)
