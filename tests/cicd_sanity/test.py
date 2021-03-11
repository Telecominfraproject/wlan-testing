import ap_connect
import datetime
import os

file = 'nola02_test'
key = 'ecw5410'

now = datetime.datetime.now()
# os.system('mkdir -p AP_Logs/' + now.strftime('%B') + '/' + now.strftime('%d') + '/' + file)
#
# logread_output, dmesg_output = ap_connect.copy_logread_dmesg('192.168.2.150', 'root', 'openwifi')
#
# with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime('%d') + '/' + file + '/' + key + '_logread_' + now.strftime('%X').replace(':', '-'), 'w') as log_file:
#     log_file.write(logread_output)
#
# with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime('%d') + '/' + file + '/' + key + '_dmesg_' + now.strftime('%X').replace(':', '-'), 'w') as dmesg_file:
#     dmesg_file.write(dmesg_output)
