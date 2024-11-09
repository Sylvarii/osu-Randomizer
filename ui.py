import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import webbrowser
import json
import os
from main import OsuRandomizerLogic

config_file = "settings.json"


class OsuRandomizer(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = OsuRandomizerLogic()
        self.sidebar_open = False
        self.api_key_input = None
        self.initui()

    def initui(self):
        self.setWindowTitle("osu!Randomizer")
        self.setGeometry(100, 100, 500, 300)
        self.setStyleSheet("background-color: darkgray;")

        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Label for result inside a large blue rectangle
        self.result_label = QLabel("", self)
        self.result_label.setFont(QFont("Arial", 14))
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("background-color: lightblue; border-radius: 15px;")
        self.result_label.setFixedSize(465, 150)

        # Layout for buttons
        button_layout = QHBoxLayout()

        # Buttons for Map URL and osu!direct link with adjusted width
        btn_open = QPushButton("Open Map URL", self)
        btn_open.clicked.connect(self.open_map_url)
        btn_open.setFixedWidth(150)
        button_layout.addWidget(btn_open)

        # Round button for generating maps
        generate_button = QPushButton("Generate", self)
        generate_button.clicked.connect(self.generate_map)
        generate_button.setFixedSize(80, 80)
        generate_button.setStyleSheet("""
            QPushButton {
                background-color: lightblue; 
                border-radius: 40px; 
                font: bold 12px Arial;
            }
        """)
        button_layout.addWidget(generate_button, alignment=Qt.AlignCenter)

        # osu!direct link button
        btn_osu_direct = QPushButton("osu!direct link", self)
        btn_osu_direct.clicked.connect(self.open_osu_direct_link)
        btn_osu_direct.setFixedWidth(150)
        button_layout.addWidget(btn_osu_direct)

        # Layout for settings button
        button_frame_right = QVBoxLayout()

        # Settings button to toggle sidebar
        btn_settings = QPushButton("Settings", self)
        btn_settings.clicked.connect(self.toggle_sidebar)
        btn_settings.setFixedHeight(300)  # Full Y-axis height
        button_frame_right.addWidget(btn_settings, alignment=Qt.AlignRight)

        # Sidebar frame with settings options (initially hidden)
        self.sidebar_frame = QFrame(self)
        self.sidebar_frame.setFixedWidth(200)
        self.sidebar_frame.setStyleSheet("background-color: lightblue; border: 1px solid gray;")
        sidebar_layout = QVBoxLayout()

        api_key_layout = QHBoxLayout()

        lbl_custom = QLabel("API Key:", self)
        api_key_layout.addWidget(lbl_custom, alignment=Qt.AlignLeft)

        self.api_key_input = QLineEdit(self)
        self.api_key_input.setEchoMode(QLineEdit.Password)
        api_key_layout.addWidget(self.api_key_input)

        save_button = QPushButton("Save API Key", self)
        save_button.clicked.connect(self.save_api_key)
        api_key_layout.addWidget(save_button)

        sidebar_layout.addLayout(api_key_layout)

        self.sidebar_frame.setLayout(sidebar_layout)
        self.sidebar_frame.setVisible(False)

        # Left and right panel organization
        left_panel = QVBoxLayout()
        left_panel.addWidget(self.result_label)
        left_panel.addLayout(button_layout)

        # Add left and right layouts to main layout
        main_layout.addLayout(left_panel)
        main_layout.addLayout(button_frame_right)
        main_layout.addWidget(self.sidebar_frame)

        # Load API key after all UI elements are initialized
        self.load_api_key()

    def open_map_url(self):
        current_map_id = self.logic.get_current_map_id()
        if current_map_id is not None:
            map_url = f"https://osu.ppy.sh/b/{current_map_id}"
            webbrowser.open(map_url)
        else:
            print("Error: current_map_id is None!")

    def open_osu_direct_link(self):
        current_map_id = self.logic.get_current_map_id()
        if current_map_id is not None:
            map_url = f"osu://b/{current_map_id}"
            webbrowser.open(map_url)
        else:
            print("Error: current_map_id is None!")

    def generate_map(self):
        result = self.logic.get_random_map()
        self.result_label.setText(result)

    def toggle_sidebar(self):
        if self.sidebar_open:
            self.sidebar_frame.setVisible(False)
            self.resize(self.prev_width, self.prev_height)
            self.adjustSize()
        else:
            self.prev_width, self.prev_height = self.width(), self.height()
            self.resize(700, 300)
            self.adjustSize()
            self.sidebar_frame.setVisible(True)

        self.sidebar_open = not self.sidebar_open

    def load_api_key(self):
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as file:
                    config = json.load(file)
                    api_key = config.get("api_key", "")
                    if api_key:
                        self.api_key_input.setText(api_key)
                        self.api_key_input.setEnabled(False)  # Disable input when key is loaded
                    else:
                        self.api_key_input.setEnabled(True)  # Allow the user to input their key if it's empty
                        self.api_key_input.setText("")  # Clear the field if there's no key in the config
            except json.JSONDecodeError:
                print(f"Error decoding JSON in {config_file}. Please check the file format.")
            except Exception as e:
                print(f"An error occurred while loading the API key: {e}")

    def save_api_key(self):
        api_key = self.api_key_input.text()
        if api_key:
            try:
                with open(config_file, 'w') as file:
                    json.dump({"api_key": api_key}, file, indent=4)
                    print(f"Saved API Key!")
            except Exception as e:
                print(f"An error occurred while saving the API key: {e}")


def main():
    app = QApplication(sys.argv)
    osu_randomizer = OsuRandomizer()
    osu_randomizer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
