#! /bin/bash
Help()
{
  echo "This script modifies lanforge scripts so that it can be imported into python as a library from the tar.gz file it creates"
  echo "store this repository in your python path, and then import lanforge_scripts from anywhere on your machine"
  echo "An example of how to run this in python is like so:"
  echo "import lanforge_scripts"
  echo "ip_var=lanforge_scripts.IPVariableTime(host='192.168.1.239',port='8080',radio='wiphy0',sta_list=['1.1.sta0000','1.1.sta0001'],ssid='lanforge',password='password',security='wpa2',upstream='eth1',name_prefix='VT',traffic_type='lf_udp',_debug_on=True)"
  echo "ip_var.build()"
  echo "ip_var.start(False,False)"
  echo ""
  echo "EXPORT TO TAR FILE"
  echo "./to_pip.sh -a -t TARGET_DIR"
  echo "The 't' flag tells to_pip where to store the tar file, -a tells it to not make a python wheel."
  echo "When the archive is made, you can install it on any computer with $(pip install lanforge_scripts.tar.gz)"
}

ARCHIVE=1
TARGET_DIR='..'

while getopts ":h:a:t:" option; do
  case "${option}" in
    h) #display help
      Help
      exit 1
      ;;
    a) #Archive
      ARCHIVE=0
      ;;
    t) #target dir
      TARGET_DIR=${OPTARG}
      ;;
    *)
      ;;
  esac
done

BASE=$(basename "$PWD")
cd ..
if [ -d "lanforge_scripts" ]
then
  echo "lanforge_scripts exists, please remove or rename that folder"
  exit 1
else
  cp -r "${BASE}" lanforge_scripts || exit 1
  cd lanforge_scripts || exit 1
fi

mv py-scripts/ py_scripts
mv py-json/ py_json
mv py-dashboard/ py_dashboard


echo "#Automate LANforge devices with lanforge-scripts

from .py_scripts import *
from .py_dashboard import *
from .py_json import *
from .py_json import LANforge
from .py_json.LANforge import *
try:
    from . import ap_ctl
except ImportError:
    print('Pexpect_serial is not installed')
from . import emailHelper
from . import lf_mail
from . import lf_tos_plus_test
from . import lf_tx_power
from . import tos_plus_auto
#from . import auto_install_gui
from . import cpu_stats
from . import lf_sniff
from . import lf_tos_test
from . import openwrt_ctl
#from . import stationStressTest
from . import wifi_ctl_9800_3504

__all__ = ['LFRequest', 'LFUtils', 'LANforge','LFCliBase']

__title__ = 'lanforge_scripts'
__version__ = '0.0.1'
__author__ = 'Candela Technologies <www.candelatech.com>'
__license__ = ''" > __init__.py

#fix files in root
sed -i -- 's/from LANforge/from py_json.LANforge/g' *.py
sed -i -- 's/from py_json/from .py_json/g' *.py

cd py_scripts || exit 1

echo "#from .connection_test import ConnectionTest
from .create_bond import CreateBond
from .create_bridge import CreateBridge
from .create_chamberview import CreateChamberview
from .create_l3 import CreateL3
from .create_l4 import CreateL4
from .create_macvlan import CreateMacVlan
from .create_qvlan import CreateQVlan
from .create_station import CreateStation
from .create_vap import CreateVAP
from .csv_convert import CSVParcer
from .csv_to_influx import CSVtoInflux
from .csv_to_grafana import UseGrafana
from .example_security_connection import IPv4Test
from .grafana_profile import UseGrafana
from .lf_ap_auto_test import ApAutoTest
from .lf_atten_mod_test import CreateAttenuator
from .lf_csv import lf_csv
from .lf_dataplane_test import DataplaneTest
from .lf_dfs_test import FileAdapter, CreateCtlr, L3VariableTime
from .lf_ftp import FtpTest
from .lf_graph import lf_bar_graph, lf_stacked_graph, lf_horizontal_stacked_graph, lf_scatter_graph, lf_line_graph
from .lf_mesh_test import MeshTest
from .lf_multipsk import MultiPsk
from .lf_report import lf_report
from .lf_rvr_test import RvrTest
from .lf_rx_sensitivity_test import RxSensitivityTest
from .lf_sniff_radio import SniffRadio
#from .lf_snp_test import  SAME CLASS NAMES AS LF_DFS_TEST
from .lf_tr398_test import TR398Test
from .lf_webpage import HttpDownload
from .lf_wifi_capacity_test import WiFiCapacityTest
from .measure_station_time_up import MeasureTimeUp
from .modify_station import ModifyStation
from .modify_vap import ModifyVAP
from .run_cv_scenario import RunCvScenario
from .sta_connect import StaConnect
from .sta_connect2 import StaConnect2
from .sta_connect_bssid_mac import client_connect
from .station_layer3 import STATION
from .stations_connected import StationsConnected
from .test_1k_clients_jedtest import Test1KClients
from .test_client_admission import LoadLayer3
from .test_fileio import FileIOTest
from .test_generic import GenTest
from .test_ip_connection import ConnectTest
from .test_ip_variable_time import IPVariableTime
from .test_ipv4_ttls import TTLSTest
from .test_ipv4_ps import IPV4VariableTime
#from .test_l3_longevity import L3VariableTime ALSO IN LF_DFS_TEST
from .test_l3_powersave_traffic import L3PowersaveTraffic
#from .test_l3_scenario_throughput import
from .test_l3_unicast_traffic_gen import L3VariableTimeLongevity
from .test_l3_WAN_LAN import VRTest
from .test_l4 import IPV4L4
from .test_status_msg import TestStatusMessage
#from .test_wanlink import LANtoWAN
#from .test_wpa_passphrases import WPAPassphrases
from .testgroup import TestGroup
from .testgroup2 import TestGroup2
from .tip_station_powersave import TIPStationPowersave
from .video_rates import VideoRates
from .wlan_capacity_calculator import main as WlanCapacityCalculator
from .ws_generic_monitor_test import WS_Listener" > __init__.py

