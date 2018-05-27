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
        #Check the title arg
        if title:
            #If something is passed, assign to the attibute
            self.title = title
        #Otherwise check the kwargs
        elif len(kwargs) > 0 and kwargs.get("title"):
            #If exists on the kwargs assign to the attribute
            self.title = kwargs.get("title")
        else:
            #If no argument and no kwargs assign default value
            self. title = "No title"

        #Check the synopse arg
        if synopse:
            #If something is passed, assign to the attibute
            self.synopse = synopse
        #Otherwise check the kwargs
        elif len(kwargs) > 0 and kwargs.get("synopse"):
            #If exists on the kwargs assign to the attribute
            self.synopse = kwargs.get("synopse")
        else:
            #If no argument and no kwargs assign default value
            self. synopse = "Empty"

        #Check the duration arg
        if duration:
            #If something is passed, assign to the attibute
            self.duration = duration
        #Otherwise check the kwargs
        elif len(kwargs) > 0 and kwargs.get("duration"):
            #If exists on the kwargs assign to the attribute
            self.duration = kwargs.get("duration")
        else:
            #If no argument and no kwargs assign default value
            self. duration = "(XX min)"

        #Check the section arg
        if section:
            #If something is passed, assign to the attibute
            self.section = section
        #Otherwise check the kwargs
        elif len(kwargs) > 0 and kwargs.get("section"):
            #If exists on the kwargs assign to the attribute
            self.section = kwargs.get("section")
        else:
            #If no argument and no kwargs assign default value
            self.section = "No section"

        #Check the director arg
        if director:
            #If something is passed, assign to the attibute
            self.director = director
        #Otherwise check the kwargs
        elif len(kwargs) > 0 and kwargs.get("director"):
            #If exists on the kwargs assign to the attribute
            self.director = kwargs.get("director")
        else:
            #If no argument and no kwargs assign default value
            self.director = "Director"

    def __dict__(self):
        """Returns a dictionary object from the properties"""
        return {"title": self.title, "director": self.director, "section": self.section, "duration": self.duration,
                "synopse": self.synopse}
