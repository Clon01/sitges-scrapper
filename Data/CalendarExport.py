from ics import Calendar, Event
import html

class CalendarExport:

    def __init__(self):
        self.c = Calendar()

    def add_session(self, session):
        try:
            e = Event()
            e.name = html.unescape(session.name)
            e.begin = session.begin
            e.duration = session.duration
            e.location = html.unescape(session.location)
            e.description = html.unescape(session.description)
            self.c.events.add(e)
        except TypeError:
            print(f"Error!!! -> {session.name}: {session.duration}")

    def save_to_file(self, filename):
        """
        Saves the added film to an html file
        :param filename: str: filename
        :return: None
        """
        # Open the filename to be re-written
        with open(filename, 'w+', encoding='utf-8') as outfile:
            # write the content of the html output to the file
            outfile.writelines(self.c)
