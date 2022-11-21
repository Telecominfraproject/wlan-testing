#!/usr/bin/env python3

""" Script for mapping module names to their docstrings, will print output in json format. Will look for all python
    files in the current directory and map filename:docstring
"""

import ast
import os


class DocstringCollector:
    def __init__(self):
        self.docstring_map = {}
        self.cur_path = os.getcwd()
        self.files = []

    def get_python_files(self):
        for file in os.listdir(self.cur_path):
            if file.endswith('.py'):
                self.files.append(file)

    def map_docstrings(self):
        if len(self.files) > 0:
            for file in self.files:
                try:
                    with open(file, 'r') as f:
                        tree = ast.parse(f.read())
                    docstring = ast.get_docstring(tree)
                    if docstring is not None:
                        self.docstring_map[file] = docstring
                except Exception as e:
                    continue
                    # print("Exception %s on %s" % (e, file))
        else:
            raise ValueError("No python files found in directory")


def main():
    collector = DocstringCollector()
    collector.get_python_files()
    collector.map_docstrings()
    # print(collector.docstring_map.keys())
    print(collector.docstring_map)


if __name__ == "__main__":
    main()