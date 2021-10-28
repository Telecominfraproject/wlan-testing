#!/usr/bin/env python3

'''

Candela Technologies Inc.
Info : Standard Script for WLAN Capaity Calculator
Date :
Author : Anjali Rahamatkar

This Script has three classes :
          1. abg11_calculator : It will take all the user input of 802.11a/b/g station,calculate Intermediate values and Theoretical values.
          2. n11_calculator : It will take all the user input of 802.11n station,calculate Intermediate values and Theoretical values.
          3. ac11_calculator : It will take all the user input of 802.11ac station,calculate Intermediate values and Theoretical values.
All classes have different functions: input_parameter() that calculates intermediate values and generate theroretical data

'''

import argparse
import json


# Class to take all user input (802.11a/b/g Standard)



class abg11_calculator():

    def __init__(self, Traffic_Type, PHY_Bit_Rate, Encryption, QoS, MAC_Frame_802_11, Basic_Rate_Set, Preamble,
                 slot_name, Codec_Type, RTS_CTS_Handshake, CTS_to_self):
        self.Traffic_Type = Traffic_Type
        self.PHY_Bit_Rate = PHY_Bit_Rate
        self.Encryption = Encryption
        self.QoS = QoS
        self.MAC_Frame_802_11 = MAC_Frame_802_11
        self.Basic_Rate_Set = Basic_Rate_Set
        self.Preamble = Preamble
        self.slot_name = slot_name
        self.Codec_Type = Codec_Type
        self.RTS_CTS_Handshake = RTS_CTS_Handshake
        self.CTS_to_self = CTS_to_self




    # This function is for calculate intermediate values and Theoretical values

    @staticmethod
    def create_argparse(prog=None, formatter_class=None, epilog=None, description=None):
        if (prog is not None) or (formatter_class is not None) or (epilog is not None) or (description is not None):
            ap = argparse.ArgumentParser(prog=prog,
                                             formatter_class=formatter_class,
                                             allow_abbrev=True,
                                             epilog=epilog,
                                             description=description)
        else:
            ap = argparse.ArgumentParser()

        # Station : 11abg

        ap.add_argument("-sta", "--station", help="Enter Station Name : [11abg,11n,11ac](by Default 11abg)")
        ap.add_argument("-t", "--traffic", help="Enter the Traffic Type : [Data,Voice](by Default Data)")
        ap.add_argument("-p", "--phy",
                        help="Enter the PHY Bit Rate of Data Flow : [1, 2, 5.5, 11, 6, 9, 12, 18, 24, 36, 48, 54](by Default 54)")
        ap.add_argument("-e", "--encryption",
                        help="Enter the Encryption  : [None,  WEP ,  TKIP, CCMP](by Default None)")
        ap.add_argument("-q", "--qos", help="Enter the QoS = : [No,  Yes](by Default [No for 11abg] and [Yes for 11n])")
        ap.add_argument("-m", "--mac",
                        help="Enter the 802.11 MAC Frame  : [Any Value](by Default [106 for 11abg] and [1538 for 11n])")
        ap.add_argument("-b", "--basic", nargs='+',
                        help="Enter the Basic Rate Set : [1,2, 5.5, 11, 6, 9, 12, 18, 24, 36, 48, 54]"
                             " (by Default [1 2 5.5 11 6 12] for 11abg, [6 12 24] for 11n/11ac])")
        ap.add_argument("-pre", "--preamble", help="Enter Preamble value : [ Short, Long, N/A](by Default Short)")
        ap.add_argument("-s", "--slot", help="Enter the Slot Time  : [Short,  Long, N/A](by Default Short)")
        ap.add_argument("-co", "--codec", help="Enter the Codec Type (Voice Traffic): {[ G.711 ,  G.723 ,  G.729]"
                                               "by Default G.723 for 11abg, G.711 for 11n} and"
                                               "{['Mixed','Greenfield'] by Default Mixed for 11ac}")
        ap.add_argument("-r", "--rts", help="Enter the RTS/CTS Handshake : [No,  Yes](by Default No)")
        ap.add_argument("-c", "--cts", help="Enter the CTS-to-self (protection)	: [No,  Yes](by Default No)")

        # Station : 11n and 11ac

        ap.add_argument("-d", "--data",
                        help="Enter the Data/Voice MCS Index : ['0','1','2','3','4','5','6','7','8','9','10',"
                             "'11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26',"
                             "'27','28','29','30','31']by Default 7")
        ap.add_argument("-ch", "--channel",
                        help="Enter the Channel Bandwidth = : ['20','40'] by Default 40 for 11n and "
                             "['20','40','80'] by Default 80 for 11ac")
        ap.add_argument("-gu", "--guard", help="Enter the Guard Interval = : ['400','800'] (by Default 400)")
        ap.add_argument("-high", "--highest",
                        help="Enter the Highest Basic MCS = : ['0','1','2','3','4','5','6','7','8','9',"
                             "'10','11','12','13','14','15','16','17','18','19','20','21','22','23','24',"
                             "'25','26','27','28','29','30','31'](by Default 1)")
        ap.add_argument("-pl", "--plcp",
                        help="Enter the PLCP Configuration = : ['Mixed','Greenfield'] (by Default Mixed) for 11n")
        ap.add_argument("-ip", "--ip",
                        help="Enter the IP Packets per A-MSDU = : ['0','1','2','3','4','5','6','7','8','9',"
                             "'10','11','12','13','14','15','16','17','18','19','20'] (by Default 0)")
        ap.add_argument("-mc", "--mc",
                        help="Enter the MAC Frames per A-MPDU = : ['0','1','2','3','4','5','6','7','8',"
                             "'9','10','11','12','13','14','15','16','17','18','19','20','21','22','23',"
                             "'24','25','26','27','28','29','30','31','32','33','34','35','36','37','38',"
                             "'39','40','41','42','43','44','45','46','47','48','49','50','51','52','53',"
                             "'54','55','56','57','58','59','60','61','62','63','64'](by Default [42 for 11n] and [64 for 11ac])")
        ap.add_argument("-cw", "--cwin",
                        help="Enter the CWmin (leave alone for default) = : [Any Value] (by Default 15)")
        ap.add_argument("-spa", "--spatial", help="Enter the Spatial Streams  = [1,2,3,4] (by Default 4)")
        ap.add_argument("-rc", "--rtscts", help="Enter the RTS/CTS Handshake and CTS-to-self "
                                                "  = ['No','Yes'] (by Default No for 11ac)")
        return ap

    def calculate(self):

        PHY_Bit_Rate_float = float(self.PHY_Bit_Rate)
        PHY_Bit_Rate_int = int(PHY_Bit_Rate_float)
        if PHY_Bit_Rate_int < 12:
            if PHY_Bit_Rate_int < 5:
                yellow_cell = PHY_Bit_Rate_int
            else:
                if PHY_Bit_Rate_int == 5:
                    yellow_cell = 5.5
                else:
                    if PHY_Bit_Rate_int == 11:
                        yellow_cell = 11
                    else:
                        if PHY_Bit_Rate_int == 6:
                            yellow_cell = 6
                        else:
                            if PHY_Bit_Rate_int == 9:
                                yellow_cell = 9
        else:
            if PHY_Bit_Rate_int == 12:
                yellow_cell = 12
            else:
                if PHY_Bit_Rate_int == 18:
                    yellow_cell = 18
                else:
                    if PHY_Bit_Rate_int == 24:
                        yellow_cell = 24
                    else:
                        if PHY_Bit_Rate_int == 36:
                            yellow_cell = 36
                        else:
                            if PHY_Bit_Rate_int == 48:
                                yellow_cell = 48
                            else:
                                yellow_cell = 54

        # (IP Packet)

        if "None" in self.Encryption:
            Enc_value = 0
        else:
            if "WEP" in self.Encryption:
                Enc_value = 8
            else:
                if "TKIP" in self.Encryption:
                    Enc_value = 20
                else:
                    Enc_value = 16
        if "Yes" in self.QoS:
            Qos_value = 2
        else:
            Qos_value = 0
        ip_packet_1 = int(self.MAC_Frame_802_11) - 36 - float(Enc_value) - float(Qos_value)
        ip_packet = int(ip_packet_1)
        if ip_packet < 20:
            get_ip_packet = "N/A"
            ip = 0
        else:
            get_ip_packet = ip_packet
            ip = 1

        # (Ethernet MAC Frame)

        encrpt = float(self.MAC_Frame_802_11) - 24 - 8 + 14 - float(Enc_value) - float(Qos_value)
        Ethernet_MAC_Frame_int = max(encrpt, 64)
        Ethernet_value = int(Ethernet_MAC_Frame_int)
        get_ethernet = Ethernet_value

        # Usable Basic Rates

        if "1" in self.Basic_Rate_Set:
            if "1" in self.Basic_Rate_Set and yellow_cell >= 1:
                Usable_Basic_Rates_1 = 1
            else:
                Usable_Basic_Rates_1 = 0
        else:
            Usable_Basic_Rates_1 = 0

        if "2" in self.Basic_Rate_Set:
            if "2" in self.Basic_Rate_Set and yellow_cell >= 2:
                Usable_Basic_Rates_2 = 2
            else:
                Usable_Basic_Rates_2 = 0
        else:
            Usable_Basic_Rates_2 = 0

        if "5.5" in self.Basic_Rate_Set:
            if "5.5" in self.Basic_Rate_Set and yellow_cell >= 5:
                Usable_Basic_Rates_5 = 5.5
            else:
                Usable_Basic_Rates_5 = 0
        else:
            Usable_Basic_Rates_5 = 0

        if "11" in self.Basic_Rate_Set:
            if "11" in self.Basic_Rate_Set and yellow_cell >= 11:
                Usable_Basic_Rates_11 = 11
            else:
                Usable_Basic_Rates_11 = 0
        else:
            Usable_Basic_Rates_11 = 0

        if "6" in self.Basic_Rate_Set:
            if "6" in self.Basic_Rate_Set and yellow_cell >= 6:
                Usable_Basic_Rates_6 = 6
            else:
                Usable_Basic_Rates_6 = 0
        else:
            Usable_Basic_Rates_6 = 0

        if "9" in self.Basic_Rate_Set:
            if "9" in self.Basic_Rate_Set and yellow_cell >= 9:
                Usable_Basic_Rates_9 = 9
            else:
                Usable_Basic_Rates_9 = 0
        else:
            Usable_Basic_Rates_9 = 0

        if "12" in self.Basic_Rate_Set:
            if "12" in self.Basic_Rate_Set and yellow_cell >= 12:
                Usable_Basic_Rates_12 = 12
            else:
                Usable_Basic_Rates_12 = 0
        else:
            Usable_Basic_Rates_12 = 0

        if "18" in self.Basic_Rate_Set:
            if "18" in self.Basic_Rate_Set and yellow_cell >= 18:
                Usable_Basic_Rates_18 = 18
            else:
                Usable_Basic_Rates_18 = 0
        else:
            Usable_Basic_Rates_18 = 0

        if "24" in self.Basic_Rate_Set:
            if "24" in self.Basic_Rate_Set and yellow_cell >= 24:
                Usable_Basic_Rates_24 = 24
            else:
                Usable_Basic_Rates_24 = 0
        else:
            Usable_Basic_Rates_24 = 0

        if "36" in self.Basic_Rate_Set:
            if "36" in self.Basic_Rate_Set and yellow_cell >= 36:
                Usable_Basic_Rates_36 = 36
            else:
                Usable_Basic_Rates_36 = 0
        else:
            Usable_Basic_Rates_36 = 0

        if "48" in self.Basic_Rate_Set:
            if "48" in self.Basic_Rate_Set and yellow_cell >= 48:
                Usable_Basic_Rates_48 = 48
            else:
                Usable_Basic_Rates_48 = 0
        else:
            Usable_Basic_Rates_48 = 0

        if "54" in self.Basic_Rate_Set:
            if "54" in self.Basic_Rate_Set and yellow_cell >= 54:
                Usable_Basic_Rates_54 = 54
            else:
                Usable_Basic_Rates_54 = 0
        else:
            Usable_Basic_Rates_54 = 0

        # Usable Mandatory Rates

        if (PHY_Bit_Rate_int <= 11) and yellow_cell >= 1:
            Mandatory_1 = 1
        else:
            Mandatory_1 = 0
        if (PHY_Bit_Rate_int <= 11) and yellow_cell >= 2:
            Mandatory_2 = 2
        else:
            Mandatory_2 = 0
        if (PHY_Bit_Rate_int <= 11) and yellow_cell >= 5:
            Mandatory_5 = 5.5
        else:
            Mandatory_5 = 0
        if (PHY_Bit_Rate_int <= 11) and yellow_cell >= 11:
            Mandatory_11 = 11
        else:
            Mandatory_11 = 0
        if (PHY_Bit_Rate_int >= 6) and yellow_cell >= 6:
            Mandatory_6 = 6
        else:
            Mandatory_6 = 0
        if (PHY_Bit_Rate_int >= 6) and yellow_cell >= 9:
            Mandatory_9 = 6
        else:
            Mandatory_9 = 0
        if (PHY_Bit_Rate_int >= 6) and yellow_cell >= 12:
            Mandatory_12 = 12
        else:
            Mandatory_12 = 0
        if (PHY_Bit_Rate_int >= 6) and yellow_cell >= 18:
            Mandatory_18 = 12
        else:
            Mandatory_18 = 0
        if (PHY_Bit_Rate_int >= 6) and yellow_cell >= 24:
            Mandatory_24 = 24
        else:
            Mandatory_24 = 0
        if (PHY_Bit_Rate_int >= 6) and yellow_cell >= 36:
            Mandatory_36 = 24
        else:
            Mandatory_36 = 0
        if (PHY_Bit_Rate_int >= 6) and yellow_cell >= 48:
            Mandatory_48 = 24
        else:
            Mandatory_48 = 0
        if (PHY_Bit_Rate_int >= 6) and yellow_cell >= 54:
            Mandatory_54 = 24
        else:
            Mandatory_54 = 0

        # CWmin_str (leave alone for default)

        if (PHY_Bit_Rate_int == 1 or PHY_Bit_Rate_int == 2 or PHY_Bit_Rate_int == 5 or PHY_Bit_Rate_int == 11):
            CWmin_str = 31
        else:
            if (
                    "1" in self.Basic_Rate_Set or "2" in self.Basic_Rate_Set or "5.5" in self.Basic_Rate_Set or "11" in self.Basic_Rate_Set) \
                    and (not ("6" in self.Basic_Rate_Set or "9" in self.Basic_Rate_Set or "12" in self.Basic_Rate_Set or
                              "18" in self.Basic_Rate_Set or "24" in self.Basic_Rate_Set or "36" in self.Basic_Rate_Set or "48" in self.Basic_Rate_Set or "54" in self.Basic_Rate_Set)):
                CWmin_str = 31
            else:
                CWmin_str = 15

        # MAC MPDU Size

        if "G.711" in self.Codec_Type:
            Codec_IP_Packet_Size = 200
            Codec_Frame_rate = 100
        else:
            if "G.723" in self.Codec_Type:
                Codec_IP_Packet_Size = 60
                Codec_Frame_rate = 67
            elif "G.729" in self.Codec_Type:
                Codec_IP_Packet_Size = 60
                Codec_Frame_rate = 100
            else:
                Codec_IP_Packet_Size = 0
                Codec_Frame_rate = 0

        if "Data" in self.Traffic_Type:
            MAC_MPDU_Size = int(self.MAC_Frame_802_11)
        else:
            if "None" in self.Encryption:
                result = Codec_IP_Packet_Size + 28 + 0
            elif "WEP" in self.Encryption:
                result = Codec_IP_Packet_Size + 28 + 8
            elif "TKIP" in self.Encryption:
                result = Codec_IP_Packet_Size + 28 + 20
            else:
                result = Codec_IP_Packet_Size + 28 + 16
            if "Yes" in self.QoS:
                final_result = result + 2
            else:
                final_result = result + 0

            MAC_MPDU_Size = final_result + 8

        # PHY Bit Rate of Control Frames

        if (PHY_Bit_Rate_int == 1 or PHY_Bit_Rate_int == 2 or PHY_Bit_Rate_int == 5 or PHY_Bit_Rate_int == 11):
            data = 1
        else:
            data = 6

        if len(self.Basic_Rate_Set) == 0:
            present_BasicRate = 0
        else:
            present_BasicRate = 1

        if present_BasicRate == 1:
            PHY_Bit = max(Usable_Basic_Rates_1, Usable_Basic_Rates_2, Usable_Basic_Rates_5,
                          Usable_Basic_Rates_11, Usable_Basic_Rates_6,
                          Usable_Basic_Rates_9, Usable_Basic_Rates_12, Usable_Basic_Rates_18,
                          Usable_Basic_Rates_24, Usable_Basic_Rates_36, Usable_Basic_Rates_48,
                          Usable_Basic_Rates_54, data)


        else:
            PHY_Bit = max(Mandatory_1, Mandatory_2, Mandatory_5, Mandatory_11, Mandatory_6, Mandatory_9,
                          Mandatory_12, Mandatory_18, Mandatory_24, Mandatory_36, Mandatory_48, Mandatory_54)

        # Ttxframe (ACK)

        if "Short" in self.Preamble:
            Preamble_1 = float(96)
        else:
            Preamble_1 = float(192)

        if (PHY_Bit == 1) or (PHY_Bit == 2) or (PHY_Bit == 5.5) or (PHY_Bit == 11):
            Ttxframe = (14 * 8) / PHY_Bit + (Preamble_1)

            Ttxframe_new = format(Ttxframe, '.2f')
        else:
            Ttxframe = int((14 * 8 + 22 + PHY_Bit * 4 - 1) / (PHY_Bit * 4)) * 4 + 20
            Ttxframe_new = format(Ttxframe, '.2f')

        # RTS/CTS Handshake Overhead

        if (PHY_Bit_Rate_int == 1 or PHY_Bit_Rate_int == 2 or PHY_Bit_Rate_int == 5 or PHY_Bit_Rate_int == 11):
            SIFS_value = float(10)
        else:
            SIFS_value = float(16)

        if "No" in self.RTS_CTS_Handshake:
            RTS_CTS_Handshake_Overhead = 0

        elif "Yes" in self.RTS_CTS_Handshake:
            if (PHY_Bit == 1) or (PHY_Bit == 2) or (PHY_Bit == 5.5) or (PHY_Bit == 11):
                RTS_CTS_Handshake = ((20 + 14) * 8) / PHY_Bit + (Preamble_1)

            else:
                RTS_CTS_Handshake = int(((20 + 14) * 8 + 22 + PHY_Bit * 4 - 1) / (PHY_Bit * 4)) * 4 + 2 * 20

            RTS_CTS_Handshake_Overhead = RTS_CTS_Handshake + (2 * SIFS_value)

        # c22 CTS-to-self Handshake Overhead

        if ("Yes" in self.CTS_to_self) and ("Yes" in self.RTS_CTS_Handshake):
            CTS_to_self_Handshake = 0
        else:
            if ("No" in self.CTS_to_self) or ("Yes" in self.RTS_CTS_Handshake):
                CTS_to_self_Handshake = 0
            else:
                if (PHY_Bit == 1) or (PHY_Bit == 2) or (PHY_Bit == 5.5) or (PHY_Bit == 11):
                    CTS_to_self_Handshake = (14 * 8) / PHY_Bit + (Preamble_1) + SIFS_value
                else:
                    CTS_to_self_Handshake = int(
                        (14 * 8 + 22 + PHY_Bit * 4 - 1) / (PHY_Bit * 4)) * 4 + 20 + SIFS_value

        # DIFS calulation

        if (PHY_Bit_Rate_int == 1 or PHY_Bit_Rate_int == 2 or PHY_Bit_Rate_int == 5 or PHY_Bit_Rate_int == 11):
            DIFS_value = 50
        elif ("Short" in self.slot_name):
            DIFS_value = 34
        else:
            DIFS_value = 50

        # MeanBackoff calculation

        if (PHY_Bit_Rate_int == 1 or PHY_Bit_Rate_int == 2 or PHY_Bit_Rate_int == 5 or PHY_Bit_Rate_int == 11):
            c4 = (CWmin_str * 20 / 2)
            MeanBackoff_value = float(c4)
        elif ("Short" in self.slot_name):
            d2 = (CWmin_str * 9 / 2)
            MeanBackoff_value = float(d2)
        else:
            d3 = (CWmin_str * 20 / 2)
            MeanBackoff_value = float(d3)

        # c27 Ndbps, MAC data bits per symbol
        Ndbps_value = yellow_cell * 4

        # Nbits, bits in MAC frame
        Nbits_value = (MAC_MPDU_Size * 8)

        # Tmac, time for MAC frame and  Tplcp, time for MAC PLCP
        if (PHY_Bit_Rate_int == 1 or PHY_Bit_Rate_int == 2 or PHY_Bit_Rate_int == 5 or PHY_Bit_Rate_int == 11):
            Tmac_value = Nbits_value / yellow_cell
            if "Short" in self.Preamble:
                Tplcp = float(96)
            else:
                Tplcp = float(192)
        else:
            Tmac_value = int((Nbits_value + 22 + Ndbps_value) / Ndbps_value) * 4
            Tplcp = float(20)

        # Ttxframe (DATA)

        Ttxframe_data = Tmac_value + Tplcp

        Client_1 = Ttxframe_data + SIFS_value + Ttxframe + DIFS_value + RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake + MeanBackoff_value
        Client_2 = Ttxframe_data + SIFS_value + Ttxframe + DIFS_value + RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake + MeanBackoff_value / 2
        Client_3 = Ttxframe_data + SIFS_value + Ttxframe + DIFS_value + RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake + MeanBackoff_value / 5
        Client_4 = Ttxframe_data + SIFS_value + Ttxframe + DIFS_value + RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake + MeanBackoff_value / 10
        Client_5 = Ttxframe_data + SIFS_value + Ttxframe + DIFS_value + RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake + MeanBackoff_value / 20
        Client_6 = Ttxframe_data + SIFS_value + Ttxframe + DIFS_value + RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake + MeanBackoff_value / 50
        Client_7 = Ttxframe_data + SIFS_value + Ttxframe + DIFS_value + RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake + MeanBackoff_value / 100
        self.Client_1_new = format(Client_1, '.2f')
        Client_2_new = format(Client_2, '.4f')
        Client_3_new = format(Client_3, '.4f')
        Client_4_new = format(Client_4, '.4f')
        Client_5_new = format(Client_5, '.4f')
        Client_6_new = format(Client_6, '.4f')
        Client_7_new = round(Client_7)

        # Max Frame Rate

        Max_Frame_Rate_C1 = 1000000 / Client_1
        self.Max_Frame_Rate_C1_round = round(Max_Frame_Rate_C1)
        Max_Frame_Rate_C2 = 1000000 / Client_2
        Max_Frame_Rate_C2_round = round(Max_Frame_Rate_C2)
        Max_Frame_Rate_C3 = 1000000 / Client_3
        Max_Frame_Rate_C3_round = round(Max_Frame_Rate_C3)
        Max_Frame_Rate_C4 = 1000000 / Client_4
        Max_Frame_Rate_C4_round = round(Max_Frame_Rate_C4)
        Max_Frame_Rate_C5 = 1000000 / Client_5
        Max_Frame_Rate_C5_round = round(Max_Frame_Rate_C5)
        Max_Frame_Rate_C6 = 1000000 / Client_6
        Max_Frame_Rate_C6_round = round(Max_Frame_Rate_C6)
        Max_Frame_Rate_C7 = 1000000 / Client_7
        Max_Frame_Rate_C7_round = round(Max_Frame_Rate_C7)

        # Max. Offered Load (802.11)

        Max_Offered_Load_C1 = Max_Frame_Rate_C1 * Nbits_value / 1000000
        self.Max_Offered_Load_C1_new = format(Max_Offered_Load_C1, '.3f')
        Max_Offered_Load_C2 = Max_Frame_Rate_C2 * Nbits_value / 1000000
        Max_Offered_Load_C2_new = format(Max_Offered_Load_C2, '.3f')
        Max_Offered_Load_C3 = Max_Frame_Rate_C3 * Nbits_value / 1000000
        Max_Offered_Load_C3_new = format(Max_Offered_Load_C3, '.3f')
        Max_Offered_Load_C4 = Max_Frame_Rate_C4 * Nbits_value / 1000000
        Max_Offered_Load_C4_new = format(Max_Offered_Load_C4, '.3f')
        Max_Offered_Load_C5 = Max_Frame_Rate_C5 * Nbits_value / 1000000
        Max_Offered_Load_C5_new = format(Max_Offered_Load_C5, '.3f')
        Max_Offered_Load_C6 = Max_Frame_Rate_C6 * Nbits_value / 1000000
        Max_Offered_Load_C6_new = format(Max_Offered_Load_C6, '.3f')
        Max_Offered_Load_C7 = Max_Frame_Rate_C7 * Nbits_value / 1000000
        Max_Offered_Load_C7_new = format(Max_Offered_Load_C7, '.3f')

        # Offered Load Per 802.11 Client

        Offered_Load_Per_Client1 = Max_Offered_Load_C1 / 1
        self.Offered_Load_Per_Client1_new = format(Offered_Load_Per_Client1, '.3f')
        Offered_Load_Per_Client2 = Max_Offered_Load_C2 / 2
        Offered_Load_Per_Client2_new = format(Offered_Load_Per_Client2, '.3f')
        Offered_Load_Per_Client3 = Max_Offered_Load_C3 / 5
        Offered_Load_Per_Client3_new = format(Offered_Load_Per_Client3, '.3f')
        Offered_Load_Per_Client4 = Max_Offered_Load_C4 / 10
        Offered_Load_Per_Client4_new = format(Offered_Load_Per_Client4, '.3f')
        Offered_Load_Per_Client5 = Max_Offered_Load_C5 / 20
        Offered_Load_Per_Client5_new = format(Offered_Load_Per_Client5, '.3f')
        Offered_Load_Per_Client6 = Max_Offered_Load_C6 / 50
        Offered_Load_Per_Client6_new = format(Offered_Load_Per_Client6, '.3f')
        Offered_Load_Per_Client7 = Max_Offered_Load_C7 / 100
        Offered_Load_Per_Client7_new = format(Offered_Load_Per_Client7, '.3f')

        # Offered Load (802.3 Side)

        Offered_Load_C1 = Max_Frame_Rate_C1 * Ethernet_MAC_Frame_int * 8 / 1000000
        self.Offered_Load_C1_new = format(Offered_Load_C1, '.3f')
        Offered_Load_C2 = Max_Frame_Rate_C2 * Ethernet_MAC_Frame_int * 8 / 1000000
        Offered_Load_C2_new = format(Offered_Load_C2, '.3f')
        Offered_Load_C3 = Max_Frame_Rate_C3 * Ethernet_MAC_Frame_int * 8 / 1000000
        Offered_Load_C3_new = format(Offered_Load_C3, '.3f')
        Offered_Load_C4 = Max_Frame_Rate_C4 * Ethernet_MAC_Frame_int * 8 / 1000000
        Offered_Load_C4_new = format(Offered_Load_C4, '.3f')
        Offered_Load_C5 = Max_Frame_Rate_C5 * Ethernet_MAC_Frame_int * 8 / 1000000
        Offered_Load_C5_new = format(Offered_Load_C5, '.3f')
        Offered_Load_C6 = Max_Frame_Rate_C6 * Ethernet_MAC_Frame_int * 8 / 1000000
        Offered_Load_C6_new = format(Offered_Load_C6, '.3f')
        Offered_Load_C7 = Max_Frame_Rate_C7 * Ethernet_MAC_Frame_int * 8 / 1000000
        Offered_Load_C7_new = format(Offered_Load_C7, '.3f')

        # IP Throughput (802.11 -> 802.3)

        if ip == 1:
            IP_Throughput_C1 = Max_Frame_Rate_C1 * ip_packet * 8 / 1000000
            self.IP_Throughput_C1_new = format(IP_Throughput_C1, '.3f')
            IP_Throughput_C2 = Max_Frame_Rate_C2 * ip_packet * 8 / 1000000
            IP_Throughput_C2_new = format(IP_Throughput_C2, '.3f')
            IP_Throughput_C3 = Max_Frame_Rate_C3 * ip_packet * 8 / 1000000
            IP_Throughput_C3_new = format(IP_Throughput_C3, '.3f')
            IP_Throughput_C4 = Max_Frame_Rate_C4 * ip_packet * 8 / 1000000
            IP_Throughput_C4_new = format(IP_Throughput_C4, '.3f')
            IP_Throughput_C5 = Max_Frame_Rate_C5 * ip_packet * 8 / 1000000
            IP_Throughput_C5_new = format(IP_Throughput_C5, '.3f')
            IP_Throughput_C6 = Max_Frame_Rate_C6 * ip_packet * 8 / 1000000
            IP_Throughput_C6_new = format(IP_Throughput_C6, '.3f')
            IP_Throughput_C7 = Max_Frame_Rate_C7 * ip_packet * 8 / 1000000
            IP_Throughput_C7_new = format(IP_Throughput_C7, '.3f')
        else:
            self.IP_Throughput_C1_new = "N/A"
            IP_Throughput_C2_new = "N/A"
            IP_Throughput_C3_new = "N/A"
            IP_Throughput_C4_new = "N/A"
            IP_Throughput_C5_new = "N/A"
            IP_Throughput_C6_new = "N/A"
            IP_Throughput_C7_new = "N/A"



        Voice_Call = Max_Frame_Rate_C1 / Codec_Frame_rate
        Voice_Call_value = round(Voice_Call)

        if "Data" in self.Traffic_Type:
            self.Maximum_Theoretical_R_value = "N/A"
        else:
            if "G.711" in self.Codec_Type:
                self.Maximum_Theoretical_R_value = 85.9
            else:
                if "G.723" in self.Codec_Type:
                    self.Maximum_Theoretical_R_value = 72.9
                else:
                    if "G.729" in self.Codec_Type:
                        self.Maximum_Theoretical_R_value = 81.7
                    else:
                        self.Maximum_Theoretical_R_value = 93.2

        if "Data" in self.Traffic_Type:
            self.Estimated_MOS_Score = "N/A"
            self.Maximum_Bidirectional_Voice_Calls = "N/A"
        else:
            if (Voice_Call_value <= 1):
                Maximum_Bidirectional_Voice_Calls1 = self.Max_Frame_Rate_C1_round / Codec_Frame_rate
            elif (Voice_Call_value <= 2):
                Maximum_Bidirectional_Voice_Calls1 = Max_Frame_Rate_C2_round / Codec_Frame_rate
            elif (Voice_Call_value <= 5):
                Maximum_Bidirectional_Voice_Calls1 = Max_Frame_Rate_C3_round / Codec_Frame_rate

            elif (Voice_Call_value <= 10):
                Maximum_Bidirectional_Voice_Calls1 = Max_Frame_Rate_C4_round / Codec_Frame_rate
            elif (Voice_Call_value <= 20):
                Maximum_Bidirectional_Voice_Calls1 = Max_Frame_Rate_C5_round / Codec_Frame_rate
            elif (Voice_Call_value <= 50):
                Maximum_Bidirectional_Voice_Calls1 = Max_Frame_Rate_C6_round / Codec_Frame_rate
            else:
                Maximum_Bidirectional_Voice_Calls1 = Max_Frame_Rate_C7_round / Codec_Frame_rate
            self.Maximum_Bidirectional_Voice_Calls = round(Maximum_Bidirectional_Voice_Calls1, 2)
            if self.Maximum_Theoretical_R_value < 0:
                self.Estimated_MOS_Score = 1
            else:
                if self.Maximum_Theoretical_R_value > 100:
                    self.Estimated_MOS_Score = 4.5

                else:
                    Estimated_MOS_Score_1 = 1 + 0.035 * self.Maximum_Theoretical_R_value + self.Maximum_Theoretical_R_value * (
                                self.Maximum_Theoretical_R_value - 60) * (
                                                    100 - self.Maximum_Theoretical_R_value) * 7 * 0.000001
                    self.Estimated_MOS_Score = round(Estimated_MOS_Score_1, 2)



    def get_result(self):

        print("\n" + "******************Station : 11abgCalculator*****************************" + "\n")
        print("Theoretical Maximum Offered Load" + "\n")
        print("1 Client:")
        All_theoretical_output = {'Packet Interval(usec)': self.Client_1_new, 'Max Frame Rate(fps)': self.Max_Frame_Rate_C1_round,
                                  'Max. Offered Load (802.11)(Mb/s)': self.Max_Offered_Load_C1_new,
                                  'Offered Load Per 802.11 Client(Mb/s)': self.Offered_Load_Per_Client1_new,
                                  'Offered Load (802.3 Side)(Mb/s)': self.Offered_Load_C1_new,
                                  'IP Throughput (802.11 -> 802.3)(Mb/s)': self.IP_Throughput_C1_new}
        print(json.dumps(All_theoretical_output, indent=4))

        print("\n" + "Theroretical Voice Call Capacity" + "\n")

        All_theoretical_voice = {'Maximum Theoretical R-value': self.Maximum_Theoretical_R_value,
                                 'Estimated MOS Score': self.Estimated_MOS_Score,
                                 'Maximum Bidirectional Voice Calls(calls)': self.Maximum_Bidirectional_Voice_Calls}
        print(json.dumps(All_theoretical_voice, indent=4))


