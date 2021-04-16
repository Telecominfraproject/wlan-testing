# create TCP and UDP traffic, run it a short amount of time.

#########################################################################################################
# Used by Nightly_Sanity and eap_connect ############################################################
#########################################################################################################

#  create TCP and UDP traffic, run it a short amount of time,
#  self.l3_udp_profile.start_cx(): To Start UDP


class createTraffic:

    def __init__(self, localrealm, sta_prefix, resource, upstream_port):
        self.localrealm = localrealm
        self.sta_prefix = sta_prefix
        self.resource = resource
        self.upstream_port = upstream_port
        self.l3_udp_profile = localrealm.new_l3_cx_profile()
        self.l3_tcp_profile = localrealm.new_l3_cx_profile()

    def lf_l3_udp_profile(self):
        # Create UDP endpoints
        self.l3_udp_profile.side_a_min_bps = 128000
        self.l3_udp_profile.side_b_min_bps = 128000
        self.l3_udp_profile.side_a_min_pdu = 1200
        self.l3_udp_profile.side_b_min_pdu = 1500
        self.l3_udp_profile.report_timer = 1000
        self.l3_udp_profile.name_prefix = "udp"
        self.l3_udp_profile.create(endp_type="lf_udp",
                                   side_a=list(self.localrealm.find_ports_like("%s*" % self.sta_prefix)),
                                   side_b="%d.%s" % (self.resource, self.upstream_port),
                                   suppress_related_commands=True)

    def lf_l3_tcp_profile(self):
        # Create TCP endpoints
        self.l3_tcp_profile.side_a_min_bps = 128000
        self.l3_tcp_profile.side_b_min_bps = 56000
        self.l3_tcp_profile.name_prefix = "tcp"
        self.l3_tcp_profile.report_timer = 1000
        self.l3_tcp_profile.create(endp_type="lf_tcp",
                                   side_a=list(self.localrealm.find_ports_like("%s*" % self.sta_prefix)),
                                   side_b="%d.%s" % (self.resource, self.upstream_port),
                                   suppress_related_commands=True)