# Fix files in py_scripts
sed -i -- 's/import importlib/ /g' *.py
sed -i -- 's/import realm/ /g' create_vap.py lf_dut_sta_vap_test.py lf_sniff_radio.py run_cv_scenario.py sta_connect.py station_layer3.py test_client_admission.py
sed -i -- 's/import realm/from realm import Realm/g' lf_atten_mod_test.py lf_multipsk.py test_fileio.py test_ip_connection.py test_ipv4_ttls.py test_l3_WAN_LAN.py test_l3_unicast_traffic_gen.py test_l4.py testgroup.py
sed -i -- 's/realm.Realm/Realm/g' lf_atten_mod_test.py lf_multipsk.py lf_sniff_radio.py station_layer3.py test_client_admission.py test_fileio.py test_ip_connection.py
sed -i -- 's/import realm/from realm import Realm, PortUtils/g' lf_ftp.py lf_webpage.py
sed -i -- 's/import realm/from realm import Realm, WifiMonitor/g' test_ipv4_ps.py
sed -i -- 's/import l3_cxprofile/from l3_cxprofile import L3CXProfile/g' test_l3_powersave_traffic.py
sed -i -- 's/import realm/from realm import Realm, StationProfile, WifiMonitor/g' test_l3_powersave_traffic.py
sed -i -- 's/import realm/from realm import Realm, PacketFilter/g' tip_station_powersave.py
sed -i -- 's/from generic_cx import GenericCx/ /g' *.py
sed -i -- 's/import wlan_theoretical_sta/from wlan_theoretical_sta import abg11_calculator, n11_calculator, ac11_calculator/g' wlan_capacity_calculator.py
sed -i -- 's/sys.path.append(os.path.join(os.path.abspath(__file__ + "..\/..\/..\/")))/ /g' *.py

