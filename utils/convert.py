from models.action import Action
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
            action_data = Action(
                currently_banned=data_item[1][0][1],
                banned=data_item[1][1][1],
                ip_list=ip_list
            )
    return Jail(name=name, filter=filter_data, actions=action_data)
