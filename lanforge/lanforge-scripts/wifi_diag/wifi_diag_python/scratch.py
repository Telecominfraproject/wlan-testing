"""
-----------------------------------------------------------------------------
Name : WIFI Diag
Author : Sushant Bawiskar
Date : 20 September 2020
------------------------------------------------------------------------------
"""

""" 
    Example:    python PcaplibFiles.py --input "11ax.pcapng","sta1.pcap" 

"""

import datetime
import pyshark
import pandas as pd
from bokeh.plotting import figure, output_file, show, save
from bokeh.io.export import get_screenshot_as_png, export_png, export_svgs, export_svg
import matplotlib.pyplot as plt
from plotly.offline import iplot, init_notebook_mode
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import matplotlib.pyplot as plt
import base64
from io import BytesIO
from htmlText import *
from Dataplot import Plot
import shutil
import argparse
import logging
import numpy as np



import os


def PacketHistogram(subtype_list, Managementls, Controlls, Data_framels, count):
    # Created a Dictonary of Management Frame : {Subtype} , Control Frame : {Subtype} , Data Frame : {Subtype}
    Type_Subtype = {"Management Frame": [Managementls], "Control Frame": [Controlls], "Data Frame": [Data_framels]}

    Type_list = []
    Sub_list = []
    pack_list = []
    per_list = []

    # To calculate Total number of Subtype of packets in Type
    # Ex. To calculate how many packets have a subtype which are in Management/Control/Data Frame Type
    for Type, Subtype in Type_Subtype.items():

        liskeys = []
        for key in subtype_list.values():
            if (key in liskeys):
                continue

            val = Subtype[0].count(key)
            liskeys.append(key)
            # liskeys.append(key)
            if (val != 0):
                # Type_list = [Type,key,val,(val*100)/count]
                Type_list.append(str(Type))
                Sub_list.append(key)
                pack_list.append(val)
                per_list.append((round((val * 100) / count, 2)))


    # Type_list.append("")
    Sub = Sub_list
    NewSubList = Sub_list
    # NewSubList.append("Sum: ")
    #
    # pack_list.append(sum(pack_list))

    NewPerList = per_list
    # NewPerList.append(sum(NewPerList))

    # print(len(subtype_list),len(NewSubList),len(pack_list),print(NewPerList))
    df_Type = pd.DataFrame(({" Type ": Type_list, " Subtype ": NewSubList, " Total Packets ": pack_list, "Percentage": NewPerList}))


    # print("df_Type",df_Type)

    df_Type = df_Type.to_html(index=False)
    # NewPerList.pop()
    # NewSubList.pop()
    plot = Plot()
    path = plot.bar(datax=NewSubList,datay=NewPerList,title="Type/SubType plot",xaxis="Subtype",yaxis="Percentage",figname="Type")

    htmltable(" Packet Type histogram", df_Type, str(path), "0", "0","Summary ")



