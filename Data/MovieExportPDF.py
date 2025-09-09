from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import KeepTogether
from reportlab.platypus.doctemplate import SimpleDocTemplate, Spacer
from reportlab.platypus.para import Paragraph
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


class MovieExportPDF:

    def __init__(self):
        # Create a new empty html object
        self.output = SimpleDocTemplate("films.pdf", pagesize=A4)
        self.spacer = Spacer(width=1, height=.2*cm)
        self.story = [self.spacer]
        self.style = getSampleStyleSheet()["BodyText"]
        self.style.alignment = TA_LEFT
        self.count = 0

    def create_matrix(self, movie):
        """
        Create a styled matrix for the PDF
        :param movie: A Movie object
        :return: Matrix of the
        """
        _director = Paragraph(movie.director, self.style)
        _title = Paragraph(movie.title, self.style)
        _section = Paragraph(movie.section, self.style)
        _duration = Paragraph(movie.duration, self.style)
        _synopse = Paragraph(movie.synopse, self.style)

        return [[_director, _title],
                  [_section, _duration],
                  ["",_synopse]]

    def add_movie(self, movie):
        """
        Add a movie object to the output html
        :param movie: A Movie object
        :return: None
        """
        # Create a matrix for the PDF
        matrix = self.create_matrix(movie)
        # Create a new table on the document
        table = Table(matrix, hAlign='LEFT', colWidths=[4*cm, 12*cm])
        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.25, colors.black),
        ]))
        # Add table to the document
        self.story.append(KeepTogether(table))
        # Add a line break after the table
        self.story.append(self.spacer)
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
        self.output.build(self.story)


