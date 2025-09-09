import requests
from bs4 import BeautifulSoup
from models.Session import Session
import hashlib
from datetime import datetime, timedelta


class CalendarScrapper:
    """Returns sessions from the website"""

    def __init__(self, base_url: str, year: str, params=None):
        """Creates a calendar scrapper object"""
        self.SEPARATOR = ", "
        self.PARAGRAF = "\n \n \n"
        self.sessions = list()
        self.locations = dict()
        self.movies = dict()
        # Stores a soup object for the main website
        self.prepare_data(base_url=base_url, year=year, params=params)

    def parse_locations(self, raw_data):
        self.locations = {i["id"]: {"id": i["id"], "name": i["name"]["ca"]} for i in raw_data.get("locations")}

    def parse_movies(self, raw_data):
        self.movies = {i["id"]: {"id": i["id"],
                                 "name": i["title"]["ca"],
                                 "synopsis": i["synopsis"]["ca"],
                                 "duration": i["duration"]}
                       for i in raw_data.get("films")}

    def prepare_data(self, base_url: str, year: str, params):
        raw_data = dict()
        response_sessions = requests.get(f"{base_url}films/{year}/sessions", params)
        if response_sessions.status_code == 200:
            raw_data = response_sessions.json()
        response_location = requests.get(f"{base_url}location/list", params)
        if response_location.status_code == 200:
            raw_data["locations"] = response_location.json().get("locations")
        response_films = requests.get(f"{base_url}films/{year}", params)
        if response_films.status_code == 200:
            raw_data["films"] = response_films.json().get("films")

        if response_sessions.status_code == 200 and response_location.status_code == 200 and response_films.status_code == 200:
            self.sessions = [n for n in raw_data.get("sessions") if "392-location" in n.get("locations")]
            self.parse_locations(raw_data)
            self.parse_movies(raw_data)

    @staticmethod
    def get_name(node) -> [str]:
        """
        Returns the title from the currently selected movie in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The movie title
        """
        try:
            # Looks up the title
            return node.get("name").get("ca")
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
            t = node.get("start_date")
            # Convert string to datetime object
            # Need to subtract 2 hrs to make it GMT or google will get the time wrong
            begin = datetime.strptime(t, "%Y-%m-%dT%H:%M:%S") - timedelta(minutes=120)
            return begin
        except (TypeError, KeyError, AttributeError) as e:
            # If the key does not exists return this default
            type(e)
            return None

    def get_location(self, node) -> [str]:
        """
        Returns the venue from the currently selected event in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The venue name
        """
        try:
            locations = list()
            for location_id in node.get("locations"):
                locations.append(self.locations.get(location_id).get("name"))
            return self.SEPARATOR.join(locations)
        except (TypeError, KeyError, AttributeError):
            # If the key does not exists return this default
            return None

    def get_duration(self, node) -> [timedelta]:
        """
        Returns the stating time from the currently selected event in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The movie title
        """
        try:
            accumulated_time = 0
            for movie_id in node.get("films"):
                accumulated_time += self.movies.get(movie_id).get("duration")
            if accumulated_time == 0:
                accumulated_time = 90
            return timedelta(minutes=accumulated_time)
        except (TypeError, KeyError, AttributeError, ValueError):
            # If the key does not exists return this default
            return timedelta(minutes=90)

    def get_description(self, node) -> [str]:
        """
        Returns a list of movie titles and synopses for the session
        :param node: The session node
        :return: A list of movies and synopses for the session
        """
        try:
            synopsis = list()
            for movie_id in node.get("films"):
                movie = self.movies.get(movie_id)
                title = movie.get("name")
                synopse = movie.get("synopsis")
                synopsis.append(f"{title}\n{synopse}")
            return self.PARAGRAF.join(synopsis)
        except (TypeError, KeyError, AttributeError, ValueError):
            # If the key does not exists return this default
            return "Error retrieving description, please try manually"


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

        # Extract a valid string for encoding
        text = self.sessions.__str__().encode("utf-8")
        # pass the string to the hasher and return the hash
        hasher.update(text)
        return hasher.hexdigest()

    def get_session(self, node):
        return Session(name=CalendarScrapper.get_name(node),
                       begin=CalendarScrapper.get_begin(node),
                       location=self.get_location(node),
                       duration=self.get_duration(node),
                       description=self.get_description(node))

    def get_sessions(self):
        """
        Generator to gat all sessions.
        :return: Returns all the sessions in the website
        """
        # For each session in the website
        for node in self.sessions:
            yield self.get_session(node=node)