def RateHistogram(DataRate, PhyType, SignalStrength, count):

    countUniqueData = []
    perUniqueData = []

    countUniquePhy = []
    perUniquePhy = []

    countUniqueSignal = []
    perUniqueSignal = []

    # This is for Data Table Histogram
    uniqueData = np.unique(DataRate)

    for i in uniqueData:
        countUniqueData.append(DataRate.count(i))

    uniqueData = [i for i in uniqueData]

    # uniqueData.append("Sum: ")
    # countUniqueData.append(sum(countUniqueData))

    dictRate = (dict(zip(uniqueData, countUniqueData, )))

    for c in countUniqueData:
        perUniqueData.append(round((c * 100) / count, 2))



    df_Rate = pd.DataFrame({" Rate MBPS ": [i for i in dictRate.keys()], " Total Packets ": [j for j in dictRate.values()], " Percentage ": [k for k in perUniqueData]})

    # df_Rate = df_Rate.T
    # df_Rate.columns = df_Rate.iloc[0]
    # df_Rate = df_Rate.drop(df_Rate.iloc[0].index.name)
    df_Rate = df_Rate.to_html(index=False)




    # uniqueData.pop()
    # perUniqueData.pop()

    plot1 = Plot()
    path = plot1.bar(datax=uniqueData, datay=perUniqueData, title="Rate plot", xaxis="Rate MBPS", yaxis="Percentage",
                    figname="rate")


    htmltable(" Encoding rate histogram.", df_Rate, str(path), "0", "0","Summary ")


    # This is for Phy Histogram
    uniquePhy = np.unique(PhyType)
    for j in uniquePhy:
        countUniquePhy.append(PhyType.count(j))

    uniquePhy = [i for i in uniquePhy]
    # uniquePhy.append("Sum: ")
    # countUniquePhy.append(sum(countUniquePhy))

    dictPhy = (dict(zip(uniquePhy, countUniquePhy)))

    for d in countUniquePhy:
        perUniquePhy.append(round((d * 100) / count, 2))

    df_Phy = pd.DataFrame({" PHY ": [i for i in dictPhy.keys()], " Total Packets ": [j for j in dictPhy.values()]," Percentage ": [k for k in perUniquePhy]})

    # print("df_Phy",df_Phy)

    # df_Phy = df_Phy.to_html()

    # df_Phy = df_Phy.T
    # df_Phy.columns = df_Phy.iloc[0]
    # df_Phy = df_Phy.drop(df_Phy.iloc[0].index.name)
    df_Phy = df_Phy.to_html(index=False)

    dictphys = [i for i in dictPhy.keys()]

    # dictphys.pop()
    # perUniquePhy.pop()

    plot2 = Plot()
    path = plot2.bar(datax=dictphys, datay=perUniquePhy, title="Phy plot", xaxis="Subtype", yaxis="Percentage",
                    figname="Phy")

    htmltable(" Phy Histogram.",df_Phy,str(path),"0","0","Summary ")

    # This is for Signal Histogram
    uniqueSignal = np.unique(SignalStrength)

    for k in uniqueSignal:
        countUniqueSignal.append(SignalStrength.count(k))

    uniqueSignal = [i for i in uniqueSignal]
    # uniqueSignal.append("Sum: ")
    # countUniqueSignal.append(sum(countUniqueSignal))

    dictSig = (dict(zip(uniqueSignal, countUniqueSignal)))

    for e in countUniqueSignal:
        perUniqueSignal.append(round((e * 100) / count, 2))

    # perUniqueSignal.append(sum(perUniqueSignal))
    # pd.DataFrame.reset_index(drop=True,inplace=True)
    # df_Sig = pd.DataFrame({"Signal": [i for i in dictSig.keys()], "Packet to Packet": [j for j in dictSig.values()],
    #                        "Percentage": [k for k in perUniqueSignal]})

    # pd.DataFrame.reset_index(drop=True,inplace=True)
    # print([k for k in dictSig.keys()])
    # print([i for i in dictSig.values()])
    # print("perUniqueSignal",perUniqueSignal)

    # pd.DataFrame
    df_Sig = pd.DataFrame({" Signal ":[k for k in dictSig.keys()]," Total Packets ":[i for i in dictSig.values()]," Percentage ":[j for j in perUniqueSignal]})

    # df_Sig = df_Sig.T
    # df_Sig.columns = df_Sig.iloc[0]
    # df_Sig = df_Sig.drop(df_Sig.iloc[0].index.name)
    # df_Sig.columns.name = None
    # df_Sig.index.name = "Signal"
    # print("df_Sig",df_Sig)
    # print("df_Sig",df_Sig)

    # df_Sig = df_Sig.to_html()

    # df_Sig = df_Sig.transpose()
    df_Sig = df_Sig.to_html(index=False)

    # perUniqueSignal.pop()
    dictSigs = [i for i in dictSig.keys()]
    # dictSigs.pop()

    plot3 = Plot()
    path = plot3.bar(datax=dictSigs, datay=perUniqueSignal, title="Signal plot", xaxis="Signal", yaxis="Percentage",
                     figname="Signal")
    htmltable(" Signal Histogram.", df_Sig, str(path), "0", "0","Summary ")

    # print(dictSigs,perUniqueSignal)


