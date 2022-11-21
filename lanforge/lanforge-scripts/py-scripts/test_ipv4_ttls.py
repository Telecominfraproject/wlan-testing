#!/usr/bin/env python3
import sys
import os
import importlib
import argparse
import time
import pprint

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
test_ip_variable_time = importlib.import_module("py-scripts.test_ip_variable_time")
IPVariableTime = test_ip_variable_time.IPVariableTime


class TTLSTest(Realm):
    def __init__(self, host="localhost", port=8080,
                 ssid="[BLANK]",
                 security="wpa2",
                 password="[BLANK]",
                 radio="wiphy0",
                 upstream_port="eth2",
                 key_mgmt="WPA-EAP",
                 pairwise="NA",
                 group="NA",
                 wpa_psk="DEFAULT",
                 wep_key="NA",
                 ca_cert="NA",
                 eap="TTLS",
                 identity="testuser",
                 anonymous_identity="NA",
                 phase1="NA",
                 phase2="NA",
                 ttls_passwd="testpasswd",
                 pin="NA",
                 pac_file="NA",
                 private_key="NA",
                 pk_passwd="NA",
                 hessid="00:00:00:00:00:01",
                 ttls_realm="localhost.localdomain",
                 client_cert="NA",
                 imsi="NA",
                 milenage="NA",
                 domain="localhost.localdomain",
                 roaming_consortium="NA",
                 venue_group="NA",
                 network_type="NA",
                 ipaddr_type_avail="NA",
                 network_auth_type="NA",
                 anqp_3gpp_cell_net="NA",
                 ieee80211w=1,
                 vap=True,
                 hs20_enable=False,
                 enable_pkc=False,
                 number_template="00000",
                 sta_list=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(lfclient_host=host, lfclient_port=port, debug_=_debug_on, _exit_on_fail=_exit_on_fail)
        self.resulting_endpoints = {}
        self.host = host
        self.port = port
        self.ssid = ssid
        self.radio = radio
        self.security = security
        self.password = password
        self.sta_list = sta_list

        self.key_mgmt = key_mgmt
        self.pairwise = pairwise
        self.group = group

        self.wpa_psk = wpa_psk
        self.key = wep_key
        self.ca_cert = ca_cert
        self.eap = eap
        self.identity = identity  # eap identity
        self.anonymous_identity = anonymous_identity
        self.phase1 = phase1
        self.phase2 = phase2
        self.ttls_passwd = ttls_passwd  # eap passwd
        self.pin = pin
        self.pac_file = pac_file
        self.private_key = private_key
        self.pk_passwd = pk_passwd
        self.hessid = hessid
        self.ttls_realm = ttls_realm
        self.client_cert = client_cert
        self.imsi = imsi
        self.milenage = milenage
        self.domain = domain
        self.roaming_consortium = roaming_consortium
        self.venue_group = venue_group
        self.network_type = network_type
        self.ipaddr_type_avail = ipaddr_type_avail
        self.network_auth_type = network_auth_type
        self.anqp_3gpp_cell_net = anqp_3gpp_cell_net

        self.ieee80211w = ieee80211w
        self.hs20_enable = hs20_enable
        self.enable_pkc = enable_pkc

        self.timeout = 60
        self.number_template = number_template
        self.debug = _debug_on
        self.station_profile = self.new_station_profile()
        self.vap = vap
        self.upstream_port = upstream_port
        self.upstream_resource = 1
        if self.vap:
            self.vap_profile = self.new_vap_profile()
            self.vap_profile.vap_name = "TestNet"

        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.mode = 0

        # Layer3 Traffic
        self.l3_cx_obj_udp = IPVariableTime(host=self.host, port=self.port, radio=self.radio,
                                            ssid=self.ssid, password=self.password, security=self.security,
                                            use_existing_sta=True, sta_list=self.sta_list, traffic_type="lf_udp",
                                            upstream=self.upstream_port)
        self.l3_cx_obj_udp.cx_profile.name_prefix = "udp-"

        self.l3_cx_obj_udp.cx_profile.side_a_min_bps = 128000
        self.l3_cx_obj_udp.cx_profile.side_a_max_bps = 128000
        self.l3_cx_obj_udp.cx_profile.side_b_min_bps = 128000
        self.l3_cx_obj_udp.cx_profile.side_b_max_bps = 128000
        self.l3_cx_obj_udp.cx_profile.side_a_min_pdu = 1200
        self.l3_cx_obj_udp.cx_profile.side_b_min_pdu = 1500
        self.l3_cx_obj_udp.cx_profile.report_timer = 1000

        self.l3_cx_obj_tcp = IPVariableTime(host=self.host, port=self.port, radio=self.radio,
                                            ssid=self.ssid, password=self.password, security=self.security,
                                            use_existing_sta=True, sta_list=self.sta_list, traffic_type="lf_tcp",
                                            upstream=self.upstream_port)
        self.l3_cx_obj_tcp.cx_profile.name_prefix = "tcp-"
        self.l3_cx_obj_tcp.cx_profile.side_a_min_bps = 128000
        self.l3_cx_obj_tcp.cx_profile.side_a_max_bps = 128000
        self.l3_cx_obj_tcp.cx_profile.side_b_min_bps = 128000
        self.l3_cx_obj_tcp.cx_profile.side_b_max_bps = 128000
        self.l3_cx_obj_tcp.cx_profile.side_a_min_pdu = 1200
        self.l3_cx_obj_tcp.cx_profile.side_b_min_pdu = 1500
        self.l3_cx_obj_tcp.cx_profile.report_timer = 1000

    def build(self,
              extra_securities=None):
        # Build stations

        self.station_profile.use_security(self.security, self.ssid, passwd=self.password)
        if extra_securities is not None:
            for security in extra_securities:
                self.station_profile.add_security_extra(security=security)
        if self.vap:
            self.vap_profile.use_security(self.security, self.ssid, passwd=self.password)
        self.station_profile.set_number_template(self.number_template)
        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.set_wifi_extra(key_mgmt=self.key_mgmt,
                                            pairwise=self.pairwise,
                                            group=self.group,
                                            psk=self.password,
                                            eap=self.eap,
                                            identity=self.identity,
                                            passwd=self.ttls_passwd,
                                            private_key=self.private_key,
                                            pk_password=self.pk_passwd,
                                            ca_cert=self.ca_cert,
                                            hessid=self.hessid)
        if self.ieee80211w:
            self.station_profile.set_command_param("add_sta", "ieee80211w", self.ieee80211w)
        if self.enable_pkc:
            self.station_profile.set_command_flag("add_sta", "enable_pkc", 1)
        if self.hs20_enable:
            self.station_profile.set_command_flag("add_sta", "hs20_enable", 1)

        if self.vap:
            self.vap_profile.set_wifi_extra(key_mgmt=self.key_mgmt,
                                            pairwise="DEFAULT",
                                            group="DEFAULT",
                                            psk=self.password,
                                            eap=self.eap,
                                            identity=self.identity,
                                            passwd=self.ttls_passwd,
                                            realm=self.ttls_realm,
                                            domain=self.domain,
                                            hessid=self.hessid)
            self.vap_profile.create(resource=1,
                                    radio=self.radio,
                                    channel=36,
                                    up_=True,
                                    debug=self.debug,
                                    suppress_related_commands_=True,
                                    use_radius=True,
                                    hs20_enable=False)
        self.station_profile.create(radio=self.radio,
                                    sta_names_=self.sta_list,
                                    debug=self.debug,
                                    use_radius=True,
                                    hs20_enable=False)
        self._pass("Station build finished")
        self.l3_cx_obj_udp.build()
        self.l3_cx_obj_tcp.build()
        if self.debug:
            pprint.pprint(self.station_profile.add_sta_data)

    def start(self, sta_list, print_pass, print_fail, wait_time=40):
        self.station_profile.admin_up()
        if self.vap:
            self.vap_profile.admin_up(1)
        associated_map = {}
        ip_map = {}
        print("Starting test...")
        for sec in range(self.timeout):
            for sta_name in sta_list:
                sta_status = self.json_get("port/1/1/" + sta_name + "?fields=port,alias,ip,ap", debug_=self.debug)
                # print(sta_status)
                if sta_status is None or sta_status['interface'] is None or sta_status['interface']['ip'] == "0.0.0.0":
                    continue
                if len(sta_status['interface']['ap']) == 17 and sta_status['interface']['ap'][-3] == ':':
                    # print("Associated", sta_name, sta_status['interface']['ap'], sta_status['interface']['ip'])
                    associated_map[sta_name] = 1
                if sta_status['interface']['ip'] != '0.0.0.0':
                    # print("IP", sta_name, sta_status['interface']['ap'], sta_status['interface']['ip'])
                    ip_map[sta_name] = 1
            if (len(sta_list) == len(ip_map)) and (len(sta_list) == len(associated_map)):
                break
            else:
                time.sleep(1)

        if self.debug:
            print("sta_list", len(sta_list), sta_list)
            print("ip_map", len(ip_map), ip_map)
            print("associated_map", len(associated_map), associated_map)
        if (len(sta_list) == len(ip_map)) and (len(sta_list) == len(associated_map)):
            self._pass("PASS: All stations associated with IP", print_pass)
        else:

            self._fail("FAIL: Not all stations able to associate/get IP", print_fail)
            if self.debug:
                print("sta_list", sta_list)
                print("ip_map", ip_map)
                print("associated_map", associated_map)

        self.l3_cx_obj_udp.start()
        self.l3_cx_obj_tcp.start()
        time.sleep(wait_time)
        # notice that this does not actually generate traffic
        # please see test_ipv4_variable_time for example of generating traffic
        return self.passes()

    def stop(self):
        # Bring stations down
        self.station_profile.admin_down()
        if self.vap:
            self.vap_profile.admin_down(1)
        self.l3_cx_obj_udp.stop()
        self.l3_cx_obj_tcp.stop()
        self.collect_endp_stats(self.l3_cx_obj_tcp.cx_profile.created_cx, traffic_type="TCP")
        self.collect_endp_stats(self.l3_cx_obj_udp.cx_profile.created_cx, traffic_type="UDP")

    def cleanup(self, sta_list):
        self.l3_cx_obj_udp.cx_profile.cleanup_prefix()
        self.l3_cx_obj_tcp.cx_profile.cleanup_prefix()
        self.station_profile.cleanup(sta_list)
        if self.vap:
            self.vap_profile.cleanup(1)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=sta_list,
                                           debug=self.debug)

    def pre_cleanup(self):
        self.l3_cx_obj_udp.cx_profile.cleanup_prefix()
        # do not clean up station if existed prior to test
        if not self.l3_cx_obj_udp.use_existing_sta:
            for sta in self.sta_list:
                self.rm_port(sta, check_exists=True, debug_=self.debug)

    def collect_endp_stats(self, endp_map, traffic_type="TCP"):
        print("Collecting Data")
        fields = "?fields=name,tx+bytes,rx+bytes"
        for (cx_name, endps) in endp_map.items():
            try:
                endp_url = "/endp/%s%s" % (endps[0], fields)
                endp_json = self.json_get(endp_url)
                self.resulting_endpoints[endp_url] = endp_json
                ptest_a_tx = endp_json['endpoint']['tx bytes']
                ptest_a_rx = endp_json['endpoint']['rx bytes']

                # ptest = self.json_get("/endp/%s?fields=tx+bytes,rx+bytes" % cx_names[cx_name]["b"])
                endp_url = "/endp/%s%s" % (endps[1], fields)
                endp_json = self.json_get(endp_url)
                self.resulting_endpoints[endp_url] = endp_json

                ptest_b_tx = endp_json['endpoint']['tx bytes']
                ptest_b_rx = endp_json['endpoint']['rx bytes']

                self.compare_vals("test" + traffic_type + "-A TX", ptest_a_tx)
                self.compare_vals("test" + traffic_type + "-A RX", ptest_a_rx)

                self.compare_vals("test" + traffic_type + "-B TX", ptest_b_tx)
                self.compare_vals("test" + traffic_type + "-B RX", ptest_b_rx)

            except Exception as e:
                print("Is this the function having the error?")
                self.error(e)

    def compare_vals(self, name, postVal, print_pass=True, print_fail=True):
        # print(f"Comparing {name}")
        if postVal > 0:
            self._pass("%s %s" % (name, postVal), print_pass)
        else:
            self._fail("%s did not report traffic: %s" % (name, postVal), print_fail)


