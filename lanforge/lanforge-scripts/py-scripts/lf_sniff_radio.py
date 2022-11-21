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
                        --monitor_name moni0a

    NOTES:

    The configuration of the monitor is: sudo iw dev <monitor> info
    Sample:

    [lanforge@ct523c-3b7b ~]$ sudo iw dev SNIFF_5G_40 info
    Interface SNIFF_5G_40
    ifindex 2413
    wdev 0x900000002
    addr 04:f0:21:85:62:22
    type monitor
    wiphy 9
    channel 36 (5180 MHz), width: 20 MHz (no HT), center1: 5180 MHz
    txpower 0.00 dBm
    [lanforge@ct523c-3b7b ~]$


"""
import sys
import os
import importlib
import argparse
import time
import paramiko


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
                 channel=None,
                 # channel_freq=None,
                 channel_bw=None,
                 center_freq=None,
                 radio_mode="AUTO",
                 debug_on_=True,
                 monitor_name=None,):
        super().__init__(lfclient_host, lfclient_port)
        self.lfclient_host = lfclient_host
        self.lfclient_port = lfclient_port
        self.debug = debug_on_
        # self.local_realm = realm.Realm(lfclient_host=self.lfclient_host,
        #                                lfclient_port=self.lfclient_port,
        #                                debug_=self.debug)
        self.monitor = self.new_wifi_monitor_profile()
        if channel != "AUTO":
            channel = int(channel)
        self.outfile = outfile
        self.radio = radio
        self.channel = channel
        self.channel_bw = channel_bw
        self.center_freq = center_freq
        self.duration = duration
        self.mode = radio_mode
        self.monitor_name = monitor_name
        # TODO allow the channel_frequency to be entered
        # if self.channel is None and self.channel_freq is None:
        #    print("either --channel or --channel_freq needs to be set")
        #    exit(1)
        # elif self.channel_freq is not None:
        #    self.freq = self.channel_freq
        if self.channel is not None:
            self.freq = self.chan_to_freq[self.channel]

        if self.channel_bw != '20':
            if self.center_freq is None:
                print("--center_freq need to be set for bw greater the 20")
                exit(1)

    def setup(self, ht40_value, ht80_value, ht160_value):
        # TODO: Store original channel settings so that radio can be set back to original values.
        self.monitor.set_flag(param_name="disable_ht40", value=ht40_value)
        self.monitor.set_flag(param_name="disable_ht80", value=ht80_value)
        self.monitor.set_flag(param_name="ht160_enable", value=ht160_value)
        self.monitor.create(radio_=self.radio, channel=self.channel, mode=self.mode, name_=self.monitor_name)

    def start(self):
        self.monitor.admin_up()
        LFUtils.wait_until_ports_appear(self.lfclient_url, self.monitor_name, debug=self.debug)
        # TODO:  Use LFUtils.wait_until_ports_admin_up instead of sleep, check return code.
        # time.sleep(5)
        self.set_freq(ssh_root=self.lfclient_host, ssh_passwd='lanforge', freq=self.freq)
        self.monitor.start_sniff(capname=self.outfile, duration_sec=self.duration)
        for i in range(0, self.duration):
            print("started sniffer, PLease wait,", self.duration - i)
            time.sleep(1)
        print("Sniffing Completed Success", "Check ", self.outfile)
        self.monitor.admin_down()
        time.sleep(2)

    # for 6E
    # For example for channel 7 with 80Mhz bw , here are the monitor commands possible
    # iw dev moni10a set freq 5955 80 5985
    # iw dev moni10a set freq 5975 80 5985
    # iw dev moni10a set freq 5995 80 5985
    # iw dev moni10a set freq 6015 80 5985

    # for 20 MHz the center frequency does not need to be entered since it is the same

    def set_freq(self, ssh_root, ssh_passwd, freq=0):
        if self.channel_bw == '20':
            cmd = f'. lanforge.profile\nsudo iw dev {self.monitor_name} set freq {freq}\n'
        else:
            cmd = f'. lanforge.profile\nsudo iw dev {self.monitor_name} set freq {freq} {self.channel_bw} {self.center_freq}\n'

        cmd1 = f'iw dev {self.monitor_name} info'
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ssh_root, 22, 'lanforge', ssh_passwd)
            time.sleep(10)
            stdout = ssh.exec_command(cmd, get_pty=True)
            stdout[0].write(f"{ssh_passwd}\n")
            stdout[0].flush()
            stdout = (stdout[1].readlines())
            print(stdout, "----- set channel frequency")
            stdout = ssh.exec_command(cmd1)
            stdout = (stdout[1].readlines())
            print(stdout, "----- channel frequency info")
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print("####", e, "####")
            exit(1)
        except TimeoutError as e:
            print("####", e, "####")
            exit(1)

    def cleanup(self):
        # TODO:  Add error checking to make sure monitor port really went away.
        # TODO:  Set radio back to original channel
        self.monitor.cleanup()


def main():
    parser = argparse.ArgumentParser(
        prog="lf_sniff_radio.py",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            lf_sniff_radio.py will create a monitor on LANforge (cli command add_monitor)

            ''',

        description='''\
        lf_sniff_radio.py will create a monitor and be able to capture wireshark pcap files:

        The monitor also uses iw commands to set up the proper bw and frequency to be monitored

        Note:

        iw [options] dev <devname> set freq <freq> [NOHT|HT20|HT40+|HT40-|5MHz|10MHz|80MHz]
	    dev <devname> set freq <control freq> [5|10|20|40|80|80+80|160] [<center1_freq> [<center2_freq>]]

        Example to monitor channel 36 (5180)
        sudo iw dev <monitor/devname> set freq 5180 40 5190

        for bw of 20 do not need to set the control frequency

        Verify the configuration with :(need to do sudo)
        iw dev <monitor/devname> info

        example:
        [lanforge@ct523c-3ba3 ~]$ sudo iw dev SNIFF_5G_40 info
        [sudo] password for lanforge:
        Interface SNIFF_5G_40
            ifindex 49
            wdev 0x2
            addr d8:f8:83:36:4c:a0
            type monitor
            wiphy 0
            channel 36 (5180 MHz), width: 20 MHz, center1: 5180 MHz
            txpower 0.00 dBm
        [lanforge@ct523c-3ba3 ~]$


        Help: 5Ghz frequencies

        ''',

        usage="""./lf_sniff_radio.py
        --mgr localhost
        --mgr_port 8080
        --radio wiphy0
        --outfile /home/lanforge/test_sniff.pcap
        --duration 1
        --channel 36
        --channel_bw 40
        --center_freq 5190
        --radio_mode AUTO
        --monitor_name Sniffer0
        """)

    parser.add_argument('--mgr', type=str, help='--mgr: IP Address of LANforge', default="localhost")
    parser.add_argument('--mgr_port', type=int, help='--mgr_port: HTTP Port of LANforge', default=8080)
    parser.add_argument('--radio', type=str, help='--radio: Radio to sniff', default="wiphy0")
    parser.add_argument('--outfile', type=str, help='--outfile: give the filename with path',
                        default="/home/lanforge/test_pcap.pcap")
    parser.add_argument('--duration', type=int, help='--duration duration in sec, for which you want to capture',
                        default=60)
    parser.add_argument('--channel', type=str, help='''
                                    --channel Set channel pn selected Radio, the channel [52, 56 ...]
                                    channel will get converted to the control frequency.
                                    Must enter Channel
                                    ''',
                        default='36')
    # parser.add_argument('--channel_freq', type=str, help='''
    #                                --channel_freq  this is the frequency that the channel operates at
    #                                Must enter --channel or --channel_freq
    #                                --channel takes presidence if both entered
    #                                ''',
    #                    default=0)
    parser.add_argument('--channel_bw', type=str, help='--channel_bw select the bandwidth to be monitored, [ [20|40|80|80+80|160]], default=20',
                        default='20')
    parser.add_argument('--center_freq', type=str, help='''
                        --center_freq  select the bandwidth to be monitored, not needed if bw is 20
                        ''',
                        default=None)

    parser.add_argument('--radio_mode', type=str, help='--radio_mode select the radio mode [AUTO, 802.11a, 802.11b, '
                                                       '802.11ab ...]', default="AUTO")
    parser.add_argument('--monitor_name', type=str, help='Wi-Fi monitor name', default="sniffer0")
    parser.add_argument('--disable_ht40', type=str, help='Enable/Disable \"disable_ht40\" [0-disable,1-enable]',
                        default=0)
    parser.add_argument('--disable_ht80', type=str, help='Enable/Disable \"disable_ht80\" [0-disable,1-enable]',
                        default=0)
    parser.add_argument('--ht160_enable', type=str, help='Enable/Disable \"ht160_enable\\ [0-disable,1-enable]" ',
                        default=0)

    args = parser.parse_args()

    # if args.channel is None and args.channel_freq is None:
    #    print('--channel or --channel_freq most be entered')

    obj = SniffRadio(lfclient_host=args.mgr,
                     lfclient_port=args.mgr_port,
                     radio=args.radio,
                     outfile=args.outfile,
                     duration=args.duration,
                     channel=args.channel,
                     # channel_freq=args.center_freq,
                     channel_bw=args.channel_bw,
                     center_freq=args.center_freq,
                     radio_mode=args.radio_mode,
                     monitor_name=args.monitor_name)
    obj.setup(int(args.disable_ht40), int(args.disable_ht80), int(args.ht160_enable))
    # TODO: Add wait-for logic instead of a sleep
    time.sleep(5)
    obj.start()
    obj.cleanup()

    # TODO:  Check if passed or not.


if __name__ == '__main__':
    main()
