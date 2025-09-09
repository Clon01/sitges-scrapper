import json
import os


class Settings:

    def __init__(self, folder):
        # Save the folder + filename for later use
        self.filename = os.path.join(os.path.dirname(os.path.abspath(folder)), "settings.json")
        # Open the file and extract the settings
        with open(self.filename) as file:
            self.settings = json.load(file)

    def banned_sections(self) -> str:
        """
        Gets all banned sections from the settings file and formats them into a regular expression string
        :return: A regular expression matching the banned sections
        """
        return "|".join(self.settings["BannedSections"])

    def check_hash(self, current_hash: str) -> [bool]:
        """
        Checks if the current hash matches the one stored in the settings
        :param current_hash: Current hash
        :return: True if the hash is the same, False if it doesn't
        """
        if "Hash" in self.settings and self.settings["Hash"] == current_hash:
            return True
        else:
            self.settings["Hash"] = current_hash
            return False

    def save_settings(self):
        """
        Saves the current settings into the settings file
        :return: None
        """
        with open(self.filename, "w+") as file:
            # Added indent=4 sort_keys=True and for readability
            json.dump(self.settings, file, indent=4, sort_keys=True)

