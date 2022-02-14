#!/usr/bin/env python3
"""
    Script for creating a variable number of virtual routers.
"""
import sys
import os
import importlib
import time
from pprint import pprint

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class CreateVR(Realm):
    def __init__(self,
                 lfclient_host="localhost",
                 lfclient_port=8080,
                 debug=False,
                 # resource=1, # USE name=1.2.vr0 convention instead
                 vr_name=None,
                 ports_list=(),
                 services_list=(),
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _proxy_str=None,
                 _capture_signal_list=()):
        super().__init__(lfclient_host=lfclient_host,
                         lfclient_port=lfclient_port,
                         debug_=debug,
                         _exit_on_error=_exit_on_error,
                         _exit_on_fail=_exit_on_fail,
                         _proxy_str=_proxy_str,
                         _capture_signal_list=_capture_signal_list)

        eid_name = self.name_to_eid(vr_name)
        self.vr_name = eid_name
        self.ports_list = ports_list
        self.services_list = services_list
        self.vr_profile = self.new_vr_profile()

    def clean(self):
        if (self.vr_name is None) or (self.vr_profile.vr_eid is None) and (
                self.vr_profile.vr_eid) == "":
            print("No vr_eid to clean")
            return
        self.rm_port("1.1.rd90a", debug_=self.debug)
        self.rm_port("1.1.rd90b", debug_=self.debug)
        self.wait_until_ports_disappear(sta_list=["1.1.rd90a", "1.1.rd90b"],
                                        debug_=self.debug)

        if (self.vr_profile.vr_eid is not None) \
                and (self.vr_profile.vr_eid[1] is not None) \
                and (self.vr_profile.vr_eid[2] is not None):
            self.vr_profile.cleanup(debug=self.debug)

        if (self.vr_name is not None) \
                and (self.vr_name[1] is not None) \
                and (self.vr_name[2] is not None):
            data = {
                "shelf": 1,
                "resource": self.vr_name[1],
                "router_name": self.vr_name[2]
            }
            self.json_post("/cli-json/rm_vr", data, debug_=self.debug)
            time.sleep(1)
            self.json_post("/cli-json/nc_show_vr", {
                "shelf": 1,
                "resource": self.vr_name[1],
                "router": "all"
            }, debug_=self.debug)
            self.json_post("/cli-json/nc_show_vrcx", {
                "shelf": 1,
                "resource": self.vr_name[1],
                "cx_name": "all"
            }, debug_=self.debug)

    def build(self):
        self.vr_profile.apply_netsmith(
            self.vr_name[1], delay=5, debug=self.debug)
        self.json_post("/cli-json/add_rdd", {
            "shelf": 1,
            "resource": self.vr_name[1],
            "port": "rd90a",
            "peer_ifname": "rd90b",
            "report_timer": "3000"
        })
        self.json_post("/cli-json/add_rdd", {
            "shelf": 1,
            "resource": self.vr_name[1],
            "port": "rd90b",
            "peer_ifname": "rd90a",
            "report_timer": "3000"
        })
        self.wait_until_ports_appear(
            sta_list=[
                "1.1.rd90a",
                "1.1.rd90b"],
            debug_=self.debug)
        self.vr_profile.vrcx_list(
            resource=self.vr_name[1],
            do_sync=True)  # do_sync
        self.vr_profile.create(vr_name=self.vr_name, debug=self.debug)
        self.vr_profile.sync_netsmith(
            resource=self.vr_name[1], debug=self.debug)
        self._pass("created router")

    def start(self):
        """
        Move a vrcx into a router and then movie it out
        :return: void
        """
        # move rd90a into router
        self.vr_profile.refresh_netsmith(
            resource=self.vr_name[1], debug=self.debug)
        if self.debug:
            pprint(("vr_eid", self.vr_name))
        self.vr_profile.wait_until_vrcx_appear(
            resource=self.vr_name[1], name_list=[
                "rd90a", "rd90b"])
        self.vr_profile.add_vrcx(
            vr_eid=self.vr_name,
            connection_name_list="rd90a",
            debug=self.debug)

        self.vr_profile.refresh_netsmith(
            resource=self.vr_name[1], debug=self.debug)
        # test to make sure that vrcx is inside vr we expect
        self.vr_profile.vrcx_list(resource=self.vr_name[1], do_sync=True)
        vr_list = self.vr_profile.router_list(
            resource=self.vr_name[1], do_refresh=True)
        router = self.vr_profile.find_cached_router(
            resource=self.vr_name[1], router_name=self.vr_name[2])
        pprint(("cached router 120: ", router))
        router_eid = LFUtils.name_to_eid(router["eid"])
        pprint(("router eid 122: ", router_eid))
        full_router = self.json_get(
            "/vr/1/%s/%s/%s" %
            (router_eid[0],
             router_eid[1],
             self.vr_name[2]),
            debug_=self.debug)
        pprint(("full router: ", full_router))
        time.sleep(5)
        if router is None:
            self._fail("Unable to find router after vrcx move " + self.vr_name)
            self.exit_fail()

    def stop(self):
        pass


def main():
    parser = LFCliBase.create_bare_argparse(
        prog=__file__,
        description="""\
{f}
--------------------
Command example:
{f} --vr_name 1.vr0 --ports 1.br0,1.rdd0a --services 1.br0=dhcp,nat --services 1.vr0=radvd
{f} --vr_name 2.vr0 --ports 2.br0,2.vap2 --services

    --debug
""".format(f=__file__))
    required = parser.add_argument_group('required arguments')
    required.add_argument('--vr_name', '--vr_names', required=True,
                          help='EID of virtual router, like 1.2.vr0')

    optional = parser.add_argument_group('optional arguments')

    optional.add_argument(
        '--ports',
        default=None,
        required=False,
        help='Comma separated list of ports to add to virtual router')
    optional.add_argument('--services', default=None, required=False,
                          help='Add router services to a port, "br0=nat,dhcp"')

    args = parser.parse_args()

    create_vr = CreateVR(lfclient_host=args.mgr,
                         lfclient_port=args.mgr_port,
                         vr_name=args.vr_name,
                         ports_list=args.ports,
                         services_list=args.services,
                         debug=args.debug,
                         _exit_on_error=True,
                         _exit_on_fail=True)
    create_vr.clean()
    create_vr.build()
    create_vr.start()
    create_vr.monitor()
    # create_vr.stop()
    # create_vr.clean()
    print('Created Virtual Router')


if __name__ == "__main__":
    main()

#
