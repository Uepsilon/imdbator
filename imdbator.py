# -*- coding: utf-8 -*-

"""IMDBator

Usage:
    imdbator.py <folder> [-acdft]
    imdbator.py --version

Options:
    <movie_folder>      Folder to search for movies
    -a --auto           Does not ask which title should be used, takes first
    -f --skip-files     Skips Files
    -d --skip-folders   Skips Folders
    -t --test           Does not rename, just Search and Prompt
    -c --canonical      Uses the Canonical Title (Lion King, The (1994))
    -h --help           Show this screen.
    --version           Show version.

"""

import os
import sys
import re
from docopt import docopt
from imdb import IMDb

passed_args = {}
folder = ""


def collec_movies_from_folder():
    movies = {'folders': [], 'files': []}

    movie_extensions = ('.mkv', '.avi', 'mp4', 'flv', 'mpg')

    for dir_entry in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, dir_entry)):
            # Directory
            movies['folders'].append(dir_entry)
        elif dir_entry.endswith(movie_extensions):
            # File
            title, extension = dir_entry.rsplit('.', 1)
            movies['files'].append({
                'filename': dir_entry,
                'title': title,
                'extension': extension
            })

    return movies


def search_imdb_by_title(title):
    imdbDB = IMDb('http')
    return imdbDB.search_movie(title)


def get_title_from_result(result):
    title = None

    # If Result is not a movie, skip it
    if result['kind'] == 'movie':
        # replace / in moviename
        if passed_args['--canonical']:
            title = re.sub('\/', '-', result['long imdb canonical title'].encode('utf-8'))
            title = title.replace(' (I)', '')  # Fix for Strange IMDB-Titles
        else:
            title = re.sub('\/', '-', result['title'].encode('utf-8'))
            title = title.replace(' (I)', '')  # Fix for Strange IMDB-Titles

            try:
                title = "{} ({})".format(
                    title,
                    result['year'])
            except KeyError:
                # print "Error caught in: {}".format(result)
                title = "{}".format(title)

    return title


def get_new_title(title, current_title):
    imdb_resultsb = search_imdb_by_title(title)
    titles = []  # List of all Titles found by IMDBPy

    # Check if first hit matches current title
    if passed_args['--auto'] and current_title is not None and get_title_from_result(imdb_resultsb[0]) == current_title:
        print "'{}' matches best Hit\n".format(current_title)
        return None

    while True:
        for result in imdb_resultsb:
            title = get_title_from_result(result)
            # Handling of skipped Results
            if title is not None:
                titles.append(title)

        for i, title in enumerate(titles, 1):
            print "{}: {}".format(i, title)

        if len(titles) > 0:
            selected_result = raw_input(
                "Select Name from List (1 - {}), try a [n]ew Searchterm or [s]kip this file: ".format(
                len(titles)))
        else:
            selected_result = raw_input(
                "Nothing found. Try a [n]ew Searchterm or [s]kip this file: ")

        if selected_result.lower() == 'n':
            new_search_term = raw_input("Title: ")
            return get_new_title(new_search_term, None)
        elif selected_result.lower() == 's':
            print "Skipped"
            return None
        elif selected_result.isdigit() and int(selected_result) <= len(titles):
            return titles[int(selected_result) - 1]
        else:
            print "Unknown Selection: '{}'. Please try again.\n".format(selected_result)


def rename_files(movies):
    print "Found {} Movies.".format(len(movies))

    for i, movie in enumerate(movies, 1):
        print "\nMovie {}/{}: {}".format(i, len(movies), movie['title'])
        new_title = get_new_title(movie['title'], movie['title'])

        if new_title is not None:
            new_file_name = new_title + "." + movie['extension']

            print "Renaming '{}' to '{}'".format(
                movie['filename'],
                new_file_name)

            if not passed_args['--test']:
                os.rename(os.path.join(folder, movie['filename']),
                          os.path.join(folder, new_file_name))
    print "\n"


def rename_folders(folders):
    print "Found {} Folders.".format(len(folders))

    for i, movie_folder in enumerate(folders, 1):
        print "\nFolder {}/{}: {}".format(i, len(folders), movie_folder)
        new_title = get_new_title(movie_folder, movie_folder)

        if new_title is not None:
            new_folder_name = new_title

            print "Renaming '{}' to '{}'".format(
                movie_folder,
                new_folder_name)

            if not passed_args['--test']:
                os.rename(os.path.join(folder, movie_folder),
                          os.path.join(folder, new_folder_name))
    print "\n"


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