def main():
    parser = Realm.create_basic_argparse(
        prog='test_ipv4_ttls.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Demonstration showing wpa2-ent ttls authentication''',

        description='''\
test_ipv4_ttls.py:
 --------------------
 Generic command layout:
 python ./test_ipv4_ttls.py

    --upstream_port eth1
    --radio wiphy0 
    --num_stations 3
    --ssid ssid-wpa-1
    --key ssid-wpa-1
    --security <security type: wpa2, open, wpa, wpa3>
    --debug

''')

    parser.add_argument('--a_min', help='--a_min bps rate minimum for side_a', default=256000)
    parser.add_argument('--b_min', help='--b_min bps rate minimum for side_b', default=256000)
    parser.add_argument('--test_duration', help='--test_duration sets the duration of the test', default="5m")
    parser.add_argument('--key-mgmt', help="--key-mgt: { %s }" % ", ".join(realm.wpa_ent_list()), default="WPA-EAP")
    parser.add_argument('--wpa_psk', help='wpa-ent pre shared key', default="[BLANK]")
    parser.add_argument('--eap', help='--eap eap method to use', default="TTLS")
    parser.add_argument('--identity', help='--identity eap identity string', default="testuser")
    parser.add_argument('--ttls_passwd', help='--ttls_passwd eap password string', default="testpasswd")
    parser.add_argument('--ttls_realm', help='--ttls_realm 802.11u home realm to use', default="localhost.localdomain")
    parser.add_argument('--domain', help='--domain 802.11 domain to use', default="localhost.localdomain")
    parser.add_argument('--hessid', help='--hessid 802.11u HESSID (MAC addr format/peer for WDS)',
                        default="00:00:00:00:00:01")
    parser.add_argument('--ieee80211w', help='--ieee80211w <disabled(0),optional(1),required(2)', default='1')
    parser.add_argument('--use_hs20', help='use HotSpot 2.0', default=False)
    parser.add_argument('--enable_pkc', help='enable opportunistic PMKSA WPA2 key caching', default=False)
    parser.add_argument('--vap', help='Create VAP on host device', default=True)
    args = parser.parse_args()
    num_sta = 2
    if args.num_stations:
        num_stations_converted = int(args.num_stations)
        num_sta = num_stations_converted

    station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=num_sta - 1, padding_number_=10000)
    ttls_test = TTLSTest(host=args.mgr,
                         port=args.mgr_port,
                         ssid=args.ssid,
                         password=args.passwd,
                         security=args.security,
                         upstream_port=args.upstream_port,
                         sta_list=station_list,
                         radio=args.radio,
                         key_mgmt=args.key_mgmt,
                         wpa_psk=args.wpa_psk,
                         eap=args.eap,
                         vap=args.vap,
                         identity=args.identity,
                         ttls_passwd=args.ttls_passwd,
                         ttls_realm=args.ttls_realm,
                         domain=args.domain,
                         hessid=args.hessid,
                         ieee80211w=args.ieee80211w,
                         hs20_enable=args.use_hs20,
                         enable_pkc=args.enable_pkc,
                         )
    ttls_test.cleanup(station_list)
    ttls_test.pre_cleanup()
    ttls_test.build()
    if not ttls_test.passes():
        print(ttls_test.get_fail_message())
        exit(1)
    ttls_test.start(station_list, False, False)
    ttls_test.stop()
    if not ttls_test.passes():
        print(ttls_test.get_fail_message())
        exit(1)
    time.sleep(30)
    ttls_test.cleanup(station_list)
    ttls_test.pre_cleanup()
    if ttls_test.passes():
        print("Full test passed, all stations associated and got IP")


if __name__ == "__main__":
    main()
