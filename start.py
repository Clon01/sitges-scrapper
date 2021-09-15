#  import pandas
from data.MovieScrapper import MovieScrapper
from data.MovieExport import ExportFactory, Formats
from data.Settings import Settings

if __name__ == '__main__':
    # Load settings.json file with the app settings
    my = Settings(__file__)
    # Create a new MovieScrapper using the URL from settings
    scrap = MovieScrapper(my.settings["URL"], my.settings.get("Params"))
    # Check if the content of the page has changed
    if not my.check_hash(scrap.get_hash()):
        # Create a new ExportFactory object
        ef = ExportFactory()
        # Add each export format to the factory
        for export in my.settings["Exports"]:
            ef.add_output(Formats[export["Format"]], export["Filename"])
        # Loop all the movies from the MovieScrapper, excluding banned sections in the settings file
        for m in scrap.get_movies_by_section(my.banned_sections()):
            # Add each movie to the export html
            ef.add_movie(m)
        # Save export to all the export configs in the factory
        ef.save_to_file()
        # Print movie total
        print("Total movie count: {}".format(ef.count()))
        # Save new hash in setting.json
        my.save_settings()
    else:
        print("The content didn't change since the last export")
