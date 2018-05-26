from lib.html import HTML


class MovieExport:

    def __init__(self):
        self.output = HTML('html')

    def add_movie(self, movie):
        """
        Add a movie object to the output html
        :param movie: A Movie object
        :return: None
        """

        t = self.output.body.table(border="1")
        r = t.tr
        r.td(movie.title, width="20%")
        r.td(movie.director)
        r2 = t.tr
        r2.td(movie.section)
        r2.td(movie.duration)
        r3 = t.tr
        r3.td()
        r3.td(movie.synopse)
        self.output.body.br

        return None

    def save_to_file(self, filename):
        """
        Saves the added film to an html file
        :param filename: str: filename
        :return: None
        """
        with open(filename, 'w+', encoding='utf-8') as outfile:
            outfile.write(self.output.__str__())


    # @staticmethod
    # def to_html(movies, filename):
    #     output = HTML('html')
    #     body = output.body
    #     with open(filename, 'w+', encoding='utf-8') as outfile:
    #         for m in movies:
    #             t = body.table(border="1")
    #             r = t.tr
    #             r.td(m.title, width="20%")
    #             r.td(m.director)
    #             r2 = t.tr
    #             r2.td(m.section)
    #             r2.td(m.duration)
    #             r3 = t.tr
    #             r3.td()
    #             r3.td(m.synopse)
    #             body.br
    #
    #             outfile.write(output.__str__())
