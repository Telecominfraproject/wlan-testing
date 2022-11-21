#!/usr/bin/env python3
"""
NAME: lf_interop_modify.py

PURPOSE: Call commands/modifications to Interop Devices

EXAMPLE:
$ ./lf_interop_modify.py gui 1 1 KEBE2021070849 --display 192.168.100.220 --screensize 0.4

NOTES:
#Currently these commands are broken due to an error in the Adb cli command handling.
#@TODO finish logic for MODIFY (batch modify) commands


TO DO NOTES:

"""

import sys

if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit()
import os
import importlib
import argparse
import pprint
import logging
from pprint import pprint
from urllib.parse import urlparse
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
lanforge_api = importlib.import_module("lanforge_client.lanforge_api")
from lanforge_client.lanforge_api import LFSession
from lanforge_client.lanforge_api import LFJsonCommand
from lanforge_client.lanforge_api import LFJsonQuery
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm

lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")
logger = logging.getLogger(__name__)

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
class InteropCommands(Realm):
    def __init__(self,
                 _host=None,
                 _port=None,
                 device_eid=None,
                 launch_gui=None,
                 install=None,
                 install_g=None,
                 wifi=None,
                 start=False,
                 stop=False,
                 log_dur=0,
                 apply=False,
                 mgr_ip=None,
                 user_name=None,
                 ssid=None,
                 passwd=None,
                 crypt=None,
                 screen_size_prcnt=None,
                 log_destination=None,
                 adb_username=None,
                 set_adb_user_name=False,
                 list_ntwk=False,
                 forget_netwrk=False,
                 ntwk_id=None,
                 _proxy_str=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(lfclient_host=_host,
                         debug_=_debug_on)
        self.device_eid = device_eid
        self.screen_size_prcnt = screen_size_prcnt
        self.launch_gui = launch_gui
        self.install = install
        self.install_g = install_g
        self.wifi = wifi
        self.start = start
        self.stop = stop
        self.log_dur = log_dur
        self.apply = apply
        self.mgr_ip = mgr_ip
        self.user_name = user_name
        self.ssid = ssid
        self.passwd = passwd
        self.crypt = crypt
        self.log_destination = log_destination
        # we cannot assume port 8080 because some labs use port translation
        self.debug = _debug_on
        self.set_adb_user_name = set_adb_user_name
        self.adb_username = adb_username
        self.list_ntwk = list_ntwk
        self.forget_netwrk = forget_netwrk
        self.ntwk_id = ntwk_id
        self.session = LFSession(lfclient_url=_host,
                                 debug=_debug_on,
                                 connection_timeout_sec=2.0,
                                 stream_errors=True,
                                 stream_warnings=True,
                                 require_session=True,
                                 exit_on_error=_exit_on_error)
        self.command: LFJsonCommand
        self.command = self.session.get_command()
        self.query: LFJsonQuery
        self.query = self.session.get_query()

    def run(self):
        if not self.device_eid:
            raise ValueError("device EID is required")

        eid = self.name_to_eid(self.device_eid)
        pprint(eid)

        cmd = None
        if self.launch_gui:
            self.command.post_adb_gui(shelf=eid[0],
                                      resource=eid[1],
                                      adb_id=eid[2],
                                      display=self.launch_gui,
                                      screen_size_prcnt=self.screen_size_prcnt,
                                      debug=self.debug)

        elif self.log_dur > 0:
            if not self.log_destination:
                raise ValueError("adb log capture requires log_destination")
            user_key = self.session.get_session_based_key()
            if self.debug:
                print("====== ====== destination [%s] dur[%s] user_key[%s] " %
                      (self.log_destination, self.log_dur, user_key))
                self.session.logger.register_method_name("json_post")
            json_response = []
            self.command.post_log_capture(shelf=eid[0],
                                          resource=eid[1],
                                          p_type="adb",
                                          identifier=eid[2],
                                          duration=self.log_dur,
                                          destination=self.log_destination,
                                          user_key=self.session.get_session_based_key(),
                                          response_json_list=json_response,
                                          debug=True)
            print(json_response)

        else:
            if self.install or self.install_g:
                fname = self.install
                cmd = "install -r -t "
                if self.install_g:
                    fname = self.install_g
                    cmd += "-g "
                cmd += "-d " + fname.strip()

            elif self.wifi:
                if not (self.wifi == "enable" or self.wifi == "disable"):
                    raise ValueError("wifi arg value must either be enable or disable")
                cmd = "shell svc wifi " + self.wifi

            elif self.start:
                cmd = "shell am start --es auto_start 1 -n com.candela.wecan/com.candela.wecan.StartupActivity"

            elif self.stop:
                cmd = "shell am force-stop com.candela.wecan"

            elif self.apply:
                if not self.user_name:
                    raise ValueError("please specify a user-name when configuring this Interop device")
                cmd = "shell am start -n com.candela.wecan/com.candela.wecan.StartupActivity "
                cmd += "--es auto_start 1 --es username " + self.user_name
                if self.mgr_ip:
                    cmd += " --es serverip " + self.mgr_ip
                if self.ssid:
                    cmd += " --es ssid " + self.ssid
                if self.passwd:
                    cmd += "--es password " + self.passwd
                if self.crypt:
                    cmd += " --es encryption " + self.crypt

            elif self.list_ntwk:
                # adb 1 1 RZ8RA1053HJ NA shell cmd -w wi-fi list-networks
                cmd = "shell cmd -w wifi list-networks"

            elif self.forget_netwrk:
                cmd = "shell cmd -w wifi forget-network " + str(self.ntwk_id)

            # print(cmd)
            response_list = []
            errors_warnings = []

            adb_key = self.session.get_session_based_key()
            self.session.logger.error("adb_key: " + adb_key)
            self.command.post_adb(shelf=eid[0],
                                  resource=eid[1],
                                  adb_id=eid[2],
                                  key=adb_key,
                                  adb_cmd=cmd,
                                  debug=self.debug,
                                  response_json_list=response_list,
                                  errors_warnings=errors_warnings,
                                  suppress_related_commands=True)
            # print(["Response", response_list])


        # to set adb_username
        if self.set_adb_user_name:
            self.command.post_add_adb(adb_device=None,
                                      adb_id=eid[2],
                                      adb_model=None,
                                      adb_product=None,
                                      lf_username=self.adb_username,
                                      resource=eid[1],
                                      shelf=eid[0],
                                      debug=True)

    def main_adb_post(self, cmd=None):
        print("cmd", cmd)
        if not self.device_eid:
            raise ValueError("device EID is required")

        eid = self.name_to_eid(self.device_eid)
        pprint(eid)

        response_list = []
        errors_warnings = []

        adb_key = self.session.get_session_based_key()
        self.session.logger.error("adb_key: " + adb_key)
        self.command.post_adb(shelf=eid[0],
                              resource=eid[1],
                              key=adb_key,
                              adb_id=eid[2],
                              adb_cmd=cmd,
                              debug=self.debug,
                              response_json_list=response_list,
                              errors_warnings=errors_warnings,
                              suppress_related_commands=True)
        print(["Response", response_list])
        return response_list

    def get_device_state(self):
        cmd = 'shell dumpsys wifi | grep "mWifiInfo SSID"'
        x = self.main_adb_post(cmd=cmd)
        y = x[0]['LAST']['callback_message']
        z = y.split(" ")
        # print(z)
        state = None
        if 'state:' in z:
            print("yes")
            ind = z.index("state:")
            print(ind)
            st = z[(int(ind) + 1)]
            print("state", st)
            state = st

        else:
            print("state is not present")
            state = "NA"
        return state

    def get_device_ssid(self):
        cmd = 'shell dumpsys wifi | grep "mWifiInfo SSID"'
        x = self.main_adb_post(cmd=cmd)
        y = x[0]['LAST']['callback_message']
        z = y.split(" ")
        print(z)
        ssid = None
        if 'SSID:' in z:
            print("yes")
            ind = z.index("SSID:")
            ssid  = z[(int(ind) + 1)]
            ssid_ = ssid.strip()
            ssid_1 = ssid_.replace('"', "")
            ssid_2 = ssid_1.replace(",", "")
            print("ssid", ssid_2)
            ssid = ssid_2
        else:
            print("ssid is not present")
            ssid = "NA"
        return ssid

    def get_wifi_health_monitor(self, ssid):
        cmd = "shell dumpsys wifi | sed -n '/^WifiHealthMonitor - Log Begin ----$/,/^WifiHealthMonitor - Log End ----$/{/^WifiHealthMonitor - Log End ----$/!p;}'"
        x = self.main_adb_post(cmd=cmd)
        y = x[0]["LAST"]["callback_message"]
        z = y.split(" ")
        # print(z)
        value = ["ConnectAttempt", "ConnectFailure", "AssocRej", "AssocTimeout" ]
        return_dict = dict.fromkeys(value)
        if "stats\nSSID:" in z:
            ind = z.index("stats\nSSID:")
            ssid_ = z[ind + 1]
            print(ssid_)
            ssid_1 = ssid.strip()
            ssid_2 = ssid_1.replace('"', "")

            if ssid_2 == ssid:
                if "ConnectAttempt:" in z:
                    connect_ind = z.index("ConnectAttempt:")
                    connect_attempt = z[connect_ind + 1]
                    print("connection attempts", connect_attempt)
                    return_dict["ConnectAttempt"] = connect_attempt
                if 'ConnectFailure:' in z:
                    connect_fail_ind = z.index('ConnectFailure:')
                    connect_failure = z[connect_fail_ind + 1]
                    print("connection failure ", connect_failure)
                    return_dict["ConnectFailure"] = connect_failure
                if 'AssocRej:' in z:
                    ass_rej_ind = z.index('AssocRej:')
                    assocrej = z[ass_rej_ind + 1]
                    print("association rejection ", assocrej)
                    return_dict["AssocRej"] = assocrej
                if 'AssocTimeout:' in z:
                    ass_ind = z.index('AssocTimeout:')
                    asso_timeout = z[ass_ind + 1]
                    print("association timeout ", asso_timeout)
                    return_dict["AssocTimeout"] = asso_timeout
            else:
                print("ssid is not present")
        print(return_dict)
        return return_dict



# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
def main():
    desc = """modifies interop device 
    Operations: 
    *    Example of loading Interop GUI: 
    lf_interop_modify.py --show_gui 192.168.100.202:1 --device 1.1.KEBE2021070849 --screensize 0.4
    *    Example of installing APK: 
    lf_interop_modify.py --install_g interop-5.4.5.apk --device 1.1.KEBE2021070849
    *    Example of capturing logs 
    lf_interop_modify.py --log_dur 5 --device 1.1.KEBE2021070849 --log_destination foo4.txt
    *    Examples of enabling/disabling wifi
    lf_interop_modify.py --wifi enable --device 1.1.KEBE2021070849
    lf_interop_modify.py --wifi disable --device 1.1.KEBE2021070849
    *    Examples of starting/stopping Interop app
    lf_interop_modify.py --start --device 1.1.KEBE2021070849
    lf_interop_modify.py --stop --device 1.1.KEBE2021070849
    *    Example of applying WiFi connection changes
    lf_interop_modify.py --apply --device 1.1.KEBE2021070849 --ssid candela-10g --user_name foobar22
    * Example for applying adb_username
    lf_interop_modify.py --host 192.168.1.31 --device 1.1.RZ8RA1053HJ --set_adb_user_name --adb_username device_1
    * Example for getting network-id list
    lf_interop_modify.py --host 192.168.1.31 --device 1.1.RZ8RA1053HJ --list_ntw
    * Example to forget a network
    lf_interop_modify.py --host 192.168.1.31 --device 1.1.RZ8RA1053HJ --ntwk_id 2  --forget_netwrk
    """

    parser = argparse.ArgumentParser(
        prog=__file__,
        formatter_class=argparse.RawTextHelpFormatter,
        description=desc)

    parser.add_argument("--debug", help='turn on debugging', action="store_true")
    parser.add_argument("--host", "--mgr", default='localhost',
                        help='specify the GUI to connect to, assumes port 8080')

    parser.add_argument('--show_gui', '--gui', type=str, default='',
                        help='Display the Android GUI on this X-windows display address (IP:display). '
                        'EG: 192.168.100.264:0.0')

    parser.add_argument('--install', '--i', type=str, default='',
                        help='Install apk with this filename')

    parser.add_argument('--install_g', '--ig', type=str, default='',
                        help='Install apk with this filename, adding the -g flag')

    parser.add_argument('--wifi', '--w', type=str, default='',
                        help='Enable or disable WiFi (enable | disable)')

    parser.add_argument('--start', action="store_true",
                        help='Start the LANforge Interop GUI')

    parser.add_argument('--stop', action="store_true",
                        help='Stop the LANforge Interop GUI')

    parser.add_argument('--apply', action="store_true",
                        help='Apply changes for (LF Mgr IP, Encryption, SSID, Passwd')

    parser.add_argument('--mgr_ip', type=str, default='',
                        help='APPLY: IP address of the LF Manager managing this Interop device')

    parser.add_argument('--user_name', '--un', type=str, default='',
                        help='APPLY: Interop device user name')

    parser.add_argument('--ssid', type=str, default='',
                        help='APPLY: SSID for Interop device WiFi connection')

    parser.add_argument('--crypt', '--enc', type=str, default='',
                        help='APPLY: Encryption for Interop device WiFi connection')

    parser.add_argument('--passwd', '--pw', type=str, default='',
                        help='APPLY: Password for Interop device WiFi connection')

    parser.add_argument('--log_dur', '--ld', type=float, default=0,
                        help='LOG: Gather ADB logs for a duration of this many minutes')

    parser.add_argument('--device', '--dev', type=str, default='',
                        help='specify the EID (serial number) of the interop device (eg 1.1.91BX93V4')

    parser.add_argument('--screensize', type=float, default='0.4',
                        help='GUI: specify the Android screen size when launching the Android GUI (percent as float)')

    parser.add_argument('--log_destination', '--log_dest',
                        help='LOG: the filename destination on the LF device where the log file should be stored'
                        'Give "stdout" to receive content as keyed text message')
    parser.add_argument('--log_level', default=None)

    parser.add_argument('--set_adb_user_name', action="store_true",
                        help='provided when want to configure adb_username')

    parser.add_argument('--adb_username',  type=str, default='',
                        help='provide user name to adb devices')

    parser.add_argument('--list_ntwk', action="store_true",
                        help='stores true when you want to get list of networks')

    parser.add_argument('--forget_netwrk', action="store_true",
                        help='stores true when you want to forget all wifi-networks')

    parser.add_argument('--ntwk_id', type=str, default='',
                        help='provide network id which you want to forget')

    args = parser.parse_args()
    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    # set the logger level to requested level
    logger_config.set_level(level=args.log_level)

    myhost = args.host
    if not (myhost.startswith("http:") or myhost.startswith("https:")):
        myhost = "http://" + args.host
    parsed_url = urlparse(myhost)
    if not parsed_url.port:
        parsed_url._replace(netloc=parsed_url.netloc.replace(str(parsed_url.port), "8080"))

    interop = InteropCommands(_host=parsed_url.hostname,
                              _port=parsed_url.port,
                              device_eid=args.device,
                              screen_size_prcnt=args.screensize,
                              launch_gui=args.show_gui,
                              install=args.install,
                              install_g=args.install_g,
                              wifi=args.wifi,
                              start=args.start,
                              stop=args.stop,
                              apply=args.apply,
                              mgr_ip=args.mgr_ip,
                              user_name=args.user_name,
                              ssid=args.ssid,
                              passwd=args.passwd,
                              crypt=args.crypt,
                              log_dur=args.log_dur,
                              log_destination=args.log_destination,
                              _proxy_str=None,
                              _debug_on=False,
                              _exit_on_error=False,
                              _exit_on_fail=False,
                              set_adb_user_name= args.set_adb_user_name,
                              adb_username=args.adb_username,
                              list_ntwk=args.list_ntwk,
                              forget_netwrk=args.forget_netwrk,
                              ntwk_id=args.ntwk_id)
    interop.run()


if __name__ == "__main__":
    main()