def PHY_BW_MCS_NCS(MCSIndex, vMCS, Bandwidth, vBW, PHY, vPHY, Spatial_Stream, vNCS,  count):

    countUniqueMCSIndex = []
    countUniqueBandwidth = []
    countUniquePHY = []
    countUniqueSpatial_stream = []

    perUniqueMCS = []
    perUniqueBW = []
    perUniquePHY = []
    perUniqueNCS = []

    uniqueMCSIndex = np.unique(MCSIndex)
    uniqueBandwidth = ((np.unique(Bandwidth)))
    # uniquePHY = ((np.unique(PHY)))
    uniqueSpatial_stream = ((np.unique(Spatial_Stream)))

    for countMCS in uniqueMCSIndex:
        countUniqueMCSIndex.append(MCSIndex.count(countMCS))

    for cnt in countUniqueMCSIndex:
        perUniqueMCS.append(round((cnt * 100) / count, 2))

    dictMCS = dict(zip(uniqueMCSIndex,countUniqueMCSIndex))
    df_MCS = pd.DataFrame({" MCS ": [k for k in dictMCS.keys()], " Total Packets ": [i for i in dictMCS.values()]," Percentage ":[j for j in perUniqueMCS]})
    # df_MCS = df_MCS.T
    # df_MCS.columns = df_MCS.iloc[0]
    # df_MCS = df_MCS.drop(df_MCS.iloc[0].index.name)
    # print("df_MCS", df_MCS)

    df_MCS = df_MCS.to_html(index=False)
    dictMCSs = [i for i in dictMCS.keys()]
    plot4 = Plot()
    path = plot4.bar(datax=dictMCSs, datay=perUniqueMCS, title="MCS plot", xaxis="MCS", yaxis="Percentage",
                     figname="MCS")
    PacketInfo = ("Data packets having MCS field: "+str(vMCS)+"<br>")
    htmltable("Data MCS Histogram.", df_MCS, str(path), "0", "0",PacketInfo)

    # print(uniqueMCSIndex, countUniqueMCSIndex)

    for countBandwidth in uniqueBandwidth:
        countUniqueBandwidth.append(Bandwidth.count(countBandwidth))

    for cnt in countUniqueBandwidth:
        perUniqueBW.append(round((cnt * 100) / count, 2))

    dictBW = dict(zip(uniqueBandwidth, countUniqueBandwidth))
    df_BW = pd.DataFrame({" Bandwidth ": [k for k in dictBW.keys()], " Total Packets ": [i for i in dictBW.values()]," Percentage ":[j for j in perUniqueBW]})
    # df_BW = df_BW.T
    # df_BW.columns = df_BW.iloc[0]
    # df_BW = df_BW.drop(df_BW.iloc[0].index.name)
    # print("df_BW", df_BW)

    df_BW = df_BW.to_html(index=False)
    dictBWs = [i for i in dictBW.keys()]
    plot5 = Plot()
    path = plot5.bar(datax=dictBWs, datay=perUniqueBW, title="Bandwidth plot", xaxis="Bandwidth", yaxis="Percentage",
                     figname="Bandwidth")

    PacketInfo = ("Data packets having BW field: " + str(vBW) + "<br>")
    htmltable("Data Bandwidth Histogram.", df_BW, str(path), "0", "0",PacketInfo)

    # print(uniqueBandwidth, countUniqueBandwidth)

    """
    #For PHY
    for countPHY in uniquePHY:
        countUniquePHY.append(PHY.count(countPHY))
        
    for cnt in countUniquePHY:
        perUniquePHY.append(round((cnt * 100) / count, 2))
    
    dictPHY = dict(zip(uniquePHY, countUniquePHY))
    df_PHY = pd.DataFrame({"PHY": [k for k in dictPHY.keys()], "Packet": [i for i in dictPHY.values()],"Percentage":[j for j in perUniquePHY]})
    df_PHY = df_PHY.T
    df_PHY.columns = df_PHY.iloc[0]
    df_PHY = df_PHY.drop(df_PHY.iloc[0].index.name)
    print("df_PHY", df_PHY)
    """


    for countNCS in uniqueSpatial_stream:
        countUniqueSpatial_stream.append(Spatial_Stream.count(countNCS))

    for cnt in countUniqueSpatial_stream:
        perUniqueNCS.append(round((cnt * 100) / count, 2))

    dictNCS = dict(zip(uniqueSpatial_stream, countUniqueSpatial_stream))
    df_NCS = pd.DataFrame({" NSS ": [k for k in dictNCS.keys()], " Total Packets ": [i for i in dictNCS.values()]," Percentage ":[j for j in perUniqueNCS]})

    # df_NCS = df_NCS.T
    # df_NCS.columns = df_NCS.iloc[0]
    # df_NCS = df_NCS.drop(df_NCS.iloc[0].index.name)
    # print("df_NCS", df_NCS)
    # df_NCS = df_NCS.T
    df_NCS = df_NCS.to_html(index=False)
    dictNCSs = [i for i in dictNCS.keys()]
    plot6 = Plot()
    path = plot6.bar(datax=dictNCSs, datay=perUniqueNCS, title="NCS plot", xaxis="Spatial stream", yaxis="Percentage",
                     figname="NSS")
    PacketInfo = ("Data packets having NSS field: " + str(vNCS) + "<br>")
    htmltable("Data NSS Histogram.", df_NCS, str(path), "0", "0",PacketInfo)