#Change importlib to pip compliant method
sed -i -- 's/import importlib/ /g' *.py
sed -i -- 's/influx = importlib.import_module("py-scripts.influx_utils")/from lanforge_scripts.py_scripts.influx_utils import RecordInflux/g' *.py
sed -i -- 's/RecordInflux = influx.RecordInflux/ /g' *.py
sed -i -- 's/create_chamberview_dut = importlib.import_module("py-scripts.create_chamberview_dut")/import create_chamberview_dut/g' *.py
sed -i -- 's/lf_kpi_csv = importlib.import_module("py-scripts.lf_kpi_csv")/from lanforge_scripts.py_scripts import lf_kpi_csv/g' *.py
sed -i -- "s/InfluxRequest = importlib.import_module('py-dashboard.InfluxRequest')/from lanforge_scripts.py_dashboard import InfluxRequest/g" *.py
sed -i -- 's/l3_cxprofile2 = importlib.import_module("py-json.l3_cxprofile2")/from lanforge_scripts.py_json import l3_cxprofile2/g' *.py
sed -i -- 's/add_dut = importlib.import_module("py-json.LANforge.add_dut")/from lanforge_scripts.py_json.LANforge import add_dut/g' *.py
sed -i -- 's/ftp_html = importlib.import_module("py-scripts.ftp_html")/from lanforge_scripts.py_scripts import ftp_html/g' *.py
sed -i -- 's/l3_cxprofile = importlib.import_module("py-json.l3_cxprofile")/from lanforge_scripts.py_json import l3_cxprofile/g' *.py
sed -i -- 's/sta_connect = importlib.import_module("py-scripts.sta_connect")/from lanforge_scripts.py_scripts import sta_connect/g' *.py
sed -i -- 's/test_ip_variable_time = importlib.import_module("py-scripts.test_ip_variable_time")/from lanforge_scripts.py_scripts import test_ip_variable_time/g' *.py
sed -i -- 's/add_sta = importlib.import_module("py-json.LANforge.add_sta")/from lanforge_scripts.py_json.LANforge import add_sta/g' *.py
sed -i -- 's/cv_dut_profile = importlib.import_module("py-json.cv_dut_profile")/from lanforge_scripts.py_json import cv_dut_profile/g' *.py
sed -i -- 's/wlan_theoretical_sta = importlib.import_module("py-json.wlan_theoretical_sta")/from lanforge_scripts.py_json import wlan_theoretical_sta/g' *.py
sed -i -- 's/port_utils = importlib.import_module("py-json.port_utils")/from lanforge_scripts.py_json import port_utils/g' *.py
sed -i -- 's/http_profile = importlib.import_module("py-json.http_profile")/from lanforge_scripts.py_json import http_profile/g' *.py
sed -i -- 's/LANforge = importlib.import_module("py-json.LANforge")/from lanforge_scripts.py_json import LANforge/g' *.py
sed -i -- 's/vap_profile = importlib.import_module("py-json.vap_profile")/from lanforge_scripts.py_json import vap_profile/g' *.py
sed -i -- 's/create_chamberview = importlib.import_module("py-scripts.create_chamberview")/from lanforge_scripts.py_scripts import create_chamberview/g' *.py
sed -i -- 's/lf_ap_auto_test = importlib.import_module("py-scripts.lf_ap_auto_test")/from lanforge_scripts.py_scripts import lf_ap_auto_test/g' *.py
sed -i -- 's/add_monitor = importlib.import_module("py-json.LANforge.add_monitor")/from lanforge_scripts.py_json.LANforge import add_monitor/g' *.py
sed -i -- 's/lf_json_autogen = importlib.import_module("py-json.LANforge.lf_json_autogen")/from lanforge_scripts.py_json.LANforge import lf_json_autogen/g' *.py
sed -i -- 's/InfluxRequest = importlib.import_module("py-dashboard.InfluxRequest")/from lanforge_scripts.py_dashboard import InfluxRequest/g' *.py
sed -i -- 's/qvlan_profile = importlib.import_module("py-json.qvlan_profile")/from lanforge_scripts.py_json import qvlan_profile/g' *.py
sed -i -- 's/cv_test_manager = importlib.import_module("py-json.cv_test_manager")/from lanforge_scripts.py_json import cv_test_manager/g' *.py
sed -i -- 's/add_vap = importlib.import_module("py-json.LANforge.add_vap")/from lanforge_scripts.py_json.LANforge import add_vap/g' *.py
sed -i -- 's/realm = importlib.import_module("py-json.realm")/from lanforge_scripts.py_json.realm import Realm,PortUtils/g' *.py
sed -i -- 's/lf_wifi_capacity_test = importlib.import_module("py-scripts.lf_wifi_capacity_test")/from lanforge_scripts.py_scripts import lf_wifi_capacity_test/g' *.py
sed -i -- 's/lf_attenmod = importlib.import_module("py-json.lf_attenmod")/from lanforge_scripts.py_json import lf_attenmod/g' *.py
sed -i -- 's/lf_csv = importlib.import_module("py-scripts.lf_csv")/from lanforge_scripts.py_scripts import lf_csv/g' *.py
sed -i -- 's/test_utility = importlib.import_module("py-json.test_utility")/from lanforge_scripts.py_json import test_utility/g' *.py
sed -i -- 's/lf_dataplane_test = importlib.import_module("py-scripts.lf_dataplane_test")/from lanforge_scripts.py_scripts import lf_dataplane_test/g' *.py
sed -i -- 's/ws_generic_monitor = importlib.import_module("py-json.ws_generic_monitor")/from lanforge_scripts.py_json import ws_generic_monitor/g' *.py
sed -i -- 's/grafana_profile = importlib.import_module("py-scripts.grafana_profile")/from lanforge_scripts.py_scripts import grafana_profile/g' *.py
sed -i -- 's/csv_to_influx = importlib.import_module("py-scripts.csv_to_influx")/from lanforge_scripts.py_scripts import csv_to_influx/g' *.py
sed -i -- 's/gen_cxprofile = importlib.import_module("py-json.gen_cxprofile")/from lanforge_scripts.py_json import gen_cxprofile/g' *.py
sed -i -- 's/lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")/from lanforge_scripts.py_json.LANforge import lfcli_base/g' *.py
sed -i -- 's/LFUtils = importlib.import_module("py-json.LANforge.LFUtils")/from lanforge_scripts.py_json.LANforge import LFUtils/g' *.py
sed -i -- 's/lfdata = importlib.import_module("py-json.lfdata")/from lanforge_scripts.py_json import lfdata/g' *.py
sed -i -- 's/cv_test_reports = importlib.import_module("py-json.cv_test_reports")/from lanforge_scripts.py_json import cv_test_reports/g' *.py
sed -i -- 's/LFRequest = importlib.import_module("py-json.LANforge.LFRequest")/from lanforge_scripts.py_json.LANforge import LFRequest/g' *.py
sed -i -- 's/lf_cv_base = importlib.import_module("py-json.lf_cv_base")/from lanforge_scripts.py_json import lf_cv_base/g' *.py
sed -i -- 's/base_profile = importlib.import_module("py-json.base_profile")/from lanforge_scripts.py_json import base_profile/g' *.py
sed -i -- 's/add_file_endp = importlib.import_module("py-json.LANforge.add_file_endp")/from lanforge_scripts.py_json.LANforge import add_file_endp/g' *.py
sed -i -- 's/lf_graph = importlib.import_module("py-scripts.lf_graph")/from lanforge_scripts.py_scripts import lf_graph/g' *.py
sed -i -- 's/GrafanaRequest = importlib.import_module("py-dashboard.GrafanaRequest")/from lanforge_scripts.py_dashboard.GrafanaRequest import GrafanaRequest/g' *.py
sed -i -- 's/GrafanaRequest = GrafanaRequest.GrafanaRequest/ /g' *.py
sed -i -- 's/station_profile = importlib.import_module("py-json.station_profile")/from lanforge_scripts.py_json import station_profile/g' *.py
sed -i -- 's/cv_test_manager = importlib.import_module("py-scripts.cv_test_manager")/from lanforge_scripts.py_scripts import cv_test_manager/g' *.py
sed -i -- 's/lf_report = importlib.import_module("py-scripts.lf_report")/from lanforge_scripts.py_scripts import lf_report/g' *.py
sed -i -- 's/wifi_monitor_profile = importlib.import_module("py-json.wifi_monitor_profile")/from lanforge_scripts.py_json import wifi_monitor_profile/g' *.py
sed -i -- 's/GhostRequest = importlib.import_module("py-dashboard.GhostRequest")/from lanforge_scripts.py_dashboard.GhostRequest import GhostRequest/g' *.py
sed -i -- 's/l4_cxprofile = importlib.import_module("py-json.l4_cxprofile")/from lanforge_scripts.py_json import l4_cxprofile/g' *.py
sed -i -- 's/influx = importlib.import_module("py-scripts.influx")/from lanforge_scripts.py_scripts import influx/g' *.py
sed -i -- 's/mac_vlan_profile = importlib.import_module("py-json.mac_vlan_profile")/from lanforge_scripts.py_json import mac_vlan_profile/g' *.py
sed -i -- 's/create_wanlink = importlib.import_module("py-json.create_wanlink")/from lanforge_scripts.py_json import create_wanlink/g' *.py
sed -i -- 's/set_port = importlib.import_module("py-json.LANforge.set_port")/from lanforge_scripts.py_json.LANforge import set_port/g' *.py
sed -i -- 's/dut_profile = importlib.import_module("py-json.dut_profile")/from lanforge_scripts.py_json import dut_profile/g' *.py
sed -i -- 's/test_group_profile = importlib.import_module("py-json.test_group_profile")/from lanforge_scripts.py_json import test_group_profile/g' *.py
sed -i -- 's/multicast_profile = importlib.import_module("py-json.multicast_profile")/from lanforge_scripts.py_json import multicast_profile/g' *.py
sed -i -- 's/set_wifi_radio = importlib.import_module("py-json.LANforge.set_wifi_radio")/from lanforge_scripts.py_json.LANforge import set_wifi_radio/g' *.py
sed -i -- 's/fio_endp_profile = importlib.import_module("py-json.fio_endp_profile")/from lanforge_scripts.py_json import fio_endp_profile/g' *.py
sed -i -- 's/PortUtils = realm.PortUtils/ /g' *.py
sed -i -- 's/Realm = realm.Realm/ /g' *.py
sed -i -- 's/lf_csv = lf_csv.lf_csv/ /g' *.py
sed -i -- 's/TestGroupProfile = realm.TestGroupProfile/ /g' *.py
sed -i -- 's/sys.path.append(os.path.join(os.path.abspath(__file__ + "..\/..\/..\/")))/ /g' *.py

