import sys
import os
import importlib

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../")))


if os.environ.get("LF_USE_AUTOGEN") == 1:
    lanforge_api = importlib.import_module("lanforge_client.lanforge_api")
    LFJsonCommand = lanforge_api.LFJsonCommand
    set_port_current_flags = LFJsonCommand.SetPortCurrentFlags.__members__
    set_port_cmd_flags = LFJsonCommand.SetPortCmdFlags.__members__
    set_port_interest_flags = LFJsonCommand.SetPortInterest.__members__

else:
    set_port_current_flags = {
        "if_down":              0x1,  # Interface Down
        "fixed_10bt_hd":        0x2,  # Fixed-10bt-HD (half duplex)
        "fixed_10bt_fd":        0x4,  # Fixed-10bt-FD
        "fixed_100bt_hd":       0x8,  # Fixed-100bt-HD
        "fixed_100bt_fd":       0x10,  # Fixed-100bt-FD
        "auto_neg":             0x100,  # auto-negotiate
        "adv_10bt_hd":          0x100000,  # advert-10bt-HD
        "adv_10bt_fd":          0x200000,  # advert-10bt-FD
        "adv_100bt_hd":         0x400000,  # advert-100bt-HD
        "adv_100bt_fd":         0x800000,  # advert-100bt-FD
        "adv_flow_ctl":         0x8000000,  # advert-flow-control
        "promisc":              0x10000000,  # PROMISC
        "use_dhcp":             0x80000000,  # USE-DHCP
        "adv_10g_hd":           0x400000000,  # advert-10G-HD
        "adv_10g_fd":           0x800000000,  # advert-10G-FD
        "tso_enabled":          0x1000000000,  # TSO-Enabled
        "lro_enabled":          0x2000000000,  # LRO-Enabled
        "gro_enabled":          0x4000000000,  # GRO-Enabled
        "ufo_enabled":          0x8000000000,  # UFO-Enabled
        "gso_enabled":          0x10000000000,  # GSO-Enabled
        "use_dhcpv6":           0x20000000000,  # USE-DHCPv6
        "rxfcs":                0x40000000000,  # RXFCS
        "no_dhcp_rel":          0x80000000000,  # No-DHCP-Release
        "staged_ifup":          0x100000000000,  # Staged-IFUP
        "http_enabled":         0x200000000000,  # Enable HTTP (nginx) service for this port.
        "ftp_enabled":          0x400000000000,  # Enable FTP (vsftpd) service for this port.
        "aux_mgt":              0x800000000000,  # Enable Auxillary-Management flag for this port.
        "no_dhcp_restart":      0x1000000000000,  # Disable restart of DHCP on link connect (ie, wifi).
                                            # This should usually be enabled when testing wifi
                                            # roaming so that the wifi station can roam
                                            # without having to re-acquire a DHCP lease each
                                            # time it roams.
        "ignore_dhcp":          0x2000000000000,  # Don't set DHCP acquired IP on interface,
                                            # instead print CLI text message. May be useful
                                            # in certain wifi-bridging scenarios where external
                                            # traffic-generator cannot directly support DHCP.

        "no_ifup_post":         0x4000000000000,  # Skip ifup-post script if we can detect that we
                                            # have roamed. Roaming  is considered true if
                                            # the IPv4 address has not changed.

        "radius_enabled":       0x20000000000000,  # Enable RADIUS service (using hostapd as radius server)
        "ipsec_client":         0x40000000000000,  # Enable client IPSEC xfrm on this port.
        "ipsec_concentrator":   0x80000000000000,  # Enable concentrator (upstream) IPSEC xfrm on this port.
        "service_dns":          0x100000000000000,  # Enable DNS (dnsmasq) service on this port.
    }
    set_port_cmd_flags = {
        "reset_transceiver":    0x1,  # Reset transciever
        "restart_link_neg":     0x2,  # Restart link negotiation
        "force_MII_probe":      0x4,  # Force MII probe
        "no_hw_probe":          0x8,  # Don't probe hardware
        "probe_wifi":           0x10,  # Probe WIFI
        "new_gw_probe":         0x20,  # Force new GW probe
        "new_gw_probe_dev":     0x40,  # Force new GW probe for ONLY this interface
        "from_user":            0x80,  # from_user (Required to change Mgt Port config
                                        # (IP, DHCP, etc)
        "skip_port_bounce":     0x100,  # skip-port-bounce  (Don't ifdown/up
                                        # interface if possible.)
        "from_dhcp":            0x200,  # Settings come from DHCP client.
        "abort_if_scripts":     0x400,  # Forceably abort all ifup/down scripts on this Port.
        "use_pre_ifdown":       0x800,  # Call pre-ifdown script before bringing interface down.
    }
    set_port_interest_flags = {
        "command_flags"     :  0x1,               # apply command flags
        "current_flags"     :  0x2,               # apply current flags
        "ip_address"        :  0x4,               # IP address
        "ip_Mask"           :  0x8,               # IP mask
        "ip_gateway"        :  0x10,              # IP gateway
        "mac_address"       :  0x20,              # MAC address
        "supported_flags"   :  0x40,              # apply supported flags
        "link_speed"        :  0x80,              # Link speed
        "mtu"               :  0x100,             # MTU
        "tx_queue_length"   :  0x200,             # TX Queue Length
        "promisc_mode"      :  0x400,             # PROMISC mode
        "interal_use_1"     :  0x800,             # (INTERNAL USE)
        "alias"             :  0x1000,            # Port alias
        "rx_all"            :  0x2000,            # Rx-ALL
        "dhcp"              :  0x4000,            # including client-id.
        "rpt_timer"         :  0x8000,            # Report Timer
        "bridge"            :  0x10000,           # BRIDGE
        "ipv6_addrs"        :  0x20000,           # IPv6 Address
        "bypass"            :  0x40000,           # Bypass
        "gen_offload"       :  0x80000,           # Generic offload flags, everything but LRO
        "cpu_mask"          :  0x100000,          # CPU Mask, useful for pinning process to CPU core
        "lro_offload"       :  0x200000,          # LRO (Must be disabled when used in Wanlink,
                                                    # and probably in routers)

        "sta_br_id"         :  0x400000,          # WiFi Bridge identifier.  0 means no bridging.
        "ifdown"            :  0x800000,          # Down interface
        "dhcpv6"            :  0x1000000,         # Use DHCPv6
        "rxfcs"             :  0x2000000,         # RXFCS
        "dhcp_rls"          :  0x4000000,         # DHCP release
        "svc_httpd"         :  0x8000000,         # Enable/disable HTTP Service for a port
        "svc_ftpd"          :  0x10000000,        # Enable/disable FTP Service for a port
        "aux_mgt"           :  0x20000000,        # Enable/disable Auxillary-Management for a port
        "no_dhcp_conn"      :  0x40000000,        # Enable/disable NO-DHCP-ON-CONNECT flag for a port
        "no_apply_dhcp"     :  0x80000000,        # Enable/disable NO-APPLY-DHCP flag for a port
        "skip_ifup_roam"    :  0x100000000,       # Enable/disable SKIP-IFUP-ON-ROAM flag for a port
    }
#