def RateAMPDU(AMPDU,count):
    countAMPDU = []
    # print("IN AMPDU")
    # print("AMPDU: ",AMPDU)

    countUniqueAMPDU = []

    perUniqueAMPDU = []
    chainCountAMPDU = []

    uniqueAMPDU = np.unique(AMPDU)
    uniqueAMPDU = [i for i in uniqueAMPDU]

    # print("uniqueAMPDU",uniqueAMPDU)
    #
    # print("len(uniqueAMPDU)",len(uniqueAMPDU))

    for countAMPDU in uniqueAMPDU:
        countUniqueAMPDU.append(AMPDU.count(countAMPDU))

    # print("countUniqueAMPDU",countUniqueAMPDU)
    # print("len(countUniqueAMPDU)",len(countUniqueAMPDU))

    chainUniqueAMPDU = np.unique(countUniqueAMPDU)
    chainUniqueAMPDU = [i for i in chainUniqueAMPDU]

    # print("chainUniqueAMPDU", chainUniqueAMPDU)
    # print("len(chainUniqueAMPDU)", len(chainUniqueAMPDU))

    for Acount in chainUniqueAMPDU:
        chainCountAMPDU.append(countUniqueAMPDU.count(Acount))

    # print(" len(chainCountAMPDU): ", len(chainCountAMPDU))
    # print("chainCountAMPDU",chainCountAMPDU)

    UniqueChainCountAMPDU = np.unique(chainCountAMPDU)
    UniqueChainCountAMPDU = [i for i in UniqueChainCountAMPDU]

    listAMPDU = []
    for un in UniqueChainCountAMPDU:
        listAMPDU.append(chainCountAMPDU.count(un))



    print(chainUniqueAMPDU,chainCountAMPDU)
    dictAMPDU = dict(zip(chainUniqueAMPDU,chainCountAMPDU))

    for acnt in chainCountAMPDU:
        perUniqueAMPDU.append(round((acnt * 100) / count, 4))
    #
    # print("dictAMPDU",dictAMPDU)
    #
    # print("len(perUniqueAMPDU)",len(perUniqueAMPDU))
    # print("perUniqueAMPDU",perUniqueAMPDU)
    #
    df_AMPDU = pd.DataFrame({" Chain count ": [k for k in dictAMPDU.keys()], " Total Packets ": [i for i in dictAMPDU.values()],
                           " Percentage ": [j for j in perUniqueAMPDU]})
    # df_AMPDU = df_AMPDU.T
    # df_AMPDU.columns = df_AMPDU.iloc[0]
    # df_AMPDU = df_AMPDU.drop(df_AMPDU.iloc[0].index)
    # df_AMPDU = df_AMPDU.T
    df_AMPDU = df_AMPDU.to_html(index=False)
    # dictAMPDUs = [i for i in dictAMPDU.keys()]
    #
    plot6 = Plot()
    path = plot6.bar(datax=chainUniqueAMPDU, datay=perUniqueAMPDU, title="AMPDU plot", xaxis="packet Chain", yaxis="Percentage",
                     figname="AMPDU")
    PacketInfo = ("EMPTY")
    htmltable("AMPDU chain count Histogram.", df_AMPDU, str(path), "0", "0", PacketInfo)





