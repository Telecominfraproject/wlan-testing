#!/usr/bin/env python3

import os
import pandas as pd
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="check_argparse.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description='''
      Check each file in py-scripts, or user defined '''
    )
    parser.add_argument("--path", default='.')
    parser.add_argument("--output", default='argparse_results')
    args = parser.parse_args()

    files = [f for f in os.listdir(args.path) if '.py' in f]
    results = dict()
    for file in files:
        text = open(os.path.join(args.path, file)).read()
        results_file = dict()
        results_file['argparse'] = 'argparse.' in text
        if results_file['argparse']:
            results_file['create_basic'] = 'create_basic_argparse' in text
            results_file['create_bare'] = 'create_bare_argparse' in text
            results_file['prog'] = 'prog=' in text
            results_file['formatter_class'] = 'formatter_class=' in text
            results_file['description'] = 'description=' in text
            results_file['epilog'] = 'epilog=' in text
            results_file['usage'] = 'usage=' in text
        results[file] = results_file
    df = pd.DataFrame(results.items())
    df.columns = ['File', 'results']
    df['argparse'] = [x['argparse'] for x in df['results']]
    for tag in ['create_basic',
                'create_bare',
                'prog',
                'formatter_class',
                'description',
                'epilog',
                'usage']:
        for result in df['results']:
            if tag in result:
                df[tag] = df['results'][tag]
    df['details'] = df['description'] + df['epilog'] + df['usage']
    df.to_csv(args.output + '.csv', index=False)


if __name__ == "__main__":
    main()
