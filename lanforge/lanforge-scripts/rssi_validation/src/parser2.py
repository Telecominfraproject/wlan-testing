import json
import fnmatch
import os
import glob
import csv
import argparse
import re
import sys

parser = argparse.ArgumentParser(description='Test specification.')
parser.add_argument('--test_dir', metavar='i', type=str, help='../json')
parser.add_argument('--csv', metavar='o', type=str, help='../output.csv')
parser.add_argument('--bandwidth', metavar='b', type=int, help='20, 40, 80')
parser.add_argument('--channel', metavar='c', type=int, help='6, 36')
parser.add_argument('--antenna', metavar='a', type=int, help='0, 1, 4, 7, 8')
args = parser.parse_args()

BANDWIDTH_OPTIONS = [args.bandwidth]
CHANNEL_OPTIONS = [args.channel]
ANTENNA_OPTIONS = [args.antenna]
ATTENUATION_OPTIONS = range(200, 960, 10)
TEST_DIR = args.test_dir
OUTPUT_CSV = args.csv

def read_from_file(filename):
    filename = open(filename, "r")
    buf = filename.read()
    filename.close
    return buf

def write_to_csv(data, file):
    with open(file, "w") as file:
        writer = csv.writer(file)
        writer.writerows(data)

def replacetext(filename, search_text,replace_text):
    with open(filename,'r+') as f:
        file = f.read()         
        file = re.sub(search_text, replace_text, file) 
        f.seek(0)          
        f.write(file) 
        f.truncate()

def parse_json(buf, field):
    test = json.loads(buf)
    iface = test[field]
    return iface

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def get_station(test_dir, sta_index):
    filenames = find('sta*.json', test_dir)
    for filename in filenames:
        buf = read_from_file(filename)
        return json.loads(buf)['interfaces'][sta_index][F'1.2.sta000{sta_index}']

def get_atten(test_dir):
    filenames = find('att*.json', test_dir)
    if (len(filenames)):
        buf = read_from_file(filenames[0])
        return json.loads(buf)['attenuator']

def dict_head(dic):
    return [key for key in dic]

def dict_data(dic):
    return [dic[key] for key in dic]

def test_head(test_dir):
    att_head = ['atten mod 1','atten mod 2','atten mod 3','atten mod 4','atten name']
    man_head = ['station', 'radio']
    sta_head = dict_head(get_station(test_dir, 0))
    return [att_head + man_head + sta_head]

def test_data(test_dir):
    att_data = dict_data(get_atten(test_dir))
    man_data = [['sta0000', 'AC2-2G' ],
                ['sta0001', 'AC2-5G' ],
                ['sta0002', 'AX210'  ],
                ['sta0003', 'N'      ],
                ['sta0004', 'MT7921K'],
                ['sta0005', 'AC3x3'  ],
                ['sta0006', 'MT7915' ]]
    sta_data = [dict_data(get_station(test_dir, n)) for n in range(0,7)]
    return [att_data + man_data[n] + sta_data[n] for n in range(0,7)]

def build_table(test_dir):
    buf = test_head(F'{test_dir}/Bandwidth{BANDWIDTH_OPTIONS[0]}/'
                    + F'Channel{CHANNEL_OPTIONS[0]}/'
                    + F'Antenna{ANTENNA_OPTIONS[0]}/'
                    + F'Attenuation{ATTENUATION_OPTIONS[0]}')
    for bandwidth in BANDWIDTH_OPTIONS:
        for channel in CHANNEL_OPTIONS:
            for antenna in ANTENNA_OPTIONS:
                for attenuation in ATTENUATION_OPTIONS:
                    buf += test_data(F'{test_dir}/Bandwidth{bandwidth}/'
                                     + F'Channel{channel}/'
                                     + F'Antenna{antenna}/'
                                     + F'Attenuation{attenuation}')
    return buf

write_to_csv(build_table(TEST_DIR), OUTPUT_CSV)
replacetext(OUTPUT_CSV, " dBm","")
replacetext(OUTPUT_CSV, "sta000","")
sys.exit(0)
