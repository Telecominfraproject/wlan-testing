# Flags for the add_sta command
add_sta_flags = {
    "wpa_enable"           : 0x10,         # Enable WPA
    "custom_conf"          : 0x20,         # Use Custom wpa_supplicant config file.
    "wep_enable"           : 0x200,        # Use wpa_supplicant configured for WEP encryption.
    "wpa2_enable"          : 0x400,        # Use wpa_supplicant configured for WPA2 encryption.
    "ht40_disable"         : 0x800,        # Disable HT-40 even if hardware and AP support it.
    "scan_ssid"            : 0x1000,       # Enable SCAN-SSID flag in wpa_supplicant.
    "passive_scan"         : 0x2000,       # Use passive scanning (don't send probe requests).
    "disable_sgi"          : 0x4000,       # Disable SGI (Short Guard Interval).
    "lf_sta_migrate"       : 0x8000,       # OK-To-Migrate (Allow station migration between LANforge radios)
    "verbose"              : 0x10000,      # Verbose-Debug:  Increase debug info in wpa-supplicant and hostapd logs.
    "80211u_enable"        : 0x20000,      # Enable 802.11u (Interworking) feature.
    "80211u_auto"          : 0x40000,      # Enable 802.11u (Interworking) Auto-internetworking feature.  Always enabled currently.
    "80211u_gw"            : 0x80000,      # AP Provides access to internet (802.11u Interworking)
    "80211u_additional"    : 0x100000,     # AP requires additional step for access (802.11u Interworking)
    "80211u_e911"          : 0x200000,     # AP claims emergency services reachable (802.11u Interworking)
    "80211u_e911_unauth"   : 0x400000,     # AP provides Unauthenticated emergency services (802.11u Interworking)
    "hs20_enable"          : 0x800000,     # Enable Hotspot 2.0 (HS20) feature.  Requires WPA-2.
    "disable_gdaf"         : 0x1000000,    # AP:  Disable DGAF (used by HotSpot 2.0).
    "8021x_radius"         : 0x2000000,    # Use 802.1x (RADIUS for AP).
    "80211r_pmska_cache"   : 0x4000000,    # Enable oportunistic PMSKA caching for WPA2 (Related to 802.11r).
    "disable_ht80"         : 0x8000000,    # Disable HT80 (for AC chipset NICs only)
    "ibss_mode"            : 0x20000000,   # Station should be in IBSS mode.
    "osen_enable"          : 0x40000000,   # Enable OSEN protocol (OSU Server-only Authentication)
    "disable_roam"         : 0x80000000,   # Disable automatic station roaming based on scan results.
    "ht160_enable"         : 0x100000000,  # Enable HT160 mode.
    "disable_fast_reauth"  : 0x200000000,  # Disable fast_reauth option for virtual stations.
    "mesh_mode"            : 0x400000000,  # Station should be in MESH mode.
    "power_save_enable"    : 0x800000000,  # Station should enable power-save.  May not work in all drivers/configurations.
    "create_admin_down"    : 0x1000000000, # Station should be created admin-down.
    "wds-mode"             : 0x2000000000, # WDS station (sort of like a lame mesh), not supported on ath10k
    "no-supp-op-class-ie"  : 0x4000000000, # Do not include supported-oper-class-IE in assoc requests.  May work around AP bugs.
    "txo-enable"           : 0x8000000000, # Enable/disable tx-offloads, typically managed by set_wifi_txo command
    "use-wpa3"             : 0x10000000000, # Enable WPA-3 (SAE Personal) mode.
    "use-bss-transition"     : 0x80000000000 # Enable BSS transition.
}
add_sta_modes = {
    "AUTO"        :  0,        #  802.11g
    "802.11a"     :  1,        #  802.11a
    "b"           :  2,        #  802.11b
    "g"           :  3,        #  802.11g
    "abg"         :  4,        #  802.11abg
    "abgn"        :  5,        #  802.11abgn
    "bgn"         :  6,        #  802.11bgn
    "bg"          :  7,        #  802.11bg
    "abgnAC"      :  8,        #  802.11abgn-AC
    "anAC"        :  9,        #  802.11an-AC
    "an"          : 10,        #  802.11an
    "bgnAC"       : 11,        #  802.11bgn-AC
    "abgnAX"      : 12,        #  802.11abgn-AX, a/b/g/n/AC/AX (dual-band AX) support
    "bgnAX"       : 13,        #  802.11bgn-AX
    "anAX"        : 14,        #  802.11an-AX
}