sed -i -- 's/from influxdb/from .influxdb/g' *.py
sed -i -- 's/py-scripts/py_scripts/g' *.py
sed -i -- 's/py-json/py_json/g' *.py
sed -i -- 's/py-dashboard/py_dashboard/g' *.py

# fix py_dashboard files
sed -i -- 's/from GrafanaRequest/from lanforge_scripts.py_dashboard.GrafanaRequest/g' *.py
sed -i -- 's/from InfluxRequest/from lanforge_scripts.py_dashboard.InfluxRequest/g' *.py
sed -i -- 's/from GhostRequest/from lanforge_scripts.py_dashboard.GhostRequest/g' *.py

#fix py_json files
sed -i -- 's/from LANforge/from lanforge_scripts.py_json.LANforge/g' *.py
sed -i -- 's/from cv_test_manager/from lanforge_scripts.py_json.cv_test_manager/g' *.py

#fix py_scripts files
sed -i -- 's/lf_report = importlib.import_module("py-scripts.lf_report")/from .lf_report import lf_report/g' *.py
sed -i -- 's/lf_graph = importlib.import_module("py-scripts.lf_graph")/from .lf_graph import lf_bar_graph, lf_scatter_graph, lf_stacked_graph, lf_horizontal_stacked_graph/g' *.py
sed -i -- 's/lf_report = lf_report.lf_report/ /g' *.py
sed -i -- 's/lf_bar_graph = lf_graph.lf_bar_graph/ /g' *.py
sed -i -- 's/lf_scatter_graph = lf_graph.lf_scatter_graph/ /g' *.py
sed -i -- 's/lf_stacked_graph = lf_graph.lf_stacked_graph/ /g' *.py
sed -i -- 's/lf_horizontal_stacked_graph = lf_graph.lf_horizontal_stacked_graph/ /g' *.py
sed -i -- 's/from lf_graph/from .lf_graph/g' *.py
sed -i -- 's/from csv_to_influx/from .csv_to_influx/g' *.py
sed -i -- 's/from csv_to_grafana/from .csv_to_grafana/g' *.py
sed -i -- 's/from grafana_profile/from .grafana_profile/g' *.py
sed -i -- 's/from influx import/from .influx import/g' *.py
sed -i -- 's/import ..py_json.LANforge/ /g' *.py
sed -i -- 's/from .influxdb/from influxdb/g' *.py
sed -i -- 's/from test_utility/from lanforge_scripts.py_json.test_utility/g' *.py
sed -i -- 's/from ftp_html/from .ftp_html/g' *.py
sed -i -- 's/from lf_csv/from .lf_csv/g' *.py
sed -i -- 's/from test_ip_variable_time/from .test_ip_variable_time/g' *.py
sed -i -- 's/from l3_cxprofile/from lanforge_scripts.py_json.l3_cxprofile/g' *.py
sed -i -- 's/from create_wanlink/from lanforge_scripts.py_json.create_wanlink/g' *.py
sed -i -- 's/from wlan_theoretical_sta/from lanforge_scripts.py_json.wlan_theoretical_sta/g' *.py
sed -i -- 's/from ws_generic_monitor/from lanforge_scripts.py_json.ws_generic_monitor/g' *.py
sed -i -- 's/from port_utils/from lanforge_scripts.py_json.port_utils/g' *.py
sed -i -- 's/wifi_monitor = importlib.import_module("py_json.wifi_monitor_profile")/from lanforge_scripts.py_json import wifi_monitor_profile/g' *.py

