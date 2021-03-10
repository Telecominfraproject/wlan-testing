import ap_connect

logread_output, dmesg_output = ap_connect.copy_logread_dmesg('192.168.2.150', 'root', 'openwifi')

print(logread_output)
print('BUFFER--------------------------------------------------------')
print(dmesg_output)
