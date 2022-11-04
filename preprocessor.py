
import argparse
import glob
import os
import pathlib
import re
import sys

from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

__version__ = "1.0"


INCLUDE_TAG = "xinclude"
VALID_INCLUDE_PATHS = re.compile(".html$")

IMPORT_TAG = "ximport"
VALID_IMPORT_PATHS = re.compile(".csv$")


def get_soup(path):
    with open(path) as f:
        html = f.read()

    return BeautifulSoup(html, "html.parser")


def write_soup(soup, path):
    formatter = HTMLFormatter(indent=4)
    html = soup.prettify(formatter=formatter)

    with open(path, 'w') as f:
        f.write(html)


def process_soup(soup, root):
    include_tags = soup.find_all(INCLUDE_TAG, path=VALID_INCLUDE_PATHS)

    for include_tag in include_tags:
        file_to_open = pathlib.Path(os.path.join(root, include_tag["path"])).resolve().__str__()
        html = get_soup(file_to_open)
        include_tag.replace_with(html)

    # TODO: import tags
    import_tags = soup.find_all(IMPORT_TAG, path=VALID_IMPORT_PATHS)

    return soup


def process_file(path, root, out):
    if (not os.path.isfile(path)):
        return

    soup = get_soup(path)

    processed_soup = process_soup(soup, root)

    outfile = os.path.join(out, os.path.basename(path))

    write_soup(processed_soup, outfile)



def parse_args():
    parser = argparse.ArgumentParser(description="Processes some html files", allow_abbrev=False, fromfile_prefix_chars='@')

    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-r", "--root", dest="root", action="store", default='.',\
            help="the root of the relative links of the xinclude tags")
    parser.add_argument("-d", "--dest", dest="out", action="store", default='.',\
            help="where to place processed files")
    parser.add_argument("files", nargs='*',\
            help="files to process")

    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.exists(args.out):
        os.mkdir(args.out)

    files_to_process = []
    for glob_pattern in args.files:
        files_to_process.extend(glob.iglob(glob_pattern))

    for file in files_to_process:
        process_file(os.path.abspath(file), os.path.abspath(args.root), args.out)


if __name__ == "__main__":
    main()

