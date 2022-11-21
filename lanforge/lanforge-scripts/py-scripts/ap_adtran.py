#!/usr/bin/env python3
import argparse
import sys
import os
import logging
import importlib
import pandas as pd
import json
import pexpect
import time
from time import sleep


'''
NAME: Adtran.py

PURPOSE: To return information/headers from teh AP and then format them into a CSV file format for testing

EXAMPLE: description = "args": ["--ap_user", "USER", "--ap_password", "PASS", "--mux_host", "192.168.1.102", "--mux_port", "23200", "--scheme", "mux_client", "--action", "cmd", "--value", "cat /proc/meminfo;top -b -n 1;cat /sys/class/thermal/thermal_zone*/temp", "--prompt", "841-t6-C160-linux:", "--log_level", "info"] 

NOTES:
    "--value" should be a list of commands that is sepeareted by semicolons
    
    right now it only prings out the information for the commands that are listed in the example


STATUS: INPROGRESS

'''




sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")





# see https://stackoverflow.com/a/13306095/11014343
logger = logging.getLogger(__name__)
class FileAdapter(object):
    def __init__(self, logger):
        self.logger = logger

    def write(self, data):
        # NOTE: data can be a partial line, multiple lines
        data = data.strip()  # ignore leading/trailing whitespace
        if data:  # non-blank
            self.logger.debug(data)
    def flush(self):
        pass  # leave it to logging to flush properly




global logfile
global output
global info_list


AP_ESCAPE       = "Escape character is '^]'."
AP_USERNAME     = "login: "
AP_PASSWORD     = "Password: "
AP_EN           = "en"
AP_MORE         = "--More--"
AP_EXIT         = "exit"
LF_PROMPT       = "$"
CR = "\r\n"
NL = "\n"


