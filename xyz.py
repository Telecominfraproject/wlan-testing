# ele_list = ['False', 'cisco series 9800', 'scheme ssh', '1645615520.000371 INFO     Spawn: ssh -p8888 -o PubkeyAuthentication=no admin@localhost', 'wifi_ctl_9800_3504.py 262', 'logg <Logger __main__ (INFO)>', "1645615522.732797 INFO     b'Password:' wifi_ctl_9800_3504.py 114", "1645615522.733179 INFO     9800 received password prompt will send password: Cisco123 i:4 before b'\\r' after b'Password:' wifi_ctl_9800_3504.py 477", "1645615522.783352 INFO     b'Cisco123' wifi_ctl_9800_3504.py 114", "1645615523.859770 INFO     b'WLC2#' wifi_ctl_9800_3504.py 114", "1645615523.860230 INFO     9800 SSH Successfully received # prompt i:4 j:0 before b' \\r\\n\\r\\n\\r\\n' after b'WLC2#' wifi_ctl_9800_3504.py 482", '1645615524.060805 INFO     Command to Process :: Ap[AP2C57.4152.385C] Action[show_ap_bssid_24g] Value[None]  wifi_ctl_9800_3504.py 996', 'Ap[AP2C57.4152.385C] Action[show_ap_bssid_24g] Value[None]', '1645615524.061102 INFO     action show_ap_bssid_24g series 9800 wifi_ctl_9800_3504.py 1582', '1645615524.061244 INFO     Command[show ap name AP2C57.4152.385C wlan dot11 24ghz] wifi_ctl_9800_3504.py 1654', "1645615524.111590 INFO     b'show ap name AP2C57.4152.385C wlan dot11 24ghz' wifi_ctl_9800_3504.py 114", '1645615524.612546 INFO     command sent show ap name AP2C57.4152.385C wlan dot11 24ghz wifi_ctl_9800_3504.py 1657', "1645615524.613034 INFO     b'show ap name' wifi_ctl_9800_3504.py 114", "1645615524.884146 INFO     b'AP2C57.4152.385C wlan dot11 24ghz\\r\\nSlot id  : 0\\r\\n  WLAN ID    BSSID\\r\\n  -------------------------\\r\\n  1          1416.9d53.58c0\\r\\n  2          1416.9d53.58c1\\r\\n\\r\\n\\r\\nWLC2#' wifi_ctl_9800_3504.py 114", '1645615524.884692 INFO     expect index: 1 wifi_ctl_9800_3504.py 1663', 'show ap name AP2C57.4152.385C wlan dot11 24ghz', 'Slot id  : 0', 'WLAN ID    BSSID', '-------------------------', '1          1416.9d53.58c0', '2          1416.9d53.58c1', '1645615524.884841 INFO     WLC2# prompt received will send logout, loop_count: 1 wifi_ctl_9800_3504.py 1672', "1645615524.935126 INFO     b'logout' wifi_ctl_9800_3504.py 114", '1645615525.035705 INFO     send close to the egg child process wifi_ctl_9800_3504.py 1730']
# indices = [i for i, s in enumerate(ele_list) if 'BSSID' in s]
# data = indices[1]
# data2 = data + 1
# data3 = data + 2
# data4 = data + 3
# data5 = data + 4
# acc_data = ele_list[int(data)]
# acc_data2 = ele_list[int(data2)]
# acc_data3 = ele_list[int(data3)]
# acc_data4 = ele_list[int(data4)]
# acc_data5 = ele_list[int(data5)]
# wlan_id_list = []
# wlan_bssid = []
# if acc_data == "WLAN ID    BSSID":
#     if acc_data2 == "-------------------------":
#         id_list = acc_data3.split()
#         # print(id_list)
#         if id_list[0] == "1":
#             wlan_id_list.append(id_list)
#             wlan_bssid.append(id_list[1])
#         else:
#             print("no wlan on slot 1 presnt")
#         id_list1 = acc_data4.split()
#         # print(id_list1)
#         if id_list1[0] == "2":
#             wlan_bssid.append(id_list1[1])
# print(wlan_bssid)
#

x =  ['687d.b45f.5c30']
y = x[0].replace(".", '')
z = ':'.join(a+b for a,b in zip(y[::2], y[1::2]))
print(y)
print(z)