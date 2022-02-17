x = ['False', 'cisco series 9800', 'scheme ssh', '1644913208.671843 INFO     Spawn: ssh -p8888 -o PubkeyAuthentication=no admin@localhost', 'wifi_ctl_9800_3504.py 254', 'logg <Logger __main__ (INFO)>', "1644913211.296255 INFO     b'Password:' wifi_ctl_9800_3504.py 111", "1644913211.296565 INFO     9800 received password prompt will send password: Cisco123 i:4 before b'\\r' after b'Password:' wifi_ctl_9800_3504.py 469", "1644913211.346690 INFO     b'Cisco123' wifi_ctl_9800_3504.py 111", "1644913212.422613 INFO     b'WLC2#' wifi_ctl_9800_3504.py 111", "1644913212.422874 INFO     9800 SSH Successfully received # prompt i:4 j:0 before b' \\r\\n\\r\\n\\r\\n' after b'WLC2#' wifi_ctl_9800_3504.py 474", '1644913212.623188 INFO     Command to Process :: Ap[AP2C57.4152.385C] Action[show_wlan_summary] Value[None]  wifi_ctl_9800_3504.py 984', 'Ap[AP2C57.4152.385C] Action[show_wlan_summary] Value[None]', 'command show wlan summary', '1644913212.623288 INFO     action show_wlan_summary series 9800 wifi_ctl_9800_3504.py 1452', '1644913212.623328 INFO     Command[show wlan summary] wifi_ctl_9800_3504.py 1524', "1644913212.673431 INFO     b'show wlan summary' wifi_ctl_9800_3504.py 111", '1644913213.174019 INFO     command sent show wlan summary wifi_ctl_9800_3504.py 1527', "1644913213.174157 INFO     b'show wlan s' wifi_ctl_9800_3504.py 111", "1644913213.343155 INFO     b'ummary\\r\\n\\r\\nNumber of WLANs: 3\\r\\n\\r\\nID   Profile Name                     SSID                             Status Security                                                                                             \\r\\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\\r\\n2    candela2ghz                      candela2ghz                      UP     [WPA2][PSK][AES]                                                                                     \\r\\n3    candela5ghz                      candela5ghz                      UP     [open]                                                                                               \\r\\n4    candela6ghz                      candela6ghz                      UP     [WPA3][SAE][AES]                                                                                     \\r\\n\\r\\nWLC2#' wifi_ctl_9800_3504.py 111", '1644913213.343388 INFO     expect index: 1 wifi_ctl_9800_3504.py 1533', 'show wlan summary', 'Number of WLANs: 3', 'ID   Profile Name                     SSID                             Status Security', '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', '2    candela2ghz                      candela2ghz                      UP     [WPA2][PSK][AES]', '3    candela5ghz                      candela5ghz                      UP     [open]', '4    candela6ghz                      candela6ghz                      UP     [WPA3][SAE][AES]', '1644913213.343424 INFO     WLC2# prompt received will send logout, loop_count: 1 wifi_ctl_9800_3504.py 1542', "1644913213.393524 INFO     b'logout' wifi_ctl_9800_3504.py 111", '1644913213.493747 INFO     send close to the egg child process wifi_ctl_9800_3504.py 1600']
# indices = [i for i, s in enumerate(x) if 'Profile Name' in s]
# print(indices)
# print(x[int(indices[1])])
# print(x[23])
# print(x[24])
# print(x[25])
# print(x[26])
# print(x[27])
# print(type(x[26]))
# ele_list1 = [y for y in (x.strip(" ") for x in x[26].splitlines()) if y]
# print("nikita",ele_list1)
# shiv = ele_list1[0].split()
# print(shiv[1])

