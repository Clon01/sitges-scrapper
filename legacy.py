from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
import pandas
import codecs
from hashlib import md5


class Movie():
    title = None
    director = None
    section = None
    duration = None
    synopse = None

    def __dict__(self):
        return {"title": self.title, "director": self.director, "section": self.section, "duration": self.duration,
                "synopse": self.synopse}


def URL2BS(url):
    f = urlopen(url)
    page_raw = f.read()
    f.close()

    return BS(page_raw, "html.parser")


def isSectionBanned(df, banned):
    filter = df['section'].str.contains(banned) == False

    return filter


movielist = []

banned = "urts|Brigadoon|Espai|Serial|SGAE|Petit|ort"

sitges = "http://www.sitgesfilmfestival.com/cat/programa/pel_licules"

html = URL2BS(sitges)

rows = html.findAll("div", {"class": "right-banner-bottom"})

for row in rows:

    movie = Movie()
    movie.title = row.h3.a.text
    movie.director = row.h6.text
    movie.section = row.p.text

    link = row.h3.a
    link = link.get('href')
    sub_html = URL2BS(link)

    try:
        movie.synopse = sub_html.find("div", {"class": "section_sinopsi"}).p.text
    except:
        None
    try:
        movie.duration = sub_html.find("div", {"class": "section_fitxa_artistica"}).p.strong.text
    except:
        None

    d = movie.__dict__()
    movielist.append(d)

df = pandas.DataFrame(movielist)
df.sort_values(by=["title"], inplace=True)

# print(df['section'].value_counts())

print(df[isSectionBanned(df, banned)].to_html(columns=["title", "director", "section", "synopse", "duration"]))

