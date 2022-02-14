"""
Name: sta_connect_bssid_mac.py
Purpose:
    This script can create stations and can be used to set multiple BSSID, MAC to each individual station.
    Also use-bss-transition   | 0x80000000000 # Enable BSS transition. flag can be set here.
Example:
    ./sta_connect_bssid_mac.py
    --mgr localhost --mgr_port 8080
    --ssid "TestAP" #ssid
    --radio wiphy0 #radio
    --security "open" // "wpa" //  "wpa2" #security
    --passwd "BLANK" #password
    --bssid 78:d2:94:4f:20:c5,78:d2:94:4f:20:c5 #bssid names
    --sta_name "sta001,sta002" #station names
    --mac 04:f0:21:89:3e:ea,04:f0:21:89:4e:ea #mac
    --bss_trans #flag to set BSS transition on all stations
"""
import sys
import os
import importlib

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class client_connect(Realm):
    def __init__(self, lfclient_host="localhost", lfclient_port=8080, radio=None, sta_name=None,
                 ssid=None, security=None, paswd=None, bssid=None, mac=None, bss_trans=False):
        super().__init__(lfclient_host, lfclient_port)
        self.station_profile = self.new_station_profile()
        self.sta_name = sta_name
        self.bssid = bssid
        self.radio = radio
        self.security = security
        self.ssid = ssid
        self.paswd = paswd
        self.mac = mac
        self.bss_trans = bss_trans

    def setup(self):
        station_ = self.sta_name.split(",")
        print(station_)
        mac_list = self.mac.split(",")
        bssid_list = self.bssid.split(",")

        self.station_profile.use_security(self.security, self.ssid, self.paswd)

        if self.bss_trans:
            self.station_profile.desired_add_sta_flags = ["use-bss-transition"]
            self.station_profile.desired_add_sta_flags_mask = ["use-bss-transition"]

        for station_name in range(len(station_)):
            stat_list = [station_[station_name]]

            print(station_name)
            self.station_profile.cleanup(stat_list)

            if self.bssid[station_name]:
                self.station_profile.set_command_param("add_sta", "ap", bssid_list[station_name])
            else:
                self.station_profile.set_command_param("add_sta", "ap", "DEFAULT")

            if self.mac[station_name]:
                self.station_profile.add_sta_data["mac"] = mac_list[station_name]
            else:
                self.station_profile.add_sta_data["mac"] = "xx:xx:xx:xx:*:*"

            print(stat_list)
            print(self.radio)
            self.station_profile.create(radio=self.radio, sta_names_=stat_list, debug=self.debug)

        self.station_profile.admin_up()
        self.wait_for_ip(station_list=station_)
        print("stations created")


def main():
    # This has --mgr, --mgr_port and --debug
    parser = LFCliBase.create_bare_argparse(prog="sta_connect_bssid_mac.py",
                                            description="""
                                            --mgr localhost --mgr_port 8080 
                                            --ssid "TestAP-Jitendra" 
                                            --radio wiphy0
                                            --security "open" // "wpa" //  "wpa2"
                                            --passwd "BLANK" 
                                            --bssid 78:d2:94:4f:20:c5,78:d2:94:4f:20:c5 
                                            --sta_name "sta001,sta002" 
                                            --mac 04:f0:21:89:3e:ea,04:f0:21:89:4e:ea
                                            --bss_trans
                                            """
                                            )

    # Adding More Arguments for custom use
    parser.add_argument('--ssid', type=str, help='--ssid', default="")
    parser.add_argument('--passwd', type=str, help='--passwd', default="BLANK")
    parser.add_argument('--security', type=str, help='--security', default="open")
    parser.add_argument('--radio', type=str, help='--radio to use',
                        default="wiphy0")
    parser.add_argument('--sta_name', type=str, help='--num_client is number of stations', default="sta001")
    parser.add_argument("--bssid", type=str, help='DUT BSSID to which we expect to connect', default="DEFAULT")
    parser.add_argument('--mac', type=str, help='--mac to stations',
                        default="xx:xx:xx:xx:*:*")
    parser.add_argument("-bt", "--bss_trans", default=False, action='store_true',
                        help="To enable BSS transition.(by default: False)")

    args = parser.parse_args()
    obj = client_connect(lfclient_host=args.mgr, lfclient_port=args.mgr_port, radio=args.radio, sta_name=args.sta_name,
                         ssid=args.ssid, security=args.security, paswd=args.passwd, bssid=args.bssid,
                         mac=args.mac, bss_trans=args.bss_trans
                         )
    obj.setup()


if __name__ == "__main__":
    main()
