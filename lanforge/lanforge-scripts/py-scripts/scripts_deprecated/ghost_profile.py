#!/usr/bin/env python3
"""
NAME: ghost_profile.py
PURPOSE: modify ghost database from the command line.
SETUP: A Ghost installation which the user has admin access to.
EXAMPLE: ./ghost_profile.py --article_text_file text.txt --title Test --authors Matthew --ghost_token SECRET_KEY --host 192.168.1.1

There is a specific class for uploading kpi graphs called kpi_to_ghost.

EXAMPLE: ./ghost_profile.py --ghost_token TOKEN --ghost_host 192.168.100.147
--folders /home/lanforge/html-reports/wifi-capacity-2021-06-04-02-51-07
--kpi_to_ghost appl --authors Matthew --title 'wifi capacity 2021 06 04 02 51 07' --server 192.168.93.51
--user_pull lanforge --password_pull lanforge --customer candela --testbed heather --test_run test-run-6
--user_push matt --password_push PASSWORD

EXAMPLE 2: ./ghost_profile.py --ghost_token TOKEN
--ghost_host 192.168.100.147 --server 192.168.93.51 --customer candela
--testbed heather --user_push matt --password_push "amount%coverage;Online" --kpi_to_ghost app
--folders /home/lanforge/html-reports/wifi-capacity-2021-06-14-10-42-29 --grafana_token TOKEN
--grafana_host 192.168.100.201

this script uses pyjwt. If you get the issue module 'jwt' has no attribute 'encode', run this: pip3 uninstall jwt pyjwt && pip install pyjwt
 Matthew Stidham
 Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.
"""
import sys
import os
import importlib
import argparse

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

# from GhostRequest import GhostRequest
GhostRequest = importlib.import_module("py-dashboard.GhostRequest")


class UseGhost(GhostRequest):
    def __init__(self,
                 _ghost_token=None,
                 host="localhost",
                 port=8080,
                 _debug_on=False,
                 _exit_on_fail=False,
                 _ghost_host="localhost",
                 _ghost_port=2368,
                 influx_host=None,
                 influx_port=None,
                 influx_org=None,
                 influx_token=None,
                 influx_bucket=None):
        super().__init__(_ghost_host,
                         str(_ghost_port),
                         _api_token=_ghost_token,
                         influx_host=influx_host,
                         influx_port=influx_port,
                         influx_org=influx_org,
                         influx_token=influx_token,
                         influx_bucket=influx_bucket,
                         debug_=_debug_on)
        self.ghost_host = _ghost_host
        self.ghost_port = _ghost_port
        self.ghost_token = _ghost_token
        self.influx_host = influx_host
        self.influx_port = influx_port
        self.influx_org = influx_org
        self.influx_token = influx_token
        self.influx_bucket = influx_bucket

    def create_post_from_file(self, title, file, tags, authors):
        text = open(file).read()
        return self.create_post(title=title, text=text, tags=tags, authors=authors)

    def kpi(self,
            authors,
            folders,
            parent_folder,
            title,
            server_pull,
            ghost_host,
            port,
            user_push,
            password_push,
            customer,
            testbed,
            test_run,
            grafana_token,
            grafana_host,
            grafana_port,
            datasource,
            grafana_bucket):
        target_folders = list()
        return self.kpi_to_ghost(authors,
                                 folders,
                                 parent_folder,
                                 title,
                                 server_pull,
                                 ghost_host,
                                 port,
                                 user_push,
                                 password_push,
                                 customer,
                                 testbed,
                                 test_run,
                                 target_folders,
                                 grafana_token,
                                 grafana_host,
                                 grafana_port,
                                 datasource,
                                 grafana_bucket)


def main():
    parser = argparse.ArgumentParser(
        prog='ghost_profile.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Manage Ghost Website''',
        description='''
        ghost_profile.py
        ----------------
        Command example:
        ./ghost_profile.py
            --ghost_token'''
    )
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--ghost_token', default=None)
    optional.add_argument('--create_post', default=None)
    optional.add_argument('--article_text_file', default=None)

    optional.add_argument('--ghost_port', help='Ghost port if different from 2368', default=2368)
    optional.add_argument('--ghost_host', help='Ghost host if different from localhost', default='localhost')
    optional.add_argument('--article_text')
    optional.add_argument('--article_tags', action='append')
    optional.add_argument('--authors', action='append')
    optional.add_argument('--title', default=None)
    optional.add_argument('--image', default=None)
    optional.add_argument('--folder', default=None)
    optional.add_argument('--custom_post', default=None)
    optional.add_argument('--kpi_to_ghost', help='Generate a Ghost report from KPI spreadsheets', action="store_true")
    optional.add_argument('--folders', action='append', default=None)
    optional.add_argument('--server_pull')
    optional.add_argument('--port', default=22)
    optional.add_argument('--user_push')
    optional.add_argument('--password_push')
    optional.add_argument('--customer')
    optional.add_argument('--testbed')
    optional.add_argument('--test_run', default=None)
    optional.add_argument('--grafana_token', default=None)
    optional.add_argument('--grafana_host', default=None)
    optional.add_argument('--grafana_port', default=3000)
    optional.add_argument('--parent_folder', default=None)
    optional.add_argument('--datasource', default='InfluxDB')
    optional.add_argument('--grafana_bucket', default=None)
    optional.add_argument('--influx_host')
    optional.add_argument('--influx_token', help='Username for your Influx database')
    optional.add_argument('--influx_bucket', help='Password for your Influx database')
    optional.add_argument('--influx_org', help='Name of your Influx database')
    optional.add_argument('--influx_port', help='Port where your influx database is located', default=8086)
    optional.add_argument('--influx_tag', action='append', nargs=2,
                          help='--influx_tag <key> <val>   Can add more than one of these.')
    optional.add_argument('--influx_mgr',
                          help='IP address of the server your Influx database is hosted if different from your LANforge Manager',
                          default=None)
    optional.add_argument('--debug', help='Enable debugging', default=False, action="store_true")
    args = parser.parse_args()

    Ghost = UseGhost(_ghost_token=args.ghost_token,
                     _ghost_port=args.ghost_port,
                     _ghost_host=args.ghost_host,
                     influx_host=args.influx_host,
                     influx_port=args.influx_port,
                     influx_org=args.influx_org,
                     influx_token=args.influx_token,
                     influx_bucket=args.influx_bucket,
                     _debug_on=args.debug)

    if args.create_post is not None:
        Ghost.create_post(args.title, args.article_text, args.article_tags, args.authors)
    if args.article_text_file is not None:
        Ghost.create_post_from_file(args.title, args.article_text_file, args.article_tags, args.authors)

    if args.image is not None:
        Ghost.upload_image(args.image)

    if args.custom_post is not None:
        if args.folders is not None:
            Ghost.custom_post(args.folders, args.authors)
        else:
            Ghost.custom_post(args.folder, args.authors)
    else:
        if args.folder is not None:
            Ghost.upload_images(args.folder)

    if args.kpi_to_ghost:
        Ghost.kpi(args.authors,
                  args.folders,
                  args.parent_folder,
                  args.title,
                  args.server_pull,
                  args.ghost_host,
                  args.port,
                  args.user_push,
                  args.password_push,
                  args.customer,
                  args.testbed,
                  args.test_run,
                  args.grafana_token,
                  args.grafana_host,
                  args.grafana_port,
                  args.datasource,
                  args.grafana_bucket)


if __name__ == "__main__":
    main()
