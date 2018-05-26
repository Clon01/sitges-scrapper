# import pandas
from data.MovieScrapper import MovieScrapper
from data.MovieExport import MovieExport

if __name__ == '__main__':
    url = "http://www.sitgesfilmfestival.com/cat/programa/pel_licules"
    scrap = MovieScrapper(url)
    exclusion = "urts|Brigadoon|Espai|Serial|SGAE|Petit|ort|Cocoon"

    # df = pandas.DataFrame(m.__dict__() for m in scrap.get_movies_by_section(exclusion))
    # df.sort_values(by=["title"], inplace=True)
    # print(df.to_html(columns=["title", "director", "section", "synopse", "duration"]))

    me = MovieExport()
    for m in scrap.get_movies_by_section(exclusion):
        me.add_movie(m)
    me.save_to_file("C:\\temp\\sitges.html")