class ap_adtran():
    
    def __init__(self,
                #lf_mgr,
                #lf_port,
                #lf_user,
                #lf_passwd,
                #resource,
                #port,
                ap_password,
                ap_user,
                mux_host,
                mux_port,
                scheme,
                prompt=None,
                user=None,
                password=None):                
        #self.lf_mgr = lf_mgr
        #self.lf_port = lf_port
        #self.lf_user = lf_user
        #self.lf_passwd = lf_passwd
        #self.resource = resource
        #self.port = port
        self.ap_user = ap_user
        self.ap_password = ap_password
        self.mux_host = mux_host
        self.mux_port = mux_port
        self.scheme = scheme
        self.prompt = prompt
        self.user = user
        self.password = password
        self.ap_file = None
        self.action = None
        self.value = None
        _ap_headers = ['Date', 'CPU', 'meminfo', 'Temperature']
        
    '''
    put in functions for adtran ap
    '''
    
    def ap_action(self):
        
        if (self.scheme == "mux_client"):
            # TODO: put a print statement that indicates that mux_sever must be running before usage
            # sudo ./mux_server.py --device /dev/ttyUSB0 --baud 115200 --port 23200
            # for client                
            cmd = "./mux_client.py --host {host} --port {port}".format(host=self.mux_host,port=self.mux_port)
            logger.info("Spawn: "+cmd+NL)
            egg = pexpect.spawn(cmd)
            egg.logfile = FileAdapter(logger)
        
        
        if self.ap_file is not None:
            ap_file = open(str(self.ap_file), "a")
            ap_file.write(ap_results)
            ap_file.close()
            logger.info("ap file written {}".format(str(self.ap_file)))
        
        
        if self.scheme == 'mux_client' or self.prompt is None:
            AP_PROMPT       = "#"
            MUX_PROMPT      = "MUX >"
        else:
            AP_PROMPT       = "{}".format(self.prompt)
            MUX_PROMPT      = "MUX >"


        
        time.sleep(0.1)
        logged_in  = False
        loop_count = 0
        while (loop_count <= 8 and logged_in == False):
            loop_count += 1
            try:
                i = egg.expect_exact([AP_ESCAPE,AP_PROMPT,AP_USERNAME,AP_PASSWORD,AP_MORE,LF_PROMPT,MUX_PROMPT,pexpect.TIMEOUT],timeout=5)
                logger.info(i)
            except BaseException:
                logger.info("pexcept exception the connection may not be present, exiting")
                exit(1)
            # AP_ESCAPE
            if i == 0:
                logger.info("Expect: {} i: {} before: {} after: {}".format(AP_ESCAPE,i,egg.before,egg.after))
                egg.sendline(CR) # Needed after Escape or should just do timeout and then a CR?
                sleep(1)
            # AP_PROMPT
            if i == 1:
                logger.info("Expect: {} i: {} before: {} after: {}".format(AP_PROMPT,i,egg.before,egg.after))
                logged_in = True 
                sleep(1)
            # AP_USERNAME
            if i == 2:
                logger.info("Expect: {} i: {} before: {} after: {}".format(AP_USERNAME,i,egg.before,egg.after))
                egg.sendline(self.ap_user) 
                sleep(2)
            # AP_PASSWORD
            if i == 3:
                logger.info("Expect: {} i: {} before: {} after: {}".format(AP_PASSWORD,i,egg.before,egg.after))
                egg.sendline(self.ap_password) 
                sleep(2)
            # AP_MORE
            if i == 4:
                logger.info("Expect: {} i: {} before: {} after: {}".format(AP_MORE,i,egg.before,egg.after))
                if (self.scheme == "serial"):
                    egg.sendline("r")
                else:
                    egg.sendcontrol('c')
                sleep(1)
            # for Testing serial connection using Lanforge
            # LF_PROMPT
            if i == 5:
                logger.info("Expect: {} i: {} before: {} after: {}".format(LF_PROMPT,i,egg.before.decode('utf-8', 'ignore'),egg.after.decode('utf-8', 'ignore')))
                if (loop_count < 3):
                    egg.send("ls -lrt")
                    sleep(1)
                if (loop_count > 4):
                    logged_in = True # basically a test mode using lanforge serial
            # MUX_PROMPT
            if i == 6:
                logger.info("Received MUX prompt, send carriage return")
                logger.info("Expect: {} i: {} before: {} after: {}".format("Timeout",i,egg.before,egg.after))
                egg.sendline(CR) 
                sleep(1)
            # TIMEOUT
            if i == 7:
                logger.info("Expect: {} i: {} before: {} after: {}".format("Timeout",i,egg.before,egg.after))
                #egg.sendline(CR) 
                sleep(1)
            
        stat_inc = 0
        info_list = list()
        temp = []
        if (self.action == "cmd"):
            commands = self.value.split(";")
            print(commands)
            for command in commands:
                if command == "headers":
                    print("MemTotal,MemFree,MemAvailable,Buffers")
                else:     
                    #print(command)
                    logger.info("execute: {command}".format(command=command))
                    egg.sendline(command)
                    egg.expect([pexpect.TIMEOUT], timeout=7)  # do not delete this for it allows for subprocess to see output
                    #logger.info(egg.before.decode('utf-8', 'ignore')) # do not delete this for it  allows for subprocess to see output
                    output = egg.before.decode('utf-8', 'ignore')
                    
                    '''
                    i = egg.expect_exact([AP_MORE,pexpect.TIMEOUT],timeout=5)
                    if i == 0:
                        egg.sendcontrol('c')
                    if i == 1:
                        logger.info("send cntl c anyway")
                        egg.sendcontrol('c')
                
                
                    '''
                    '''
                    print("START")
                    for i in range(len(info_list)):
                        print(info_list[i])
                    print("END")

                    #logger.info(output)
                    '''
                    
                    '''
                    proess string into list
                    run list

                    logger.info("execute: {command}".format(command=command))
                    egg.sendline(command)
                    egg.expect([pexpect.TIMEOUT], timeout=7)  # do not delete this for it allows for subprocess to see output
                    print(egg.before.decode('utf-8', 'ignore')) # do not delete this for it  allows for subprocess to see output
                    i = egg.expect_exact([AP_MORE,pexpect.TIMEOUT],timeout=5)
                    if i == 0:
                        egg.sendcontrol('c')
                    if i == 1:
                        logger.info("send cntl c anyway")
                        egg.sendcontrol('c')
                    '''
                
            temp = output.split(CR) # need to clear the value of temp before moving on to next command
                    
            for i in range(len(temp)):
                    #print("line " + str(i) + ": " +  temp[i])
                    if  temp[i].strip() == "top -b -n 1" :
                        info_list.append(temp[i].strip())
                        info_list.append(temp[i + 1].strip())
                        info_list.append(temp[i + 2].strip())
                        info_list.append(temp[i + 3].strip())
                        #info_list.append(temp[i + 4].strip())
                                
                                

                    elif temp[i].strip() == "cat /proc/meminfo":
                        info_list.append(temp[i].strip())
                        info_list.append(temp[i + 1].strip())
                        info_list.append(temp[i + 2].strip())
                        info_list.append(temp[i + 3].strip())
                        info_list.append(temp[i + 4].strip())
                                
                                

                    elif temp[i].strip() == "cat /sys/class/thermal/thermal_zone*/temp":
                        info_list.append(temp[i].strip())
                        info_list.append(temp[i + 1].strip())
        
        return info_list

               
                
                

           
           
        
        
            
        
    
    '''
     seperates the info from info_list and then creates a csv entry that will then be insereted into the csv file
    '''
    def create_csv(self, list_info):
        entries = []
        for i in range(len(list_info)):
            print(list_info[i])
        for i in range(len(list_info)):
            if list_info[i] == "cat /proc/meminfo":
                entries.append(list_info[i + 1][list_info[i + 1].find(":") + 1:list_info[i + 1].rfind("k")].strip())
                entries.append(list_info[i + 2][list_info[i + 2].find(":") + 1:list_info[i + 2].rfind("k")].strip())
                entries.append(list_info[i + 3][list_info[i + 3].find(":") + 1:list_info[i + 3].rfind("k")].strip())
                entries.append(list_info[i + 4][list_info[i + 4].find(":") + 1:list_info[i + 4].rfind("k")].strip())
                
            elif list_info[i] == "top -b -n 1":
                line_one = list_info[i + 1].split(" ")
                line_two = list_info[i + 2].split(" ")
                line_three = list_info[i + 3].split(" ")

                #print(line_one)
                entries.append(line_one[2])
                entries.append(line_one[7])
                entries.append(line_one[12][:line_one[12].find(",")])
                entries.append(line_one[13][:line_one[13].find(",")])
                entries.append(line_one[14])
                entries.append(line_two[1])
                entries.append(line_two[5])
                entries.append(line_two[7])
                entries.append(line_two[1])
                entries.append(line_three[5])
                #print(line_one[2], line_one[7], line_one[12][:line_one[12].find(",")], line_one[13][:line_one[13].find(",")], line_one[14])
                #print(line_two)
                #print(line_three)
                

                
            elif list_info[i] == "cat /sys/class/thermal/thermal_zone*/temp":
                return

        print(entries)
         

    


    def get_CPU(self):
        '''
        use the top command and CPU stat commands go get info from cpu and return only the relevant lines
        '''
        logger.info("0.05 0.11 0.09 1/132 13830")
        CPU_info = "0.05 0.11 0.09 1/132 13830"
        return CPU_info

    def get_meminfo(self):
        '''
        use the command meminfo and gather relevant data such as current memory data
        '''
        return
    
    def make_csv(self):
        '''
        from all data gathered, with timestamps make an ordered csv with proper headers for information gathered about AP during testing
        '''
        return
    
    def return_headers(self):
        '''
        return headers for the csv format
        '''
        return
    
    def return_data(self):
        '''

        '''
        return
    
    




