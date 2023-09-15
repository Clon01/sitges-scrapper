from datetime import datetime, timedelta


class Session:
    """Data model for movie objects"""
    def __init__(self, name=None, begin=None, duration=None, location=None, description=None, **kwargs):
        """
        Creates a new session object
        :param name: Name of the movie (Optional)
        :param begin: Start time (Optional)
        :type begin: datetime
        :param duration: Duration (Optional)
        :param duration: timedelta
        :param location: Location (Optional)
        :param kwargs:
        """

        # Check the name arg
        if name:
            # If something is passed, assign to the attribute
            self.name = name
        # Otherwise check the kwargs
        elif len(kwargs) > 0 and kwargs.get("name"):
            # If exists on the kwargs assign to the attribute
            self.name = kwargs.get("name")
        else:
            # If no argument and no kwargs assign default value
            self. name = "Untitled"

        # Check the begin arg
        if begin:
            # If something is passed, assign to the attribute
            self.begin = begin
        # Otherwise check the kwargs
        elif len(kwargs) > 0 and kwargs.get("begin"):
            # If exists on the kwargs assign to the attribute
            self.begin = kwargs.get("begin")
        else:
            # If no argument and no kwargs assign default value
            self. begin = "Error"

        # Check the duration arg
        if duration and type(duration) == timedelta:
            # If something is passed, assign to the attribute
            self.duration = duration
        # Otherwise check the kwargs
        elif len(kwargs) > 0 and kwargs.get("duration"):
            # If exists on the kwargs assign to the attribute
            self.duration = kwargs.get("duration")
        else:
            # If no argument and no kwargs assign default value
            self. duration = "Error"

        # Check the location arg
        if location:
            # If something is passed, assign to the attribute
            self.location = location
        # Otherwise check the kwargs
        elif len(kwargs) > 0 and kwargs.get("location"):
            # If exists on the kwargs assign to the attribute
            self.location = kwargs.get("location")
        else:
            # If no argument and no kwargs assign default value
            self. location = "Nowhere"

        if description:
            self.description = description
        else:
            self.description = self.name
