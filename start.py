from data.MovieScrapper import MovieScrapper

if __name__ == '__main__':
    url = "http://www.sitgesfilmfestival.com/cat/programa/pel_licules"
    scrp = MovieScrapper(url)
    exclusion = "urts|Brigadoon|Espai|Serial|SGAE|Petit|ort"
    movies = scrp.get_movies_by_section(exclusion)

for m in movies:
    print("Movie: {} - {}".format(m.title, m.duration))