def main():
    '''
    first connect to mux_client from here, then log into adtran ap
    '''
    adtran_host = "localhost"
    adtran_port = 8080
    
    parser = argparse.ArgumentParser(
    prog="ap_adtran.py",
    formatter_class=argparse.RawTextHelpFormatter,
    description="""
    example
    Adtran script for returning AP information
    """)
    
    parser.add_argument("--lf_mgr", type=str, help="address of the LANforge GUI machine (localhost is default)",
                    default='localhost')
    parser.add_argument("--lf_port", help="IP Port the LANforge GUI is listening on (8080 is default)",
                        default=8080)
    parser.add_argument("--lf_user", type=str, help="user: lanforge")
    parser.add_argument("--lf_passwd", type=str, help="passwd: lanforge")
    
    parser.add_argument("--resource", type=str, help="LANforge Station resource ID to use, default is 1", default=1)
    parser.add_argument('--log_level', default=None, help='Set logging level: debug | info | warning | error | critical')

    parser.add_argument("--ap_user", type=str, help="--ap_user 'username'")
    parser.add_argument("--ap_password", type=str, help="--ap_password 'password'")
    parser.add_argument("--mux_host", type=str, help=" --mux_host 127.0.0.1", default='127.0.0.1')
    parser.add_argument("--mux_port", type=int, help=" --mux_port 23200", default=23200)
    parser.add_argument("--scheme", type=str, help= "--scheme mux_serial", default='mux_serial')
    parser.add_argument("--prompt", type=str, help="--prompt '841-t6-C160-linux: ~ #'", default='841-t6-C160-linux: ~ #')
    parser.add_argument("--action",  type=str, help="action,  cmd")
    parser.add_argument("--value",   type=str, help="value,  cmd value")

    
    # logging configuration
    parser.add_argument(
        "--lf_logger_config_json",
        help="--lf_logger_config_json <json file> , json configuration of logger")
    # TODO check command
    parser.add_argument("--get_requests", type=str, help="perform get request may be a list:  port | radio | port_rssi")
    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    # set the logger level to debug
    if args.log_level:
        logger_config.set_level(level=args.log_level)

    
        
    
    # lf_logger_config_json will take presidence to changing debug levels
    if args.lf_logger_config_json:
        # logger_config.lf_logger_config_json = "lf_logger_config.json"
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()
    
    ap = ap_adtran(
                ap_user=args.ap_user,
                ap_password=args.ap_password,
                mux_host=args.mux_host,
                mux_port=args.mux_port,
                scheme=args.scheme,
                prompt=args.prompt)

    CPU = ap.get_CPU()
    ap.action = args.action
    ap.value = args.value
    listinfo = ap.ap_action()
    ap.create_csv(listinfo)
    logger.info("CPU information {CPU}".format(CPU=CPU))

if __name__ == '__main__':
    main()