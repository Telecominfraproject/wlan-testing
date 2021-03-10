##################################################################################
# Module contains functions to get specific data from AP CLI using SSH
#
# Used by Nightly_Sanity and Throughput_Test #####################################
##################################################################################

import paramiko
from paramiko import SSHClient
import socket
import os
import subprocess

owrt_args = "--prompt root@OpenAp -s serial --log stdout --user root --passwd openwifi"

def ssh_cli_active_fw(ap_ip, username, password):
    print(ap_ip)
    try:
        if 'tty' in ap_ip:
            print("AP is connected using serial cable")
            ap_cmd = '/usr/opensync/bin/ovsh s AWLAN_Node -c | grep FW_IMAGE_ACTIVE'
            cmd = "cd ../../lanforge/lanforge-scripts && python3 openwrt_ctl.py %s -t %s --action cmd --value \"%s\""%(owrt_args, ap_ip, ap_cmd)
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as p:
                output, errors = p.communicate()
            version_matrix = str(output.decode('utf-8').splitlines())
            version_matrix_split = version_matrix.partition('FW_IMAGE_ACTIVE","')[2]
            cli_active_fw = version_matrix_split.partition('"],[')[0]
            print(cli_active_fw)

            ap_cmd = '/usr/opensync/bin/ovsh s Manager -c | grep status'
            cmd = "cd ../../lanforge/lanforge-scripts && python3 openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (owrt_args, ap_ip, ap_cmd)
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as p:
                output, errors = p.communicate()
            status = str(output.decode('utf-8').splitlines())

        else:
            print("AP is accessible by SSH")
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ap_ip, username=username, password=password, timeout=5)
            stdin, stdout, stderr = client.exec_command('/usr/opensync/bin/ovsh s AWLAN_Node -c | grep FW_IMAGE_ACTIVE')
            version_matrix = str(stdout.read(), 'utf-8')
            err = str(stderr.read(), 'utf-8')
            #print("version-matrix: %s  stderr: %s" % (version_matrix, err))
            version_matrix_split = version_matrix.partition('FW_IMAGE_ACTIVE","')[2]
            cli_active_fw = version_matrix_split.partition('"],[')[0]
            stdin, stdout, stderr = client.exec_command('/usr/opensync/bin/ovsh s Manager -c | grep status')
            status = str(stdout.read(), 'utf-8')


        print("status: %s"  %(status))

        if "ACTIVE" in status:
            # print("AP is in Active state")
            state = "active"
        elif "BACKOFF" in status:
            # print("AP is in Backoff state")
            state = "backoff"
        else:
            # print("AP is not in Active state")
            state = "unknown"

        cli_info = {
            "state": state,
            "active_fw": cli_active_fw
        }

        return (cli_info)

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
        if 'tty' in ap_ip:
            ap_cmd = 'iwinfo | grep ESSID'
            cmd = "cd ../../lanforge/lanforge-scripts && python3 openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
            owrt_args, ap_ip, ap_cmd)
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as p:
                output, errors = p.communicate()
            for line in output.decode('utf-8').splitlines():
                print(line)

        else:
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
        if 'tty' in ap_ip:
            ap_cmd = "/usr/opensync/bin/ovsh s Wifi_VIF_Config -c | grep 'ssid               :'"
            cmd = "cd ../../lanforge/lanforge-scripts && python3 openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
            owrt_args, ap_ip, ap_cmd)
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as p:
                output, errors = p.communicate()
            ssid_output_raw = output.decode('utf-8').splitlines()
            raw = output.decode('utf-8').splitlines()
            ssid_output = []
            for line in raw:
                if 'ssid               :' in line:
                    ssid_output.append(line)
            print(ssid_output)
            ssid_list = [s.replace('ssid               : ','') for s in ssid_output]
            return ssid_list
        else:
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
        if 'tty' in ap_ip:
            ap_cmd = "/usr/opensync/bin/ovsh s Wifi_VIF_State -c | grep 'ssid               :'"
            cmd = "cd ../../lanforge/lanforge-scripts && python3 openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
            owrt_args, ap_ip, ap_cmd)
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as p:
                output, errors = p.communicate()
            ssid_output_raw = output.decode('utf-8').splitlines()
            raw = output.decode('utf-8').splitlines()
            ssid_output = []
            for line in raw:
                if 'ssid               :' in line:
                    ssid_output.append(line)
            print(ssid_output)
            ssid_list = [s.replace('ssid               : ','') for s in ssid_output]
            return ssid_list
        else:
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

def copy_logread_dmesg(ap_ip, username, password):
    try:
        if 'tty' in ap_ip:
            ap_cmd = "logread"
            cmd = "cd ../../lanforge/lanforge-scripts && python3 openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
                owrt_args, ap_ip, ap_cmd)
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as p:
                output, errors = p.communicate()
            logread_output = output.decode('utf-8')

            ap_cmd = "dmesg"
            cmd = "cd ../../lanforge/lanforge-scripts && python3 openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
                owrt_args, ap_ip, ap_cmd)
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as p:
                output, errors = p.communicate()
            dmesg_output = output.decode('utf-8')

            return logread_output, dmesg_output

        else:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ap_ip, username=username, password=password, timeout=5)
            stdin, stdout, stderr = client.exec_command('logread')
            logread_output = str(stdout.read(), 'utf-8')

            stdin, stdout, stderr = client.exec_command('dmesg')
            dmesg_output = str(stdout.read(), 'utf-8')

            return logread_output, dmesg_output

    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication Error, Check Credentials")
        return "ERROR"
    except paramiko.SSHException:
        print("Cannot SSH to the AP")
        return "ERROR"
    except socket.timeout:
        print("AP Unreachable")
        return "ERROR"