rm -r scripts_deprecated

cd ../py_json || exit 1
#Fix files in py_json
sed -i -- 's/import importlib/ /g' *.py
sed -i -- 's/import realm/from realm import PortUtils/g' test_utility.py

#Change importlib to pip compliant method
sed -i -- 's/mac_vlan_profile = importlib.import_module("py-json.mac_vlan_profile")/from lanforge_scripts.py_json import mac_vlan_profile/g' *.py
sed -i -- 's/dut_profile = importlib.import_module("py-json.dut_profile")/from lanforge_scripts.py_json import dut_profile/g' *.py
sed -i -- 's/l4_cxprofile = importlib.import_module("py-json.l4_cxprofile")/from lanforge_scripts.py_json import l4_cxprofile/g' *.py
sed -i -- 's/http_profile = importlib.import_module("py-json.http_profile")/from lanforge_scripts.py_json import http_profile/g' *.py
sed -i -- 's/port_utils = importlib.import_module("py-json.port_utils")/from lanforge_scripts.py_json.port_utils import PortUtils/g' *.py
sed -i -- 's/wifi_monitor_profile = importlib.import_module("py_json.wifi_monitor_profile")/from lanforge_scripts.py_json import wifi_monitor_profile/g' *.py
sed -i -- 's/wifi_monitor = importlib.import_module("py_json.wifi_monitor_profile")/from lanforge_scripts.py_json import wifi_monitor_profile/g' *.py
sed -i -- 's/fio_endp_profile = importlib.import_module("py-json.fio_endp_profile")/from lanforge_scripts.py_json import fio_endp_profile/g' *.py
sed -i -- 's/lfdata = importlib.import_module("py-json.lfdata")/from lanforge_scripts.py_json import lfdata/g' *.py
sed -i -- 's/multicast_profile = importlib.import_module("py-json.multicast_profile")/from lanforge_scripts.py_json import multicast_profile/g' *.py
sed -i -- 's/lf_attenmod = importlib.import_module("py-json.lf_attenmod")/from lanforge_scripts.py_json import lf_attenmod/g' *.py
sed -i -- 's/l3_cxprofile2 = importlib.import_module("py-json.l3_cxprofile2")/from lanforge_scripts.py_json import l3_cxprofile2/g' *.py
sed -i -- 's/l3_cxprofile = importlib.import_module("py-json.l3_cxprofile")/from lanforge_scripts.py_json import l3_cxprofile/g' *.py
sed -i -- 's/gen_cxprofile = importlib.import_module("py-json.gen_cxprofile")/from lanforge_scripts.py_json import gen_cxprofile/g' *.py
sed -i -- 's/test_group_profile = importlib.import_module("py-json.test_group_profile")/from lanforge_scripts.py_json import test_group_profile/g' *.py
sed -i -- 's/qvlan_profile = importlib.import_module("py-json.qvlan_profile")/from lanforge_scripts.py_json import qvlan_profile/g' *.py
sed -i -- 's/vap_profile = importlib.import_module("py-json.vap_profile")/from lanforge_scripts.py_json import vap_profile/g' *.py
sed -i -- 's/station_profile = importlib.import_module("py-json.station_profile")/from lanforge_scripts.py_json import station_profile/g' *.py
sed -i -- 's/mac_vlan_profile = importlib.import_module("py-json.mac_vlan_profile")/from lanforge_scripts.py_json import mac_vlan_profile/g' *.py
sed -i -- 's/add_monitor = importlib.import_module("py-json.LANforge.add_monitor")/from lanforge_scripts.py_json.LANforge import add_monitor/g' *.py
sed -i -- 's/dut_profile = importlib.import_module("py-json.dut_profile")/from lanforge_scripts.py_json import dut_profile/g' *.py
sed -i -- 's/set_port = importlib.import_module("py-json.LANforge.set_port")/from lanforge_scripts.py_json.LANforge import set_port/g' *.py
sed -i -- 's/l4_cxprofile = importlib.import_module("py-json.l4_cxprofile")/from lanforge_scripts.py_json import l4_cxprofile/g' *.py
sed -i -- 's/set_wifi_radio = importlib.import_module("py-json.LANforge.set_wifi_radio")/from lanforge_scripts.py_json.LANforge import set_wifi_radio/g' *.py
sed -i -- 's/http_profile = importlib.import_module("py-json.http_profile")/from lanforge_scripts.py_json import http_profile/g' *.py
sed -i -- 's/cv_test_reports = importlib.import_module("py-json.cv_test_reports")/from lanforge_scripts.py_json import cv_test_reports/g' *.py
sed -i -- 's/add_sta = importlib.import_module("py-json.LANforge.add_sta")/from lanforge_scripts.py_json.LANforge import add_sta/g' *.py
sed -i -- 's/port_utils = importlib.import_module("py-json.port_utils")/from lanforge_scripts.py_json import port_utils/g' *.py
sed -i -- 's/lf_cv_base = importlib.import_module("py-json.lf_cv_base")/from lanforge_scripts.py_json import lf_cv_base/g' *.py
sed -i -- 's/lf_json_autogen = importlib.import_module("py-json.LANforge.lf_json_autogen")/from lanforge_scripts.py_json.LANforge import lf_json_autogen/g' *.py
sed -i -- 's/wifi_monitor_profile = importlib.import_module("py-json.wifi_monitor_profile")/from lanforge_scripts.py_json import wifi_monitor_profile/g' *.py
sed -i -- 's/InfluxRequest = importlib.import_module("py-dashboard.InfluxRequest")/from lanforge_scripts.py_dashboard import InfluxRequest/g' *.py
sed -i -- 's/fio_endp_profile = importlib.import_module("py-json.fio_endp_profile")/from lanforge_scripts.py_json import fio_endp_profile/g' *.py
sed -i -- 's/add_dut = importlib.import_module("py-json.LANforge.add_dut")/from lanforge_scripts.py_json.LANforge import add_dut/g' *.py
sed -i -- 's/base_profile = importlib.import_module("py-json.base_profile")/from lanforge_scripts.py_json import base_profile/g' *.py
sed -i -- 's/lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")/from lanforge_scripts.py_json.LANforge.lfcli_base import LFCliBase/g' *.py
sed -i -- 's/lfdata = importlib.import_module("py-json.lfdata")/from lanforge_scripts.py_json import lfdata/g' *.py
sed -i -- 's/LFRequest = importlib.import_module("py-json.LANforge.LFRequest")/from lanforge_scripts.py_json.LANforge import LFRequest/g' *.py
sed -i -- 's/multicast_profile = importlib.import_module("py-json.multicast_profile")/from lanforge_scripts.py_json import multicast_profile/g' *.py
sed -i -- 's/add_vap = importlib.import_module("py-json.LANforge.add_vap")/from lanforge_scripts.py_json.LANforge import add_vap/g' *.py
sed -i -- 's/lf_attenmod = importlib.import_module("py-json.lf_attenmod")/from lanforge_scripts.py_json import lf_attenmod/g' *.py
sed -i -- 's/LFUtils = importlib.import_module("py-json.LANforge.LFUtils")/from lanforge_scripts.py_json.LANforge import LFUtils/g' *.py
sed -i -- 's/gen_cxprofile = importlib.import_module("py-json.gen_cxprofile")/from lanforge_scripts.py_json import gen_cxprofile/g' *.py
sed -i -- 's/LANforge = importlib.import_module("py-json.LANforge")/from lanforge_scripts.py_json import LANforge/g' *.py
sed -i -- 's/= importlib.import_module("py-json. )/from lanforge_scripts.py_json import  /g' *.py
sed -i -- 's/realm = importlib.import_module("py-json.realm")/from lanforge_scripts.py_json import realm/g' *.py
sed -i -- 's/test_group_profile = importlib.import_module("py-json.test_group_profile")/from lanforge_scripts.py_json import test_group_profile/g' *.py
sed -i -- 's/qvlan_profile = importlib.import_module("py-json.qvlan_profile")/from lanforge_scripts.py_json import qvlan_profile/g' *.py
sed -i -- 's/vap_profile = importlib.import_module("py-json.vap_profile")/from lanforge_scripts.py_json import vap_profile/g' *.py
sed -i -- 's/station_profile = importlib.import_module("py-json.station_profile")/from lanforge_scripts.py_json import station_profile/g' *.py
sed -i -- 's/PortUtils = port_utils.PortUtils/ /g' *.py
sed -i -- 's/LFCliBase = lfcli_base.LFCliBase/ /g' *.py
sed -i -- 's/pandas_extensions = importlib.import_module("py-json.LANforge.pandas_extensions")/from .LANforge.pandas_extensions import pandas_extensions/g' *.py
sed -i -- 's/pandas_extensions.pandas_extensions/pandas_extensions/g' *.py
sed -i -- 's/vr_profile2 = importlib.import_module("py-json.vr_profile2")/from lanforge_scripts.py_json import vr_profile2/g' *.py
sed -i -- 's/port_probe = importlib.import_module("py-json.port_probe")/from lanforge_scripts.py_json import port_probe/g' *.py
sed -i -- 's/LFRequest.LFRequest/LFRequest/g' *.py

