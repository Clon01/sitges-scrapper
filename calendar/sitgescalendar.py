from data.Settings import Settings
from data.CalendarExport import CalendarExport
from data.CalendarScrapper import CalendarScrapper


if __name__ == '__main__':
    # Load settings.json file with the app settings
    my = Settings(__file__)
    # Create a new CalendarScrapper using the URL from settings
    scrap = CalendarScrapper(my.settings["URL"])
    # Check if the content of the page has changed
    if not my.check_hash(scrap.get_hash()):
        # Create a CalendarExport object
        ce = CalendarExport()
        # Loop calendar entries into CalendarExport
        for session in scrap.get_sessions():
            if session.begin != "Error":
                ce.add_session(session)
        # Save export html to the file from settings
        ce.save_to_file(my.settings["ExportFile"])
        # Save new hash in setting.json
        my.save_settings()
    else:
        print("The content didn't change since the last export")
