# IMDBator

Renames Movies in a folder. Searchs for Titles at IMDB.

## Features

Crawls a directory and collects all movies (mkv, mp4, flv, avi) and folders. 
Then uses their names to search imdb for the most fitting entry and uses it to 
rename the File / Folder using the format "{title} ({year})". 

## Usage

Just download this, satisfy the Dependencies then run from the git-folder:

    python imbator.py /your/movie/folder [-adft]

## Options

* -a      Automatic (Skipps Files / Folders which names already match top Searchresult)
* -c      Uses the Canonical Title (Lion King, The (1994)) instead of normal Title (The Lion King (1994)) 
* -d      No Folders
* -f      No Files
* -t      Testrun (Just shows what it would do without renaming)


## Dependencies

[Docops](https://github.com/docopt/docopt)  
[IMDbPY](http://imdbpy.sourceforge.net/) (Caution: Must be [latest development Version](http://imdbpy.sourceforge.net/development.html))