# fix py_dashboard files
sed -i -- 's/from GrafanaRequest/from lanforge_scripts.py_dashboard.GrafanaRequest/g' *.py
sed -i -- 's/from InfluxRequest/from lanforge_scripts.py_dashboard.InfluxRequest/g' *.py
sed -i -- 's/from GhostRequest/from lanforge_scripts.py_dashboard.GhostRequest/g' *.py

#fix py_json files
sed -i -- 's/from LANforge/from .LANforge/g' *.py
sed -i -- 's/from realm/from .realm/g' *.py
sed -i -- 's/from cv_test_manager/from .cv_test_manager/g' *.py
sed -i -- 's/from lf_cv_base/from .lf_cv_base/g' *.py
sed -i -- 's/from lfdata/from .lfdata/g' *.py
sed -i -- 's/from base_profile/from .base_profile/g' *.py
sed -i -- 's/from test_utility/from .test_utility/g' *.py


# shellcheck disable=SC2039
realmfiles=("l3_cxprofile"
            "l4_cxprofile"
            "lf_attenmod"
            "multicast_profile"
            "http_profile"
            "station_profile"
            "fio_endp_profile"
            "test_group_profile"
            "dut_profile"
            "vap_profile"
            "mac_vlan_profile"
            "wifi_monitor_profile"
            "gen_cxprofile"
            "qvlan_profile"
            "lfdata")
