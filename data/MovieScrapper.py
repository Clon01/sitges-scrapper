import re
import requests
from bs4 import BeautifulSoup
from models.Movie import Movie
import hashlib


class MovieScrapper:
    """Returns movies from the website"""

    def __init__(self, url: str):
        """Creates a movie scrapper object"""
        # Stores a soup object for the main website
        self.soup = self.get_movie_soup(url)

    @staticmethod
    def get_title(node) -> [str]:
        """
        Returns the title from the currently selected movie in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The movie title
        """
        try:
            # Looks up the title
            return node.h3.a.text
        except (TypeError, KeyError, AttributeError):
            # If the key does not exists return this default
            return None

    @staticmethod
    def get_director(node) -> [str]:
        """
        Returns the director from the currently selected movie in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The movie director
        """
        try:
            #  Looks up the director
            return node.h6.text
        except (TypeError, KeyError, AttributeError):
            #  If the key does not exists return this default
            return None

    @staticmethod
    def get_section(node) -> [str]:
        """
        Returns the section from the currently selected movie in the BeautifulSoup node
        :rtype: str
        :param node: A soup object positioned in the movie root
        :return: str: The movie section
        """
        try:
            #  Looks up the section
            return node.p.text
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
    def get_movie_soup(link) -> [BeautifulSoup]:
        """
        Returns a BeautifulSoup object for the movie sub page
        :param link: str: Link to the movie sub page
        :return: A soup object containing the full sub page
        """
        #  if the link is something
        if link:
            # Request the URL and parse the text into a soup object
            return BeautifulSoup(requests.get(link).text, "html.parser")
        else:
            # If the link is empty return None
            return None

    @staticmethod
    def get_synopse(soup) -> [str]:
        """
        Returns the synopse from the movie page in the BeautifulSoup node
        :param soup: A soup object containing the movie page
        :return: str: The movie synopse
        """
        if soup:
            try:
                #  Looks up the synopse
                return soup.find("div", {"class": "section_sinopsi"}).p.text
            except (TypeError, KeyError, AttributeError):
                #  If the key does not exists return this default
                return None
        else:
            return None

    @staticmethod
    def get_duration(soup) -> [str]:
        """
        Returns the duration from the movie page in the BeautifulSoup node
        :param soup: A soup object containing the movie page
        :return: str: The movie duration
        """
        if soup:
            try:
                #  Looks up the duration
                return soup.find("div", {"class": "section_fitxa_artistica"}).p.strong.text
            except (TypeError, KeyError, AttributeError):
                #  If the key does not exists return this default
                return None
        else:
            return None

    def get_movie(self, node) -> Movie:
        """
        Returns a Movie object with all the data found in the bs4 node
        :param node: A soup object positioned in the movie root
        :return: The Movie object
        """
        # Get the link for the movie and generate a soup for this movie subpage
        # This is required because synopse and duration are obtained from the subpage
        subpage = self.get_movie_soup(self.get_link(node))
        # Create a Movie object and return it on the fly getting each argument from it's own method
        return Movie(title=self.get_title(node), director=self.get_director(node), section=self.get_section(node),
                     synopse=self.get_synopse(subpage), duration=self.get_duration(subpage))

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
        # For each node in all movies
        for node in self.slice_soup_by_movies():
            # Check if movie section is banned
            if not self.is_movie_in_section(node, exclusion):
                # When not banned, return node
                yield self.get_movie(node)

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
        div = self.soup.find("div", {"class": "Grid"})
        # Extract a valid string for encoding
        text = div.__str__().encode("utf-8")
        # pass the string to the hasher and return the hash
        hasher.update(text)
        return hasher.hexdigest()

