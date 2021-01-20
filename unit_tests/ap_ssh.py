##################################################################################
# Module contains functions to get specific data from AP CLI using SSH
#
# Used by Nightly_Sanity and Throughput_Test #####################################
##################################################################################

import paramiko
from paramiko import SSHClient
import socket

owrt_args = "--prompt root@OpenAp -s serial --log stdout --user root --passwd openwifi"

def ssh_cli_connect(command_line_args):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ap_ip = command_line_args.ap_ip
    ap_username = command_line_args.ap_username
    ap_password = command_line_args.ap_password

    jumphost_ip = command_line_args.ap_jumphost_address
    jumphost_username = command_line_args.ap_jumphost_username
    jumphost_password = command_line_args.ap_jumphost_password
    jumphost_port = command_line_args.ap_jumphost_port

    if command_line_args.ap_jumphost_address != None:
        print("Connecting to jumphost: %s@%s:%s with password: %s"%(jumphost_username, jumphost_ip, jumphost_port, jumphost_password))
        client.connect(jumphost_ip, username=jumphost_username, password=jumphost_password,
                       port=jumphost_port, timeout=10)
    else:
        print("Connecting to AP with ssh: %s@%s with password: %s"%(ap_username, ap_ip, jumphost_password))
        client.connect(ap_ip, username=ap_username, password=ap_password, timeout=10)
    return client

def ssh_cli_active_fw(command_line_args):
    try:
        client = ssh_cli_connect(command_line_args)

        jumphost_wlan_testing = command_line_args.ap_jumphost_wlan_testing
        jumphost_tty = command_line_args.ap_jumphost_tty

        ap_cmd = "/usr/opensync/bin/ovsh s AWLAN_Node -c | grep FW_IMAGE_ACTIVE"
        if command_line_args.ap_jumphost_address != None:
            cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\""%(jumphost_wlan_testing, owrt_args, jumphost_tty, ap_cmd)
            stdin, stdout, stderr = client.exec_command(cmd)
        else:
            stdin, stdout, stderr = client.exec_command(ap_cmd)

        version_matrix = str(stdout.read(), 'utf-8')
        err = str(stderr.read(), 'utf-8')
        print("version-matrix: %s  stderr: %s"%(version_matrix, err))
        version_matrix_split = version_matrix.partition('FW_IMAGE_ACTIVE","')[2]
        cli_active_fw = version_matrix_split.partition('"],[')[0]
        #print("Active FW is",cli_active_fw)

        ap_cmd = "/usr/opensync/bin/ovsh s Manager -c | grep status"
        if command_line_args.ap_jumphost_address != None:
            cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\""%(jumphost_wlan_testing, owrt_args, jumphost_tty, ap_cmd)
            stdin, stdout, stderr = client.exec_command(cmd)
        else:
            stdin, stdout, stderr = client.exec_command(ap_cmd)

        status = str(stdout.read(), 'utf-8')
        err = str(stderr.read(), 'utf-8')

        print("status: %s  stderr: %s"%(status, err))

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

def iwinfo_status(command_line_args):
    try:
        client = ssh_cli_connect(command_line_args)

        jumphost_wlan_testing = command_line_args.ap_jumphost_wlan_testing
        jumphost_tty = command_line_args.ap_jumphost_tty

        ap_cmd = "iwinfo | grep ESSID"
        if command_line_args.ap_jumphost_address != None:
            cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\""%(jumphost_wlan_testing, owrt_args, jumphost_tty, ap_cmd)
            stdin, stdout, stderr = client.exec_command(cmd)
        else:
            stdin, stdout, stderr = client.exec_command(ap_cmd)

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


def ap_ssh_ovsh_nodec(command_line_args, key):
    try:
        jumphost_wlan_testing = command_line_args.ap_jumphost_wlan_testing
        jumphost_tty = command_line_args.ap_jumphost_tty

        client = ssh_cli_connect(command_line_args)

        ap_cmd = "/usr/opensync/bin/ovsh s AWLAN_Node -c"
        if command_line_args.ap_jumphost_address != None:
            cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\""%(jumphost_wlan_testing, owrt_args, jumphost_tty, ap_cmd)
            stdin, stdout, stderr = client.exec_command(cmd)
        else:
            stdin, stdout, stderr = client.exec_command(ap_cmd)

        output = str(stdout.read(), 'utf-8')

        if key != None:
            for line in output.splitlines():
                toks = line.split(':', 1)
                try:
                    k = toks[0].strip(' ')
                    v = toks[1].strip(' ')
                    if k == 'id':
                        return v
                except Exception as e1:
                    print(e1)
                    print(line)
                    print(toks)

        return output

    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication Error, Check Credentials")
        return "ERROR"
    except paramiko.SSHException:
        print("Cannot SSH to the AP")
        return "ERROR"
    except socket.timeout:
        print("AP Unreachable")
        return "ERROR"

# This can throw exceptions, calling code beware.
def ap_ssh_cmd(command_line_args, ap_cmd):
    jumphost_wlan_testing = command_line_args.ap_jumphost_wlan_testing
    jumphost_tty = command_line_args.ap_jumphost_tty

    client = ssh_cli_connect(command_line_args)

    if command_line_args.ap_jumphost_address != None:
        cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\""%(jumphost_wlan_testing, owrt_args, jumphost_tty, ap_cmd)
        stdin, stdout, stderr = client.exec_command(cmd)
    else:
        stdin, stdout, stderr = client.exec_command(ap_cmd)

    output = str(stdout.read(), 'utf-8')
    return output

def get_vif_config(command_line_args):
    try:
        client = ssh_cli_connect(command_line_args)

        jumphost_wlan_testing = command_line_args.ap_jumphost_wlan_testing
        jumphost_tty = command_line_args.ap_jumphost_tty

        ap_cmd = "/usr/opensync/bin/ovsh s Wifi_VIF_Config -c | grep 'ssid               :'"

        if command_line_args.ap_jumphost_address != None:
            cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\""%(jumphost_wlan_testing, owrt_args, jumphost_tty, ap_cmd)
            stdin, stdout, stderr = client.exec_command(cmd)
        else:
            stdin, stdout, stderr = client.exec_command(ap_cmd)

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

def get_vif_state(command_line_args):
    try:
        client = ssh_cli_connect(command_line_args)

        jumphost_wlan_testing = command_line_args.ap_jumphost_wlan_testing
        jumphost_tty = command_line_args.ap_jumphost_tty

        ap_cmd = "/usr/opensync/bin/ovsh s Wifi_VIF_State -c | grep 'ssid               :'"

        if command_line_args.ap_jumphost_address != None:
            cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\""%(jumphost_wlan_testing, owrt_args, jumphost_tty, ap_cmd)
            stdin, stdout, stderr = client.exec_command(cmd)
        else:
            stdin, stdout, stderr = client.exec_command(ap_cmd)

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
