from collections import OrderedDict 

import uuid

from datetime import datetime


# A dictionary of all channels with messages.
# each channel stores no more than 100 messages.
channels = {}

"""
Example of data structure. 

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

"""

# Logic around channels

def is_channel_exist(channel_name):
    for channel in channels.values():
        if channel["name"] == channel_name:
            return True

    return False

def generate_uuid():
    new_id = str(uuid.uuid4())
    
    return new_id

def add_channel(channel_name):
    channel_id = generate_uuid()
    channels[channel_id] = {
        "name": channel_name,
        "id": channel_id,
        "messages": OrderedDict()
    }

    return channel_id

# Logic around messages

def storage_limit(channel_id):
    """ 
    Check is there already 100 messages stored for this channel.
    Delete old messages if necessary.
    """
    while len(channels[channel_id]["messages"]) >= 100:
        # Delete the first message (FIFO)
        channels[channel_id]["messages"].popitem(last=False)

def delete(channel_id, message_id):
    channels[channel_id]["messages"].pop(message_id)

def add_message(message_text, username, channel_id):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_id  = generate_uuid()
    message = {
        "id": message_id,
        "message_text": message_text,
        "username": username,
        "time": time
    }
    # Check the storage limit
    storage_limit(channel_id)

    # Add message id and message to ordered dictionary    
    channels[channel_id]["messages"][message_id] = message

    print(message)

    return message










