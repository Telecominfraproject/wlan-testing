#!/usr/bin/python3

'''
NAME:
mux_client.py

PURPOSE:
a client, used to interact with the connected serial port server mux

EXAMPLE:
./mux_client.py --host "local_host" --port 23200

NOTES:

    mux_client.py copied from https://github.com/greearb/mux_serial

    Defaults:
        _default_host = 'localhost'
        _default_port = 23200

'''

import sys
if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit()

import socket
import argparse
import telnetlib

_default_host = 'localhost'
_default_port = 23200


class mux_client():
    def __init__(self, host=_default_host, port=_default_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.tn = None

    def interact(self):
        print(
            "MUX > Connected to {host}:{port}".format(
                host=self.host,
                port=self.port))
        print("MUX > Use ctrl+c to stop ..")

        self.tn = telnetlib.Telnet(self.host, self.port)
        try:
            self.tn.interact()

        except socket.error as e:
            print('\nMUX > Socket error: %s' % e.strerror, file=sys.stderr)

        except (KeyboardInterrupt, SystemExit):
            pass

        finally:
            self.close()

    def start_telnet(self):
        self.tn = telnetlib.Telnet(self.host, self.port)

    def write_str(self, cmd):
        cmd = cmd.encode('utf-8')
        self.tn.write(cmd)

    def read_lazy(self):
        return self.tn.read_lazy()

    def read_until(self, prompt):
        byte_prompt = prompt.encode('utf_8')
        info = self.tn.read_until(byte_prompt, timeout=5)
        return info

    def close_silent(self):
        self.sock.close()

    def close(self):
        print('\nMUX > Closing...', file=sys.stderr)
        self.sock.close()
        print('MUX > Done! =)', file=sys.stderr)


def main():

    parser = argparse.ArgumentParser(
        prog='mux_client.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        mux_client.py:
            ''',

        description='''\
NAME:
mux_client.py

PURPOSE:
a client, used to interact with the connected serial port server mux

EXAMPLE:
./mux_client.py --host "local_host" --port 23200

NOTES:
    Defaults:
        _default_host = 'localhost'
        _default_port = 23200

        ''')
    parser.add_argument('--host', help='Host', default=_default_host)

    parser.add_argument('--port',help='Host port', type=int, default=_default_port)

    args = parser.parse_args()

    client = mux_client(host=str(args.host), port=int(args.port))
    client.interact()

    if not sys.flags.interactive:
        client.close()


if __name__ == '__main__':
    main()
