import json

from models.stats import Stats
from models.filter import Filter
from models.ip import Ip
from models.jail import Jail


def convert_json_to_jail(name, json_data):
    filter_data = None
    action_data = None
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
            action_data = Stats(
                currently_banned=data_item[1][0][1],
                banned=data_item[1][1][1],
                ip_list=ip_list
            )
    return Jail(name=name, filter=filter_data, actions=action_data)


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

