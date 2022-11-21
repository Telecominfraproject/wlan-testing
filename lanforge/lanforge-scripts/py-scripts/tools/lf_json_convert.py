#!/usr/bin/env python3
'''
File: read in .json and convert for cookbook
Usage: lf_json_convert.py --file <file>
Example: lf_json_convert.py --file <file.json>
'''
# visit http://127.0.0.1:8050/ in your web browser.
import sys
import os
import importlib
import argparse

class file_convert():
    def __init__(self,
                _file = ''):
        self.file = _file
        self.file2 = "cookbook_{}".format(_file)

    # Helper methods
    def json_file(self):
        file_fd = open(self.file, 'r')
        file2_fd = open(self.file2, 'w+')
        file2_fd.write('{\n')
        file2_fd.write('"text": [ "<pre>**{}**\\n",'.format(self.file))
        for line in file_fd:
            line = line.replace('"','&quot;').replace('\n','')
            # to avoid --raw_line \"  issues the \" it creates a \& which the reader does not like
            line = line.replace('\&','\\\&')
            line = '"' + line + '\\n",'

            file2_fd.write('{}\n'.format(line))
        file2_fd.write('"</pre>"]\n')
        file2_fd.write('},')
        file_fd.close()
        file2_fd.close()

# Feature, Sum up the subtests passed/failed from the kpi files for each run, poke those into the database, and generate a kpi graph for them.
def main():

    parser = argparse.ArgumentParser(
        prog='lf_json_convert.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        lf_json_convert.py converts json for cookbook the output is <file>_edit
        NOTE: CANNOT have extra blank lines at the end of the json to display correctly.

            ''',
        description='''\
File: read in .json and convert for cookbook
Usage: lf_json_convert.py --file <file>
Example: lf_json_convert.py --file <file.json>

        ''')
    parser.add_argument('--file', help='--file file.json', required=True) #TODO is this needed

    args = parser.parse_args()

    __file = args.file

    convert = file_convert(_file = __file)
    convert.json_file()

if __name__ == '__main__':
    main()
    