##Class to take all user input (802.11n Standard)

class n11_calculator(abg11_calculator):

    def __init__(self, Traffic_Type, Data_Voice_MCS, Channel_Bandwidth, Guard_Interval_value, Highest_Basic_str,
                 Encryption, QoS,
                 IP_Packets_MSDU_str, MAC_Frames_per_A_MPDU_str, BSS_Basic_Rate, MAC_MPDU_Size_Data_Traffic,
                 Codec_Type, PLCP, CWmin, RTS_CTS_Handshake, CTS_to_self,PHY_Bit_Rate=None,MAC_Frame_802_11=None,Basic_Rate_Set=None,Preamble=None,slot_name=None):
        super().__init__(Traffic_Type, PHY_Bit_Rate, Encryption, QoS, MAC_Frame_802_11, Basic_Rate_Set, Preamble,
                 slot_name, Codec_Type, RTS_CTS_Handshake, CTS_to_self)
        self.Data_Voice_MCS = Data_Voice_MCS
        self.Channel_Bandwidth = Channel_Bandwidth
        self.Guard_Interval_value = Guard_Interval_value
        self.Highest_Basic_str = Highest_Basic_str
        self.IP_Packets_MSDU_str = IP_Packets_MSDU_str
        self.MAC_Frames_per_A_MPDU_str = MAC_Frames_per_A_MPDU_str
        self.BSS_Basic_Rate = BSS_Basic_Rate
        self.MAC_MPDU_Size_Data_Traffic = MAC_MPDU_Size_Data_Traffic
        self.PLCP = PLCP
        self.CWmin = CWmin


    # This function is for calculate intermediate values and Theoretical values

    def calculate(self):
        global HT_data_temp
        global temp_value
        SIFS = 16.00
        DIFS = 34.00
        Slot_Time = 9.00
        Tsymbol_Control = 4.00
        # *********************************************Auxilliary  Data***********************************************
        Non_HT_Ref = ['6', '12', '18', '24', '36', '48', '54', '54', '6', '12', '18', '24', '36', '48', '54', '54', '6',
                      '12', '18', '24', '36', '48', '54', '54', '6', '12', '18', '24', '36', '48', '54', '54']
        HT_LTFs = ['0', '1', '3', '3']
        Ndbps_20MHz = ['26', '52', '78', '104', '156', '208', '234', '260']
        Ndbps_40MHz = ['54', '108', '162', '216', '324', '432', '486', '540']
        Nes = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
               '2', '2', '2', '1', '1', '1', '1', '2', '2', '2', '2', ]

        Data_Voice_MCS_int = int(self.Data_Voice_MCS)
        IP_Packets_MSDU = int(self.IP_Packets_MSDU_str)
        IP_Packets_MSDU_loc = IP_Packets_MSDU + 1
        Highest_Basic = int(self.Highest_Basic_str)

        i = 0
        while True:
            if Data_Voice_MCS_int == i:
                Non_HT = Non_HT_Ref[i]
                break
            i = i + 1

        Non_HT_value = int(Non_HT)

        if Non_HT_value >= 6:
            if "6" in self.BSS_Basic_Rate:
                Allowed_control6 = 6
            else:
                if (not (
                        "6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate or "18" in self.BSS_Basic_Rate or
                        "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    Allowed_control6 = 6
                else:
                    Allowed_control6 = 0
        else:
            Allowed_control6 = 0

        if Non_HT_value >= 9:
            if "9" in self.BSS_Basic_Rate:
                Allowed_control9 = 9
            else:
                if (not (
                        "6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate or "18" in self.BSS_Basic_Rate or
                        "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    Allowed_control9 = 6
                else:
                    Allowed_control9 = 0
        else:
            Allowed_control9 = 0

        if Non_HT_value >= 12:
            if "12" in self.BSS_Basic_Rate:
                Allowed_control12 = 12
            else:
                if (not (
                        "6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate or "18" in self.BSS_Basic_Rate or
                        "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    Allowed_control12 = 12
                else:
                    Allowed_control12 = 0
        else:
            Allowed_control12 = 0

        if Non_HT_value >= 18:
            if "18" in self.BSS_Basic_Rate:
                Allowed_control18 = 18
            else:
                if (not (
                        "6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate or "18" in self.BSS_Basic_Rate or
                        "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    Allowed_control18 = 12
                else:
                    Allowed_control18 = 0
        else:
            Allowed_control18 = 0

        if Non_HT_value >= 24:
            if "24" in self.BSS_Basic_Rate:
                Allowed_control24 = 24
            else:
                if (not (
                        "6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate or "18" in self.BSS_Basic_Rate or
                        "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    Allowed_control24 = 24
                else:
                    Allowed_control24 = 0
        else:
            Allowed_control24 = 0

        if Non_HT_value >= 36:
            if "36" in self.BSS_Basic_Rate:
                Allowed_control36 = 36
            else:
                if (not (
                        "6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate or "18" in self.BSS_Basic_Rate or
                        "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    Allowed_control36 = 24
                else:
                    Allowed_control36 = 0
        else:
            Allowed_control36 = 0

        if Non_HT_value >= 48:
            if "48" in self.BSS_Basic_Rate:
                Allowed_control48 = 48
            else:
                if (not (
                        "6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate or "18" in self.BSS_Basic_Rate or
                        "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    Allowed_control48 = 24
                else:
                    Allowed_control48 = 0
        else:
            Allowed_control48 = 0

        if Non_HT_value >= 54:
            if "54" in self.BSS_Basic_Rate:
                Allowed_control54 = 54
            else:
                if (not (
                        "6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate or "18" in self.BSS_Basic_Rate or
                        "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    Allowed_control54 = 24
                else:
                    Allowed_control54 = 0
        else:
            Allowed_control54 = 0

        # g24 QoS Hdr
        if "Yes" in self.QoS:
            QoS_1 = 1
        elif "No" in self.QoS:
            QoS_1 = 0
        if (QoS_1 == 1) or (IP_Packets_MSDU > 1):
            QoS_Hdr = 2
        else:
            QoS_Hdr = 0

        # g23 Encrypt Hdr

        if "None" in self.Encryption:
            Encrypt_Hdr = 0
        else:
            if "WEP" in self.Encryption:
                Encrypt_Hdr = 8
            elif "TKIP" in self.Encryption:
                Encrypt_Hdr = 20
            else:
                Encrypt_Hdr = 16
        # c36 Codec IP Packet Size

        if "G.711" in self.Codec_Type:
            Codec_IP_Packet_Size = 200
            Codec_Frame_Rate = 100

        else:
            if "G.723" in self.Codec_Type:
                Codec_IP_Packet_Size = 60
                Codec_Frame_Rate = 67

            else:
                if "G.729" in self.Codec_Type:
                    Codec_IP_Packet_Size = 60
                    Codec_Frame_Rate = 100

                else:
                    Codec_IP_Packet_Size = 0
                    Codec_Frame_Rate = 0

        # c17  MAC MPDU Size

        if "Data" in self.Traffic_Type:
            MAC_MPDU_Size = int(self.MAC_MPDU_Size_Data_Traffic)

        else:
            if ((IP_Packets_MSDU == 0)):
                MAC_MPDU_Size = (Codec_IP_Packet_Size + 28 + QoS_Hdr + Encrypt_Hdr + 8)

            else:
                MAC_MPDU_Size_1 = (Codec_IP_Packet_Size + 28 + QoS_Hdr + Encrypt_Hdr + 8 + (IP_Packets_MSDU_loc - 1) * (
                        14 + 3))
                MAC_MPDU_Size = int(MAC_MPDU_Size_1 / (IP_Packets_MSDU_loc - 1))

        # MSDU Size

        if IP_Packets_MSDU == 0:
            MSDU_final = MAC_MPDU_Size - 28 - QoS_Hdr - Encrypt_Hdr


        else:
            MSDU_1 = (MAC_MPDU_Size - 28 - QoS_Hdr - Encrypt_Hdr - (IP_Packets_MSDU) * (14 + 3))
            MSDU_final = MSDU_1 / IP_Packets_MSDU

        if MSDU_final < 0:
            msdu_str = str(MSDU_final)
            x = msdu_str.split(".")
            sec = len(x[0])
            if sec > 2:
                MSDU = int(MSDU_final) - 1
            else:
                MSDU = int(MSDU_final)
        else:
            MSDU = int(MSDU_final)

        if (MSDU - 8) < 20:
            IP_Packet_value = "N/A"
            ip_value = 0
        else:
            IP_Packet_value = MSDU - 8
            ip_value = 1

        if ip_value == 0:
            Ethernet_value = "N/A"
            eth_value = 0
        else:
            ip_1 = int(IP_Packet_value)
            Ethernet_value = max(ip_1 + 18, 64)
            eth_value = 1

        # HT-LTFs

        temp_value = int(Data_Voice_MCS_int / 8)

        def HT_value_func():
            if temp_value == 0:
                HT_data_temp = HT_LTFs[0]
            elif temp_value == 1:
                HT_data_temp = HT_LTFs[1]
            elif temp_value == 2:
                HT_data_temp = HT_LTFs[2]
            elif temp_value == 3:
                HT_data_temp = HT_LTFs[3]
            return HT_data_temp

        HT_data = HT_value_func()
        HT_data_1 = int(HT_data)

        # c20 Tppdu_fixed (HT Data Frames)

        if "Mixed" in self.PLCP:
            Tppdu_fixed_Data_Frame = float(36 + 4 * HT_data_1)
            PLCP_Configuration_int = 1
        elif "Greenfield" in self.PLCP:
            Tppdu_fixed_Data_Frame = float(24 + 4 * HT_data_1)
            PLCP_Configuration_int = 2

        # c21 Tppdu_fixed (HT Control Frames)

        Data_min = min(Data_Voice_MCS_int, Highest_Basic)
        temp_value = int(Data_min / 8) + 1
        HT_data_temp_1 = HT_value_func()
        HT_data_2 = int(HT_data_temp_1)

        if "Mixed" in self.PLCP:
            Tppdu_fixed_Control_Frames = float(36 + 4 * HT_data_2)

        elif "Greenfield" in self.PLCP:
            Tppdu_fixed_Control_Frames = float(24 + 4 * HT_data_2)

        # Non-HT Reference Rate
        # Offset calculation

        i = 0
        while True:
            if Data_Voice_MCS_int == i:
                Non_HT = Non_HT_Ref[i]
                Nes_data = Nes[i]
                break
            i = i + 1

        # PHY Bit Rate of Control Frames

        PHY_Bit_Rate_of_Control_Frames = max(Allowed_control6, Allowed_control9,
                                             Allowed_control12, Allowed_control18,
                                             Allowed_control24, Allowed_control36,
                                             Allowed_control48, Allowed_control54, 6)

        # Ndbps, data bits per symbol (Data)

        def Ndbps_fun():
            if Data_Voice_MCS_int == 0 or Data_Voice_MCS_int == 8 or Data_Voice_MCS_int == 16 or Data_Voice_MCS_int == 24:
                Ndbps_20 = Ndbps_20MHz[0]
                Ndbps_40 = Ndbps_40MHz[0]
            elif Data_Voice_MCS_int == 1 or Data_Voice_MCS_int == 9 or Data_Voice_MCS_int == 17 or Data_Voice_MCS_int == 25:
                Ndbps_20 = Ndbps_20MHz[1]
                Ndbps_40 = Ndbps_40MHz[1]
            elif Data_Voice_MCS_int == 2 or Data_Voice_MCS_int == 10 or Data_Voice_MCS_int == 18 or Data_Voice_MCS_int == 26:
                Ndbps_20 = Ndbps_20MHz[2]
                Ndbps_40 = Ndbps_40MHz[2]

            elif Data_Voice_MCS_int == 3 or Data_Voice_MCS_int == 11 or Data_Voice_MCS_int == 19 or Data_Voice_MCS_int == 27:
                Ndbps_20 = Ndbps_20MHz[3]
                Ndbps_40 = Ndbps_40MHz[3]
            elif Data_Voice_MCS_int == 4 or Data_Voice_MCS_int == 12 or Data_Voice_MCS_int == 20 or Data_Voice_MCS_int == 28:
                Ndbps_20 = Ndbps_20MHz[4]
                Ndbps_40 = Ndbps_40MHz[4]
            elif Data_Voice_MCS_int == 5 or Data_Voice_MCS_int == 13 or Data_Voice_MCS_int == 21 or Data_Voice_MCS_int == 29:
                Ndbps_20 = Ndbps_20MHz[5]
                Ndbps_40 = Ndbps_40MHz[5]
            elif Data_Voice_MCS_int == 6 or Data_Voice_MCS_int == 14 or Data_Voice_MCS_int == 22 or Data_Voice_MCS_int == 30:
                Ndbps_20 = Ndbps_20MHz[6]
                Ndbps_40 = Ndbps_40MHz[6]
            elif Data_Voice_MCS_int == 7 or Data_Voice_MCS_int == 15 or Data_Voice_MCS_int == 23 or Data_Voice_MCS_int == 31:
                Ndbps_20 = Ndbps_20MHz[7]
                Ndbps_40 = Ndbps_40MHz[7]
            Ndbps_20_int = int(Ndbps_20)
            Ndbps_40_int = int(Ndbps_40)
            return Ndbps_20_int, Ndbps_40_int

        if "20" in self.Channel_Bandwidth:

            if Data_Voice_MCS_int >= 0 and Data_Voice_MCS_int < 8:
                Ndbps_20_int, Ndbps_40_int = Ndbps_fun()
                data_bits = Ndbps_20_int * 1
            if Data_Voice_MCS_int >= 8 and Data_Voice_MCS_int < 16:
                Ndbps_20_int, Ndbps_40_int = Ndbps_fun()
                data_bits = Ndbps_20_int * 2
            if Data_Voice_MCS_int >= 16 and Data_Voice_MCS_int < 24:
                Ndbps_20_int, Ndbps_40_int = Ndbps_fun()
                data_bits = Ndbps_20_int * 3
            if Data_Voice_MCS_int >= 24 and Data_Voice_MCS_int < 32:
                Ndbps_20_int, Ndbps_40_int = Ndbps_fun()
                data_bits = Ndbps_20_int * 4


        elif "40" in self.Channel_Bandwidth:

            if Data_Voice_MCS_int >= 0 and Data_Voice_MCS_int < 8:
                Ndbps_20_int, Ndbps_40_int = Ndbps_fun()
                data_bits = Ndbps_40_int * 1
            if Data_Voice_MCS_int >= 8 and Data_Voice_MCS_int < 16:
                Ndbps_20_int, Ndbps_40_int = Ndbps_fun()
                data_bits = Ndbps_40_int * 2
            if Data_Voice_MCS_int >= 16 and Data_Voice_MCS_int < 24:
                Ndbps_20_int, Ndbps_40_int = Ndbps_fun()
                data_bits = Ndbps_40_int * 3
            if Data_Voice_MCS_int >= 24 and Data_Voice_MCS_int < 32:
                Ndbps_20_int, Ndbps_40_int = Ndbps_fun()
                data_bits = Ndbps_40_int * 4

        # Ndbps, data bits per symbol (Control)

        if PHY_Bit_Rate_of_Control_Frames < 7:
            if PHY_Bit_Rate_of_Control_Frames < 3:
                PHY = PHY_Bit_Rate_of_Control_Frames
            else:
                if PHY_Bit_Rate_of_Control_Frames == 3:
                    PHY = 5.5
                else:
                    if PHY_Bit_Rate_of_Control_Frames == 4:
                        PHY = 11
                    else:
                        if PHY_Bit_Rate_of_Control_Frames == 5:
                            PHY = 6
                        else:
                            if PHY_Bit_Rate_of_Control_Frames == 6:
                                PHY = 9
        else:
            if PHY_Bit_Rate_of_Control_Frames == 8:
                PHY = 18
            else:
                if PHY_Bit_Rate_of_Control_Frames == 9:
                    PHY = 24
                else:
                    if PHY_Bit_Rate_of_Control_Frames == 10:
                        PHY = 36
                    else:
                        if PHY_Bit_Rate_of_Control_Frames == 11:
                            PHY = 48
                        else:
                            PHY = 54
        Ndbps_data_bits_per_symbol_Control = PHY * 4
        MAC_Frames_per_A_MPDU = int(self.MAC_Frames_per_A_MPDU_str)

        # g22 A-MPDU Pad

        if ((MAC_Frames_per_A_MPDU == 0)):
            MPDU_Pad = int(0)

        else:
            x = int((MAC_MPDU_Size % 4))
            y = int((4 - x))
            MPDU_Pad = int((y % 4))

        # c26 Nbits, Bits per MAC PPDU

        MAC_Frames_per_A_MPDU_loc = MAC_Frames_per_A_MPDU + 1
        if (MAC_Frames_per_A_MPDU == 0):
            Nbits_Bits_per_MAC_PPDU = MAC_MPDU_Size * 8

        else:
            Nbits_Bits_per_MAC_PPDU = ((MAC_MPDU_Size + 4) * (MAC_Frames_per_A_MPDU_loc - 1) + MPDU_Pad * (
                    MAC_Frames_per_A_MPDU_loc - 2)) * 8

        # c27 Tsymbol(Data), Data Symbol Period

        if "400" in self.Guard_Interval_value:
            Guard_Interval_1 = 1
        elif "800" in self.Guard_Interval_value:
            Guard_Interval_1 = 0
        calculation = (((Data_Voice_MCS_int > 7 and PLCP_Configuration_int == 2) or PLCP_Configuration_int == 1))
        if (Guard_Interval_1 == 1) and calculation:
            Tsymbol_Data_Symbol_Period = 3.60

        else:
            Tsymbol_Data_Symbol_Period = 4

        Nes_data_int = int(Nes_data)

        # Ttxframe (DATA)

        if "40" in self.Channel_Bandwidth:
            offset = 6 * Nes_data_int
        else:
            offset = 6

        Ttxframe_1 = Tppdu_fixed_Data_Frame + int(
            (16 + offset + Nbits_Bits_per_MAC_PPDU + data_bits - 1) / data_bits) * Tsymbol_Data_Symbol_Period
        Ttxframe_2 = format(Ttxframe_1, '.2f')
        Ttxframe = float(Ttxframe_2)

        # c30 Ttxframe (Ack)

        Ttxframe_Ack = int(
            (22 + 14 * 8 + PHY_Bit_Rate_of_Control_Frames * 4 - 1) / (PHY_Bit_Rate_of_Control_Frames * 4)) * 4 + 20

        # c31 Ttxframe (Compressed BlockAck)

        Ttxframe_Compressed_BlockAck = int(
            (22 + 32 * 8 + PHY_Bit_Rate_of_Control_Frames * 4 - 1) / (PHY_Bit_Rate_of_Control_Frames * 4)) * 4 + 20

        # g20 Use BlockAck
        if (MAC_Frames_per_A_MPDU == 0):
            Use_BlockAck = False

        else:
            Use_BlockAck = True

        # c34 Ack Response Overhead
        if Use_BlockAck:
            Ack_Response_Overhead = 0

        else:
            Ack_Response_Overhead = SIFS + Ttxframe_Ack

        # c35 BlockAck Response Overhead

        if Use_BlockAck:
            BlockAck_Response_Overhead = SIFS + Ttxframe_Compressed_BlockAck

        else:
            BlockAck_Response_Overhead = 0
        CWmin_leave_alone_for_default = int(self.CWmin)
        MeanBackoff = CWmin_leave_alone_for_default * Slot_Time / 2

        # c32 RTS/CTS Handshake Overhead

        if "Yes" in self.RTS_CTS_Handshake:
            if "20" in self.Channel_Bandwidth:
                RTS_CTS_Handshake_Overhead = 2 * 20 + 4 * int((22 + (20 + 14) * 8 + 24 * 4 - 1) / (24 * 4)) + 2 * SIFS

            else:
                RTS_CTS_Handshake_Overhead = 2 * 20 + int(
                    (22 + (20 + 14) * 8 + 24 - 1) / 24) * Tsymbol_Control + 2 * SIFS

        else:
            RTS_CTS_Handshake_Overhead = 0

        # c33CTS-to-self Handshake Overhead

        if "Yes" in self.RTS_CTS_Handshake:
            CTS_to_self_Handshake_Overhead = 0

        else:
            if "Yes" in self.CTS_to_self:
                if "20" in self.Channel_Bandwidth:
                    CTS_to_self_Handshake_Overhead = 20 + 4 * int((22 + 14 * 8 + 24 * 4 - 1) / (24 * 4)) + SIFS

                else:
                    CTS_to_self_Handshake_Overhead = 20 + int((22 + 14 * 8 + 24 - 1) / 24) * Tsymbol_Control + SIFS

            else:
                CTS_to_self_Handshake_Overhead = 0

        # MAC PPDU Interval

        # MeanBackoff

        MAC_PPDU_Interval_1 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 1)
        self.Client_1_new = format(MAC_PPDU_Interval_1, '.2f')
        MAC_PPDU_Interval_2 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 2)
        Client_2_new = format(MAC_PPDU_Interval_2, '.2f')
        MAC_PPDU_Interval_3 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 5)
        Client_3_new = format(MAC_PPDU_Interval_3, '.2f')
        MAC_PPDU_Interval_4 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 10)
        Client_4_new = format(MAC_PPDU_Interval_4, '.2f')
        MAC_PPDU_Interval_5 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 20)
        Client_5_new = format(MAC_PPDU_Interval_5, '.2f')
        MAC_PPDU_Interval_6 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 50)
        Client_6_new = format(MAC_PPDU_Interval_6, '.2f')
        MAC_PPDU_Interval_7 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 100)
        Client_7_new = format(MAC_PPDU_Interval_7, '.3f')

        # Max PPDU Rate

        Max_PPDU_Rate_1 = 1000000 / MAC_PPDU_Interval_1
        self.Client_8_new = format(Max_PPDU_Rate_1, '.2f')
        Max_PPDU_Rate_2 = 1000000 / MAC_PPDU_Interval_2
        Client_9_new = format(Max_PPDU_Rate_2, '.2f')
        Max_PPDU_Rate_3 = 1000000 / MAC_PPDU_Interval_3
        Client_10_new = format(Max_PPDU_Rate_3, '.2f')
        Max_PPDU_Rate_4 = 1000000 / MAC_PPDU_Interval_4
        Client_11_new = format(Max_PPDU_Rate_4, '.2f')
        Max_PPDU_Rate_5 = 1000000 / MAC_PPDU_Interval_5
        Client_12_new = format(Max_PPDU_Rate_5, '.2f')
        Max_PPDU_Rate_6 = 1000000 / MAC_PPDU_Interval_6
        Client_13_new = format(Max_PPDU_Rate_6, '.2f')
        Max_PPDU_Rate_7 = 1000000 / MAC_PPDU_Interval_7
        Client_14_new = format(Max_PPDU_Rate_7, '.2f')

        # c44 Max_MAC_MPDU_Rate_1
        if (MAC_Frames_per_A_MPDU > 0):
            Max_MAC_MPDU_Rate_1 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_1
            Max_MAC_MPDU_Rate_2 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_2
            Max_MAC_MPDU_Rate_3 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_3
            Max_MAC_MPDU_Rate_4 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_4
            Max_MAC_MPDU_Rate_5 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_5
            Max_MAC_MPDU_Rate_6 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_6
            Max_MAC_MPDU_Rate_7 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_7
        else:
            Max_MAC_MPDU_Rate_1 = Max_PPDU_Rate_1
            Max_MAC_MPDU_Rate_2 = Max_PPDU_Rate_2
            Max_MAC_MPDU_Rate_3 = Max_PPDU_Rate_3
            Max_MAC_MPDU_Rate_4 = Max_PPDU_Rate_4
            Max_MAC_MPDU_Rate_5 = Max_PPDU_Rate_5
            Max_MAC_MPDU_Rate_6 = Max_PPDU_Rate_6
            Max_MAC_MPDU_Rate_7 = Max_PPDU_Rate_7

        self.Client_15_new = round(Max_MAC_MPDU_Rate_1)
        Client_16_new = round(Max_MAC_MPDU_Rate_2)
        Client_17_new = round(Max_MAC_MPDU_Rate_3)
        Client_18_new = round(Max_MAC_MPDU_Rate_4)
        Client_19_new = round(Max_MAC_MPDU_Rate_5)
        Client_20_new = round(Max_MAC_MPDU_Rate_6)
        Client_21_new = round(Max_MAC_MPDU_Rate_7)

        # Max MAC MSDU Rate

        if (IP_Packets_MSDU > 0):
            Max_MAC_MSDU_Rate_1 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_1
            Max_MAC_MSDU_Rate_2 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_2
            Max_MAC_MSDU_Rate_3 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_3
            Max_MAC_MSDU_Rate_4 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_4
            Max_MAC_MSDU_Rate_5 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_5
            Max_MAC_MSDU_Rate_6 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_6
            Max_MAC_MSDU_Rate_7 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_7

        else:
            Max_MAC_MSDU_Rate_1 = Max_MAC_MPDU_Rate_1
            Max_MAC_MSDU_Rate_2 = Max_MAC_MPDU_Rate_2
            Max_MAC_MSDU_Rate_3 = Max_MAC_MPDU_Rate_3
            Max_MAC_MSDU_Rate_4 = Max_MAC_MPDU_Rate_4
            Max_MAC_MSDU_Rate_5 = Max_MAC_MPDU_Rate_5
            Max_MAC_MSDU_Rate_6 = Max_MAC_MPDU_Rate_6
            Max_MAC_MSDU_Rate_7 = Max_MAC_MPDU_Rate_7

        self.Client_22_new = round(Max_MAC_MSDU_Rate_1)
        Client_23_new = round(Max_MAC_MSDU_Rate_2)
        Client_24_new = round(Max_MAC_MSDU_Rate_3)
        Client_25_new = round(Max_MAC_MSDU_Rate_4)
        Client_26_new = round(Max_MAC_MSDU_Rate_5)
        Client_27_new = round(Max_MAC_MSDU_Rate_6)
        Client_28_new = round(Max_MAC_MSDU_Rate_7)

        # Max. 802.11 MAC Frame Data Rate
        Max_802_11_MAC_Frame_Data_Rate_1 = Max_MAC_MPDU_Rate_1 * MAC_MPDU_Size * 8 / 1000000
        Max_802_11_MAC_Frame_Data_Rate_2 = Max_MAC_MPDU_Rate_2 * MAC_MPDU_Size * 8 / 1000000
        Max_802_11_MAC_Frame_Data_Rate_3 = Max_MAC_MPDU_Rate_3 * MAC_MPDU_Size * 8 / 1000000
        Max_802_11_MAC_Frame_Data_Rate_4 = Max_MAC_MPDU_Rate_4 * MAC_MPDU_Size * 8 / 1000000
        Max_802_11_MAC_Frame_Data_Rate_5 = Max_MAC_MPDU_Rate_5 * MAC_MPDU_Size * 8 / 1000000
        Max_802_11_MAC_Frame_Data_Rate_6 = Max_MAC_MPDU_Rate_6 * MAC_MPDU_Size * 8 / 1000000
        Max_802_11_MAC_Frame_Data_Rate_7 = Max_MAC_MPDU_Rate_7 * MAC_MPDU_Size * 8 / 1000000

        self.Client_29_new = format(Max_802_11_MAC_Frame_Data_Rate_1, '.3f')
        Client_30_new = format(Max_802_11_MAC_Frame_Data_Rate_2, '.3f')
        Client_31_new = format(Max_802_11_MAC_Frame_Data_Rate_3, '.3f')
        Client_32_new = format(Max_802_11_MAC_Frame_Data_Rate_4, '.3f')
        Client_33_new = format(Max_802_11_MAC_Frame_Data_Rate_5, '.3f')
        Client_34_new = format(Max_802_11_MAC_Frame_Data_Rate_6, '.3f')
        Client_35_new = format(Max_802_11_MAC_Frame_Data_Rate_7, '.3f')

        # Max. 802.11 MAC Payload Goodput

        Max_802_11_MAC_Payload_Goodput_1 = MSDU * 8 * Max_MAC_MSDU_Rate_1 / 1000000
        Max_802_11_MAC_Payload_Goodput_2 = MSDU * 8 * Max_MAC_MSDU_Rate_2 / 1000000
        Max_802_11_MAC_Payload_Goodput_3 = MSDU * 8 * Max_MAC_MSDU_Rate_3 / 1000000
        Max_802_11_MAC_Payload_Goodput_4 = MSDU * 8 * Max_MAC_MSDU_Rate_4 / 1000000
        Max_802_11_MAC_Payload_Goodput_5 = MSDU * 8 * Max_MAC_MSDU_Rate_5 / 1000000
        Max_802_11_MAC_Payload_Goodput_6 = MSDU * 8 * Max_MAC_MSDU_Rate_6 / 1000000
        Max_802_11_MAC_Payload_Goodput_7 = MSDU * 8 * Max_MAC_MSDU_Rate_7 / 1000000

        self.Client_36_new = format(Max_802_11_MAC_Payload_Goodput_1, '.3f')
        Client_37_new = format(Max_802_11_MAC_Payload_Goodput_2, '.3f')
        Client_38_new = format(Max_802_11_MAC_Payload_Goodput_3, '.3f')
        Client_39_new = format(Max_802_11_MAC_Payload_Goodput_4, '.3f')
        Client_40_new = format(Max_802_11_MAC_Payload_Goodput_5, '.3f')
        Client_41_new = format(Max_802_11_MAC_Payload_Goodput_6, '.3f')
        Client_42_new = format(Max_802_11_MAC_Payload_Goodput_7, '.3f')

        # MAC Goodput Per 802.11 Client

        MAC_Goodput_Per_802_11_Client_1 = Max_802_11_MAC_Payload_Goodput_1 / 1
        MAC_Goodput_Per_802_11_Client_2 = Max_802_11_MAC_Payload_Goodput_2 / 2
        MAC_Goodput_Per_802_11_Client_3 = Max_802_11_MAC_Payload_Goodput_3 / 5
        MAC_Goodput_Per_802_11_Client_4 = Max_802_11_MAC_Payload_Goodput_4 / 10
        MAC_Goodput_Per_802_11_Client_5 = Max_802_11_MAC_Payload_Goodput_5 / 20
        MAC_Goodput_Per_802_11_Client_6 = Max_802_11_MAC_Payload_Goodput_6 / 50
        MAC_Goodput_Per_802_11_Client_7 = Max_802_11_MAC_Payload_Goodput_7 / 100

        self.Client_43_new = format(MAC_Goodput_Per_802_11_Client_1, '.3f')
        Client_44_new = format(MAC_Goodput_Per_802_11_Client_2, '.3f')
        Client_45_new = format(MAC_Goodput_Per_802_11_Client_3, '.3f')
        Client_46_new = format(MAC_Goodput_Per_802_11_Client_4, '.3f')
        Client_47_new = format(MAC_Goodput_Per_802_11_Client_5, '.3f')
        Client_48_new = format(MAC_Goodput_Per_802_11_Client_6, '.3f')
        Client_49_new = format(MAC_Goodput_Per_802_11_Client_7, '.3f')

        # Offered Load (802.3 Side)

        # c49
        if eth_value != 0:

            Offered_Load_8023_Side_1 = Max_MAC_MSDU_Rate_1 * Ethernet_value * 8 / 1000000
            Offered_Load_8023_Side_2 = Max_MAC_MSDU_Rate_2 * Ethernet_value * 8 / 1000000
            Offered_Load_8023_Side_3 = Max_MAC_MSDU_Rate_3 * Ethernet_value * 8 / 1000000
            Offered_Load_8023_Side_4 = Max_MAC_MSDU_Rate_4 * Ethernet_value * 8 / 1000000
            Offered_Load_8023_Side_5 = Max_MAC_MSDU_Rate_5 * Ethernet_value * 8 / 1000000
            Offered_Load_8023_Side_6 = Max_MAC_MSDU_Rate_6 * Ethernet_value * 8 / 1000000
            Offered_Load_8023_Side_7 = Max_MAC_MSDU_Rate_7 * Ethernet_value * 8 / 1000000
            self.Client_50_new = format(Offered_Load_8023_Side_1, '.3f')
            Client_51_new = format(Offered_Load_8023_Side_2, '.3f')
            Client_52_new = format(Offered_Load_8023_Side_3, '.3f')
            Client_53_new = format(Offered_Load_8023_Side_4, '.3f')
            Client_54_new = format(Offered_Load_8023_Side_5, '.3f')
            Client_55_new = format(Offered_Load_8023_Side_6, '.3f')
            Client_56_new = format(Offered_Load_8023_Side_7, '.3f')

        else:
            self.Client_50_new = "N/A"
            Client_51_new = "N/A"
            Client_52_new = "N/A"
            Client_53_new = "N/A"
            Client_54_new = "N/A"
            Client_55_new = "N/A"
            Client_56_new = "N/A"

        IP_Packet_value_str = str(IP_Packet_value)
        if "N/A" not in IP_Packet_value_str:
            IP_Goodput_802_11_8023_1 = Max_MAC_MSDU_Rate_1 * ip_1 * 8 / 1000000
            IP_Goodput_802_11_8023_2 = Max_MAC_MSDU_Rate_2 * ip_1 * 8 / 1000000
            IP_Goodput_802_11_8023_3 = Max_MAC_MSDU_Rate_3 * ip_1 * 8 / 1000000
            IP_Goodput_802_11_8023_4 = Max_MAC_MSDU_Rate_4 * ip_1 * 8 / 1000000
            IP_Goodput_802_11_8023_5 = Max_MAC_MSDU_Rate_5 * ip_1 * 8 / 1000000
            IP_Goodput_802_11_8023_6 = Max_MAC_MSDU_Rate_6 * ip_1 * 8 / 1000000
            IP_Goodput_802_11_8023_7 = Max_MAC_MSDU_Rate_7 * ip_1 * 8 / 1000000
            self.Client_57_new = format(IP_Goodput_802_11_8023_1, '.3f')
            Client_58_new = format(IP_Goodput_802_11_8023_2, '.3f')
            Client_59_new = format(IP_Goodput_802_11_8023_3, '.3f')
            Client_60_new = format(IP_Goodput_802_11_8023_4, '.3f')
            Client_61_new = format(IP_Goodput_802_11_8023_5, '.3f')
            Client_62_new = format(IP_Goodput_802_11_8023_6, '.3f')
            Client_63_new = format(IP_Goodput_802_11_8023_7, '.3f')

        else:
            self.Client_57_new = "N/A"
            Client_58_new = "N/A"
            Client_59_new = "N/A"
            Client_60_new = "N/A"
            Client_61_new = "N/A"
            Client_62_new = "N/A"
            Client_63_new = "N/A"

        # Theoretical Voice Call Capacity

        # c53
        if "Data" in self.Traffic_Type:
            self.Maximum_Theoretical_R_value = "N/A"
            self.Estimated_MOS_Score = "N/A"
        else:
            if "G.711" in self.Codec_Type:
                self.Maximum_Theoretical_R_value = 85.9
            else:
                if "G.723" in self.Codec_Type:
                    self.Maximum_Theoretical_R_value = 72.9
                else:
                    if "G.729" in self.Codec_Type:
                        self.Maximum_Theoretical_R_value = 81.7
                    else:
                        self.Maximum_Theoretical_R_value = 93.2

            if self.Maximum_Theoretical_R_value < 0:
                self.Estimated_MOS_Score = 1
            else:
                if self.Maximum_Theoretical_R_value > 100:
                    self.Estimated_MOS_Score = 4.5
                else:
                    self.Estimated_MOS_Score_1 = (
                            1 + 0.035 * self.Maximum_Theoretical_R_value + self.Maximum_Theoretical_R_value * (
                            self.Maximum_Theoretical_R_value - 60) * (
                                    100 - self.Maximum_Theoretical_R_value) * 7 * 0.000001)
                    self.Estimated_MOS_Score = format(self.Estimated_MOS_Score_1, '.2f')

        # Voice_Call_Range
        try:
            Voice_Call_Range = round(Max_PPDU_Rate_1 / Codec_Frame_Rate)

            # c55 Maximum Bidirectional Voice Calls
            if Voice_Call_Range <= 1:
                Maximum_Bidirectional = Max_MAC_MSDU_Rate_1 / Codec_Frame_Rate

            else:
                if Voice_Call_Range <= 2:
                    Maximum_Bidirectional = Max_MAC_MSDU_Rate_2 / Codec_Frame_Rate

                else:
                    if Voice_Call_Range <= 5:
                        Maximum_Bidirectional = Max_MAC_MSDU_Rate_3 / Codec_Frame_Rate

                    else:
                        if Voice_Call_Range <= 10:
                            Maximum_Bidirectional = Max_MAC_MSDU_Rate_4 / Codec_Frame_Rate

                        else:
                            if Voice_Call_Range <= 20:
                                Maximum_Bidirectional = Max_MAC_MSDU_Rate_5 / Codec_Frame_Rate

                            else:
                                if Voice_Call_Range <= 50:
                                    Maximum_Bidirectional = Max_MAC_MSDU_Rate_6 / Codec_Frame_Rate

                                else:

                                    Maximum_Bidirectional = Max_MAC_MSDU_Rate_7 / Codec_Frame_Rate
        except ZeroDivisionError:
            pass

        if "Data" in self.Traffic_Type:
            self.Maximum_Bidirectional_Voice_Calls = "N/A"
        else:
            self.Maximum_Bidirectional_Voice_Calls = round(Maximum_Bidirectional, 2)



    def get_result(self):

        print("\n" + "******************Station : 11nCalculator*****************************" + "\n")
        print("Theoretical Maximum Offered Load" + "\n")
        print("1 Client:")
        All_theoretical_output = {'MAC PPDU Interval(usec)': self.Client_1_new,
                                   'Max PPDU Rate(fps)': self.Client_8_new,
                                  'Max MAC MPDU Rate': self.Client_15_new,
                                  'Max MAC MSDU Rate': self.Client_22_new,
                                  'Max. 802.11 MAC Frame Data Rate(Mb/s)': self.Client_29_new,
                                  'Max. 802.11 MAC Payload Goodput(Mb/s)': self.Client_36_new,
                                  'MAC Goodput Per 802.11 Client(Mb/s)': self.Client_43_new,
                                  'Offered Load (802.3 Side)(Mb/s)': self.Client_50_new,
                                  'IP Goodput (802.11 -> 802.3)(Mb/s)': self.Client_57_new}
        print(json.dumps(All_theoretical_output, indent=4))

        print("\n" + "Theroretical Voice Call Capacity" + "\n")

        All_theoretical_voice = {'Maximum Theoretical R-value': self.Maximum_Theoretical_R_value,
                                 'Estimated MOS Score': self.Estimated_MOS_Score,
                                 'Maximum Bidirectional Voice Calls(calls)': self.Maximum_Bidirectional_Voice_Calls}
        print(json.dumps(All_theoretical_voice, indent=4))


##Class to take all user input (802.11ac Standard)

class ac11_calculator(n11_calculator):



    def __init__(self, Traffic_Type, Data_Voice_MCS, spatial, Channel_Bandwidth, Guard_Interval_value,
                 Highest_Basic_str, Encryption, QoS,IP_Packets_MSDU_str, MAC_Frames_per_A_MPDU_str, BSS_Basic_Rate, MAC_MPDU_Size_Data_Traffic,
                 Codec_Type, CWmin, RTS_CTS,PLCP = None,RTS_CTS_Handshake=None,CTS_to_self=None):
        super().__init__(Traffic_Type, Data_Voice_MCS, Channel_Bandwidth, Guard_Interval_value, Highest_Basic_str,
                 Encryption, QoS,
                 IP_Packets_MSDU_str, MAC_Frames_per_A_MPDU_str, BSS_Basic_Rate, MAC_MPDU_Size_Data_Traffic,
                 Codec_Type, PLCP, CWmin, RTS_CTS_Handshake, CTS_to_self)

        self.spatial = spatial
        self.RTS_CTS = RTS_CTS


    # This function is for calculate intermediate values and Theoretical values

    def calculate(self):

        SIFS = 16.00
        DIFS = 34.00
        Slot_Time = 9.00
        Tsymbol_control_Symbol_Period = 4.00
        Codec_IP_Packet_Size = 200
        Codec_Frame_Rate = 100
        # ********************Auxilliary data****************************

        HT_LTFs = ['1', '2', '4', '4']
        Ndbps_20MHz = ['26', '52', '78', '104', '156', '208', '234', '260', '312', '1040']
        Ndbps_40MHz = ['54', '108', '162', '216', '324', '432', '486', '540', '648', '720']
        Ndbps_80MHz = ['117', '234', '351', '468', '702', '936', '1053', '1170', '1404', '1560']
        Non_HT_Ref = ['6', '12', '18', '24', '36', '48', '54', '54', '54', '54']
        Nes1 = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                '1', '1', '1', '1', '1', '1', '1', '1', '1']
        Nes2 = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                '2', '2', '2', '1', '1', '1', '2', '2', '2']
        Nes3 = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                '2', '2', '2', '1', '2', '2', '2', '2', '3']
        Nes4 = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '2', '1',
                '1', '1', '1', '2', '2', '2', '3', '3', '3']

        Data_Voice_MCS_int = int(self.Data_Voice_MCS)
        CWmin_leave_alone_for_default = int(self.CWmin)
        spatial_int = int(self.spatial)
        MAC_Frames_per_A_MPDU = int(self.MAC_Frames_per_A_MPDU_str)

        i = 0
        while True:
            if Data_Voice_MCS_int == i:
                Non_HT = Non_HT_Ref[i]
                break
            i = i + 1

        Non_HT_value = int(Non_HT)

        if Non_HT_value >= 6:
            if "6" in self.BSS_Basic_Rate:
                allowed_control6 = 6
            else:
                if (not ("6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate
                         or "18" in self.BSS_Basic_Rate or "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or
                         "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    allowed_control6 = 6
                else:
                    allowed_control6 = 0
        else:
            allowed_control6 = 0

        if Non_HT_value >= 9:
            if "9" in self.BSS_Basic_Rate:
                allowed_control9 = 9
            else:
                if (not ("6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate
                         or "18" in self.BSS_Basic_Rate or "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or
                         "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    allowed_control9 = 6
                else:
                    allowed_control9 = 0
        else:
            allowed_control9 = 0

        if Non_HT_value >= 12:
            if "12" in self.BSS_Basic_Rate:
                allowed_control12 = 12
            else:
                if (not ("6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate
                         or "18" in self.BSS_Basic_Rate or "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or
                         "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    allowed_control12 = 12
                else:
                    allowed_control12 = 0
        else:
            allowed_control12 = 0

        if Non_HT_value >= 18:
            if "18" in self.BSS_Basic_Rate:
                allowed_control18 = 18
            else:
                if (not ("6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate
                         or "18" in self.BSS_Basic_Rate or "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or
                         "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    allowed_control18 = 12
                else:
                    allowed_control18 = 0
        else:
            allowed_control18 = 0

        if Non_HT_value >= 24:
            if "24" in self.BSS_Basic_Rate:
                allowed_control24 = 24
            else:
                if (not ("6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate
                         or "18" in self.BSS_Basic_Rate or "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or
                         "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    allowed_control24 = 24
                else:
                    allowed_control24 = 0
        else:
            allowed_control24 = 0

        if Non_HT_value >= 36:
            if "36" in self.BSS_Basic_Rate:
                allowed_control36 = 36
            else:
                if (not ("6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate
                         or "18" in self.BSS_Basic_Rate or "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or
                         "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    allowed_control36 = 24
                else:
                    allowed_control36 = 0
        else:
            allowed_control36 = 0

        if Non_HT_value >= 48:
            if "48" in self.BSS_Basic_Rate:
                allowed_control48 = 48
            else:
                if (not ("6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate
                         or "18" in self.BSS_Basic_Rate or "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or
                         "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    allowed_control48 = 24
                else:
                    allowed_control48 = 0
        else:
            allowed_control48 = 0

        if Non_HT_value >= 54:
            if "54" in self.BSS_Basic_Rate:
                allowed_control54 = 54
            else:
                if (not ("6" in self.BSS_Basic_Rate or "9" in self.BSS_Basic_Rate or "12" in self.BSS_Basic_Rate
                         or "18" in self.BSS_Basic_Rate or "24" in self.BSS_Basic_Rate or "36" in self.BSS_Basic_Rate or
                         "48" in self.BSS_Basic_Rate or "54" in self.BSS_Basic_Rate)):
                    allowed_control54 = 24
                else:
                    allowed_control54 = 0
        else:
            allowed_control54 = 0

        MeanBackoff = CWmin_leave_alone_for_default * Slot_Time / 2

        IP_Packets_MSDU = int(self.IP_Packets_MSDU_str)
        if "Mixed" in self.Codec_Type:
            plcp = 1
        elif "Greenfield" in self.Codec_Type:
            plcp = 2

        RTS_CTS_Handshake = 1
        if "No" in self.RTS_CTS:
            CTS_to_self = 1
        elif "Yes" in self.RTS_CTS:
            CTS_to_self = 2

        # g24 QoS Hdr

        if "Yes" in self.QoS:
            QoS_1 = 1
        elif "No" in self.QoS:
            QoS_1 = 0
        if (QoS_1 == 1) or (IP_Packets_MSDU > 1):
            QoS_Hdr = 2

        else:
            QoS_Hdr = 0

        # g23 Encrypt Hdr

        if "None" in self.Encryption:
            Encrypt_Hdr = 0

        else:
            if "WEP" in self.Encryption:
                Encrypt_Hdr = 8

            elif "TKIP" in self.Encryption:
                Encrypt_Hdr = 20

            else:
                Encrypt_Hdr = 16

        # c18 MAC MPDU Size

        IP_Packets_MSDU_loc = IP_Packets_MSDU + 1

        if "Data" in self.Traffic_Type:
            MAC_MPDU_Size = int(self.MAC_MPDU_Size_Data_Traffic)

        else:
            if (IP_Packets_MSDU == 0):
                MAC_MPDU_Size = (Codec_IP_Packet_Size + 28 + QoS_Hdr + Encrypt_Hdr + 8)

            else:
                MAC_MPDU_Size_1 = (
                        Codec_IP_Packet_Size + 28 + QoS_Hdr + Encrypt_Hdr + 8 + (IP_Packets_MSDU_loc - 1) * (
                        14 + 3))
                MAC_MPDU_Size = int(MAC_MPDU_Size_1 / (IP_Packets_MSDU_loc - 1))

        # MSDU Size

        if IP_Packets_MSDU == 0:
            MSDU_final = MAC_MPDU_Size - 28 - QoS_Hdr - Encrypt_Hdr


        else:
            MSDU_1 = (MAC_MPDU_Size - 28 - QoS_Hdr - Encrypt_Hdr - (IP_Packets_MSDU) * (14 + 3))
            MSDU_final = (int(MSDU_1 / (IP_Packets_MSDU)))
        if MSDU_final < 0:
            MSDU = MSDU_final - 1
        else:
            MSDU = MSDU_final

        if (MSDU - 8) < 20:
            IP_Packet_value = "N/A"
            ip_value = 0
        else:
            IP_Packet_value = MSDU - 8
            ip_value = 1

        if ip_value == 0:
            Ethernet_value = "N/A"
            eth_value = 0
        else:
            ip_1 = int(IP_Packet_value)
            Ethernet_value = max(ip_1 + 18, 64)
            eth_value = 1

        i = 1
        while True:
            if int(spatial_int) == i:
                offset_str = HT_LTFs[i - 1]
                break
            i = i + 1
        offset = int(offset_str)
        Tppdu_fixed = 36 + offset * 4

        # Tppdu_fixed (HT Control Frames)

        offset_str_1 = HT_LTFs[0]
        offset_1 = int(offset_str_1)

        Tppdu_fixed_control = 36 + offset_1 * 4

        # c23 VHT Data Rate
        # Ndbps, data bits per symbol (Data)
        # offset
        j = 0
        while True:
            if Data_Voice_MCS_int == j:
                if "20" in self.Channel_Bandwidth:
                    Ndbps_str = Ndbps_20MHz[j]
                    break
                elif "40" in self.Channel_Bandwidth:
                    Ndbps_str = Ndbps_40MHz[j]
                    break
                elif "80" in self.Channel_Bandwidth:
                    Ndbps_str = Ndbps_80MHz[j]
                    break
            j = j + 1
        Ndbps = int(Ndbps_str)

        Ndbps_bits_per_symbol_Data = Ndbps * spatial_int

        # c27 Tsymbol(Data), Data Symbol Period
        if "400" in self.Guard_Interval_value:
            Guard_Interval_1 = 1
        elif "800" in self.Guard_Interval_value:
            Guard_Interval_1 = 0

        calculation = (((Data_Voice_MCS_int > 7 and plcp == 2) or plcp == 1))

        if (Guard_Interval_1 == 1) and calculation:
            Tsymbol_Data_Symbol_Period = 3.60


        else:
            Tsymbol_Data_Symbol_Period = 4

        VHT_Data_Rate = Ndbps_bits_per_symbol_Data / Tsymbol_Data_Symbol_Period

        # Non-HT Reference Rate
        k = 0
        while True:
            if Data_Voice_MCS_int == k:
                Non_HT = Non_HT_Ref[k]
                break
            k = k + 1

        Non_HT_value = int(Non_HT)

        # PHY Bit Rate of Control Frames

        PHY_Bit_Rate_of_Control_Frames = max(allowed_control6, allowed_control9,
                                             allowed_control12, allowed_control18,
                                             allowed_control24, allowed_control36,
                                             allowed_control48, allowed_control54, 6)

        # c27 Ndbps, data bits per symbol (Control)

        if PHY_Bit_Rate_of_Control_Frames < 7:
            if PHY_Bit_Rate_of_Control_Frames < 3:
                PHY = PHY_Bit_Rate_of_Control_Frames
            else:
                if PHY_Bit_Rate_of_Control_Frames == 3:
                    PHY = 5.5
                else:
                    if PHY_Bit_Rate_of_Control_Frames == 4:
                        PHY = 11
                    else:
                        if PHY_Bit_Rate_of_Control_Frames == 5:
                            PHY = 6
                        else:
                            if PHY_Bit_Rate_of_Control_Frames == 6:
                                PHY = 9
        else:
            if PHY_Bit_Rate_of_Control_Frames == 8:
                PHY = 18
            else:
                if PHY_Bit_Rate_of_Control_Frames == 9:
                    PHY = 24
                else:
                    if PHY_Bit_Rate_of_Control_Frames == 10:
                        PHY = 36
                    else:
                        if PHY_Bit_Rate_of_Control_Frames == 11:
                            PHY = 48
                        else:
                            PHY = 54
        Ndbps_bits_per_symbol_Control = PHY * 4

        # Nbits, Bits per MAC PPDU
        # A-MPDU Pad

        if ((MAC_Frames_per_A_MPDU == 0)):
            MPDU_Pad = int(0)

        else:
            x = int((MAC_MPDU_Size % 4))
            y = int((4 - x))
            MPDU_Pad = int((y % 4))

        MAC_Frames_per_A_MPDU_loc = MAC_Frames_per_A_MPDU + 1
        if (MAC_Frames_per_A_MPDU == 0):
            Nbits_Bits_per_MAC_PPDU = MAC_MPDU_Size * 8

        else:
            Nbits_Bits_per_MAC_PPDU = ((MAC_MPDU_Size + 4) * (MAC_Frames_per_A_MPDU_loc - 1) + MPDU_Pad * (
                    MAC_Frames_per_A_MPDU_loc - 2)) * 8

        # Nes, Number of BCC encoders

        l = 0
        while True:
            if Data_Voice_MCS_int == l:
                if "20" in self.Channel_Bandwidth:
                    Nes = 0 * 10 + Data_Voice_MCS_int
                elif "40" in self.Channel_Bandwidth:
                    Nes = 1 * 10 + Data_Voice_MCS_int
                elif "80" in self.Channel_Bandwidth:
                    Nes = 2 * 10 + Data_Voice_MCS_int

                if spatial_int == 1:
                    Nes_str = Nes1[Nes]
                    break
                elif spatial_int == 2:
                    Nes_str = Nes2[Nes]
                    break
                elif spatial_int == 3:
                    Nes_str = Nes3[Nes]
                    break
                elif spatial_int == 4:
                    Nes_str = Nes4[Nes]
                    break
            l = l + 1

        Nes_int = int(Nes_str)

        # Ttxframe (DATA)

        Ttxframe = Tppdu_fixed + int((16 + 6 * Nes_int + Nbits_Bits_per_MAC_PPDU + Ndbps_bits_per_symbol_Data - 1)
                                     / Ndbps_bits_per_symbol_Data) * Tsymbol_Data_Symbol_Period

        Ttxframe_Ack = int(
            (22 + 14 * 8 + PHY_Bit_Rate_of_Control_Frames * 4 - 1) / (PHY_Bit_Rate_of_Control_Frames * 4)) * 4 + 20

        # c34 Ttxframe (Compressed BlockAck)

        Ttxframe_Compressed_BlockAck = int((22 + 32 * 8 + PHY_Bit_Rate_of_Control_Frames * 4 - 1)
                                           / (PHY_Bit_Rate_of_Control_Frames * 4)) * 4 + 20

        # c35 RTS/CTS Handshake Overhead

        if RTS_CTS_Handshake == 2:
            if "20" in self.Channel_Bandwidth:
                RTS_CTS_Handshake_Overhead = 2 * 20 + 4 * int(
                    (22 + (20 + 14) * 8 + 24 * 4 - 1) / (24 * 4)) + 2 * SIFS
            else:
                RTS_CTS_Handshake_Overhead = 2 * 20 + int(
                    (22 + (20 + 14) * 8 + 24 - 1) / 24) * Tsymbol_control_Symbol_Period + 2 * SIFS
        else:
            RTS_CTS_Handshake_Overhead = 0

        # c36 CTS-to-self Handshake Overhead

        if RTS_CTS_Handshake == 2:
            CTS_to_self_Handshake_Overhead = 0
        else:
            if CTS_to_self == 2:
                if "20" in self.Channel_Bandwidth:
                    CTS_to_self_Handshake_Overhead = 20 + 4 * int((22 + 14 * 8 + 24 * 4 - 1) / (24 * 4)) + SIFS
                else:
                    CTS_to_self_Handshake_Overhead = 20 + int(
                        (22 + 14 * 8 + 24 - 1) / 24) * Tsymbol_control_Symbol_Period + SIFS
            else:
                CTS_to_self_Handshake_Overhead = 0

        # c37 Ack Response Overhead
        # g20 Use BlockAck

        if (MAC_Frames_per_A_MPDU == 0):
            Use_BlockAck = False
        else:
            Use_BlockAck = True

        if Use_BlockAck:
            Ack_Response_Overhead = 0
        else:
            Ack_Response_Overhead = SIFS + Ttxframe_Ack

        # c38BlockAck Response Overhead

        if Use_BlockAck:
            BlockAck_Response_Overhead = SIFS + Ttxframe_Compressed_BlockAck
        else:
            BlockAck_Response_Overhead = 0

        # c42 MAC PPDU Interval

        MAC_PPDU_Interval_1 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 1)
        self.Client_1_new = format(MAC_PPDU_Interval_1, '.2f')
        MAC_PPDU_Interval_2 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 2)
        Client_2_new = format(MAC_PPDU_Interval_2, '.2f')

        MAC_PPDU_Interval_3 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 5)
        Client_3_new = format(MAC_PPDU_Interval_3, '.2f')

        MAC_PPDU_Interval_4 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 10)
        Client_4_new = format(MAC_PPDU_Interval_4, '.2f')
        MAC_PPDU_Interval_5 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 20)
        Client_5_new = format(MAC_PPDU_Interval_5, '.2f')
        MAC_PPDU_Interval_6 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 50)
        Client_6_new = format(MAC_PPDU_Interval_6, '.2f')
        MAC_PPDU_Interval_7 = RTS_CTS_Handshake_Overhead + CTS_to_self_Handshake_Overhead + Ttxframe + Ack_Response_Overhead + BlockAck_Response_Overhead + DIFS + (
                MeanBackoff / 100)
        Client_7_new = format(MAC_PPDU_Interval_7, '.3f')

        # Max PPDU Rate

        Max_PPDU_Rate_1 = 1000000 / MAC_PPDU_Interval_1
        self.Client_8_new = format(Max_PPDU_Rate_1, '.2f')
        Max_PPDU_Rate_2 = 1000000 / MAC_PPDU_Interval_2
        Client_9_new = format(Max_PPDU_Rate_2, '.2f')
        Max_PPDU_Rate_3 = 1000000 / MAC_PPDU_Interval_3
        Client_10_new = format(Max_PPDU_Rate_3, '.2f')
        Max_PPDU_Rate_4 = 1000000 / MAC_PPDU_Interval_4
        Client_11_new = format(Max_PPDU_Rate_4, '.2f')
        Max_PPDU_Rate_5 = 1000000 / MAC_PPDU_Interval_5
        Client_12_new = format(Max_PPDU_Rate_5, '.2f')
        Max_PPDU_Rate_6 = 1000000 / MAC_PPDU_Interval_6
        Client_13_new = format(Max_PPDU_Rate_6, '.2f')
        Max_PPDU_Rate_7 = 1000000 / MAC_PPDU_Interval_7
        Client_14_new = format(Max_PPDU_Rate_7, '.2f')

        # c44 Max_MAC_MPDU_Rate_1

        if (MAC_Frames_per_A_MPDU > 0):
            Max_MAC_MPDU_Rate_1 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_1
            Max_MAC_MPDU_Rate_2 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_2
            Max_MAC_MPDU_Rate_3 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_3
            Max_MAC_MPDU_Rate_4 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_4
            Max_MAC_MPDU_Rate_5 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_5
            Max_MAC_MPDU_Rate_6 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_6
            Max_MAC_MPDU_Rate_7 = (MAC_Frames_per_A_MPDU) * Max_PPDU_Rate_7
        else:
            Max_MAC_MPDU_Rate_1 = Max_PPDU_Rate_1
            Max_MAC_MPDU_Rate_2 = Max_PPDU_Rate_2
            Max_MAC_MPDU_Rate_3 = Max_PPDU_Rate_3
            Max_MAC_MPDU_Rate_4 = Max_PPDU_Rate_4
            Max_MAC_MPDU_Rate_5 = Max_PPDU_Rate_5
            Max_MAC_MPDU_Rate_6 = Max_PPDU_Rate_6
            Max_MAC_MPDU_Rate_7 = Max_PPDU_Rate_7

        self.Client_15_new = round(Max_MAC_MPDU_Rate_1)
        Client_16_new = round(Max_MAC_MPDU_Rate_2)
        Client_17_new = round(Max_MAC_MPDU_Rate_3)
        Client_18_new = round(Max_MAC_MPDU_Rate_4)
        Client_19_new = round(Max_MAC_MPDU_Rate_5)
        Client_20_new = round(Max_MAC_MPDU_Rate_6)
        Client_21_new = round(Max_MAC_MPDU_Rate_7)

        # Max MAC MSDU Rate

        if (IP_Packets_MSDU > 0):
            Max_MAC_MSDU_Rate_1 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_1
            Max_MAC_MSDU_Rate_2 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_2
            Max_MAC_MSDU_Rate_3 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_3
            Max_MAC_MSDU_Rate_4 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_4
            Max_MAC_MSDU_Rate_5 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_5
            Max_MAC_MSDU_Rate_6 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_6
            Max_MAC_MSDU_Rate_7 = (IP_Packets_MSDU) * Max_MAC_MPDU_Rate_7

        else:
            Max_MAC_MSDU_Rate_1 = Max_MAC_MPDU_Rate_1
            Max_MAC_MSDU_Rate_2 = Max_MAC_MPDU_Rate_2
            Max_MAC_MSDU_Rate_3 = Max_MAC_MPDU_Rate_3
            Max_MAC_MSDU_Rate_4 = Max_MAC_MPDU_Rate_4
            Max_MAC_MSDU_Rate_5 = Max_MAC_MPDU_Rate_5
            Max_MAC_MSDU_Rate_6 = Max_MAC_MPDU_Rate_6
            Max_MAC_MSDU_Rate_7 = Max_MAC_MPDU_Rate_7

        self.Client_22_new = round(Max_MAC_MSDU_Rate_1)
        Client_23_new = round(Max_MAC_MSDU_Rate_2)
        Client_24_new = round(Max_MAC_MSDU_Rate_3)
        Client_25_new = round(Max_MAC_MSDU_Rate_4)
        Client_26_new = round(Max_MAC_MSDU_Rate_5)
        Client_27_new = round(Max_MAC_MSDU_Rate_6)
        Client_28_new = round(Max_MAC_MSDU_Rate_7)

        # Max. 802.11 MAC Frame Data Rate

        Max_802_11_MAC_Frame_Data_Rate_1 = Max_MAC_MPDU_Rate_1 * MAC_MPDU_Size * 8 / 1000000
        Max_802_11_MAC_Frame_Data_Rate_2 = Max_MAC_MPDU_Rate_2 * MAC_MPDU_Size * 8 / 1000000
        Max_802_11_MAC_Frame_Data_Rate_3 = Max_MAC_MPDU_Rate_3 * MAC_MPDU_Size * 8 / 1000000
        Max_802_11_MAC_Frame_Data_Rate_4 = Max_MAC_MPDU_Rate_4 * MAC_MPDU_Size * 8 / 1000000
        Max_802_11_MAC_Frame_Data_Rate_5 = Max_MAC_MPDU_Rate_5 * MAC_MPDU_Size * 8 / 1000000
        Max_802_11_MAC_Frame_Data_Rate_6 = Max_MAC_MPDU_Rate_6 * MAC_MPDU_Size * 8 / 1000000
        Max_802_11_MAC_Frame_Data_Rate_7 = Max_MAC_MPDU_Rate_7 * MAC_MPDU_Size * 8 / 1000000

        self.Client_29_new = format(Max_802_11_MAC_Frame_Data_Rate_1, '.3f')
        Client_30_new = format(Max_802_11_MAC_Frame_Data_Rate_2, '.3f')
        Client_31_new = format(Max_802_11_MAC_Frame_Data_Rate_3, '.3f')
        Client_32_new = format(Max_802_11_MAC_Frame_Data_Rate_4, '.3f')
        Client_33_new = format(Max_802_11_MAC_Frame_Data_Rate_5, '.3f')
        Client_34_new = format(Max_802_11_MAC_Frame_Data_Rate_6, '.3f')
        Client_35_new = format(Max_802_11_MAC_Frame_Data_Rate_7, '.3f')

        # Max. 802.11 MAC Payload Goodput

        Max_802_11_MAC_Payload_Goodput_1 = MSDU * 8 * Max_MAC_MSDU_Rate_1 / 1000000
        Max_802_11_MAC_Payload_Goodput_2 = MSDU * 8 * Max_MAC_MSDU_Rate_2 / 1000000
        Max_802_11_MAC_Payload_Goodput_3 = MSDU * 8 * Max_MAC_MSDU_Rate_3 / 1000000
        Max_802_11_MAC_Payload_Goodput_4 = MSDU * 8 * Max_MAC_MSDU_Rate_4 / 1000000
        Max_802_11_MAC_Payload_Goodput_5 = MSDU * 8 * Max_MAC_MSDU_Rate_5 / 1000000
        Max_802_11_MAC_Payload_Goodput_6 = MSDU * 8 * Max_MAC_MSDU_Rate_6 / 1000000
        Max_802_11_MAC_Payload_Goodput_7 = MSDU * 8 * Max_MAC_MSDU_Rate_7 / 1000000

        self.Client_36_new = format(Max_802_11_MAC_Payload_Goodput_1, '.3f')
        Client_37_new = format(Max_802_11_MAC_Payload_Goodput_2, '.3f')
        Client_38_new = format(Max_802_11_MAC_Payload_Goodput_3, '.3f')
        Client_39_new = format(Max_802_11_MAC_Payload_Goodput_4, '.3f')
        Client_40_new = format(Max_802_11_MAC_Payload_Goodput_5, '.3f')
        Client_41_new = format(Max_802_11_MAC_Payload_Goodput_6, '.3f')
        Client_42_new = format(Max_802_11_MAC_Payload_Goodput_7, '.3f')

        # MAC Goodput Per 802.11 Client

        MAC_Goodput_Per_802_11_Client_1 = Max_802_11_MAC_Payload_Goodput_1 / 1
        MAC_Goodput_Per_802_11_Client_2 = Max_802_11_MAC_Payload_Goodput_2 / 2
        MAC_Goodput_Per_802_11_Client_3 = Max_802_11_MAC_Payload_Goodput_3 / 5
        MAC_Goodput_Per_802_11_Client_4 = Max_802_11_MAC_Payload_Goodput_4 / 10
        MAC_Goodput_Per_802_11_Client_5 = Max_802_11_MAC_Payload_Goodput_5 / 20
        MAC_Goodput_Per_802_11_Client_6 = Max_802_11_MAC_Payload_Goodput_6 / 50
        MAC_Goodput_Per_802_11_Client_7 = Max_802_11_MAC_Payload_Goodput_7 / 100

        self.Client_43_new = format(MAC_Goodput_Per_802_11_Client_1, '.3f')
        Client_44_new = format(MAC_Goodput_Per_802_11_Client_2, '.3f')
        Client_45_new = format(MAC_Goodput_Per_802_11_Client_3, '.3f')
        Client_46_new = format(MAC_Goodput_Per_802_11_Client_4, '.3f')
        Client_47_new = format(MAC_Goodput_Per_802_11_Client_5, '.3f')
        Client_48_new = format(MAC_Goodput_Per_802_11_Client_6, '.3f')
        Client_49_new = format(MAC_Goodput_Per_802_11_Client_7, '.3f')

        # Offered Load (802.3 Side)

        if eth_value != 0:

            Offered_Load_8023_Side_1 = Max_MAC_MSDU_Rate_1 * Ethernet_value * 8 / 1000000
            Offered_Load_8023_Side_2 = Max_MAC_MSDU_Rate_2 * Ethernet_value * 8 / 1000000
            Offered_Load_8023_Side_3 = Max_MAC_MSDU_Rate_3 * Ethernet_value * 8 / 1000000
            Offered_Load_8023_Side_4 = Max_MAC_MSDU_Rate_4 * Ethernet_value * 8 / 1000000
            Offered_Load_8023_Side_5 = Max_MAC_MSDU_Rate_5 * Ethernet_value * 8 / 1000000
            Offered_Load_8023_Side_6 = Max_MAC_MSDU_Rate_6 * Ethernet_value * 8 / 1000000
            Offered_Load_8023_Side_7 = Max_MAC_MSDU_Rate_7 * Ethernet_value * 8 / 1000000
            self.Client_50_new = format(Offered_Load_8023_Side_1, '.3f')
            Client_51_new = format(Offered_Load_8023_Side_2, '.3f')
            Client_52_new = format(Offered_Load_8023_Side_3, '.3f')
            Client_53_new = format(Offered_Load_8023_Side_4, '.3f')
            Client_54_new = format(Offered_Load_8023_Side_5, '.3f')
            Client_55_new = format(Offered_Load_8023_Side_6, '.3f')
            Client_56_new = format(Offered_Load_8023_Side_7, '.3f')

        else:
            self.Client_50_new = "N/A"
            Client_51_new = "N/A"
            Client_52_new = "N/A"
            Client_53_new = "N/A"
            Client_54_new = "N/A"
            Client_55_new = "N/A"
            Client_56_new = "N/A"

        IP_Packet_value_str = str(IP_Packet_value)
        if "N/A" not in IP_Packet_value_str:
            IP_Goodput_802_11_8023_1 = Max_MAC_MSDU_Rate_1 * ip_1 * 8 / 1000000
            IP_Goodput_802_11_8023_2 = Max_MAC_MSDU_Rate_2 * ip_1 * 8 / 1000000
            IP_Goodput_802_11_8023_3 = Max_MAC_MSDU_Rate_3 * ip_1 * 8 / 1000000
            IP_Goodput_802_11_8023_4 = Max_MAC_MSDU_Rate_4 * ip_1 * 8 / 1000000
            IP_Goodput_802_11_8023_5 = Max_MAC_MSDU_Rate_5 * ip_1 * 8 / 1000000
            IP_Goodput_802_11_8023_6 = Max_MAC_MSDU_Rate_6 * ip_1 * 8 / 1000000
            IP_Goodput_802_11_8023_7 = Max_MAC_MSDU_Rate_7 * ip_1 * 8 / 1000000
            self.Client_57_new = format(IP_Goodput_802_11_8023_1, '.3f')
            Client_58_new = format(IP_Goodput_802_11_8023_2, '.3f')
            Client_59_new = format(IP_Goodput_802_11_8023_3, '.3f')
            Client_60_new = format(IP_Goodput_802_11_8023_4, '.3f')
            Client_61_new = format(IP_Goodput_802_11_8023_5, '.3f')
            Client_62_new = format(IP_Goodput_802_11_8023_6, '.3f')
            Client_63_new = format(IP_Goodput_802_11_8023_7, '.3f')

        else:
            self.Client_57_new = "N/A"
            Client_58_new = "N/A"
            Client_59_new = "N/A"
            Client_60_new = "N/A"
            Client_61_new = "N/A"
            Client_62_new = "N/A"
            Client_63_new = "N/A"

            # Theoretical Voice Call Capacity

        if "Data" in self.Traffic_Type:
            self.Maximum_Theoretical_R_value = "N/A"
            self.Estimated_MOS_Score = "N/A"
        else:

            self.Maximum_Theoretical_R_value = 85.9
            if self.Maximum_Theoretical_R_value < 0:
                self.Estimated_MOS_Score = 1
            else:
                if self.Maximum_Theoretical_R_value > 100:
                    self.Estimated_MOS_Score = 4.5
                else:
                    Estimated_MOS_Score_1 = (1 + 0.035 * self.Maximum_Theoretical_R_value + self.Maximum_Theoretical_R_value * (
                            self.Maximum_Theoretical_R_value - 60) * (100 - self.Maximum_Theoretical_R_value) * 7 * 0.000001)
                    self.Estimated_MOS_Score = format(Estimated_MOS_Score_1, '.2f')

        # Voice_Call_Range

        try:
            Voice_Call_Range = round(Max_PPDU_Rate_1 / Codec_Frame_Rate)

            # c55 Maximum Bidirectional Voice Calls

            if Voice_Call_Range <= 1:
                Maximum_Bidirectional = Max_MAC_MSDU_Rate_1 / Codec_Frame_Rate

            else:
                if Voice_Call_Range <= 2:
                    Maximum_Bidirectional = Max_MAC_MSDU_Rate_2 / Codec_Frame_Rate

                else:
                    if Voice_Call_Range <= 5:
                        Maximum_Bidirectional = Max_MAC_MSDU_Rate_3 / Codec_Frame_Rate

                    else:
                        if Voice_Call_Range <= 10:
                            Maximum_Bidirectional = Max_MAC_MSDU_Rate_4 / Codec_Frame_Rate

                        else:
                            if Voice_Call_Range <= 20:
                                Maximum_Bidirectional = Max_MAC_MSDU_Rate_5 / Codec_Frame_Rate

                            else:
                                if Voice_Call_Range <= 50:
                                    Maximum_Bidirectional = Max_MAC_MSDU_Rate_6 / Codec_Frame_Rate

                                else:

                                    Maximum_Bidirectional = Max_MAC_MSDU_Rate_7 / Codec_Frame_Rate
        except ZeroDivisionError:
            pass

        if "Data" in self.Traffic_Type:
            self.Maximum_Bidirectional_Voice_Calls = "N/A"
        else:
            self.Maximum_Bidirectional_Voice_Calls = round(Maximum_Bidirectional, 2)


    def get_result(self):

        print("\n" + "******************Station : 11ac Calculator*****************************" + "\n")
        print("Theoretical Maximum Offered Load" + "\n")
        print("1 Client:")
        All_theoretical_output = {'MAC PPDU Interval(usec)': self.Client_1_new, 'Max PPDU Rate(fps)': self.Client_8_new,
                                  'Max MAC MPDU Rate': self.Client_15_new,
                                  'Max MAC MSDU Rate': self.Client_22_new,
                                  'Max. 802.11 MAC Frame Data Rate(Mb/s)': self.Client_29_new,
                                  'Max. 802.11 MAC Payload Goodput(Mb/s)': self.Client_36_new,
                                  'MAC Goodput Per 802.11 Client(Mb/s)': self.Client_43_new,
                                  'Offered Load (802.3 Side)(Mb/s)': self.Client_50_new,
                                  'IP Goodput (802.11 -> 802.3)(Mb/s)': self.Client_57_new}
        print(json.dumps(All_theoretical_output, indent=4))

        print("\n" + "Theroretical Voice Call Capacity" + "\n")

        All_theoretical_voice = {'Maximum Theoretical R-value': self.Maximum_Theoretical_R_value,
                                 'Estimated MOS Score': self.Estimated_MOS_Score,
                                 'Maximum Bidirectional Voice Calls(calls)': self.Maximum_Bidirectional_Voice_Calls}
        print(json.dumps(All_theoretical_voice, indent=4))