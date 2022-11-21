#!/usr/bin/python3
"""
NAME: lf_tx_power_dbm_tool.py

PURPOSE:
calcuate the combined spatial stream power.

EXAMPLE:


LICENSE:
    Free to distribute and modify. LANforge systems must be licensed.
    Copyright 2022 Candela Technologies Inc


INCLUDE_IN_README

NOTE: To convert the per spatial stream dBm to combined dBm
convert dBm to watts (power) for each spatial stream,  add the power values then convert back to dBm
https://www.rapidtables.com/convert/power/dBm_to_Watt.html
https://www.rapidtables.com/convert/power/Watt_to_dBm.html

Thank-you to:
https://www.thepacketologist.com/2021/10/power-conversion-in-python/

"""

import argparse
import math
import importlib

# TODO set up with logger
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

def convert_input():
    value = input("Whate is the numberical value of teh unit of power?:").lower()
    unit = ""
    while unit == "":
        unit = input("What unit would you like to convert this too? (dBm/mW): ").lower()
        if unit == "dbm" or unit =="mw":
            unit = unit
        else:
            unit = ""
    return value, unit

def convert_dbm_to_mw(value):
    # P(mW) = 1W * 10(P(dBm) / 10)
    dbm = int(value)
    mw = 1 * 10 ** (dbm/10)
    print(f"{dbm} dBm = {round(mw, 8)} mW")
    return mw

def convert_mw_to_dbm(value):
    # P(dBm) = 10 * log10( P(mW) / 1mW)
    mw = value
    dbm = 10 * math.log10(mw/1)
    print(f"{round(mw,8)} mW = {round(dbm, 8)} dBm")
    return dbm

def convert_per_ss_dbm_to_combined(ss_list):
    total_mw = 0.0
    for value in ss_list:
        value = int(value)
        print("dbm value {value}".format(value=value))
        mw = convert_dbm_to_mw(value)
        print("mw: {mw}".format(mw=round(mw,8)))
        total_mw += mw
    
    print("total_mw: {total_mw}".format(total_mw=round(total_mw,8)))

    combined_dbm = convert_mw_to_dbm(total_mw)
    print("combined_dbm = {combined_dbm}".format(combined_dbm=round(combined_dbm,8)))

    return combined_dbm
    

def main():
    parser = argparse.ArgumentParser(
        description="Convert power values from dBm to mW or mW to dBm"
    )
    
    parser.add_argument(
        "--dbm",
        "--dbm2mw",
        dest="dbm2mw",
        help="Converts value from dBm to mW",
        metavar="10",
        type=int,
    )
    parser.add_argument(
        "--ss_dbm",
        "--ss_list_dbm",
        dest="ss_list_dbm",
        help="pass in a spatial stream list --ss_dbm '-55 -53 -60 -22",
        type=str,
    )

    parser.add_argument(
        "--mw",
        "--mw2dbm",
        dest="mw2dbm",
        help="Converts value from mW to dBm.",
        metavar="50",
        type=float,
    )

    args = parser.parse_args()
    if args.dbm2mw is not None or args.mw2dbm is not None or args.ss_list_dbm:
        if args.dbm2mw:
            convert_dbm_to_mw(args.dbm2mw)
        elif args.mw2dbm:
            convert_mw_to_dbm(args.mw2dbm)
        else:
            convert_per_ss_dbm_to_combined(args.ss_list_dbm.split())
    else:
        value, unit = convert_input()
        if unit == "mw":
            convert_dbm_to_mw(value)
        elif unit == "dbm":
            convert_mw_to_dbm(value)

if __name__ == "__main__":
    main()


