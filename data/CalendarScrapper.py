import requests
from bs4 import BeautifulSoup
from models.Session import Session
import hashlib
from datetime import datetime, timedelta


class CalendarScrapper:
    """Returns sessions from the website"""

    def __init__(self, url: str):
        """Creates a calendar scrapper object"""
        # Stores a soup object for the main website
        self.soup = BeautifulSoup(requests.get(url).text, "html.parser")

    @staticmethod
    def get_name(node) -> [str]:
        """
        Returns the title from the currently selected movie in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The movie title
        """
        try:
            # Looks up the title
            return node.a.text.strip()
        except (TypeError, KeyError, AttributeError):
            # If the key does not exists return this default
            return None

    @staticmethod
    def get_begin(node) -> [datetime]:
        """
        Returns the stating time from the currently selected event in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The movie title
        """
        try:
            # Looks up the time
            t = node.find("td", {"class": "col-md-1 text-center"})
            # Extract and strip the text
            s = t.text.strip()
            # Add the timezone information to the string
            s += " +0200"
            # Convert string to datetime object
            begin = datetime.strptime(s, "%d-%m-%Y\n\n%H:%M %z")
            return begin
        except (TypeError, KeyError, AttributeError) as e:
            # If the key does not exists return this default
            type(e)
            return None

    @staticmethod
    def get_location(node) -> [str]:
        """
        Returns the venue from the currently selected event in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The venue name
        """
        try:
            # Looks up the location
            t = node.find("td", {"class": "col-md-2"})
            # Extract and strip the text
            return t.text.strip()
        except (TypeError, KeyError, AttributeError):
            # If the key does not exists return this default
            return None

    @staticmethod
    def get_duration(node) -> [timedelta]:
        """
        Returns the stating time from the currently selected event in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The movie title
        """
        try:
            # Looks up the time
            t = node.findAll("td", {"class": "col-md-2"})
            if len(t) > 1:
                # Extract and strip the text
                s = t[-1].text.strip()
                # Remove the last character
                s = s[:-1]
                return timedelta(minutes=float(s))
            raise AttributeError
        except (TypeError, KeyError, AttributeError, ValueError):
            # If the key does not exists return this default
            return timedelta(minutes=90)

    def slice_soup_by_sessions(self):
        """
        Generator with all movie nodes in the URL
        :return: A generator of soup nodes containing movie info
        """
        # For each movie matched by tag and class
        for node in self.soup.findAll("tr", {"class": "row"}):
            # Return this node
            yield node

    def get_hash(self):
        """
        Generates a sha256 hash from the retrieved website
        :return: An hexadecimal digest string.
        """
        # Create a sha256 hasher object
        hasher = hashlib.sha256()
        # Extract only the div containing the movie list
        # This has to be done because of dynamic javascript in other parts of the html
        # will return a different hash even if the user readable content has not changed
        div = self.soup.find("table", {"id": "program-table"})
        # Extract a valid string for encoding
        text = div.__str__().encode("utf-8")
        # pass the string to the hasher and return the hash
        hasher.update(text)
        return hasher.hexdigest()

    @staticmethod
    def get_session(node):
        return Session(name=CalendarScrapper.get_name(node), begin=CalendarScrapper.get_begin(node),
                       location=CalendarScrapper.get_location(node), duration=CalendarScrapper.get_duration(node))

    def get_sessions(self):
        """
        Generator to gat all sessions.
        :return: Returns all the sessions in the website
        """
        # For each session in the website
        for node in self.slice_soup_by_sessions():
            yield CalendarScrapper.get_session(node=node)

