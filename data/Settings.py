import json
import os


class Settings:

    def __init__(self, dir):

        filename = os.path.join(os.path.dirname(os.path.abspath(dir)), "settings.json")
        with open(filename) as file:
            self.settings = json.load(file)

    def banned_sections(self) -> str:

        return "|".join(self.settings["BannedSections"])

    def save_settings(self):
        # TODO Create method to save settings before closure
        pass