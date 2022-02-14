#!/usr/bin/env python3
"""
    NAME:       lf_sniff_radio.py
    PURPOSE:    THis script will sniff a Radio after changing the Radio settings.

                Radio settings: channel radio mode  AUTO, 802.11a, 802.11b, etc... refer
                                        py-json/LANforge/set_wifi_radio.py for different modes

    EXAMPLE:    python3 lf_sniff_radio.py
                        --mgr localhost
                        --mgr_port 8080
                        --outfile /home/lanforge/test_sniff.pcap
                        --duration 20
                        --channel 52
                        --radio_mode AUTO

"""
import sys
import os
import importlib
import argparse
import time

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class SniffRadio(Realm):
    def __init__(self,
                 lfclient_host="localhost",
                 lfclient_port=8080,
                 radio="wiphy0",
                 outfile="/home/lanforge/test_pcap.pcap",
                 duration=60,
                 channel=52,
                 radio_mode="AUTO",
                 debug_on_=False):
        super().__init__(lfclient_host, lfclient_port)
        self.lfclient_host = lfclient_host
        self.lfclient_port = lfclient_port
        self.debug = debug_on_
        self.local_realm = realm.Realm(lfclient_host=self.lfclient_host,
                                       lfclient_port=self.lfclient_port,
                                       debug_=self.debug)
        self.monitor = self.local_realm.new_wifi_monitor_profile()
        if channel != "AUTO":
            channel = int(channel)
        self.channel = channel
        self.duration = duration
        self.outfile = outfile
        self.mode = radio_mode
        self.radio = radio

    def setup(self, ht40_value, ht80_value, ht160_value):
        # TODO: Store original channel settings so that radio can be set back to original values.
        self.monitor.set_flag(param_name="disable_ht40", value=ht40_value)
        self.monitor.set_flag(param_name="disable_ht80", value=ht80_value)
        self.monitor.set_flag(param_name="ht160_enable", value=ht160_value)
        self.monitor.create(radio_=self.radio, channel=self.channel, mode=self.mode, name_="moni3a")

    def start(self):
        self.monitor.admin_up()
        # TODO:  Use LFUtils.wait_until_ports_admin_up instead of sleep, check return code.
        time.sleep(5)
        self.monitor.start_sniff(capname=self.outfile, duration_sec=self.duration)
        for i in range(0, self.duration):
            print("started sniffer, PLease wait,", self.duration - i)
            time.sleep(1)
        print("Sniffing Completed Success", "Check ", self.outfile)
        self.monitor.admin_down()
        time.sleep(2)

    def cleanup(self):
        # TODO:  Add error checking to make sure monitor port really went away.
        # TODO:  Set radio back to original channel
        self.monitor.cleanup()


def main():
    parser = argparse.ArgumentParser(
        prog="lf_sniff_radio.py",
        formatter_class=argparse.RawTextHelpFormatter,
        usage=
        """./lf_sniff_radio.py 
        --mgr localhost
        --mgr_port 8080 
        --radio wiphy0  
        --outfile /home/lanforge/test_sniff.pcap
        --duration 1
        --channel 52
        --radio_mode AUTO
        """)

    parser.add_argument('--mgr', type=str, help='--mgr: IP Address of LANforge', default="localhost")
    parser.add_argument('--mgr_port', type=int, help='--mgr_port: HTTP Port of LANforge', default=8080)
    parser.add_argument('--radio', type=str, help='--radio: Radio to sniff', default="wiphy0")
    parser.add_argument('--outfile', type=str, help='--outfile: give the filename with path',
                        default="/home/lanforge/test_pcap.pcap")
    parser.add_argument('--duration', type=int, help='--duration duration in sec, for which you want to capture',
                        default=60)
    parser.add_argument('--channel', type=str, help='--channel Set channel pn selected Radio, [52, 56 ...]',
                        default=0)
    parser.add_argument('--radio_mode', type=str, help='--radio_mode select the radio mode [AUTO, 802.11a, 802.11b, '
                                                       '802.11ab ...]', default="AUTO")
    parser.add_argument('--disable_ht40', type=str, help='Enable/Disable \"disable_ht40\" [0-disable,1-enable]', default=0)
    parser.add_argument('--disable_ht80', type=str, help='Enable/Disable \"disable_ht80\" [0-disable,1-enable]', default=0)
    parser.add_argument('--ht160_enable', type=str, help='Enable/Disable \"ht160_enable\ [0-disable,1-enable]" ', default=0)

    args = parser.parse_args()

    obj = SniffRadio(lfclient_host=args.mgr,
                     lfclient_port=args.mgr_port,
                     outfile=args.outfile,
                     duration=args.duration,
                     channel=args.channel,
                     radio=args.radio,
                     radio_mode=args.radio_mode
                     )
    obj.setup(int(args.disable_ht40), int(args.disable_ht80), int(args.ht160_enable))
    # TODO: Add wait-for logic instead of a sleep
    time.sleep(5)
    obj.start()
    obj.cleanup()

    # TODO:  Check if passed or not.

if __name__ == '__main__':
    main()
