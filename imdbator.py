# -*- coding: utf-8 -*-

"""IMDBator

Usage:
    imdbator.py <folder> [-adf]
    imdbator.py --version

Options:
    <movie_folder>      Folder to search for movies
    -a --auto           Does not ask which title should be used, takes first
    -f --skip-files     Skips Files
    -d --skip-folders   Skips Folders
    -h --help           Show this screen.
    --version           Show version.

"""

import os
import sys
from docopt import docopt
from imdb import IMDb

passed_args = {}
folder = ""


def collec_movies_from_folder():
    movies = {'folders': [], 'files': []}

    movie_extensions = ('.mkv', '.avi')

    for dir_entry in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, dir_entry)):
            movies['folders'].append(dir_entry.decode('utf-8'))
            # Directory
        elif dir_entry.endswith(movie_extensions):
            # File
            title = dir_entry.split('.')[0].decode('utf-8')
            extension = dir_entry.split('.')[1]
            movies['files'].append({
                'filename': dir_entry,
                'title': title,
                'extension': extension
            })

    return movies


def search_by_title(title):
    imdbDB = IMDb('http')
    return imdbDB.search_movie(title)


def rename_files(movies):
    for movie in movies:
        search_result = search_by_title(movie['title'])

        for result in search_result:
            new_file_name = result['title'] + " ("+ str(result['year']) + ")." + movie['extension']

            if not passed_args['--auto']:
                print "Rename '" +  movie['title'] + "' to '" + new_file_name + "'?"
                decision = raw_input("[y]es | [n]o | [s]kip: ")

                if decision.lower() == 'y':
                    os.rename(folder + "/" + movie['filename'], folder + "/" + new_file_name)
                    break
                elif decision.lower() == 's':
                    # Skip Movie
                    print "Skipped\n"
                    break
            else:
                print "Renaming '" + movie['filename'] + "' to '" + new_file_name + "'"
                os.rename(folder + "/" + movie['filename'], folder + "/" + new_file_name)
                break


def rename_folders(folders):
    for movie_folder in folders:
        search_result = search_by_title(movie_folder)

        for result in search_result:
            new_folder_name = result['title'] + " (" + str(result['year']) + ")"

            if not passed_args['--auto']:
                print "Rename '" +  movie_folder + "' to '" + new_folder_name + "'?"
                decision = raw_input("[y]es | [n]o | [s]kip: ")

                if decision.lower() == 'y':
                    os.rename(os.path.join(folder, movie_folder), os.path.join(folder, new_folder_name))
                    break
                elif decision.lower() == 's':
                    # Skip Movie
                    print "Skipped\n"
                    break
            else:
                print "Renaming '" + movie_folder + "' to '" + new_folder_name + "'"
                os.rename(os.path.join(folder, movie_folder), os.path.join(folder, new_folder_name))
                break


def main(args):
    global passed_args, folder
    passed_args = args
    folder = args['<folder>']

    if not os.path.exists(folder):
        print "Given Folder is not valid"
        sys.exit(1)

    movies = collec_movies_from_folder()

    if not passed_args['--skip-files']:
        rename_files(movies['files'])

    if not passed_args['--skip-folders']:
        rename_folders(movies['folders'])

if __name__ == '__main__':
    args = docopt(__doc__, version='IMDBator: 0.1')
    main(args)