# shellcheck disable=SC2039
for i in "${realmfiles[@]}"; do
str="s/from ${i}/from .${i}/g"
sed -i -- "${str}" realm.py
done
sed -i -- 's/from lanforge_scripts.LANforge/from .LANforge/g' realm.py
sed -i -- 's/from port_utils/from .port_utils/g' *.py

#fix py_scripts files
sed -i -- 's/from lf_report/from lanforge_scripts.py_scripts import lf_report/g' *.py
sed -i -- 's/from lf_graph/from lanforge_scripts.py_scripts.lf_graph/g' *.py
sed -i -- 's/from create_station/from lanforge_scripts.py_scripts.create_station/g' *.py
sed -i -- 's/from cv_test_reports/from .cv_test_reports/g' *.py

rm -r deprecated

cd LANforge || exit 1
echo "
from .add_dut import dut_params, dut_flags
from .add_file_endp import fe_fstype, fe_payload_list, fe_fio_flags, fe_base_endpoint_types
#from .lf_json_autogen import LFJsonGet, LFJsonPost
from .lfcli_base import LFCliBase
from .LFRequest import LFRequest
from .LFUtils import *
from .pandas_extensions import pandas_extensions" > __init__.py
sed -i -- 's/import importlib/ /g' *.py
sed -i -- 's/Logg = importlib.import_module("lanforge_client.logg")/from lanforge_client import logg/g' *.py
sed -i -- 's/lanforge_api = importlib.import_module("lanforge_client.lanforge_api")/from lanforge_client import lanforge_api/g' *.py
sed -i -- 's/from LFRequest import LFRequest/from .LFRequest import LFRequest/g' *.py
sed -i -- 's/from LFRequest/from .LFRequest/g' *.py
sed -i -- 's/from LANforge import LFRequest/import .LFRequest/g' LFUtils.py
sed -i -- 's/from LFUtils/from .LFUtils/g' *.py
sed -i -- 's/from LANforge.LFUtils/from .LFUtils/g' *.py
sed -i -- 's/from LANforge import LFRequest/from . import LFRequest/g' *.py
sed -i -- 's/import LANforge/import /g' *.py
sed -i -- 's/import LANforge.LFUtils/from . import LFUtils/g' *.py
sed -i -- 's/import LANforge.LFRequest/ /g' lfcli_base.py
sed -i -- 's/import .LFRequest/from . import LFRequest/g' *.py
sed -i -- 's/import .LFUtils/from . import LFUtils/g' *.py
sed -i -- 's/LANforge.LFUtils./LFUtils./g' *.py
sed -i -- 's/lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")/from .lfcli_base import LFCliBase/g' *.py
sed -i -- 's/LFRequest = importlib.import_module("py-json.LANforge.LFRequest")/from .LFRequest import LFRequest/g' *.py
sed -i -- 's/LFRequest.LFRequest/LFRequest/g' *.py
sed -i -- 's/LFCliBase = lfcli_base.LFCliBase/from .lfcli_base import LFCliBase/g' *.py

