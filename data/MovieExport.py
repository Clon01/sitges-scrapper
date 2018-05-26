from lib.html import HTML


class MovieExport:


    @staticmethod
    def to_html(movies, filename):
        output = HTML('html')
        body = output.body
        with open(filename, 'w+', encoding='utf-8') as outfile:
            for m in movies:
                t = body.table(border="1")
                r = t.tr
                r.td(m.title, width="20%")
                r.td(m.director)
                r2 = t.tr
                r2.td(m.section)
                r2.td(m.duration)
                r3 = t.tr
                r3.td()
                r3.td(m.synopse)
                body.br

                outfile.write(output.__str__())
