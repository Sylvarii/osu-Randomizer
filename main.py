import random
import requests
import time
import json

import dict
import config_manager


class OsuRandomizerLogic:
    def __init__(self):
        self.current_map_id = None

    def get_random_map(self):
        with open("settings.json", "r") as file:
            settings = json.load(file)

        api_key = settings["api_key"]

        latest_map_id = config_manager.update_map_id(api_key)
        if latest_map_id is None:
            print("Unable to retrieve latest map ID.")
            return

        print(f"Latest map ID: {latest_map_id}")

        while True:
            map_id = random.randint(1, latest_map_id)
            url = f"https://osu.ppy.sh/api/get_beatmaps?k={api_key}&b={map_id}"

            response = requests.get(url)
            data = response.json()

            if data:
                mode = int(data[0]['mode'])
                max_combo = data[0]['max_combo']
                ranked = int(data[0]['approved'])
                sr = round(float(data[0]['difficultyrating']), 2)

                mode_name = dict.ruleset_dict.get(mode)
                ranked_status = dict.ranked_status.get(ranked)

                if max_combo is None:
                    print(f"Beatmap ID {map_id} is empty. Generating new one.")
                    time.sleep(0.2)
                    continue

                max_combo_value = int(max_combo)

                if mode == 0 and (max_combo_value > 200 or ranked > 0):
                    self.current_map_id = map_id
                    result = f"{data[0]['artist']} - {data[0]['title']} [{data[0]['version']}]\n({sr}*) by {data[0]['creator']}"
                    print(f"Beatmap ID {map_id} meets the criteria. Ranked Status: {ranked_status}.\n\n{result}")
                    return result
                elif max_combo_value <= 200 and ranked <= 0:
                    print(f"Beatmap ID {map_id} filtered. Generating a new one.")
                    time.sleep(0.2)
                elif mode_name != "osu!standard":
                    print(f"Beatmap ID {map_id} exists in the {mode_name} ruleset. Generating a new one.")
                    time.sleep(0.2)
            else:
                print(f"Beatmap ID {map_id} doesn't exist. Generating a new one.")
                time.sleep(0.2)

    def get_current_map_id(self):
        return self.current_map_id
