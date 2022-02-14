#!/usr/bin/env python3
"""
Candela Technologies Inc.
Info : Standard Script for WLAN Capacity Calculator
Date :
Author : Anjali Rahamatkar
"""
import sys
import os
import importlib
import argparse
import logging


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

wlan_theoretical_sta = importlib.import_module("py-json.wlan_theoretical_sta")


def main():

    parse = wlan_theoretical_sta.abg11_calculator.create_argparse(prog='wlan_capacity_calculator.py',
                                                                  formatter_class=argparse.RawTextHelpFormatter,
                                                                  epilog='''\
             This python script calculates the theoretical value of three different stations( 11abg/11n/11ac)''',
                                                                  description='''\
        wlan_capacity_calculator.py
        ---------------------------------------------------------------------------

    Example of command line to run(11ac Station):
   ./wlan_capacity_calculator.py 
        -sta 11ac 
        -t Voice 
        -d 9 
        -spa 3    
        -ch 20
        -gu 800 
        -high 1
        -e TKIP
        -q Yes 
        -ip 3
        -mc 0
        -b 6 12 24 54
        -m 1518
        -co Greenfield
        -cw 15
            ''')

    try:
        args = parse.parse_args()
        # Station
        if args.station:
            Calculator_name = args.station
        else:
            Calculator_name = "11abg"

        # Traffic Type
        if args.traffic:
            traffic_name = args.traffic
        else:
            traffic_name = "Data"

        # PHY Bit Rate
        if args.phy:
            phy_name = args.phy
        else:
            phy_name = "54"

        # Encryption
        if args.encryption:
            encryption_name = args.encryption
        else:
            encryption_name = "None"

        # QoS

        if args.qos:
            qos_name = args.qos
        else:
            if "11abg" in Calculator_name:
                qos_name = "No"
            if "11n" in Calculator_name or "11ac" in Calculator_name:
                qos_name = "Yes"

        # 802.11 MAC Frame

        if args.mac:
            mac_name = args.mac
        else:
            mac_name = "1518"

        # Basic Rate Set

        if args.basic:
            basic_name = args.basic
        else:
            basic_name = ['1', '2', '5.5', '11', '6', '12', '24']

        # Preamble value

        if args.preamble:
            preamble_name = args.preamble
        else:
            preamble_name = "Short"

        # Slot Time

        if args.slot:
            slot_name = args.slot
        else:
            slot_name = "Short"

        # Codec Type (Voice Traffic)

        if args.codec:
            codec_name = args.codec
        else:
            if "11abg" in Calculator_name:
                codec_name = "G.723"
            if "11n" in Calculator_name:
                codec_name = "G.711"
            if "11ac" in Calculator_name:
                codec_name = "Mixed"

        # RTS/CTS Handshake

        if args.rts:
            rts_name = args.rts
        else:
            rts_name = "No"

        # CTS - to - self(protection)

        if args.cts:
            cts_name = args.cts
        else:
            cts_name = "No"

        # station = 11n and 11ac

        # Data/Voice MCS Index

        if args.data:
            data_name = args.data
        else:
            if "11n" in Calculator_name:
                data_name = "7"
            if "11ac" in Calculator_name:
                data_name = "9"

        # Channel Bandwidth

        if args.channel:
            channel_name = args.channel
        else:
            if "11n" in Calculator_name:
                channel_name = "40"
            if "11ac" in Calculator_name:
                channel_name = "80"

        # Guard Interval

        if args.guard:
            guard_name = args.guard
        else:
            guard_name = "400"

        # Highest Basic MCS

        if args.highest:
            highest_name = args.highest
        else:
            highest_name = '1'

        # PLCP Configuration

        if args.plcp:
            plcp_name = args.plcp
        else:
            plcp_name = "Mixed"

        # IP Packets per A-MSDU

        if args.ip:
            ip_name = args.ip
        else:
            ip_name = "0"

        # MAC Frames per A-MPDU

        if args.mc:
            mc_name = args.mc
        else:
            if "11n" in Calculator_name:
                mc_name = '42'
            if "11ac" in Calculator_name:
                mc_name = '64'

        # CWmin (leave alone for default)

        if args.cwin:
            cwin_name = args.cwin
        else:
            cwin_name = '15'

        # Spatial Streams

        if args.spatial:
            spatial_name = args.spatial
        else:
            spatial_name = '4'

        # RTS/CTS Handshake and CTS-to-self

        if args.rtscts:
            rtscts_name = args.rtscts
        else:
            rtscts_name = 'No'

    except Exception as e:
        logging.exception(e)
        exit(2)

    # Select station(802.11a/b/g/n/ac standards)

    if "11abg" in Calculator_name:
        Station1 = wlan_theoretical_sta.abg11_calculator(traffic_name, phy_name, encryption_name, qos_name, mac_name, basic_name,
                                                         preamble_name, slot_name, codec_name, rts_name, cts_name)
        Station1.calculate()
        Station1.get_result()

    if "11n" in Calculator_name:
        Station2 = wlan_theoretical_sta.n11_calculator(traffic_name, data_name, channel_name, guard_name, highest_name, encryption_name,
                                                       qos_name, ip_name,
                                                       mc_name, basic_name, mac_name,
                                                       codec_name, plcp_name, cwin_name, rts_name, cts_name)
        Station2.calculate()
        Station2.get_result()
    if "11ac" in Calculator_name:
        Station3 = wlan_theoretical_sta.ac11_calculator(traffic_name, data_name, spatial_name, channel_name, guard_name, highest_name,
                                                        encryption_name, qos_name, ip_name, mc_name, basic_name, mac_name,
                                                        codec_name, cwin_name, rtscts_name)
        Station3.calculate()
        Station3.get_result()


if __name__ == "__main__":
    main()
