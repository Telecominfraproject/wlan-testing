##################################################################################
# Module contains functions to get specific data from AP CLI using SSH
#
# Used by Nightly_Sanity and Throughput_Test #####################################
##################################################################################

import paramiko
from paramiko import SSHClient
import socket

def ssh_cli_active_fw(ap_ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ap_ip, username=username, password=password, timeout=5)
        stdin, stdout, stderr = client.exec_command('/usr/opensync/bin/ovsh s AWLAN_Node -c | grep FW_IMAGE_ACTIVE')

        version_matrix = str(stdout.read())
        version_matrix_split = version_matrix.partition('FW_IMAGE_ACTIVE","')[2]
        cli_active_fw = version_matrix_split.partition('"],[')[0]
        #print("Active FW is",cli_active_fw)

        stdin, stdout, stderr = client.exec_command('/usr/opensync/bin/ovsh s Manager -c | grep status')
        status = str(stdout.read())

        if "ACTIVE" in status:
            #print("AP is in Active state")
            state = "active"
        elif "BACKOFF" in status:
            #print("AP is in Backoff state")
            state = "backoff"
        else:
            #print("AP is not in Active state")
            state = "unknown"

        cli_info = {
            "state": state,
            "active_fw": cli_active_fw
        }

        return(cli_info)

    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication Error, Check Credentials")
        return "ERROR"
    except paramiko.SSHException:
        print("Cannot SSH to the AP")
        return "ERROR"
    except socket.timeout:
        print("AP Unreachable")
        return "ERROR"

def iwinfo_status(ap_ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ap_ip, username=username, password=password, timeout=5)
        stdin, stdout, stderr = client.exec_command('iwinfo | grep ESSID')

        for line in stdout.read().splitlines():
            print(line)

    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication Error, Check Credentials")
        return "ERROR"
    except paramiko.SSHException:
        print("Cannot SSH to the AP")
        return "ERROR"
    except socket.timeout:
        print("AP Unreachable")
        return "ERROR"

def get_vif_config(ap_ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ap_ip, username=username, password=password, timeout=5)
        stdin, stdout, stderr = client.exec_command(
        "/usr/opensync/bin/ovsh s Wifi_VIF_Config -c | grep 'ssid               :'")

        output = str(stdout.read(), 'utf-8')
        ssid_output = output.splitlines()
        ssid_list = [s.strip('ssid               : ') for s in ssid_output]
        return ssid_list

    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication Error, Check Credentials")
        return "ERROR"
    except paramiko.SSHException:
        print("Cannot SSH to the AP")
        return "ERROR"
    except socket.timeout:
        print("AP Unreachable")
        return "ERROR"

def get_vif_state(ap_ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ap_ip, username=username, password=password, timeout=5)
        stdin, stdout, stderr = client.exec_command(
        "/usr/opensync/bin/ovsh s Wifi_VIF_State -c | grep 'ssid               :'")

        output = str(stdout.read(), 'utf-8')
        ssid_output = output.splitlines()
        ssid_list = [s.strip('ssid               : ') for s in ssid_output]
        return ssid_list

    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication Error, Check Credentials")
        return "ERROR"
    except paramiko.SSHException:
        print("Cannot SSH to the AP")
        return "ERROR"
    except socket.timeout:
        print("AP Unreachable")
        return "ERROR"