class shark:
    def __init__(self):
        # FilePath having pcap file
        # self.FilePath = "wifi_diag.pcap"
        # self.FilePath = "C:\Candela\Scripts\Lanforge scripts\lanforge-scripts-master\wifi_diag\wifi_diag.pcapng"
        # self.FilePath = "wifi_diag.pcap"
        # self.FilePath = "C:\candela\pcap\wifi.pcapng"
        # self.FilePath = "C:\candela\pcap\\ac_28Sept.pcapng"
        # self.FilePath = "C:\candela\pcap\\11ax.pcapng"
        # self.FilePath = "C:\candela\pcap\\11ax_cap2_Copy.pcapng"
        # self.FilePath = "C:\candela\pcap\sta1.pcap"
        self.FilePath = output

        self.cap = pyshark.FileCapture(self.FilePath)
        # print("Strt time stamp :",datetime.datetime.now())

    def Extract(self):

        type_list = {"0": "Management frame", "1": "Control Frame", "2": "Data frame"}
        subtype_list = {"80": "Beacon frame", "d0": "Action", "b4": "Request-to-send", "d4": "Acknowledgement", \
                        "88": "QoS Data", "84": "Block Ack Req", "94": "Block Ack Req", \
                        "40": "Probe Request", "50": "Probe Response", "b0": "Authentication",
                        "a2": "Disassociate", "a8": "QoS Data + CF-Poll", "c8":"QoS Null function", \
                        "10": "Association Response", "00": "Association Request", "c4": "Clear-to-send", \
                        "98": "QoS Data + CF-Acknowledgment", "24": "Trigger", "28": "Data + CF-Poll" ,\
                        "d8": "Unknown", "54": "VHT/HE NDP Announcement", "e8": "QoS CF-Poll", \
                        "b8" : "QoS Data + CF-Ack + CF-Poll", "18": "Data + CF-Ack", "48" : "Null function", \
                        "69" : "CF-Poll", "08": "Data"
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
        """ Comment   
        """






        # print(wlan_radio_Fields_keys,wlan_radio_Fields_values)

        # if "wlan_radio.phy" and "wlan_radio.11ac.bandwidth" and "wlan_radio.11ac.mcs" and "wlan_radio.11ac.nss" in wlan_radio_Fields_keys:
        #     # print(dir(packet.wlan_radio._all_fields["wlan_radio.phy"]))
        #     # print(packet.wlan_radio._all_fields["wlan_radio.phy"].showname_value) #for PHY
        #     # print(packet.wlan_radio._all_fields["wlan_radio.11ac.bandwidth"].showname_value) #for BW
        #     # print(packet.wlan_radio._all_fields["wlan_radio.11ac.mcs"].showname_value) #for MCS
        #     # print(packet.wlan_radio._all_fields["wlan_radio.11ac.nss"].showname_value) #for Spatial streams
        #     PHY.append(packet.wlan_radio._all_fields["wlan_radio.phy"].showname_value)
        #     Bandwidth.append(packet.wlan_radio._all_fields["wlan_radio.11ac.bandwidth"].showname_value)
        #     MCSIndex.append(packet.wlan_radio._all_fields["wlan_radio.11ac.mcs"].showname_value)
        #     Spatial_Stream.append(packet.wlan_radio._all_fields["wlan_radio.11ac.nss"].showname_value)

        # _data = (packet.wlan_radio._all_fields)
        # print(type(_data))
        # phy, _11ac_short_gi, _11ac_bandwidth, _11ac_user, _11ac_mcs, _11ac_nss, _11ac_fec, _data_rate = (packet.wlan_radio._all_fields)
        # print(phy.get_field_value)


        """
        comment
        """


        for packet in self.cap:
            count += 1

            # print("Count :",end= " ")
            print(count)


            try:
                WLAN_RADIO = packet.wlan_radio
                wlan_radio_Fields_keys = []
                wlan_radio_Fields_values = []

                for keys, values in packet.wlan_radio._all_fields.items():
                    # print(keys, ":", values)
                    wlan_radio_Fields_keys.append(keys)
                    wlan_radio_Fields_values.append(values)
                # print("---------------------------------------------")

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

                print("\r"+count,":",packet.wlan_radio._all_fields.items())


                # if "wlan_radio.11ac.bandwidth" and "wlan_radio.11ac.bandwidth" and "wlan_radio.phy" and \
                #         "wlan_radio.11ac.mcs" and "wlan_radio.11ac.nss" in wlan_radio_Fields_keys:
                    # print(dir(packet.wlan_radio._all_fields["wlan_radio.phy"]))
                    # print(packet.wlan_radio._all_fields["wlan_radio.phy"].showname_value) #for PHY
                    # print(packet.wlan_radio._all_fields["wlan_radio.11ac.bandwidth"].showname_value) #for BW
                    # print(packet.wlan_radio._all_fields["wlan_radio.11ac.mcs"].showname_value) #for MCS
                    # print(packet.wlan_radio._all_fields["wlan_radio.11ac.nss"].showname_value) #for Spatial streams

                # if "wlan_radio.phy" in wlan_radio_Fields_keys:
                #     PHY.append(packet.wlan_radio._all_fields["wlan_radio.phy"].showname_value)
                #     vPHY +=1
                # else:
                #     vNotPHY +=1
                #     # print("PHY NF")
                #
                # if "wlan_radio.11ac.bandwidth" in wlan_radio_Fields_keys:
                #     Bandwidth.append(packet.wlan_radio._all_fields["wlan_radio.11ac.bandwidth"].showname_value)
                #     vBW +=1
                # else:
                #     vNotBW += 1
                #     # print("Bandwidth NF")
                #
                # if "wlan_radio.11ac.mcs" in wlan_radio_Fields_keys:
                #     MCSIndex.append(packet.wlan_radio._all_fields["wlan_radio.11ac.mcs"].showname_value)
                #     vMCS +=1
                # else:
                #     vNotMCS +=1
                #     # print("MCS Index NF")
                #
                # if "wlan_radio.11ac.nss" in wlan_radio_Fields_keys:
                #     Spatial_Stream.append(packet.wlan_radio._all_fields["wlan_radio.11ac.nss"].showname_value)
                #     vNCS += 1
                # else:
                #     vNOTNCS += 1
                #     # print("Spatial stream NF")
            except:
                pass

        # print("Here")
        # print("MCSIndex",len(MCSIndex),MCSIndex)
        # print("Bandwidth",len(Bandwidth),Bandwidth)
        # print("PHY",len(PHY),PHY)
        # print("Spatial_Stream",len(Spatial_Stream),Spatial_Stream)
        if vAMPDU != 0:
            RateAMPDU(AMPDU,count)

        # print("Data Frames: ",vDataType)

        # if vax11 == 1:
        #     print("vNOTNCS :", vNOTNCS, "vNotBW :", vNotBW, "vNotMCS:", vNotMCS, "vNotPHY:", vNotPHY)
        #     PHY_BW_MCS_NCS_11ax(MCSIndex, vMCS, vNotMCS, Bandwidth, vBW, vNotBW, PHY, vPHY, vNotPHY, count)
        # else:
        # print("vNotBW :",vNotBW,"vNotMCS:",vNotMCS,"vNotPHY:",vNotPHY)
        PHY_BW_MCS_NCS(MCSIndex, vMCS, Bandwidth, vBW, PHY, vPHY, Spatial_Stream, vNCS,  count)



        # print("After appending time stamp :", datetime.datetime.now())
        RateHistogram(DataRate, PhyType, SignalStrength, count)
        # print("After RateHist time stamp :", datetime.datetime.now())
        PacketHistogram(subtype_list, Managementls, Controlls, Data_framels, count)
        # print("After PacketHist time stamp :", datetime.datetime.now())



if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="To create a single pcap file combining multiple pcap files")
    # parser.add_argument("-o", "--output", type=str, help="Enter the output pcap file name")
    parser.add_argument("-i", "--input", type=str,
                        help="Enter the Name of the pcap files which needs to be combined")

    args = None

    try:
        args = parser.parse_args()
        output = "wifi_diag.pcap"

        if (args.input is not None):
            input = args.input  # 'C:\candela\pcap\\11ax.pcapng','C:\candela\pcap\sta1.pcap'
            input = input.split(",")
            print(input)

        # if (args.input is None):
        #     input = "11ax.pcapng", "sta1.pcap"

    except Exception as e:
        logging.exception(e)
        exit(2)

    with open(output, 'wb') as wfd:
        print("input", input)
        for f in (input):
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd)

    htmlstart()
    downloadBtn()
    htmlobj("This is HTML objective")

    htmlpointview()
    htmlTableSummary("This is html table summary")
    myUL()


    Extract = shark()
    Extract.Extract()
    # htmltable()

    closemyUl()
    htmlclose()


