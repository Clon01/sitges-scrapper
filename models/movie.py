class Movie:
    """Data model for movie objects"""
    def __init__(self, title=None, director=None, section=None, duration=None, synopse=None, **kwargs):
        """
        Creates a new Movie object
        :param title: str: The movie title (Optional)
        :param director: str: The movie director (Optional)
        :param section: str: The movie section (Optional)
        :param duration: str: The movie duration (Optional)
        :param synopse: str: The movie description (Optional)
        :param kwargs: Dictionary with all the parameters above (Optional)
        """
        self.synopse = synopse
        self.duration = duration
        self.section = section
        self.director = director
        self.title = title

    def __dict__(self):
        """Returns a dictionary object from the properties"""
        return {"title": self.title, "director": self.director, "section": self.section, "duration": self.duration,
                "synopse": self.synopse}