ele_list = ['False', 'cisco series 9800', 'scheme ssh', '1645020440.892164 INFO     Spawn: ssh -p8888 -o PubkeyAuthentication=no admin@localhost', 'wifi_ctl_9800_3504.py 257', 'logg <Logger __main__ (INFO)>', "1645020443.532597 INFO     b'Password:' wifi_ctl_9800_3504.py 112", "1645020443.533311 INFO     9800 received password prompt will send password: Cisco123 i:4 before b'\\r' after b'Password:' wifi_ctl_9800_3504.py 472", "1645020443.583640 INFO     b'Cisco123' wifi_ctl_9800_3504.py 112", "1645020444.551045 INFO     b'WLC2#' wifi_ctl_9800_3504.py 112", "1645020444.551557 INFO     9800 SSH Successfully received # prompt i:4 j:0 before b' \\r\\n\\r\\n\\r\\n' after b'WLC2#' wifi_ctl_9800_3504.py 477", '1645020444.752241 INFO     Command to Process :: Ap[AP2C57.4152.385C] Action[show_wlan_summary] Value[None]  wifi_ctl_9800_3504.py 991', 'Ap[AP2C57.4152.385C] Action[show_wlan_summary] Value[None]', 'command show wlan summary', '1645020444.752580 INFO     action show_wlan_summary series 9800 wifi_ctl_9800_3504.py 1459', '1645020444.752726 INFO     Command[show wlan summary] wifi_ctl_9800_3504.py 1531', "1645020444.803075 INFO     b'show wlan summary' wifi_ctl_9800_3504.py 112", '1645020445.304044 INFO     command sent show wlan summary wifi_ctl_9800_3504.py 1534', "1645020445.304592 INFO     b'show wlan s' wifi_ctl_9800_3504.py 112", "1645020445.471429 INFO     b'ummary\\r\\n\\r\\nNumber of WLANs: 4\\r\\n\\r\\nID   Profile Name                     SSID                             Status Security                                                                                             \\r\\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\\r\\n1    ssid_wpa2_5g                     ssid_wpa2_5g                     UP     [WPA2][PSK][AES]                                                                                     \\r\\n2    candela2ghz                      candela2ghz                      UP     [WPA2][PSK][AES]                                                                                     \\r\\n3    candela5ghz                      candela5ghz                      UP     [open]                                                                                               \\r\\n4    candela6ghz                      candela6ghz                      UP     [WPA3][SAE][AES]                                                                                     \\r\\n\\r\\nWLC2#' wifi_ctl_9800_3504.py 112", '1645020445.471954 INFO     expect index: 1 wifi_ctl_9800_3504.py 1540', 'show wlan summary', 'Number of WLANs: 4', 'ID   Profile Name                     SSID                             Status Security', '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', '1    ssid_wpa2_5g                     ssid_wpa2_5g                     UP     [WPA2][PSK][AES]', '2    candela2ghz                      candela2ghz                      UP     [WPA2][PSK][AES]', '3    candela5ghz                      candela5ghz                      UP     [open]', '4    candela6ghz                      candela6ghz                      UP     [WPA3][SAE][AES]', '1645020445.472097 INFO     WLC2# prompt received will send logout, loop_count: 1 wifi_ctl_9800_3504.py 1549', "1645020445.522448 INFO     b'logout' wifi_ctl_9800_3504.py 112", '1645020445.622994 INFO     send close to the egg child process wifi_ctl_9800_3504.py 1607']
# print(ele_list)
indices = [i for i, s in enumerate(ele_list) if 'Profile Name' in s]


print(indices)
data = indices[1]
data2 = data+1
data3 = data+2
data4 = data+3
data5 = data+4
acc_data = ele_list[int(data)]
acc_data2 = ele_list[int(data2)]
acc_data3 = ele_list[int(data3)]
acc_data4 = ele_list[int(data4)]
acc_data5 = ele_list[int(data5)]
print(acc_data4)
ident_list = []
if acc_data == 'ID   Profile Name                     SSID                             Status Security':
    print("yes")
    if acc_data2 == "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------":
        print("yes")
        id_list = acc_data3.split()
        print(id_list)
        if id_list[0] == "1":
            ident_list.append(id_list[1])
        else:
            ident_list.append("0")
        id_list2 = acc_data4.split()
        print(id_list2)
        if id_list2[0] == "2":
            ident_list.append(id_list2[1])
        else :
            ident_list.append("0")
        id_list3 = acc_data5.split()
        print(id_list3)
        if id_list3[0] == "3":
            ident_list.append(id_list3[1])
        else:
            ident_list.append("0")
else:
  print("There is no Profile name")
print(ident_list)
























# res = any('' in ele for ele in ele_list1)
# indices = [i for i, s in enumerate(ele_list1[0]) if '' in s]
# print(indices)
# # print(res)
# for i in ele_list1:
#  print("hi",i)
#  if '' in i:
#   for n in i:
#    print(n)
#    if '' in n:
#     print("space")
#
#
# print(ele_list1[0][5:])