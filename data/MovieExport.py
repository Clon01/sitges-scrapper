from lib.html import HTML
from enum import Enum, auto
from csv import DictWriter


class Formats(Enum):
    HTML = auto()
    CSV = auto()


class ExportFactory:

    def __init__(self):
        self._factory = dict()
        self._factory[Formats.HTML.name] = Movie2HTML
        self._factory[Formats.CSV.name] = Movie2CSV
        self._exporter = list()
        self._movies = list()

    def add_output(self, file_format:Formats, file_name):
        self._exporter.append(
            self._factory[file_format.name](file_name)
        )

    def add_movie(self, movie):
        self._movies.append(movie)

    def save_to_file(self):
        for exporter in self._exporter:
            for movie in self._movies:
                exporter.add_movie(movie)
            exporter.save_to_file()

    def count(self):
        return len(self._movies)


class MovieExport:

    def __init__(self):
        # Create a new empty html object
        self.output = HTML('html')
        self.count = 0

    def add_movie(self, movie):
        """
        Add a movie object to the output html
        :param movie: A Movie object
        :return: None
        """
        # Create a new table on the html
        t = self.output.body.table(border="1")
        # Add a first row
        r = t.tr
        # Write title and director on the first row
        # Also define 20/80% ratio for 2 cells
        r.td(movie.director, width="20%")
        r.td(movie.title)
        # Add a secod row
        r2 = t.tr
        # Write section and duration on the second row
        r2.td(movie.section)
        r2.td(movie.duration)
        # Add a third row
        r3 = t.tr
        # Start with an empty row then write the synopse
        r3.td()
        r3.td(movie.synopse)
        # Add a line break after the table
        self.output.body.br()
        # Add 1 to the movie counter
        self.count += 1
        # This function returns nothing
        return None

    def save_to_file(self, filename):
        """
        Saves the added film to an html file
        :param filename: str: filename
        :return: None
        """
        # Open the filename to be re-written
        with open(filename, 'w+', encoding='utf-8') as outfile:
            # write the content of the html output to the file
            outfile.write(self.output.__str__())

    # def count(self):
    #     """
    #     Counts the number of movies
    #     :return: Number of movies in this instance
    #     :rtype: int
    #     """
    #     return self.counter


class Movie2HTML:

    def __init__(self, file_name):
        # Create a new empty html object
        self.output = HTML('html')
        self.file_name = file_name

    def add_movie(self, movie):
        """
        Add a movie object to the output html
        :param movie: A Movie object
        :return: None
        """
        # Create a new table on the html
        t = self.output.body.table(border="1")
        # Add a first row
        r = t.tr
        # Write title and director on the first row
        # Also define 20/80% ratio for 2 cells
        r.td(movie.director, width="20%")
        r.td(movie.title)
        # Add a secod row
        r2 = t.tr
        # Write section and duration on the second row
        r2.td(movie.section)
        r2.td(movie.duration)
        # Add a third row
        r3 = t.tr
        # Start with an empty row then write the synopse
        r3.td()
        r3.td(movie.synopse)
        # Add a line break after the table
        self.output.body.br()
        # This function returns nothing

    def save_to_file(self):
        """
        Saves the added film to an html file
        :return: None
        """
        # Open the filename to be re-written
        with open(self.file_name, 'w+', encoding='utf-8') as outfile:
            # write the content of the html output to the file
            outfile.write(self.output.__str__())


class Movie2CSV:

    def __init__(self, file_name):
        self.file_name = file_name
        self._movies = list()

    def add_movie(self, movie):
        self._movies.append(
            {
                "Title": movie.title,
                "Year": movie.duration[-4:],
                "Directors": movie.director.replace('&', ',')
            }
        )

    def save_to_file(self):
        with open(self.file_name, 'w+') as csv_file:
            csv_writer = DictWriter(csv_file, self._movies[0].keys(), lineterminator='\n')
            csv_writer.writeheader()
            csv_writer.writerows(self._movies)
