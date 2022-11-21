#!/usr/bin/env python3
import sys
import os
import importlib
import pprint

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase


class MULTICASTProfile(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port, local_realm,
                 report_timer_=3000, name_prefix_="Unset", number_template_="00000", debug_=False):
        """

        :param lfclient_host:
        :param lfclient_port:
        :param local_realm:
        :param name_prefix_: prefix string for connection
        :param number_template_: how many zeros wide we padd, possibly a starting integer with left padding
        :param debug_:
        """
        super().__init__(lfclient_host, lfclient_port, debug_)
        self.lfclient_url = "http://%s:%s" % (lfclient_host, lfclient_port)
        self.debug = debug_
        self.local_realm = local_realm
        self.report_timer = report_timer_
        self.created_mc = {}
        self.name_prefix = name_prefix_
        self.number_template = number_template_

    def clean_mc_lists(self):
        # Clean out our local lists, this by itself does NOT remove anything from LANforge manager.
        # but, if you are trying to modify existing connections, then clearing these arrays and
        # re-calling 'create' will do the trick.
        self.created_mc = {}

    def get_mc_names(self):
        return self.created_mc.keys()

    def refresh_mc(self, debug_=False):
        for endp_name in self.get_mc_names():
            self.json_post("/cli-json/show_endpoints", {
                "endpoint": endp_name
            }, debug_=debug_)

    def start_mc(self, suppress_related_commands=None, debug_=False):
        if self.debug:
            debug_ = True

        for endp_name in self.get_mc_names():
            print("Starting mcast endpoint: %s" % endp_name)
            json_data = {
                "endp_name": endp_name
            }
            url = "cli-json/start_endp"
            self.local_realm.json_post(url, json_data, debug_=debug_,
                                       suppress_related_commands_=suppress_related_commands)

        pass

    def stop_mc(self, suppress_related_commands=None, debug_=False):
        if self.debug:
            debug_ = True
        for endp_name in self.get_mc_names():
            json_data = {
                "endp_name": endp_name
            }
            url = "cli-json/stop_endp"
            self.local_realm.json_post(url, json_data, debug_=debug_,
                                       suppress_related_commands_=suppress_related_commands)

        pass

    def cleanup_prefix(self):
        self.local_realm.cleanup_cxe_prefix(self.name_prefix)

    def cleanup(self, suppress_related_commands=None, debug_=False):
        if self.debug:
            debug_ = True

        for endp_name in self.get_mc_names():
            self.local_realm.rm_endp(endp_name, debug_=debug_, suppress_related_commands_=suppress_related_commands)

    def create_mc_tx(self, endp_type, side_tx, mcast_group="224.9.9.9", mcast_dest_port=9999,
                     suppress_related_commands=None, debug_=False):
        if self.debug:
            debug_ = True

        side_tx_info = self.local_realm.name_to_eid(side_tx)
        side_tx_shelf = side_tx_info[0]
        side_tx_resource = side_tx_info[1]
        side_tx_port = side_tx_info[2]
        side_tx_name = "%smtx-%s-%i" % (self.name_prefix, side_tx_port, len(self.created_mc))

        # add_endp mcast-xmit-sta 1 1 side_tx mc_udp -1 NO 4000000 0 NO 1472 0 INCREASING NO 32 0 0
        json_data = {
            'alias': side_tx_name,
            'shelf': side_tx_shelf,
            'resource': side_tx_resource,
            'port': side_tx_port,
            'type': endp_type,
            'ip_port': -1,
            'is_rate_bursty':
                'NO', 'min_rate': 256000,
            'max_rate': 0,
            'is_pkt_sz_random': 'NO',
            'min_pkt': 1472,
            'max_pkt': 0,
            'payload_pattern': 'INCREASING',
            'use_checksum': 'NO',
            'ttl': 32,
            'send_bad_crc_per_million': 0,
            'multi_conn': 0
        }

        url = "/cli-json/add_endp"
        self.local_realm.json_post(url, json_data, debug_=debug_, suppress_related_commands_=suppress_related_commands)

        json_data = {
            'name': side_tx_name,
            'ttl': 32,
            'mcast_group': mcast_group,
            'mcast_dest_port': mcast_dest_port,
            'rcv_mcast': 'No'
        }

        url = "cli-json/set_mc_endp"
        self.local_realm.json_post(url, json_data, debug_=debug_, suppress_related_commands_=suppress_related_commands)

        self.created_mc[side_tx_name] = side_tx_name

        these_endp = [side_tx_name]
        self.local_realm.wait_until_endps_appear(these_endp, debug=debug_)

    def create_mc_rx(self, endp_type, side_rx, mcast_group="224.9.9.9", mcast_dest_port=9999,
                     suppress_related_commands=None, debug_=False):
        if self.debug:
            debug_ = True

        these_endp = []

        for port_name in side_rx:
            side_rx_info = self.local_realm.name_to_eid(port_name)
            side_rx_shelf = side_rx_info[0]
            side_rx_resource = side_rx_info[1]
            side_rx_port = side_rx_info[2]
            side_rx_name = "%smrx-%s-%i" % (self.name_prefix, side_rx_port, len(self.created_mc))
            # add_endp mcast-rcv-sta-001 1 1 sta0002 mc_udp 9999 NO 0 0 NO 1472 0 INCREASING NO 32 0 0
            json_data = {
                'alias': side_rx_name,
                'shelf': side_rx_shelf,
                'resource': side_rx_resource,
                'port': side_rx_port,
                'type': endp_type,
                'ip_port': 9999,
                'is_rate_bursty': 'NO',
                'min_rate': 0,
                'max_rate': 0,
                'is_pkt_sz_random': 'NO',
                'min_pkt': 1472,
                'max_pkt': 0,
                'payload_pattern': 'INCREASING',
                'use_checksum': 'NO',
                'ttl': 32,
                'send_bad_crc_per_million': 0,
                'multi_conn': 0
            }

            url = "cli-json/add_endp"
            self.local_realm.json_post(url, json_data, debug_=debug_,
                                       suppress_related_commands_=suppress_related_commands)

            json_data = {
                'name': side_rx_name,
                'ttl': 32,
                'mcast_group': mcast_group,
                'mcast_dest_port': mcast_dest_port,
                'rcv_mcast': 'Yes'
            }
            url = "cli-json/set_mc_endp"
            self.local_realm.json_post(url, json_data, debug_=debug_,
                                       suppress_related_commands_=suppress_related_commands)

            self.created_mc[side_rx_name] = side_rx_name
            these_endp.append(side_rx_name)

        self.local_realm.wait_until_endps_appear(these_endp, debug=debug_)

    def to_string(self):
        pprint.pprint(self)
