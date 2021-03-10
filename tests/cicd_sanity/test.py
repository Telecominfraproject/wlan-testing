import ap_connect
from datetime import datetime
import os

now = datetime.now()
os.system('mkdir -p AP_Logs/' + now.strftime('%B') + '/' + now.strftime('%d'))

logread_output, dmesg_output = ap_connect.copy_logread_dmesg('192.168.2.150', 'root', 'openwifi')

with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime('%d') + '/log_read.log', 'w') as file:
    file.write(logread_output)

with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime('%d') + '/dmesg.log', 'w') as file:
    file.write(dmesg_output)