#Convert from importlib to pip compliant method
sed -i -- 's/LFUtils = importlib.import_module("py-json.LFUtils.)/from .LFUtils import debug_printer/g' *.py
sed -i -- 's/LFUtils.debug_printer/debug_printer/g' *.py
sed -i -- 's/LFRequest = importlib.import_module("py-json.LFRequest.)/from .LFRequest import debug_printer/g' *.py
sed -i -- 's/lanforge-scripts/lanforge_scripts/g' *.py
sed -i -- 's/LFUtils.debug_printer/debug_printer/g' *.py
sed -i -- 's/lf_json_autogen = importlib.import_module("py-json.LANforge.lf_json_autogen")/from .lf_json_autogen import LFJsonPost/g' *.py
sed -i -- 's/LFJsonPost = lf_json_autogen.LFJsonPost/ /g' *.py

cd ../../py_dashboard || exit 1
echo "
from .GrafanaRequest import GrafanaRequest
from .InfluxRequest import RecordInflux
from .GhostRequest import GhostRequest" > __init__.py
sed -i -- 's/import importlib/ /g' *.py
sed -i -- 's/GrafanaRequest = importlib.import_module("py-dashboard.GrafanaRequest")/from .GrafanaRequest import GrafanaRequest/g' *.py
sed -i -- 's/InfluxRequest = importlib.import_module("py-dashboard.InfluxRequest")/from .InfluxRequest import RecordInflux/g' *.py
sed -i -- 's/RecordInflux = InfluxRequest.RecordInflux/ /g' *.py

echo "${ARCHIVE}"
py_modules=(        'ap_ctl'
                    'emailHelper'
                    'lf_mail'
                    'lf_tos_plus_test'
                    'lf_tx_power'
                    'tos_plus_auto'
                    'auto_install_gui'
                    'cpu_stats'
                    'lf_sniff'
                    'lf_tos_test'
                    'openwrt_ctl'
                    'stationStressTest'
                    'wifi_ctl_9800_3504')
if [[ $ARCHIVE -eq 1 ]]; then
  echo "Saving archive to ${TARGET_DIR}"
  cd ..
  mkdir lanforge_scripts
  mv py_json lanforge_scripts
  mv py_dashboard lanforge_scripts
  mv py_scripts lanforge_scripts
  mv label-printer lanforge_scripts/label_printer
  mv "auto-install-gui.py" "auto_install_gui.py"
  for i in "${py_modules[@]}"; do
    mv "$i.py" lanforge_scripts || exit 1
  done
  rm ./*.pl
  rm ./*.bash
  rm -r gui
  rm -r json
  rm -r LANforge
  rm -r __pycache__
  mv ./*.py lanforge_scripts
  mv lanforge_scripts/setup.py .
  rm speedtest-cli
  rm WlanPro.desktop
  mv wifi_diag lanforge_scripts
  #tar -zcvf ${TARGET_DIR}/lanforge_scripts.tar.gz *
  #zip ${TARGET_DIR}/lanforge_scripts.zip *
  python3 -m pip install --upgrade build
  python3 -m build --wheel
  echo "You can find the wheel in ../lanforge_scripts/dist/*.whl"
else
  echo "Not saving archive"
fi
exit 0