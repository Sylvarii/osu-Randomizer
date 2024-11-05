import random
import requests
import time
import tkinter as tk
import webbrowser

import dict
import config_manager

# Global variables
result_label = ""
current_map_id = None


def get_random_map():
    global current_map_id

    api_key = ""

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

        # Debugging:
        # print(f"Response data for map ID: {map_id}: {data}")

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
                current_map_id = map_id
                result = f"{data[0]['artist']} - {data[0]['title']} [{data[0]['version']}]\n({sr}*) by {data[0]['creator']}"
                print(f"Beatmap ID {map_id} meets the criteria. Ranked Status: {ranked_status}.\n\n{result}")
                return result  # Breaking the while loop
            elif max_combo_value <= 200 and ranked <= 0:
                print(f"Beatmap ID {map_id} filtered. Generating a new one.")
                time.sleep(0.2)
            elif mode_name != "osu!standard":
                print(f"Beatmap ID {map_id} exists in the {mode_name} ruleset. Generating a new one.")
                time.sleep(0.2)
        else:
            print(f"Beatmap ID {map_id} doesn't exist. Generating a new one.")
            time.sleep(0.2)


def open_map_url():
    if current_map_id is not None:
        map_url = f"https://osu.ppy.sh/b/{current_map_id}"
        webbrowser.open(map_url)


def open_osu_direct_link():
    if current_map_id is not None:
        map_url = f"osu://b/{current_map_id}"
        webbrowser.open(map_url)


def draw_rounded_rectangle(canvas, x1, y1, x2, y2, r, **kwargs):
    # Thanks, ChatGPT, for rounded corners rectangle
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2, x1, y2 - r,
        x1, y1 + r, x1, y1,
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)


def generate_map():
    global result_label
    result = get_random_map()
    if result_label and isinstance(result_label, tk.Label):
        result_label.config(text=result)


def main():
    global result_label

    root = tk.Tk()
    root.title("osu!Randomizer")

    # Set dark gray background for the main window
    root.configure(bg='darkgray')

    canvas = tk.Canvas(root, width=465, height=150, bg='darkgray', highlightthickness=0)
    canvas.pack()

    draw_rounded_rectangle(canvas, 20, 20, 450, 150, r=20, fill="lightblue", outline="")

    # Label for the result
    result_label = tk.Label(root, text="", bg="lightblue", font=("Arial", 14), justify="center", wraplength=400)
    result_label.place(x=30, y=50, width=410, height=75)

    # Frame for the left buttons
    button_frame_left = tk.Frame(root, bg='darkgray')  # Set background to dark gray
    button_frame_left.pack(side=tk.LEFT, padx=10, pady=20, expand=True)

    # Two buttons for Open Map URL
    btn_open = tk.Button(button_frame_left, text="Open Map URL", command=open_map_url, width=30)
    btn_open.pack(pady=5)

    # Button for osu!direct link
    btn_osu_direct = tk.Button(button_frame_left, text="osu!direct link", command=open_osu_direct_link, width=30)
    btn_osu_direct.pack(pady=5)

    # Frame for the right button
    button_frame_right = tk.Frame(root, bg='darkgray')  # Set background to dark gray
    button_frame_right.pack(side=tk.RIGHT, padx=10, pady=20, expand=True)

    # Round button for generating maps
    def create_round_button(canvas, x, y, radius):
        # Create a round button on the canvas
        button_id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='lightblue', outline='')

        # Add text to the button
        text_id = canvas.create_text(x, y, text="Generate", font=("Arial", 10, "bold"))

        # Bind mouse events to change color and call generate_map
        canvas.tag_bind(button_id, '<Button-1>', lambda e: generate_map())  # Left click
        canvas.tag_bind(text_id, '<Button-1>', lambda e: generate_map())  # Left click for text as well

        # Change color on hover
        canvas.tag_bind(button_id, '<Enter>', lambda e: canvas.itemconfig(button_id, fill='lightblue'))  # Mouse enter
        canvas.tag_bind(button_id, '<Leave>', lambda e: canvas.itemconfig(button_id, fill='lightblue'))  # Mouse leave

        # Ensure clicking anywhere inside the button is captured, not just on the text
        canvas.tag_bind(button_id, '<Button-1>', lambda e: generate_map())  # Left click

        return button_id

    # Create a canvas for the round button
    canvas = tk.Canvas(button_frame_right, width=100, height=100, bg='darkgray', highlightthickness=0)
    canvas.pack()

    # Create the round button
    create_round_button(canvas, 45, 45, 40)  # 40 is the radius of the circle

    root.mainloop()


if __name__ == "__main__":
    main()
