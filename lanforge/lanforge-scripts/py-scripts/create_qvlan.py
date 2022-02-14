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


class CreateQVlan(Realm):
    def __init__(self,
                 host="localhost",
                 port=8080,
                 qvlan_parent=None,
                 num_ports=1,
                 dhcp=True,
                 netmask=None,
                 first_qvlan_ip=None,
                 gateway=None,
                 port_list=None,
                 ip_list=None,
                 exit_on_error=False,
                 debug=False):
        super().__init__(host, port)
        if port_list is None:
            port_list = []
        if ip_list is None:
            ip_list = []
        self.host = host
        self.port = port
        self.qvlan_parent = qvlan_parent
        self.debug = debug
        self.port_list = port_list
        self.ip_list = ip_list
        self.exit_on_error = exit_on_error

        self.qvlan_profile = self.new_qvlan_profile()
        self.qvlan_profile.num_qvlans = int(num_ports)
        self.qvlan_profile.desired_qvlans = self.port_list
        self.qvlan_profile.qvlan_parent = self.qvlan_parent
        self.qvlan_profile.dhcp = dhcp
        self.qvlan_profile.netmask = netmask
        self.qvlan_profile.first_ip_addr = first_qvlan_ip
        self.qvlan_profile.gateway = gateway
        self.qvlan_profile.dhcp = dhcp

    def build(self):
        logger.info("Creating QVLAN stations")
        if self.qvlan_profile.create(
            debug=self.debug,
            sleep_time=0,
            ):
            self._pass("802.1q VLAN creation successful.")
        else:
            self._fail("802.1q VLAN creation failed.")


def main():
    parser = LFCliBase.create_bare_argparse(
        prog='create_qvlan.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Creates Q-VLAN stations attached to the Eth port of the user's choice.''',

        description='''\
        create_qvlan.py:
        ---------------------
        Generic command ''')
    parser.add_argument('--radio', help='radio EID, e.g: 1.wiphy2')
    parser.add_argument(
        '--qvlan_parent',
        help='specifies parent port for qvlan creation',
        default=None,
        required=True)
    parser.add_argument(
        '--first_port',
        help='specifies name of first port to be used',
        default=None)
    parser.add_argument(
        '--num_ports',
        type=int,
        help='number of ports to create',
        default=1)
    parser.add_argument(
        '--first_qvlan_ip',
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
        '--use_ports',
        help='list of comma separated ports to use with ips, \'=\' separates name and ip { port_name1=ip_addr1,port_name1=ip_addr2 }.  Ports without ips will be left alone',
        default=None)
    tg_group = parser.add_mutually_exclusive_group()
    tg_group.add_argument(
        '--add_to_group',
        help='name of test group to add cxs to',
        default=None)
    parser.add_argument(
        '--cxs',
        help='list of cxs to add/remove depending on use of --add_to_group or --del_from_group',
        default=None)
    parser.add_argument(
        '--use_qvlans',
        help='will create qvlans',
        action='store_true',
        default=False)

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

    update_group_args = {
        "name": None,
        "action": None,
        "cxs": None
    }
    # update_group_args['name'] =
    if args.first_qvlan_ip in ["dhcp", "DHCP"]:
        dhcp = True
    else:
        dhcp = False
    update_group_args['action'] = "add"
    update_group_args['cxs'] = args.cxs
    port_list = []
    ip_list = []
    if args.first_port and args.use_ports:
        if args.first_port.startswith("sta"):
            if args.num_ports and args.num_ports > 0:
                start_num = int(args.first_port[3:])
                port_list = LFUtils.port_name_series(
                    prefix="sta",
                    start_id=start_num,
                    end_id=start_num + args.num_ports - 1,
                    padding_number=10000,
                    radio=args.radio)
                print(1)
        else:
            if args.num_ports and args.qvlan_parent and (args.num_ports > 0) and args.qvlan_parent in args.first_port:
                start_num = int(
                    args.first_port[args.first_port.index('#') + 1:])
                port_list = LFUtils.port_name_series(
                    prefix=str(
                        args.qvlan_parent) + "#",
                    start_id=start_num,
                    end_id=start_num + args.num_ports - 1,
                    padding_number=10000,
                    radio=args.radio)
                print(2)
            else:
                raise ValueError(
                    "Invalid values for num_ports [%s], qvlan_parent [%s], and/or first_port [%s].\n"
                    "first_port must contain parent port and num_ports must be greater than 0" %
                    (args.num_ports, args.qvlan_parent, args.first_port))
    else:
        if not args.use_ports:
            num_ports = int(args.num_ports)
            port_list = LFUtils.port_name_series(
                prefix=str(
                    args.qvlan_parent) + "#",
                start_id=1,
                end_id=num_ports,
                padding_number=10000,
                radio=args.radio)
            print(3)
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

    print(port_list)
    print(ip_list)
    create_qvlan = CreateQVlan(args.mgr,
                               args.mgr_port,
                               qvlan_parent=args.qvlan_parent,
                               num_ports=args.num_ports,
                               dhcp=dhcp,
                               netmask=args.netmask,
                               first_qvlan_ip=args.first_qvlan_ip,
                               gateway=args.gateway,
                               port_list=port_list,
                               ip_list=ip_list,
                               debug=args.debug)
    create_qvlan.build()

    # TODO:  Add code to clean up the stations built, unless --noclean is specified.

    if create_qvlan.passes():
        logging.info('Created %s QVLAN stations' % args.num_ports)
        create_qvlan.exit_success()
    else:
        create_vlan.exit_fail()


if __name__ == "__main__":
    main()
