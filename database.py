import threading
import json
import datetime
from custom_exceptions import *
import os

lock = threading.Lock()

def _load_file():
    """
    NOT TREAD SAFE. Loads database.json from the disk, if the file does not exist, it will be created with an empty json
    object.
    :return: A json object from database.json
    """
    # Create file if none exists
    if not os.path.exists("database.json"):
        _save_file({})

    with open("database.json", "r") as data:
        json_data = json.loads(data.read())

    return json_data

def _save_file(json_data):
    """
    NOT THREAD SAFE. Saves the given json_data to database.json on the disk.
    :param json_data: Data to save to database.py
    """
    with open("database.json", "w") as data:
        data.write(json.dumps(json_data))

def add_incident(guild_id, incident_name):
    """
    THREAD SAFE. Adds an incident to a given server in the database with the current time, if the incident already
     exists in the database, an exception will be raised.
    :param guild_id: Server id to add the incident to
    :param incident_name: Name of the incident to add
    :raises IncidentAlreadyExistsException: Raised if the given exception already exists in the given server
    """
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
    """
    THREAD SAFE. Gets the time stamp of the given incident from the given server, if the incident does not exist in the
    given server, an exception will be raised.
    :param guild_id: Server to check for incident in
    :param incident_name: Incident to check for
    :raises NoSuchIncidentException: Raised if the given incident name does not exist in the given server
    """
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

def reset_incident(guild_id, incident_name):
    """
    THREAD SAFE. Resets the timestamp for the given incident from the given server to the current time, if the incident
    does not exist, an exception to be raised
    :param guild_id: Server to check for incident in
    :param incident_name: Incident name to reset
    :raises NoSuchIncidentException:
    """
    with lock:
        json_data = _load_file()

        # Convert to string because 1 != "1"
        guild_id = str(guild_id)

        if guild_id not in json_data or incident_name not in json_data[guild_id]:
            raise NoSuchIncidentException(f"Incident '{incident_name}' not found in guild '{guild_id}'")

        json_data[guild_id][incident_name] = str(datetime.datetime.now())

        _save_file(json_data)

def remove_incident(guild_id, incident_name):
    """
    THREAD SAFE. Removes a given incident from the given server in the database, if the incident does not exist, an
    exception is raised.
    :param guild_id: Server to check for incident in
    :param incident_name: Incident name to remove
    :raises NoSuchIncidentException: Raised if the given incident is not found in the server
    """
    with lock:
        json_data = _load_file()

        # Convert to string because 1 != "1"
        guild_id = str(guild_id)

        if guild_id not in json_data or incident_name not in json_data[guild_id]:
            raise NoSuchIncidentException(f"Incident '{incident_name}' not found in guild '{guild_id}'")

        json_data[guild_id][incident_name] = str(datetime.datetime.now())

        _save_file(json_data)