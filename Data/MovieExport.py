from lib.html import HTML


class MovieExport:

    def __init__(self):
        # Create a new empty html object
        self.output = HTML('html', escape=False)
        self.count = 0

    def add_movie(self, movie):
        """
        Add a movie object to the output html
        :param movie: A Movie object
        :return: None
        """
        # Create a new table on the html
        #t = self.output.body.table(border="1")
        t = self.output.body.table()
        # Add a first row
        r = t.tr
        # Write title and director on the first row
        # Also define 20/80% ratio for 2 cells
        r.td(movie.director, escape=False)
        r.td(movie.title, escape=False)
        # Add a secod row
        r2 = t.tr
        # Write section and duration on the second row
        r2.td(movie.section, escape=False)
        r2.td(movie.duration, escape=False)
        # Add a third row
        r3 = t.tr
        # Start with an empty row then write the synopse
        r3.td()
        r3.td(movie.synopse, escape=False)
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
