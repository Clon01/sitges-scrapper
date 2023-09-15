import re
import requests
from bs4 import BeautifulSoup
import hashlib
import concurrent.futures
from models.Movie import Movie
from html2text import html2text


class MovieScrapper:
    """Returns movies from the website"""

    def __init__(self, url: str, params=None):
        """Creates a movie scrapper object"""
        self.SEPARATOR = ", "
        self.movies = list()
        self.directors = dict()
        self.sections = dict()
        self.countries = dict()
        self.prepare_data(url, params)

    def parse_directors(self, raw_data):
        self.directors = {i["id"]: {"id": i["id"], "name": i["name"]["ca"]} for i in raw_data.get("directors")}

    def parse_sections(self, raw_data):
        self.sections = {i["id"]: {"id": i["id"], "name": i["name"]["ca"]} for i in raw_data.get("sections")}

    def parse_countries(self, raw_data):
        self.countries = {i["id"]: {"id": i["id"], "name": i["name"]["ca"]} for i in raw_data.get("countries")}

    def prepare_data(self, url, params):
        raw_data = dict()
        response = requests.get(url, params)
        if response.status_code == 200:
            raw_data = response.json()
            self.movies = raw_data.get("films")
            self.parse_directors(raw_data)
            self.parse_sections(raw_data)
            self.parse_countries(raw_data)



    @staticmethod
    def get_title(node) -> [str]:
        """
        Returns the title from the currently selected movie in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The movie title
        """
        try:
            # Looks up the title
            return node.get("title").get("ca")
        except (TypeError, KeyError, AttributeError):
            # If the key does not exists return this default
            return None

    def get_director(self, node) -> [str]:
        """
        Returns the director from the currently selected movie in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The movie director
        """
        try:
            directors = list()
            #  Looks up the director
            for director_id in node.get("directors"):
                directors.append(self.directors.get(director_id).get("name"))
            return self.SEPARATOR.join(directors)
        except (TypeError, KeyError, AttributeError):
            #  If the key does not exists return this default
            return None

    def get_section(self, node) -> [str]:
        """
        Returns the section from the currently selected movie in the BeautifulSoup node
        :rtype: str
        :param node: A soup object positioned in the movie root
        :return: str: The movie section
        """
        try:
            sections = list()
            #  Looks up the section
            for section_id in node.get("sections"):
                sections.append(self.sections.get(section_id).get("name"))
            return self.SEPARATOR.join(sections)

        except (TypeError, KeyError, AttributeError):
            #  If the key does not exists return this default
            return ""

    @staticmethod
    def get_link(node) -> [str]:
        """
        Returns the link from the currently selected movie in the BeautifulSoup node
        :rtype: str
        :param node: A soup object positioned in the movie root
        :return: str: The movie section
        """
        try:
            #  Looks up the link
            return node.h3.a["href"]
        except (TypeError, KeyError, AttributeError):
            #  If the key does not exists return this default
            return ""

    @staticmethod
    def get_movie_soup(link, params=None) -> [BeautifulSoup]:
        """
        Returns a BeautifulSoup object for the movie sub page
        :param link: str: Link to the movie sub page
        :param params: Parameters to pass to the URL
        :type params: Dict or None
        :return: A soup object containing the full sub page
        """
        #  if the link is something
        if link:
            # Request the URL and parse the text into a soup object
            return BeautifulSoup(requests.get(link, params=params).text, "html.parser")
        else:
            # If the link is empty return None
            return None

    @staticmethod
    def get_synopsis(node) -> [str]:
        """
        Returns the synopsis from the movie page in the BeautifulSoup node
        :param node: A soup object containing the movie page
        :return: str: The movie synopsis
        """

        try:
            #  Looks up the synopsis
            return html2text(node.get("synopsis").get("ca"))
        except (TypeError, KeyError, AttributeError):
            #  If the key does not exists return this default
            return None


    def get_duration(self, node) -> [str]:
        """
        Returns the duration from the movie page in the BeautifulSoup node
        :param node: A soup object containing the movie page
        :return: str: The movie duration
        """

        try:
            #  Gets all countries
            countries = list()
            for country_id in node.get("countries"):
                countries.append(self.countries.get(country_id).get("name"))
            duration = node.get("duration")
            year = node.get("year")
            return f"{duration} mins. {self.SEPARATOR.join(countries)} / {year}"

        except (TypeError, KeyError, AttributeError, IndexError):
            #  If the key does not exists return this default
            return None


    def get_movie(self, node) -> Movie:
        """
        Returns a Movie object with all the data found in the bs4 node
        :param node: A soup object positioned in the movie root
        :return: The Movie object
        """
        # Create a Movie object and return it on the fly getting each argument from it's own method
        return Movie(
            title=self.get_title(node),
            director=self.get_director(node),
            section=self.get_section(node),
            synopse=self.get_synopsis(node),
            duration=self.get_duration(node)
        )

    def is_movie_in_section(self, node, exclusion: str) -> [str]:
        """
        Returns a list of movies excluding all movies in the matching sections
        :param node: A soup object positioned in the movie root
        :param exclusion: str: Regular expression. All movies with a section matching this string will not be returned
        :return: A collection of Movie objects
        """
        # Return true if the regular expression on exclusion matches the movie section
        return re.search(exclusion, self.get_section(node))

    def slice_soup_by_movies(self):
        """
        Generator with all movie nodes in the URL
        :return: A generator of soup nodes containing movie info
        """
        # For each movie matched by tag and class
        for node in self.soup.findAll("div", {"class": "right-banner-bottom"}):
            # Return this node
            yield node

    def get_movies_by_section(self, exclusion: str):
        """
        Generator of movies excluding all movies in the matching sections
        :param exclusion: str: Regular expression. All movies with a section matching this string will not be returned
        :return: A generator of Movie objects
        """
        # Build a list with all movies except banned sections
        nodes = [node for node in self.movies if not self.is_movie_in_section(node, exclusion)]
        # Create concurrent threads to run requests while waiting for the next response
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Yield avery returned movie
            for movie in executor.map(self.get_movie, nodes):
                yield movie

    def get_hash(self):
        """
        Generates a sha256 hash from the retrieved website
        :return: An hexadecimal digest string.
        """
        # Create a sha256 hasher object
        hasher = hashlib.sha256()
        # Extract only the div containing the movie list
        # will return a different hash even if the user readable content has not changed

        # Extract a valid string for encoding
        text = self.movies.__str__().encode("utf-8")
        # pass the string to the hasher and return the hash
        hasher.update(text)
        return hasher.hexdigest()



