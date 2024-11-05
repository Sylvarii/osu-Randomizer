import json
import time
import requests

config_file = "config.json"


def load_config():
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):  # File doesn't exist or is empty
        return {}


def save_config(latest_map_id, last_update):
    data = {
        "latest_map_id": latest_map_id,
        "last_update": last_update
    }
    with open(config_file, 'w') as file:
        json.dump(data, file)


def get_latest_map_id(api_key):
    url = f"https://osu.ppy.sh/api/get_beatmaps?k={api_key}"
    response = requests.get(url)
    data = response.json()

    if data:
        latest_map_id = int(data[0]['beatmap_id'])
        return latest_map_id
    else:
        print("Failed to retrieve the latest map ID.")
        return None


def update_map_id(api_key):  # Limiting API usage
    config = load_config()
    last_update = config.get("last_update", 0)
    latest_map_id = config.get("latest_map_id")

    if time.time() - last_update > 86400 or latest_map_id is None:  # Check if last update was at least 24h ago
        print("Updating latest map ID...")
        latest_map_id = get_latest_map_id(api_key)
        if latest_map_id is not None:
            save_config(latest_map_id, time.time())
    else:
        print("Using cached map ID.")

    return latest_map_id
