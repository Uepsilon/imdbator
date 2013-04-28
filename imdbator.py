# -*- coding: utf-8 -*-

"""IMDBator

Usage:
    imdbator.py <folder> [-adft]
    imdbator.py --version

Options:
    <movie_folder>      Folder to search for movies
    -a --auto           Does not ask which title should be used, takes first
    -f --skip-files     Skips Files
    -d --skip-folders   Skips Folders
    -t --test           Does not rename, just Search and Prompt
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
            movies['folders'].append(dir_entry)
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
    print "Found " + str(len(movies)) + " Movies."

    i = 0
    for movie in movies:
        i += 1
        search_result = search_by_title(movie['title'])
        print "\nHandling Movie " + str(i) + "/" + str(len(movies))

        j = 0
        for result in search_result:
            j += 1
            print "Result " + str(j) + "/" + str(len(search_result))

            try:
                new_file_name = result['title'] + " ("+ str(result['year']) + ")." + movie['extension']
            except KeyError:
                print "Error caught in: " + str(result)
                raise

            if not passed_args['--auto']:
                print "Rename '" +  movie['filename'].decode('utf-8') + "' to '" + new_file_name + "'?"
                decision = raw_input("[y]es | [n]o | [s]kip: ")

                if decision.lower() == 'y':
                    if not passed_args['--test']:
                        os.rename(folder + "/" + movie['filename'], folder + "/" + new_file_name)
                    break
                elif decision.lower() == 's':
                    # Skip Movie
                    print "Skipped"
                    break
            else:
                print "Renaming '" + movie['filename'].decode('utf-8') + "' to '" + new_file_name + "'"
                if not passed_args['--test']:
                    os.rename(folder + "/" + movie['filename'], folder + "/" + new_file_name)
                break


def rename_folders(folders):
    print "Found " + str(len(folders)) + " Folders"

    i = 0
    for movie_folder in folders:
        i += 1

        print "\nHandling Folder " + str(i) + "/" + str(len(folders))

        search_result = search_by_title(movie_folder)

        j = 0
        for result in search_result:
            j += 1

            print "Result " + str(j) + "/" + str(len(search_result))

            try:
                new_folder_name = result['title'] + " (" + str(result['year']) + ")"
            except KeyError:
                print "Error caught in: " + str(result)
                raise

            if not passed_args['--auto']:
                print "Rename '" +  movie_folder.decode('utf-8') + "' to '" + new_folder_name + "'?"
                decision = raw_input("[y]es | [n]o | [s]kip: ")

                if decision.lower() == 'y':
                    if not passed_args['--test']:
                        os.rename(os.path.join(folder, movie_folder), os.path.join(folder, new_folder_name))
                    break
                elif decision.lower() == 's':
                    # Skip Movie
                    print "Skipped"
                    break
            else:
                print "Renaming '" + movie_folder.decode('utf-8') + "' to '" + new_folder_name + "'"
                if not passed_args['--test']:
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
