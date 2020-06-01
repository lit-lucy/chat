from collections import OrderedDict 
import uuid


# A dictionary of all channels with messages.
# each channel stores no more than 100 messages.
channels = {}

message_1 = {
    "id": 11,
    "message_text": "asdasdasd",
    "user": "user1",
    "time": "2020-06-01 12:12",
}

message_2 = {
    "id": 12,
    "message_text": "asdasdasd2",
    "user": "user2",
    "time": "2020-06-01 12:13",
}

chanel1 = {
    "id": "chanel_1",
    "name": "chanel name",
    "messages": {
        "11": message_1,
        "12": message_2,
    }
}
chanel2 = {
    ...
}

channels = {
    "chanel_1": chanel1,
    "chanel_2": chanel2,
} 

def is_channel_exist(channel_name):
    for channel_id in channels.keys():
        if channel_id["name"] == channel_name:
            return True

    return False

def generate_uuid():
    uuid = str(uuid.uuid4())
    return uuid

def add_channel(channel_name, channel_id):
    channels[channel_id] = {"name": channel_name}



