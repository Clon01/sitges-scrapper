from data.Settings import Settings
import csv
from data.CalendarScrapper import CalendarScrapper


def map_session_ro_row(session):
    date = session.begin.strftime("%d-%m-%Y")
    time = session.begin.strftime("%H:%M:%S")
    title = session.name
    duration = session.duration.total_seconds()/60
    print([date, time, title, duration])
    return [date, time, title, duration]


def export_csv(events):
    with open('test.csv', 'w') as output:
        writer = csv.writer(output)
        writer.writerows(map(map_session_ro_row, events))


if __name__ == '__main__':
    # Load settings.json file with the app settings
    my = Settings(__file__)
    # Create a new CalendarScrapper using the URL from settings
    scrap = CalendarScrapper(my.settings["URL"], my.settings.get("Params"))
    # Create a list
    events = list()
    # Loop calendar entries into CalendarExport
    for session in scrap.get_sessions():
        if session.begin != "Error":
            events.append(session)
    # Save export html to the file from settings
    export_csv(events)


