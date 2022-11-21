#!/usr/bin/env python3
"""
Library to Run Dataplane Test: Using lf_cv_base class

"""
import sys
import os
import importlib

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lf_cv_base = importlib.import_module("py-json.lf_cv_base")
ChamberViewBase = lf_cv_base.ChamberViewBase


class DataPlaneTest(ChamberViewBase):

    def __init__(self, lfclient_host="localhost", lfclient_port=8080, debug_=False):
        super().__init__(_lfjson_host=lfclient_host, _lfjson_port=lfclient_port, _debug=debug_)
        self.set_config()

    def set_config(self):
        blob_data = """show_events: 1 show_log: 0 port_sorting: 0 kpi_id: Dataplane Pkt-Size bg: 0xE0ECF8 test_rig: show_scan: 1 auto_helper: 0 skip_2: 0 skip_5: 0 skip_5b: 1 skip_dual: 0 skip_tri: 1 selected_dut: TIP duration: 15000 traffic_port: 1.1.136 sta00500 upstream_port: 1.1.2 eth2 path_loss: 10 speed: 85% speed2: 0Kbps min_rssi_bound: -150 max_rssi_bound: 0 channels: AUTO modes: Auto pkts: 60;142;256;512;1024;MTU spatial_streams: AUTO security_options: AUTObandw_options: AUTO traffic_types: UDP;TCP directions: DUT Transmit;DUT Receive txo_preamble: OFDM txo_mcs: 0 CCK, OFDM, HT, VHT txo_retries: No Retry txo_sgi: OFF txo_txpower: 15 attenuator: 0 attenuator2: 0 attenuator_mod: 255 attenuator_mod2: 255 attenuations: 0..+50..950 attenuations2: 0..+50..950 chamber: 0 tt_deg: 0..+45..359 cust_pkt_sz: show_bar_labels: 1 show_prcnt_tput: 0 show_3s: 0 show_ll_graphs: 1 show_gp_graphs: 1 show_1m: 1 pause_iter: 0 show_realtime: 1 operator: mconn: 1 mpkt: 1000 tos: 0 loop_iterations: 1"""
        self.add_text_blobs(type="Plugin-Settings", name="dataplane-test-latest-shivam", data=blob_data)
        pass

    def set_params(self):
        pass

    def run_test(self):
        pass

    def wait_until_test_finishes(self):
        pass

    def collect_reports(self):
        pass


def main():
    DataPlaneTest(lfclient_host="localhost", lfclient_port=8080, debug_=True)


if __name__ == '__main__':
    main()
