import json
import os
import pathlib
import string
import sys

base = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

def main():
    with open(base / 'index.html', 'r') as f:
        overview_template = string.Template(f.read())

    with open(base / 'overviews.json', 'r') as f:
        overview_config = json.load(f)[sys.argv[1]]

    print(overview_template.safe_substitute(**overview_config))

if __name__ == '__main__':
    main()