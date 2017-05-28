#!/usr/bin/env python3
# BACKUP THUNDERBIRD FILTERS

from time import gmtime, strftime
import tarfile
import os

# get current date
current_date = strftime("%Y-%m-%d", gmtime())

# find files and store in array
def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

# create archive
#tar = tarfile.open(current_date + ".tar.gz", "w:gz")
#for name in ["file1", "file2", "file3"]:
#    tar.add(name)
#tar.close()

def main():
    filename = 'msgFilterRules.dat'
    path = os.getenv("HOME") + '/.thunderbird'

    filters = find_all(filename, path)

    # create archive from filters found
    tar = tarfile.open(current_date + ".tar.gz", "w:gz")
    for name in filters:
      tar.add(name)
    tar.close()


if __name__ == '__main__':
    main()
