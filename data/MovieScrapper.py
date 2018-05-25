import re
import requests
from bs4 import BeautifulSoup
from models.movie import Movie


class MovieScrapper:
    """Returns movies from the website"""

    def __init__(self, url: str):
        """Creates a movie scrapper object"""
        self.soup = self.get_movie_soup(url)

    def get_title(self, node):
        """
        Returns the title from the currently selected movie in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The movie title
        """
        try:
            return node.h3.a.text
        except (TypeError, KeyError, AttributeError):
            return None

    def get_director(self, node):
        """
        Returns the director from the currently selected movie in the BeautifulSoup node
        :param node: A soup object positioned in the movie root
        :return: str: The movie director
        """
        try:
            return node.h6.text
        except (TypeError, KeyError, AttributeError):
            return None

    def get_section(self, node) -> str:
        """
        Returns the section from the currently selected movie in the BeautifulSoup node
        :rtype: str
        :param node: A soup object positioned in the movie root
        :return: str: The movie section
        """
        try:
            return node.p.text
        except (TypeError, KeyError, AttributeError):
            return None

    def get_link(self, node) -> str:
        """
        Returns the link from the currently selected movie in the BeautifulSoup node
        :rtype: str
        :param node: A soup object positioned in the movie root
        :return: str: The movie section
        """
        try:
            return node.h3.a["href"]
        except (TypeError, KeyError, AttributeError):
            return None

    def get_movie_soup(self, link):
        """
        Returns a BeautifulSoup object for the movie sub page
        :param link: str: Link to the movie sub page
        :return: A soup object containing the full sub page
        """
        if link:
            return BeautifulSoup(requests.get(link).text, "html.parser")
        else:
            return None

    def get_synopse(self, soup):
        """
        Returns the synopse from the movie page in the BeautifulSoup node
        :param soup: A soup object containing the movie page
        :return: str: The movie synopse
        """
        if soup:
            try:
                return soup.find("div", {"class": "section_sinopsi"}).p.text
            except (TypeError, KeyError, AttributeError):
                return None
        else:
            return None

    def get_duration(self, soup):
        """
        Returns the duration from the movie page in the BeautifulSoup node
        :param soup: A soup object containing the movie page
        :return: str: The movie duration
        """
        if soup:
            try:
                return soup.find("div", {"class": "section_fitxa_artistica"}).p.strong.text
            except (TypeError, KeyError, AttributeError):
                return None
        else:
            return None

    def get_movie(self, node):
        """
        Returns a Movie object with all the data found in the bs4 node
        :param node: A soup object positioned in the movie root
        :return: The Movie object
        """
        subpage = self.get_movie_soup(self.get_link(node))
        return Movie(title=self.get_title(node), director=self.get_director(node), section=self.get_section(node),
                     synopse=self.get_synopse(subpage), duration=self.get_duration(subpage))

    def is_movie_in_section(self, node, exclusion: str):
        """
        Returns a list of movies excluding all movies in the matching sections
        :param node: A soup object positioned in the movie root
        :param exclusion: str: Regular expression. All movies with a section matching this string will not be returned
        :return: A collection of Movie objects
        """
        re.match(exclusion, self.get_section(node))
        
    def slice_soup_by_movies(self):
        """
        Returns a list with all movie nodes
        :return: A collection of soup nodes containing movie info
        """
        for node in self.soup.findAll("div", {"class": "right-banner-bottom"}):
            yield node

    def get_movies_by_section(self, exclusion: str):
        """
        Returns a list of movies excluding all movies in the matching sections
        :param exclusion: str: Regular expression. All movies with a section matching this string will not be returned
        :return: A collection of Movie objects
        """
        for node in self.slice_soup_by_movies():
            if not self.is_movie_in_section(node, exclusion):
                yield self.get_movie(node)
