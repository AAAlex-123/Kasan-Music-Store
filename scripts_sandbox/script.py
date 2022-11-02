
import argparse # TODO: use it
import glob
import re
import sys

from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

INCLUDE_TAG = "xinclude"
VALID_INCLUDE_PATHS = re.compile(".html$")

IMPORT_TAG = "ximport"
VALID_IMPORT_PATHS = re.compile(".csv$")

def arg_parse():
    """
    returns: a list of the files read from sys.argv, interpreted as glob
    """

    args = sys.argv

    files = []
    for glob_pattern in args[args.index("--") + 1:]:
        files.extend(glob.iglob(glob_pattern))

    return files


def get_soup(path):
    """
    returns: a BeautifulSoup object of the file at the specified path
    """

    with open(path) as f:
        html = f.read()

    return BeautifulSoup(html, "html.parser")

def write_soup(path, soup):
    """
    writes the soup to the path
    """

    with open(path + "_", 'w') as f:
        formatter = HTMLFormatter(indent=4)
        # print(index.prettify(formatter=formatter))
        f.write(soup.prettify(formatter=formatter))


def process(file):
    soup = get_soup(file)

    include_tags = soup.find_all(INCLUDE_TAG, path=VALID_INCLUDE_PATHS)

    for include_tag in include_tags:
        file_to_open = include_tag["path"]
        header = get_soup(file_to_open)
        include_tag.replace_with(header)

    # TODO: import tags
    import_tags = soup.find_all(IMPORT_TAG, path=VALID_IMPORT_PATHS)

    write_soup(file, soup)


def main():
    files = arg_parse()

    for file in files:
        process(file)


if __name__ == "__main__":
    main()

