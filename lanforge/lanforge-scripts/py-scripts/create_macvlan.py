#!/usr/bin/env python3
import sys
import os
import importlib
import argparse
import logging

logger = logging.getLogger(__name__)

if sys.version_info[0] != 3:
    logger.critical("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
add_file_endp = importlib.import_module("py-json.LANforge.add_file_endp")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")


class CreateMacVlan(Realm):
    def __init__(self, host, port,
                 upstream_port="eth1",
                 num_ports=1,
                 macvlan_parent=None,
                 first_mvlan_ip=None,
                 netmask=None,
                 gateway=None,
                 dhcp=True,
                 port_list=None,
                 ip_list=None,
                 connections_per_port=1,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port, debug_=_debug_on,
                         _exit_on_error=_exit_on_error,
                         _exit_on_fail=_exit_on_fail)
        self.port = port
        self.upstream_port = upstream_port
        self.port_list = []
        self.connections_per_port = connections_per_port
        self.ip_list = ip_list
        self.netmask = netmask
        self.gateway = gateway
        self.dhcp = dhcp
        if macvlan_parent is not None:
            self.macvlan_parent = macvlan_parent
            self.port_list = port_list

        self.mvlan_profile = self.new_mvlan_profile()

        self.mvlan_profile.num_macvlans = int(num_ports)
        self.mvlan_profile.desired_macvlans = self.port_list
        self.mvlan_profile.macvlan_parent = self.macvlan_parent[2]
        self.mvlan_profile.shelf = self.macvlan_parent[0]
        self.mvlan_profile.resource = self.macvlan_parent[1]
        self.mvlan_profile.dhcp = dhcp
        self.mvlan_profile.netmask = netmask
        self.mvlan_profile.first_ip_addr = first_mvlan_ip
        self.mvlan_profile.gateway = gateway

        self.created_ports = []

    def build(self):
        # Build stations
        print("Creating MACVLANs")
        if self.mvlan_profile.create(
            admin_down=False,
            sleep_time=0,
            debug=self.debug):
            self._pass("MACVLAN build finished")
            self.created_ports += self.mvlan_profile.created_macvlans
        else:
            self._fail("MACVLAN port build failed.")


def main():
    parser = LFCliBase.create_bare_argparse(
        prog='create_macvlan.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Creates MACVLAN endpoints.''',

        description='''\
create_macvlan.py:
--------------------
Generic command layout:
./create_macvlan.py --macvlan_parent <port> --num_ports <num ports>
                 --first_mvlan_ip <first ip in series> --netmask <netmask to use> --gateway <gateway ip addr>

./create_macvlan.py --macvlan_parent eth2 --num_ports 3 --first_mvlan_ip 192.168.92.13
                 --netmask 255.255.255.0 --gateway 192.168.92.1

./create_macvlan.py --macvlan_parent eth1 --num_ports 3
                 --use_ports eth1#0,eth1#1,eth1#2 --connections_per_port 2

./create_macvlan.py --macvlan_parent eth1 --num_ports 3
                 --first_mvlan_ip 10.40.3.100 --netmask 255.255.240.0 --gateway 10.40.0.1
                 --add_to_group test_wo

./create_macvlan.py --macvlan_parent eth1 --num_ports 3
                 --use_ports eth1#0=10.40.3.103,eth1#1,eth1#2 --connections_per_port 2
                 --netmask 255.255.240.0 --gateway 10.40.0.1

                 You can only add MAC-VLANs to Ethernet, Bonding, Redir, and 802.1Q VLAN devices.

''')
    parser.add_argument(
        '--num_stations',
        help='Number of stations to create',
        default=0)
    parser.add_argument(
        '-u',
        '--upstream_port',
        help='non-station port that generates traffic: <resource>.<port>, e.g: 1.eth1',
        default='1.eth1')
    parser.add_argument(
        '--macvlan_parent',
        help='specifies parent port for macvlan creation',
        required=True)
    parser.add_argument(
        '--first_port',
        help='specifies name of first port to be used',
        default=None)
    parser.add_argument(
        '--num_ports',
        help='number of ports to create',
        default=1)
    parser.add_argument(
        '--connections_per_port',
        help='specifies number of connections to be used per port',
        default=1,
        type=int)
    parser.add_argument(
        '--use_ports',
        help='list of comma separated ports to use with ips, \'=\' separates name and ip'
        '{ port_name1=ip_addr1,port_name1=ip_addr2 }. '
        'Ports without ips will be left alone',
        default=None)
    parser.add_argument(
        '--first_mvlan_ip',
        help='specifies first static ip address to be used or dhcp',
        default=None)
    parser.add_argument(
        '--netmask',
        help='specifies netmask to be used with static ip addresses',
        default=None)
    parser.add_argument(
        '--gateway',
        help='specifies default gateway to be used with static addressing',
        default=None)
    parser.add_argument(
        '--cxs',
        help='list of cxs to add/remove depending on use of --add_to_group or --del_from_group',
        default=None)

    # TODO:  Use lfcli_base for common arguments.
    parser.add_argument('--log_level',
                        default=None,
                        help='Set logging level: debug | info | warning | error | critical')
    parser.add_argument('--lf_logger_config_json',
                        help="--lf_logger_config_json <json file> , json configuration of logger")
    args = parser.parse_args()

    logger_config = lf_logger_config.lf_logger_config()
    # set the logger level to requested value
    logger_config.set_level(level=args.log_level)
    logger_config.set_json(json_file=args.lf_logger_config_json)

    args.macvlan_parent = LFUtils.name_to_eid(args.macvlan_parent)
    port_list = []
    ip_list = []
    if args.first_port is not None and args.use_ports is not None:
        if args.first_port.startswith("sta"):
            if (args.num_ports is not None) and (int(args.num_ports) > 0):
                start_num = int(args.first_port[3:])
                num_ports = int(args.num_ports)
                port_list = LFUtils.port_name_series(
                    prefix="sta",
                    start_id=start_num,
                    end_id=start_num + num_ports - 1,
                    padding_number=10000)
        else:
            if (args.num_ports is not None) and args.macvlan_parent is not None and (
                    int(args.num_ports) > 0) and args.macvlan_parent[2] in args.first_port:
                start_num = int(
                    args.first_port[args.first_port.index('#') + 1:])
                num_ports = int(args.num_ports)
                port_list = LFUtils.port_name_series(
                    prefix=args.macvlan_parent[2] + "#",
                    start_id=start_num,
                    end_id=start_num + num_ports - 1,
                    padding_number=100000)
            else:
                raise ValueError(
                    "Invalid values for num_ports [%s], macvlan_parent [%s], and/or first_port [%s].\n"
                    "first_port must contain parent port and num_ports must be greater than 0" %
                    (args.num_ports, args.macvlan_parent, args.first_port))
    else:
        if args.use_ports is None:
            num_ports = int(args.num_ports)
            port_list = LFUtils.port_name_series(
                prefix=args.macvlan_parent[2] + "#",
                start_id=0,
                end_id=num_ports - 1,
                padding_number=100000)
        else:
            temp_list = args.use_ports.split(',')
            for port in temp_list:
                port_list.append(port.split('=')[0])
                if '=' in port:
                    ip_list.append(port.split('=')[1])
                else:
                    ip_list.append(0)

            if len(port_list) != len(ip_list):
                raise ValueError(
                    temp_list, " ports must have matching ip addresses!")

    if args.first_mvlan_ip is not None:
        if args.first_mvlan_ip.lower() == "dhcp":
            dhcp = True
        else:
            dhcp = False
    else:
        dhcp = True
    # print(port_list)

    # exit(1)
    ip_test = CreateMacVlan(args.mgr,
                            args.mgr_port,
                            port_list=port_list,
                            ip_list=ip_list,
                            upstream_port=args.upstream_port,
                            _debug_on=args.debug,
                            macvlan_parent=args.macvlan_parent,
                            first_mvlan_ip=args.first_mvlan_ip,
                            netmask=args.netmask,
                            gateway=args.gateway,
                            dhcp=dhcp,
                            num_ports=args.num_ports,
                            connections_per_port=args.connections_per_port,
                            # want a mount options param
                            )

    ip_test.build()

    # TODO:  Cleanup by default, add --noclean option to not do cleanup.

    if ip_test.passes():
        print('Created %s MacVlan connections' % args.num_ports)
        ip_test.exit_success()
    else:
        ip_test.exit_fail()


if __name__ == "__main__":
    main()
