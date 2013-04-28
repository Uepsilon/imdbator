"""IMDBator

Usage:
    imdbator.py <folder> [-a]
    imdbator.py --version

Options:
    <movie_folder>  Folder to search for movies
    -a --auto       Does not ask which title should be used, takes first
    -h --help       Show this screen.
    --version       Show version.

"""
import os
import sys
from docopt import docopt
from imdb import IMDb

passed_args = {}


def collec_movies_from_folder(folder):
    movies = []

    movie_extensions = ('.mkv', '.avi')

    for file in os.listdir(folder):
        if file.endswith(movie_extensions):
            # Moviename as Index
            title = file.split('.')[0]
            extension = file.split('.')[1]
            movies.append({
                'filename': file,
                'title': title,
                'extension': extension
            })

    return movies


def rename_movies(folder, movies):
    imdbDB = IMDb('http')

    for movie in movies:
        search_result = imdbDB.search_movie(movie['title'])

        for result in search_result:
            new_filename = result['title'] + " ("+ str(result['year']) + ")." + movie['extension']

            if not passed_args['--auto']:
                print "Rename '" +  movie['title'] + "' to '" + new_filename + "'?"
                decision = raw_input("[y]es | [n]o | [s]kip: ")

                if decision.lower() == 'y':
                    os.rename(folder + "/" + movie['filename'], folder + "/" + new_filename)
                    break
                elif decision.lower() == 's':
                    # Skip Movie
                    print "Skipped\n"
                    break
            else:
                print "Renaming '" + movie['filename'] + "' to '" + new_filename + "'"
                os.rename(folder + "/" + movie['filename'], folder + "/" + new_filename)
                break


def main(args):
    global passed_args
    passed_args = args

    if not os.path.exists(passed_args['<folder>']):
        print "Given Folder is not valid"
        sys.exit(1)

    movie_folder = passed_args['<folder>']
    movies = collec_movies_from_folder(movie_folder)

    rename_movies(movie_folder, movies)

if __name__ == '__main__':
    args = docopt(__doc__, version='IMDBator: 0.1')
    main(args)
