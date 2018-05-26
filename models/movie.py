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

        if title:
            self.title = title
        elif len(kwargs) > 0 and kwargs.get("title"):
            self.title = kwargs.get("title")
        else:
            self. title = ""

        if synopse:
            self.synopse = synopse
        elif len(kwargs) > 0 and kwargs.get("synopse"):
            self.synopse = kwargs.get("synopse")
        else:
            self. synopse = ""

        if duration:
            self.duration = duration
        elif len(kwargs) > 0 and kwargs.get("duration"):
            self.duration = kwargs.get("duration")
        else:
            self. duration = ""

        if section:
            self.section = section
        elif len(kwargs) > 0 and kwargs.get("section"):
            self.section = kwargs.get("section")
        else:
            self.section = ""

        if director:
            self.director = director
        elif len(kwargs) > 0 and kwargs.get("director"):
            self.director = kwargs.get("director")
        else:
            self.director = ""

    def __dict__(self):
        """Returns a dictionary object from the properties"""
        return {"title": self.title, "director": self.director, "section": self.section, "duration": self.duration,
                "synopse": self.synopse}
