import json

from dependencies import send_command
from models.stats import Stats
from models.filter import Filter
from models.ip import Ip
from models.jail import Jail


def convert_json_to_jail(name, json_data):
    filter_data = None
    stats_data = None
    for data_item in json_data:
        if data_item[0] == "Filter":
            filter_data = Filter(
                currently_failed=data_item[1][0][1],
                failed=data_item[1][1][1],
                file_list=data_item[1][2][1]
            )
        elif data_item[0] == "Actions":
            ip_list = []
            for ip in data_item[1][2][1]:
                ip_list.append(Ip(ip=ip))
            stats_data = Stats(
                currently_banned=data_item[1][0][1],
                banned=data_item[1][1][1],
                ip_list=ip_list
            )
    return Jail(name=name, filter=filter_data, stats=stats_data)


def convert_query_to_ban_model(result):
    ban_list = []

    for item in result:
        item["data"] = json.loads(item["data"])
        # Check data and convert in string if it is a dict
        for data in item["data"].items():
            if data[0] is not None and data[0] == "matches":
                index = 0
                for match in data[1]:
                    # if match is a list convert into string
                    if type(match) is list:
                        match = "".join(match)
                        # replace the match in the data
                        item["data"]["matches"][index] = match
                    index += 1
        ban_list.append(item)
    return ban_list


def convert_command_result_to_jail_entities(jails, status):
    if status[0] is not None and status[0][1] > 0:
        # get list of jails
        list_of_jails = status[1][1].split(", ")
        for jail in list_of_jails:
            # get the name of the jail
            jail_name = jail
            jail_info = send_command(f"status {jail_name}")
            jail_entity = convert_json_to_jail(jail_name, jail_info)
            # create a new jail object
            jails.append(jail_entity)


def convert_stats_formatted(stats):
    formatted_stats = {}
    for stat in stats:
        if stat[1] not in formatted_stats:
            formatted_stats[stat[1]] = {}
        formatted_stats[stat[1]][stat[2]] = stat[3]
    return formatted_stats


def aggregate_stats(stats):
    if len(stats) == 0:
        return None
    aggregated_stats = {}
    for jail, jail_stats in stats.items():
        for date, date_stats in jail_stats.items():
            if date not in aggregated_stats:
                aggregated_stats[date] = {}
            for key, value in date_stats.items():
                if key not in aggregated_stats[date]:
                    aggregated_stats[date][key] = 0
                aggregated_stats[date][key] += value
    return aggregated_stats
