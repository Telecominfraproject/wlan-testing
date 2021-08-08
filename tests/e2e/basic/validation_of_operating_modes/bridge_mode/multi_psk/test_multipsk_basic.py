setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g_br",
             "appliedRadios": ["2G"],
             "security_key": "something",
             "multi-psk": [
                 {
                     "key": "aaaaaaaa",
                     "vlan-id": 100
                 },
                 {
                     "key": "bbbbbbbb"
                 }
             ],
             },
            {"ssid_name": "ssid_wpa2_5g_br",
             "appliedRadios": ["5G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 100,
                 "egress-rate": 100
             }
             }]},
    "rf": {},
    "radius": False
}
