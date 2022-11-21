#!/usr/bin/env python3
"""
NAME: wifi_diag.py

PURPOSE: wifi_diag.py provides a comprehensive set of information for the packet captured(pcap) file
        and generates a report based on input pcap file.The script will analyze the PCAP file and provide the
        various analytical results such as A-MPDU percentage with histogram,various percentage of the pcakets
        received for the different MCS, the report will include Bandwidth, Number of Spatial streams, encoding rate,
        RSSI, percentage of control frames and management frames, etc.

EXAMPLE:  python3 wifi_diag.py --input <pcap(Packet Capture) file path>

VERIFIED_ON: 18 August 2022

LICENSE:
    Free to distribute and modify. LANforge systems must be licensed.
    Copyright 2022 Candela Technologies Inc

INCLUDE_IN_README: False
"""

import sys
import pyshark
import numpy as np
import pandas as pd
import logging
import argparse
import shutil
import os
import importlib

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../")))

lf_report = importlib.import_module("py-scripts.lf_report")
lf_report = lf_report.lf_report
lf_graph = importlib.import_module("py-scripts.lf_graph")
lf_bar_graph = lf_graph.lf_bar_graph


class wifi_diag:
    def __init__(self):
        self.FilePath = output
        self.cap = pyshark.FileCapture(self.FilePath)

    # This is for AMPDU Histogram
    def RateAMPDU(self, AMPDU, count):

        countUniqueAMPDU = []

        perUniqueAMPDU = []
        chainCountAMPDU = []

        uniqueAMPDU = np.unique(AMPDU)
        uniqueAMPDU = [i for i in uniqueAMPDU]

        for countAMPDU in uniqueAMPDU:
            countUniqueAMPDU.append(AMPDU.count(countAMPDU))

        chainUniqueAMPDU = np.unique(countUniqueAMPDU)
        chainUniqueAMPDU = [i for i in chainUniqueAMPDU]

        for Acount in chainUniqueAMPDU:
            chainCountAMPDU.append(countUniqueAMPDU.count(Acount))

        UniqueChainCountAMPDU = np.unique(chainCountAMPDU)
        UniqueChainCountAMPDU = [i for i in UniqueChainCountAMPDU]

        listAMPDU = []
        for un in UniqueChainCountAMPDU:
            listAMPDU.append(chainCountAMPDU.count(un))

        print(chainUniqueAMPDU, chainCountAMPDU)
        dictAMPDU = dict(zip(chainUniqueAMPDU, chainCountAMPDU))

        for acnt in chainCountAMPDU:
            perUniqueAMPDU.append(round((acnt * 100) / count, 4))

        df_AMPDU = pd.DataFrame(
            {" Chain count ": [k for k in dictAMPDU.keys()], " Total Packets ": [i for i in dictAMPDU.values()],
             " Percentage ": [j for j in perUniqueAMPDU]})

        PacketInfo = ("Representing AMPDU chain count  Histogram.")

        report.set_table_title("AMPDU chain count Histogram")
        report.build_table_title()

        report.set_text("About:")
        report.build_text()

        report.set_text(PacketInfo)
        report.build_text()

        report.set_table_dataframe(df_AMPDU)
        report.build_table()

        # AMPDU graph only used,when pcap file has data of AMPDU
        dataset = [perUniqueAMPDU]
        x_axis_values = chainUniqueAMPDU

        if x_axis_values == []:
            x_axis_valuess = x_axis_values.append(0)
            print("The Data for AMPDU chain count Histogram is", x_axis_valuess)

        graph = lf_bar_graph(_data_set=dataset,
                             _xaxis_name="packet Chain",
                             _yaxis_name="Percentage",
                             _xaxis_categories=x_axis_values,
                             _graph_image_name="AMPDU",
                             _label=["Total Packets"],
                             _color=['blue'],
                             _color_edge='black',
                             _figsize=(16, 7),
                             _grp_title="AMPDU plot",
                             _xaxis_step=1,
                             _show_bar_value=True,
                             _text_font=7,
                             _text_rotation=45,
                             _xticks_font=7,
                             _legend_loc="best",
                             _legend_box=(1, 1),
                             _legend_ncol=1,
                             _legend_fontsize=None,
                             _enable_csv=False)

        graph_png = graph.build_bar_graph()

        report.set_graph_image(graph_png)
        report.move_graph_image()
        report.build_graph()

    # This is for MCS Histogram
    def MCSHistogram(self, MCSIndex, vMCS, count):
        countUniqueMCSIndex = []

        perUniqueMCS = []

        uniqueMCSIndex = np.unique(MCSIndex)

        for countMCS in uniqueMCSIndex:
            countUniqueMCSIndex.append(MCSIndex.count(countMCS))

        for cnt in countUniqueMCSIndex:
            perUniqueMCS.append(round((cnt * 100) / count, 2))

        dictMCS = dict(zip(uniqueMCSIndex, countUniqueMCSIndex))
        df_MCS = pd.DataFrame(
            {" MCS ": [k for k in dictMCS.keys()], " Total Packets ": [i for i in dictMCS.values()],
             " Percentage ": [j for j in perUniqueMCS]})

        dictMCSs = [i for i in dictMCS.keys()]
        PacketInfo = ("Data packets having MCS field: " + str(vMCS) + "<br>")

        report.set_table_title("Data MCS Histogram")
        report.build_table_title()

        report.set_text("About:")
        report.build_text()

        report.set_text(PacketInfo)
        report.build_text()

        report.set_table_dataframe(df_MCS)
        report.build_table()

        # MCS graph only used,when pcap file has data of MCS
        dataset = [perUniqueMCS]
        x_axis_values = dictMCSs
        if x_axis_values == []:
            x_axis_valuess = x_axis_values.append(0)
            print("The Data for Data MCS Histogram is", x_axis_valuess)

        graph = lf_bar_graph(_data_set=dataset,
                             _xaxis_name="packet Chain",
                             _yaxis_name="Percentage",
                             _xaxis_categories=x_axis_values,
                             _graph_image_name="MCS",
                             _label=["Total Packets"],
                             _color=['blue'],
                             _color_edge='black',
                             _figsize=(16, 7),
                             _grp_title="MCS",
                             _xaxis_step=1,
                             _show_bar_value=True,
                             _text_font=7,
                             _text_rotation=45,
                             _xticks_font=7,
                             _legend_loc="best",
                             _legend_box=(1, 1),
                             _legend_ncol=1,
                             _legend_fontsize=None,
                             _enable_csv=False)

        graph_png = graph.build_bar_graph()

        report.set_graph_image(graph_png)
        report.move_graph_image()
        report.build_graph()

    # This is for Bandwidth Histogram
    def BandwidthHistogram(self, Bandwidth, vBW, count):
        countUniqueBandwidth = []
        perUniqueBW = []

        uniqueBandwidth = ((np.unique(Bandwidth)))

        for countBandwidth in uniqueBandwidth:
            countUniqueBandwidth.append(Bandwidth.count(countBandwidth))

        for cnt in countUniqueBandwidth:
            perUniqueBW.append(round((cnt * 100) / count, 2))

        dictBW = dict(zip(uniqueBandwidth, countUniqueBandwidth))
        df_BW = pd.DataFrame(
            {" Bandwidth ": [k for k in dictBW.keys()], " Total Packets ": [i for i in dictBW.values()],
             " Percentage ": [j for j in perUniqueBW]})

        dictBWs = [i for i in dictBW.keys()]
        PacketInfo = ("Data packets having Bandwidth field: " + str(vBW) + "<br>")

        report.set_table_title("Data Bandwidth Histogram")
        report.build_table_title()

        report.set_text("About:")
        report.build_text()

        report.set_text(PacketInfo)
        report.build_text()

        report.set_table_dataframe(df_BW)
        report.build_table()

        # Bandwidth graph only used,when pcap file has data of
        dataset = [perUniqueBW]
        x_axis_values = dictBWs

        if x_axis_values == []:
            x_axis_valuess = x_axis_values.append(0)
            print("The Data for Data Bandwidth Histogram is", x_axis_valuess)

        graph = lf_bar_graph(_data_set=dataset,
                             _xaxis_name="Bandwidth",
                             _yaxis_name="Percentage",
                             _xaxis_categories=x_axis_values,
                             _graph_image_name="Bandwidth",
                             _label=["Total Packets"],
                             _color=['blue'],
                             _color_edge='black',
                             _figsize=(16, 7),
                             _grp_title="Bandwidth plot",
                             _xaxis_step=1,
                             _show_bar_value=True,
                             _text_font=7,
                             _text_rotation=45,
                             _xticks_font=7,
                             _legend_loc="best",
                             _legend_box=(1, 1),
                             _legend_ncol=1,
                             _legend_fontsize=None,
                             _enable_csv=False)

        graph_png = graph.build_bar_graph()

        report.set_graph_image(graph_png)
        report.move_graph_image()
        report.build_graph()

    # This is for NSS Histogram
    def NSSHistogram(self, Spatial_Stream, vNCS, count):
        countUniqueSpatial_stream = []
        perUniqueNCS = []

        uniqueSpatial_stream = ((np.unique(Spatial_Stream)))

        for countNCS in uniqueSpatial_stream:
            countUniqueSpatial_stream.append(Spatial_Stream.count(countNCS))

        for cnt in countUniqueSpatial_stream:
            perUniqueNCS.append(round((cnt * 100) / count, 2))

        dictNCS = dict(zip(uniqueSpatial_stream, countUniqueSpatial_stream))
        df_NCS = pd.DataFrame(
            {" NSS ": [k for k in dictNCS.keys()], " Total Packets ": [i for i in dictNCS.values()],
             " Percentage ": [j for j in perUniqueNCS]})
        dictNCSs = [i for i in dictNCS.keys()]
        PacketInfo = ("Data packets having NSS field: " + str(vNCS) + "<br>")

        report.set_table_title("Data NSS Histogram")
        report.build_table_title()

        report.set_text("About:")
        report.build_text()

        report.set_text(PacketInfo)
        report.build_text()

        report.set_table_dataframe(df_NCS)
        report.build_table()

        # NSS graph only used,when pcap file has data of NSS
        dataset = [perUniqueNCS]
        x_axis_values = dictNCSs

        if x_axis_values == []:
            x_axis_valuess = x_axis_values.append(0)
            print("The Data for Data NSS Histogram is", x_axis_valuess)

        graph = lf_bar_graph(_data_set=dataset,
                             _xaxis_name="Spatial stream",
                             _yaxis_name="Percentage",
                             _xaxis_categories=x_axis_values,
                             _graph_image_name="NSS",
                             _label=["Total Packets"],
                             _color=['blue'],
                             _color_edge='black',
                             _figsize=(16, 7),
                             _grp_title="NCS plot",
                             _xaxis_step=1,
                             _show_bar_value=True,
                             _text_font=7,
                             _text_rotation=45,
                             _xticks_font=7,
                             _legend_loc="best",
                             _legend_box=(1, 1),
                             _legend_ncol=1,
                             _legend_fontsize=None,
                             _enable_csv=False)

        graph_png = graph.build_bar_graph()

        report.set_graph_image(graph_png)
        report.move_graph_image()
        report.build_graph()

    # This is for Rate Histogram
    def RateHistogram(self, DataRate, count):
        countUniqueData = []
        perUniqueData = []

        uniqueData = np.unique(DataRate)

        for i in uniqueData:
            countUniqueData.append(DataRate.count(i))

        uniqueData = [i for i in uniqueData]

        dictRate = (dict(zip(uniqueData, countUniqueData, )))

        for c in countUniqueData:
            perUniqueData.append(round((c * 100) / count, 2))

        df_Rate = pd.DataFrame(
            {" Rate MBPS ": [i for i in dictRate.keys()], " Total Packets ": [j for j in dictRate.values()],
             " Percentage ": [k for k in perUniqueData]})

        report.set_table_title("Encoding rate histogram")
        report.build_table_title()

        report.set_text("About:")
        report.build_text()

        report.set_text("Packet rates encoding")
        report.build_text()

        report.set_table_dataframe(df_Rate)
        report.build_table()

        dataset = [perUniqueData]
        x_axis_values = uniqueData

        if x_axis_values == []:
            x_axis_valuess = x_axis_values.append(0)
            print("The Data for Encoding rate histogram is", x_axis_valuess)

        graph = lf_bar_graph(_data_set=dataset,
                             _xaxis_name="Rate MBPS",
                             _yaxis_name="Percentage",
                             _xaxis_categories=x_axis_values,
                             _graph_image_name="Rate",
                             _label=["Total Packets"],
                             _color=['blue'],
                             _color_edge='black',
                             _figsize=(16, 7),
                             _grp_title="Rate plot",
                             _xaxis_step=1,
                             _show_bar_value=True,
                             _text_font=7,
                             _text_rotation=45,
                             _xticks_font=7,
                             _legend_loc="best",
                             _legend_box=(1, 1),
                             _legend_ncol=1,
                             _legend_fontsize=None,
                             _enable_csv=False)

        graph_png = graph.build_bar_graph()

        report.set_graph_image(graph_png)
        report.move_graph_image()
        report.build_graph()

    #This is for Phy Histogram
    def PhyHistogram(self, PhyType, count):
        countUniquePhy = []
        perUniquePhy = []
        uniquePhy = np.unique(PhyType)

        for j in uniquePhy:
            countUniquePhy.append(PhyType.count(j))

        uniquePhy = [i for i in uniquePhy]

        dictPhy = (dict(zip(uniquePhy, countUniquePhy)))

        for d in countUniquePhy:
            perUniquePhy.append(round((d * 100) / count, 2))

        df_Phy = pd.DataFrame(
            {" PHY ": [i for i in dictPhy.keys()], " Total Packets ": [j for j in dictPhy.values()],
             " Percentage ": [k for k in perUniquePhy]})

        dictphys = [i for i in dictPhy.keys()]

        report.set_table_title(" Phy Histogram")
        report.build_table_title()

        report.set_text("About:")
        report.build_text()

        report.set_text("Representation in Phy Histogram.")
        report.build_text()

        report.set_table_dataframe(df_Phy)
        report.build_table()

        # Phy graph only used,when pcap file has data of Phy
        dataset = [perUniquePhy]
        x_axis_values = dictphys

        if x_axis_values == []:
            x_axis_valuess = x_axis_values.append(0)
            print("The Data for Phy Histogram is", x_axis_valuess)

        graph = lf_bar_graph(_data_set=dataset,
                             _xaxis_name="Subtype",
                             _yaxis_name="Percentage",
                             _xaxis_categories=x_axis_values,
                             _graph_image_name="Phy",
                             _label=["Total Packets"],
                             _color=['blue'],
                             _color_edge='black',
                             _figsize=(16, 7),
                             _grp_title="Phy plot",
                             _xaxis_step=1,
                             _show_bar_value=True,
                             _text_font=7,
                             _text_rotation=45,
                             _xticks_font=7,
                             _legend_loc="best",
                             _legend_box=(1, 1),
                             _legend_ncol=1,
                             _legend_fontsize=None,
                             _enable_csv=False)

        graph_png = graph.build_bar_graph()

        report.set_graph_image(graph_png)
        report.move_graph_image()
        report.build_graph()

    # This is for Signal Histogram
    def SignalHistogram(self, SignalStrength, count):
        countUniqueSignal = []
        perUniqueSignal = []
        uniqueSignal = np.unique(SignalStrength)

        for k in uniqueSignal:
            countUniqueSignal.append(SignalStrength.count(k))

        uniqueSignal = [i for i in uniqueSignal]
        dictSig = (dict(zip(uniqueSignal, countUniqueSignal)))

        for e in countUniqueSignal:
            perUniqueSignal.append(round((e * 100) / count, 2))

        df_Sig = pd.DataFrame(
            {" Signal ": [k for k in dictSig.keys()], " Total Packets ": [i for i in dictSig.values()],
             " Percentage ": [j for j in perUniqueSignal]})

        dictSigs = [i for i in dictSig.keys()]

        report.set_table_title("Signal Histogram")
        report.build_table_title()

        report.set_text("About:")
        report.build_text()

        report.set_text("Representing Signal Histogram.")
        report.build_text()

        report.set_table_dataframe(df_Sig)
        report.build_table()

        # Signal graph only used,when pcap file has data of Signal
        dataset = [perUniqueSignal]
        x_axis_values = dictSigs

        if x_axis_values == []:
            x_axis_valuess = x_axis_values.append(0)
            print("The Data for Signal Histogram is", x_axis_valuess)

        graph = lf_bar_graph(_data_set=dataset,
                             _xaxis_name="Signal",
                             _yaxis_name="Percentage",
                             _xaxis_categories=x_axis_values,
                             _graph_image_name="Signal",
                             _label=["Total Packets"],
                             _color=['blue'],
                             _color_edge='black',
                             _figsize=(16, 7),
                             _grp_title="Signal plot",
                             _xaxis_step=1,
                             _show_bar_value=True,
                             _text_font=7,
                             _text_rotation=45,
                             _xticks_font=7,
                             _legend_loc="best",
                             _legend_box=(1, 1),
                             _legend_ncol=1,
                             _legend_fontsize=None,
                             _enable_csv=False)

        graph_png = graph.build_bar_graph()

        report.set_graph_image(graph_png)
        report.move_graph_image()
        report.build_graph()

    # This is for Packet Histogram
    def PacketHistogram(self, subtype_list, Managementls, Controlls, Data_framels, count):
        Type_Subtype = {"Management Frame": [Managementls], "Control Frame": [Controlls], "Data Frame": [Data_framels]}

        Type_list = []
        Sub_list = []
        pack_list = []
        per_list = []

        for Type, Subtype in Type_Subtype.items():

            liskeys = []
            for key in subtype_list.values():
                if (key in liskeys):
                    continue

                val = Subtype[0].count(key)
                liskeys.append(key)
                if (val != 0):
                    Type_list.append(str(Type))
                    Sub_list.append(key)
                    pack_list.append(val)
                    per_list.append((round((val * 100) / count, 2)))

        NewSubList = Sub_list
        NewPerList = per_list

        df_Type = pd.DataFrame(
            ({" Type ": Type_list, " Subtype ": NewSubList, " Total Packets ": pack_list, "Percentage": NewPerList}))

        report.set_table_title("Packet Type histogram")
        report.build_table_title()

        report.set_text("About:")
        report.build_text()

        report.set_text("Different Packet type histogram.")
        report.build_text()

        report.set_table_dataframe(df_Type)
        report.build_table()

        # Packet graph only used,when pcap file has data of Packet
        dataset = [NewPerList]
        x_axis_values = NewSubList

        if x_axis_values == []:
            x_axis_valuess = x_axis_values.append(0)
            print("The Data for Packet Type histogram is", x_axis_valuess)

        graph = lf_bar_graph(_data_set=dataset,
                             _xaxis_name="Subtype",
                             _yaxis_name="Percentage",
                             _xaxis_categories=x_axis_values,
                             _graph_image_name="Type",
                             _label=["Total Packets"],
                             _color=['blue'],
                             _color_edge='black',
                             _figsize=(23, 7),
                             _grp_title="Type/SubType plot",
                             _xaxis_step=1,
                             _show_bar_value=True,
                             _text_font=8,
                             _text_rotation=45,
                             _xticks_font=9,
                             _legend_loc="best",
                             _legend_box=(1, 1),
                             _legend_ncol=1,
                             _legend_fontsize=None,
                             _enable_csv=False)

        graph_png = graph.build_bar_graph()

        report.set_graph_image(graph_png)
        report.move_graph_image()
        report.build_graph()

    # collect data from input pcap
    def main(self):
        type_list = {"0": "Management frame", "1": "Control Frame", "2": "Data frame"}
        subtype_list = {"80": "Beacon frame", "d0": "Action", "b4": "Request-to-send", "d4": "Acknowledgement", \
                        "88": "QoS Data", "84": "Block Ack Req", "94": "Block Ack Req", \
                        "40": "Probe Request", "50": "Probe Response", "b0": "Authentication",
                        "a2": "Disassociate", "a8": "QoS Data + CF-Poll", "c8": "QoS Null function", \
                        "10": "Association Response", "00": "Association Request", "c4": "Clear-to-send", \
                        "98": "QoS Data + CF-Acknowledgment", "24": "Trigger", "28": "Data + CF-Poll", \
                        "d8": "Unknown", "54": "VHT/HE NDP Announcement", "e8": "QoS CF-Poll", \
                        "b8": "QoS Data + CF-Ack + CF-Poll", "18": "Data + CF-Ack", "48": "Null function", \
                        "69": "CF-Poll", "08": "Data"
                        }


        Managementls = []
        Controlls = []
        Data_framels = []
        PhyType = []
        DataRate = []
        SignalStrength = []


        MCSIndex = []
        Bandwidth = []
        PHY = []
        Spatial_Stream = []
        AMPDU = []

        vDataType = 0
        count = 0
        vWLAN_RADIO = 0
        vsignalstrength = 0
        vPhy = 0
        vdatarate = 0
        vWLAN = 0

        vNotPHY = 0
        vNotBW = 0
        vNotMCS = 0
        vNOTNCS = 0
        vMCS = 0
        vPHY = 0
        vBW = 0
        vNCS = 0
        vAMPDU = 0
        vNotAMPD = 0

        for packet in self.cap:
            count += 1
            print(count)


            try:
                WLAN_RADIO = packet.wlan_radio
                wlan_radio_Fields_keys = []
                wlan_radio_Fields_values = []

                for keys, values in packet.wlan_radio._all_fields.items():
                    # print(keys, ":", values)
                    wlan_radio_Fields_keys.append(keys)
                    wlan_radio_Fields_values.append(values)

                vWLAN_RADIO = 1
                try:
                    signalstrength = WLAN_RADIO.signal_dbm
                    vsignalstrength = 1
                except:
                    pass

                try:
                    phy = WLAN_RADIO.phy.showname_value
                    vPhy = 1
                except:
                    pass

                try:
                    datarate = WLAN_RADIO.data_rate
                    vdatarate = 1
                except:
                    pass

            except:
                pass
                # print("WLAN RADIO NOT FOUND")

            try:
                RADIOTAP = packet.radiotap
                # radiotap_field_keys = []
                # radiotap_field_values = []
                #
                # for keys, values in packet.radiotap._all_fields.items():
                #     print(keys, ":", values)
                #     radiotap_field_keys.append(keys)
                #     radiotap_field_values.append(values)

                # print("*****************RADIOTAP**************************")
            except:
                # print("RADIOTAP NOT FOUND")
                pass

            try:
                WLAN = packet.wlan
                # for keys, values in packet.wlan._all_fields.items():
                #     print(keys, ":", values)
                # print("***********************************************")
                vWLAN = 1
            except:
                pass
                # print("WLAN NOT FOUND")


            PacketCount = (packet.number)


            if vWLAN == 1:
                # print("WLAN found")
                # Type/Subtype raw value
                type_raw = (str(packet.wlan.fc_type.raw_value))
                subtype_raw = ((packet.wlan.fc_type_subtype.raw_value))

                # Name of values Types/Subtype
                type = (str(packet.wlan.fc_type.showname_value))
                subtype = (str(packet.wlan.fc_type_subtype.showname_value))

                # Sorting Subtypes by Types as a refrence
                if (type_raw == "0"):
                    try:
                        Managementls.append(subtype_list[subtype_raw])
                    except:
                        pass

                elif (type_raw == "1"):
                    try:
                        Controlls.append(subtype_list[subtype_raw])
                    except:
                        print("Control Frame", subtype, subtype_raw)

                elif (type_raw == "2"):

                    try:
                        vDataType += 1

                        Data_framels.append(subtype_list[subtype_raw])
                        checkType =  packet.wlan_radio._all_fields["wlan_radio.phy"]


                        try:

                            if "wlan_radio.11ac.bandwidth" and "wlan_radio.11ac.mcs" and "wlan_radio.11ac.nss" in wlan_radio_Fields_keys:
                                print("in 11ac")
                                try:

                                    if "wlan_radio.11ac.bandwidth" in wlan_radio_Fields_keys:
                                        Bandwidth.append(packet.wlan_radio._all_fields["wlan_radio.11ac.bandwidth"].showname_value)
                                        vBW += 1
                                        # print("11 ac bandwidth")

                                    if "wlan_radio.11ac.mcs" in wlan_radio_Fields_keys:
                                        MCSIndex.append(packet.wlan_radio._all_fields["wlan_radio.11ac.mcs"].showname_value)
                                        vMCS += 1
                                        # print("11 ac MCS")

                                    if "wlan_radio.11ac.nss" in wlan_radio_Fields_keys:
                                        Spatial_Stream.append(packet.wlan_radio._all_fields["wlan_radio.11ac.nss"].showname_value)
                                        vNCS += 1
                                        # print("11 ac NSS")


                                except:
                                    print("wlan_radio.11ac.bandwidth  or wlan_radio.11ac.mcs or wlan_radio.11ac.nss not found")

                            try:
                                # print("in 11ax")
                                radiotap_field_keys = []
                                radiotap_field_values = []

                                for keys, values in packet.radiotap._all_fields.items():
                                    # print(keys, ":", values)
                                    radiotap_field_keys.append(keys)
                                    radiotap_field_values.append(values)

                                if "radiotap.he.data_3.data_mcs" and "radiotap.he.data_5.data_bw_ru_allocation" and "radiotap.he.data_6.nsts" in radiotap_field_keys:

                                    print("in 11ax inside")
                                    try:
                                        if "radiotap.he.data_3.data_mcs" in radiotap_field_keys:
                                            # print("in 11ax radiotap")
                                            MCSIndex.append(packet.radiotap._all_fields["radiotap.he.data_3.data_mcs"].showname_value)
                                            vMCS += 1
                                    except:
                                        print("MCS not found in ax")

                                    try:
                                        if "radiotap.he.data_5.data_bw_ru_allocation" in radiotap_field_keys:
                                            # print("in BW radiotap 11ax")
                                            Bandwidth.append(packet.radiotap._all_fields["radiotap.he.data_5.data_bw_ru_allocation"].showname_value)
                                            vBW += 1

                                    except:
                                        print("BW not found in ax")

                                    try:
                                        if "radiotap.he.data_6.nsts" in radiotap_field_keys:
                                            # print("in 11ax radiotap nsts")
                                            Spatial_Stream.append(packet.radiotap._all_fields["radiotap.he.data_6.nsts"].showname_value)
                                            vNCS += 1


                                    except:
                                        print("NSTS not found in ax")
                            except:
                                print("radiotap.he.data_3.data_mcs  or radiotap.he.data_5.data_bw_ru_allocation or radiotap.he.data_6.nsts not found")

                            if "wlan_radio.a_mpdu_aggregate_id" in wlan_radio_Fields_keys:
                                AMPDU.append((packet.wlan_radio._all_fields["wlan_radio.a_mpdu_aggregate_id"].showname_value))
                                vAMPDU += 1

                            if "wlan_radio.phy" in wlan_radio_Fields_keys:
                                PHY.append(packet.wlan_radio._all_fields["wlan_radio.phy"].showname_value)
                                vPHY += 1


                        except:
                            pass
                            # print("comming out through try in except")


                    except:
                        print("Data frame", subtype, subtype_raw)

                else:
                    print("\nMissing Type in table : ", type_raw, subtype, subtype_raw, "\n")
            else:
                print("Packet Number :",count,":"," WLAN NOT FOUND")

            vWLAN = 0
            if vdatarate == 1:
                DataRate.append(datarate)

            if vPhy == 1:
                PhyType.append(phy)

            if vsignalstrength == 1:
                SignalStrength.append(signalstrength)

            try:

                print("\r" + count, ":", packet.wlan_radio._all_fields.items())
            except:
                pass
        if vAMPDU != 0:
            wd_obj.RateAMPDU(AMPDU, count)

        wd_obj.MCSHistogram(MCSIndex, vMCS, count)
        wd_obj.BandwidthHistogram(Bandwidth, vBW, count)
        wd_obj.NSSHistogram(Spatial_Stream, vNCS, count)
        wd_obj.RateHistogram(DataRate, count)
        wd_obj.PhyHistogram(PhyType, count)
        wd_obj.SignalHistogram(SignalStrength, count)
        wd_obj.PacketHistogram(subtype_list, Managementls, Controlls, Data_framels, count)

        report.build_footer()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="To create a report from a pcap files")
    parser.add_argument("-i", "--input", type=str,
                        help="Enter the Name of the pcap files which needs to generatate pdf report.")

    args = None

    try:
        args = parser.parse_args()
        output = "wifi_diag.pcap"

        if (args.input is not None):
            input = args.input  # 'C:\candela\pcap\\11ax.pcapng','C:\candela\pcap\sta1.pcap'
            input = input.split(",")
            # print("The input pcap file is :",input)

    except Exception as e:
        logging.exception(e)
        exit(2)

    with open(output, 'wb') as wfd:
        print("input", input)
        for f in (input):
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd)

    report = lf_report(_output_html="wifi-diag.html", _output_pdf="wifi-diag.pdf",
                       _results_dir_name="Wifi_Diag_Test", _path=".")

    report_path = report.get_path()
    report_path_date_time = report.get_path_date_time()
    report.set_title("Wifi diag")
    report.build_banner()

    report.set_obj_html("Objective",
                        "The WiFi Diag testing feature provides a comprehensive set of "
                        "information for the packet captured for RF environment. The script"
                        " will take the input from the PCAP file, normally generated using "
                        "Wireshark sniffing tool, which is integrated in the LANforge for "
                        "analysis. The script will analyze the PCAP file and provide the "
                        "various analytical results such as A-MPDU percentage with histogram. "
                        "The test report will include, various percentage of the pcakets "
                        "received for the different MCS. Based on the PCAP file, the report "
                        "will include Bandwidth, Number of Spatial streams, encoding rate, "
                        "RSSI, percentage of control frames and management frames, etc. ")
    report.build_objective()

    wd_obj = wifi_diag()
    wd_obj.main()

    html_file = report.write_html()
    print("Returned html file in {}".format(html_file))
    report.write_pdf(_page_size='Legal', _orientation='Portrait')
