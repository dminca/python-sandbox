#!/usr/bin/env python3
# BACKUP THUNDERBIRD FILTERS

from time import gmtime, strftime
import tarfile
import os

# get current date
current_date = strftime("%Y-%m-%d", gmtime())

def find_all(name, path):
    """Return list of paths

    Traverse directory until reaches the file that's being searched,
    after file is found, return the full path to file in a list.
    """
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

def main():
    """Create archive from Thunderbird filters

    After searching for the filename and returning its fullpath in a list,
    loop through the list and generate .tar.gz archive from fullpath.

    The archive name follows UNIX time pattern: YYYY-m-d.tar.gz
    """
    filename = 'msgFilterRules.dat'
    path = os.getenv("HOME") + '/.thunderbird'
    output = os.getenv("HOME") + '/Dropbox/Apps/PersonalThunderbirdFiltersBackup/'

    filters = find_all(filename, path)

    # create archive from filters found
    tar = tarfile.open(output + current_date + ".tar.gz", "w:gz")
    for name in filters:
      tar.add(name)
    tar.close()


if __name__ == '__main__':
    main()
