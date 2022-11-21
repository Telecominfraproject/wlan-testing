#!/usr/bin/env python3
import argparse


class LogFilter:
    @staticmethod
    def log_filter(input_file=None, timestamp=None, output_file=None):
        file = open(input_file).read()
        file_lines = file.split('\n')
        output_file = open(output_file, 'w')
        for line in file_lines:
            if line[0:13].isdigit():
                key = int(line[0:13])
                if key > timestamp:
                    output_file.write(line + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', help='Name of Log file to be parsed', required=True)
    parser.add_argument('--timestamp', help='timestamp to filter log from', required=True)
    parser.add_argument('--output_file', help='File path to save output to', required=True)
    args = parser.parse_args()

    LogFilter.log_filter(input_file=args.input_file, timestamp=args.timestamp, output_file=args.output_file)


if __name__ == "__main__":
    main()
