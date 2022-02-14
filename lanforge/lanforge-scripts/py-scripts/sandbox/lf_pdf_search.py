#!/usr/bin/python3

'''
NAME:
lf_pdf_search.py

PURPOSE:
lf_pdf_search.py will run a pdf grep looking for specific information in pdf files 
"pdfgrep -r --include 'ASA*.pdf' 'ASA End Date'" 

EXAMPLE:
lf_pdf_search.py

NOTES:
1. copy lf_pdf_search.py to a directory that has the pdf information

TO DO NOTES:


'''
import datetime
import pprint
import sys
if sys.version_info[0]  != 3:
    print("This script requires Python3")
    exit()


import os
import socket
import logging
import time
from time import sleep
import argparse
import json
import configparser
import subprocess
import csv
import shutil
import os.path
import xlsxwriter
import re
import pandas as pd


class lf_pdf_search():
     def __init__(self):

          self.renewal_info = ""
          self.timeout = 10
          self.outfile = "pdf_search"
          self.result = ""
          self.stdout_log_txt = ""
          self.stdout_log = ""
          self.stderr_log_txt = ""
          self.stderr_log = ""
          self.processed_log_txt = ""
          self.dataframe = ""
          self.pdf_search_csv = ""

     def get_data(self):

          # o.k. a little over kill here ,  just save data to file to help debug if something goes wrong
          if self.outfile is not None:
               self.stdout_log_txt = self.outfile
               self.stdout_log_txt = self.stdout_log_txt + "-{}-stdout.txt".format("test")
               self.stdout_log = open(self.stdout_log_txt, 'w+')
               self.stderr_log_txt = self.outfile
               self.stderr_log_txt = self.stderr_log_txt + "-{}-stderr.txt".format("test")                    
               #self.logger.info("stderr_log_txt: {}".format(stderr_log_txt))
               self.stderr_log = open(self.stderr_log_txt, 'w+')

               print("Names {} {}".format(self.stdout_log.name, self.stderr_log.name))

          # have ability to pass in a specific command
          command = "pdfgrep -r --include 'ASA*.pdf' 'ASA End Date'"
          print("running {}".format(command))

          process = subprocess.Popen(['pdfgrep','-r','--include','ASA*.pdf','ASA End Date'], shell=False, stdout=self.stdout_log, stderr=self.stderr_log, universal_newlines=True)
          try:
               process.wait(timeout=int(self.timeout))
               self.result = "SUCCESS"
          except subprocess.TimeoutExpired:
               process.terminate()
               self.result = "TIMEOUT"

          self.stdout_log.close()
          self.stderr_log.close()

          return self.stdout_log_txt

     def preprocess_data(self):
          pass

     # this method uses pandas dataframe - will use for data manipulation, 
     # the data mainupulation may be done in other manners
     def datafile_to_dataframe(self):
          # note the error_bad_lines=False will miss one of the lines 
          delimiter_list = [':']
          try:
               self.dataframe = pd.read_csv(self.stdout_log_txt, delimiter = [':'])
               #self.dataframe = pd.read_csv(self.stdout_log_txt, sep = ':')
          except:
               print("one of the files may have a SN: in it need to correct ")
               self.dataframe = pd.read_csv(self.stdout_log_txt, delimiter = ':', error_bad_lines=False)
          #print(self.dataframe)
          print("saving data to .csv")
          # this removes the extention of .txt
          self.pdf_search_csv= self.stdout_log_txt[:-4]
          self.pdf_search_csv = self.pdf_search_csv + ".csv"
          self.pdf_search_csv = self.dataframe.to_csv(self.pdf_search_csv,mode='w',index=False)


def main():
    # arguments
    parser = argparse.ArgumentParser(
        prog='lf_pdf_search.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            lf_pdf_search.py : for running scripts listed in lf_check_config.ini file
            ''',
        description='''\
lf_pdf_search.py
-----------

Summary :
---------
show renewas
            ''')

    parser.add_argument('--outfile', help="--outfile <Output Generic Name>  used as base name for all files generated", default="")
    parser.add_argument('--logfile', help="--logfile <logfile Name>  logging for output of lf_pdf_search script", default="lf_pdf_search.log")

    args = parser.parse_args()    

    pdf_search = lf_pdf_search()
    output_file = pdf_search.get_data()

    pdf_search.datafile_to_dataframe()

    print("output file: {}".format(str(output_file)))
    print("END lf_pdf_search.py")


if __name__ == "__main__":
     main()