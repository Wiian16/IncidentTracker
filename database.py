import threading
import json
import datetime
from custom_exceptions import *
import os

lock = threading.Lock()

def _load_file():
    # Create file if none exists
    if not os.path.exists("database.json"):
        _save_file({})

    with open("database.json", "r") as data:
        json_data = json.loads(data.read())

    return json_data

def _save_file(json_data):
    with open("database.json", "w") as data:
        data.write(json.dumps(json_data))

def add_incident(guild_id, incident_name):
    # Acquire lock for thread safety
    with lock:
        json_data = _load_file()

        # Convert to string because 1 != "1"
        guild_id = str(guild_id)

        if guild_id not in json_data:
            json_data[guild_id] = {}

        if incident_name in json_data[guild_id]:
            raise IncidentAlreadyExistsException(f"Incident '{incident_name}' already exists in guild '{guild_id}'")

        json_data[guild_id][incident_name] = str(datetime.datetime.now())

        _save_file(json_data)

def get_incident(guild_id, incident_name):
    # Acquire lock for thread safety
    with lock:
        json_data = _load_file()

        # Convert to string because 1 != "1"
        guild_id = str(guild_id)

        if guild_id not in json_data:
            raise NoSuchIncidentException(f"Incident '{incident_name}' not found in guild '{guild_id}'")

        if incident_name not in json_data[guild_id]:
            raise NoSuchIncidentException(f"Incident '{incident_name}' not found in guild '{guild_id}'")

        datetime_format ="%Y-%m-%d %H:%M:%S.%f"

        incident_time = datetime.datetime.strptime(json_data[guild_id][incident_name], datetime_format)

        return incident_time
