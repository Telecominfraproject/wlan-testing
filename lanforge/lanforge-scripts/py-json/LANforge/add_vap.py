add_vap_flags = {
"enable_wpa"           : 0x10,            # Enable WPA
"hostapd_config"       : 0x20,            # Use Custom hostapd config file.
"enable_80211d"        : 0x40,            # Enable 802.11D to broadcast country-code & channels in VAPs
"short_preamble"       : 0x80,            # Allow short-preamble
"pri_sec_ch_enable"    : 0x100,           # Enable Primary/Secondary channel switch.
"wep_enable"           : 0x200,           # Enable WEP Encryption
"wpa2_enable"          : 0x400,           # Enable WPA2 Encryption
"disable_ht40"         : 0x800,           # Disable HT-40 (will use HT-20 if available).
"verbose"              : 0x10000,         # Verbose-Debug:  Increase debug info in wpa-supplicant and hostapd logs.
"80211u_enable"        : 0x20000,         # Enable 802.11u (Interworking) feature.
"80211u_auto"          : 0x40000,         # Enable 802.11u (Interworking) Auto-internetworking feature.  Always enabled currently.
"80211u_gw"            : 0x80000,         # AP Provides access to internet (802.11u Interworking)
"80211u_additional"    : 0x100000,        # AP requires additional step for access (802.11u Interworking)
"80211u_e911"          : 0x200000,        # AP claims emergency services reachable (802.11u Interworking)
"80211u_e911_unauth"   : 0x400000,        # AP provides Unauthenticated emergency services (802.11u Interworking)
"hs20_enable"          : 0x800000,        # Enable Hotspot 2.0 (HS20) feature.  Requires WPA-2.
"disable_dgaf"         : 0x1000000,       # AP Disable DGAF (used by HotSpot 2.0).
"8021x_radius"         : 0x2000000,       # Use 802.1x (RADIUS for AP).
"80211r_pmska_cache"   : 0x4000000,       # Enable oportunistic PMSKA caching for WPA2 (Related to 802.11r).
"disable_ht80"         : 0x8000000,       # Disable HT80 (for AC chipset NICs only)
"80211h_enable"        : 0x10000000,      # Enable 802.11h (needed for running on DFS channels)  Requires 802.11d.
"osen_enable"          : 0x40000000,      # Enable OSEN protocol (OSU Server-only Authentication)
"ht160_enable"         : 0x100000000,     # Enable HT160 mode.
"create_admin_down"    : 0x1000000000,    # Station should be created admin-down.
"use-wpa3"             : 0x10000000000,   # Enable WPA-3 (SAE Personal) mode.
"use-bss-load"         : 0x20000000000,   # Enable BSS Load IE in Beacons and Probe Responses (.11e).
"use-rrm-report"       : 0x40000000000,   # Enable Radio measurements IE in beacon and probe responses.
"use-bss-transition"   : 0x80000000000,   # Enable BSS transition.
}
