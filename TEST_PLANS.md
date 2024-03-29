## Test Plans and Markers associated with them are provided in this file :ledger:

:speaking_head: SANITY 

    1. Client Connectivity Tests
        client_connectivity_tests and tls and bridge
        client_connectivity_tests and ttls and nat
        client_connectivity_tests and general and vlan
    2. DFS Test
        dfs_tests and wpa2_personal and bandwidth_80MHz
    3. Dynamic Vlan Test
        dynamic_vlan_tests and wpa2_enterprise and dynamic_precedence_over_ssid or absence_of_radius_vlan_identifier and wpa2_enterprise
    4. MULTI VLAN Test
        multi_vlan_tests and wpa2_personal or multi_vlan_tests and wpa
    5. Rate Limiting Tests
        rate_limiting_tests and upload_download and batch_size_125 and twog
    6. Rate Limiting With Radius Test
        rate_limiting_with_radius_tests and twog_upload_per_ssid or twog_download_perssid_persta
    7. MultiPsk Test
        multi_psk_tests
    8. Throughput Benchmark Test
        peak_throughput_tests and channel_11 and tcp_download and bridge and twog and channel_width_40 and wpa2_personal or peak_throughput_tests and channel_36 and tcp_download and bridge and fiveg and channel_width_80 and wpa2_personal
    9. Test Connectivity
        test_resources
    10. SDK Tests
        ow_sanity_lf and ow_sdk_tests


:speaking_head: INTEROP

    1. Client Connect Tests
        client_connect_tests and general and bridge
        client_connect_tests and general and nat
        client_connect_tests and general and vlan
        client_connect_tests and enterprise and bridge
        client_connect_tests and enterprise and nat
        client_connect_tests and enterprise and vlan
    2. Client Connectivity Tests
        client_connectivity_tests and general and bridge
        client_connectivity_tests and general and nat
        client_connectivity_tests and general and vlan
        client_connectivity_tests and enterprise and bridge
        client_connectivity_tests and enterprise and nat
        client_connectivity_tests and enterprise and vlan
    3. Rate Limiting Tests
        rate_limiting_tests and bridge
        rate_limiting_tests and nat
        rate_limiting_tests and vlan
    4. Toggle Airplane mode Tests (Client Reconnect Tests)
        toggle_airplane_tests and general and bridge
        toggle_airplane_tests and general and nat
        toggle_airplane_tests and general and vlan
        toggle_airplane_tests and enterprise and bridge
        toggle_airplane_tests and enterprise and nat
        toggle_airplane_tests and enterprise and vlan
    5. Toggle Wifi mode Tests (Client Reconnect Tests)
        toggle_wifi_mode and general and bridge
        toggle_wifi_mode and general and nat
        toggle_wifi_mode and general and vlan
        toggle_wifi_mode and enterprise and bridge
        toggle_wifi_mode and enterprise and nat
        toggle_wifi_mode and enterprise and vlan



More Markers related to other test plans will be added soon in the future