#  import pandas
from data.MovieScrapper import MovieScrapper
from data.MovieExport import MovieExport
from data.Settings import Settings

if __name__ == '__main__':
    # Load settings.json file with the app settings
    my = Settings(__file__)
    # Create a new MovieScrapper using the URL from settings
    scrap = MovieScrapper(my.settings["URL"], my.settings.get("Params"))
    # Check if the content of the page has changed
    if not my.check_hash(scrap.get_hash()):
        # Create a new MovieExport object
        me = MovieExport()
        # Loop all the movies from the MovieScrapper, excluding banned sections in the settings file
        for m in scrap.get_movies_by_section(my.banned_sections()):
            # Add each movie to the export html
            me.add_movie(m)
        # Save export html to the file from settings
        me.save_to_file(my.settings["ExportFile"])
        # Save new hash in setting.json
        my.save_settings()
    else:
        print("The content didn't change since the last export")
