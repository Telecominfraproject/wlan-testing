# import os
# import sys
# import base64
# import urllib.request
# from bs4 import BeautifulSoup
# import ssl
# import subprocess
# from artifactory import ArtifactoryPath
# import tarfile
# import paramiko
# from paramiko import SSHClient
# from scp import SCPClient
# import pexpect
# from pexpect import pxssh
# import paramiko
# from scp import SCPClient
# import pprint
# from pprint import pprint
# from os import listdir
# import re
#
# # For finding files
# # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
# import glob
#
# external_results_dir = / var / tmp / lanforge
#
# local_dir = os.getenv('LOG_DIR')
# print("Local Directory where all files will be copied and logged", local_dir)
# cicd_user = os.getenv('CICD_USER')
# print("cicd_user = ", cicd_user)
# cicd_pw = os.getenv('CICD_PW')
# print("cicd pw =", cicd_pw)
# ap_pw = os.getenv('AP_PW')
# ap_user = os.getenv('AP_USER')
# tr_user = os.getenv('TR_USER')
# print("Testrail user id = ", tr_user)
# tr_pw = os.getenv('TR_PW')
# print("Testrail password =", tr_pw)
# aws_host = '3.96.56.0'
# aws_user = 'ubuntu'
#
# if sys.version_info[0] != 3:
#     print("This script requires Python 3")
#     exit(1)
# if 'py-json' not in sys.path:
#     sys.path.append('../py-json')
#
# from LANforge.LFUtils import *
# # if you lack __init__.py in this directory you will not find sta_connect module#
# import sta_connect
# import testrail_api
# from sta_connect import StaConnect
# from testrail_api import APIClient
#
# client: APIClient = APIClient('https://telecominfraproject.testrail.com')
# client.user = tr_user
# client.password = tr_pw
#
# print('Beginning file download with requests')
#
#
# class GetBuild:
#     def __init__(self):
#         self.user = cicd_user
#         self.password = cicd_pw
#         ssl._create_default_https_context = ssl._create_unverified_context
#
#     def get_latest_image(self, url):
#
#         auth = str(
#             base64.b64encode(
#                 bytes('%s:%s' % (cicd_user, cicd_pw), 'utf-8')
#             ),
#             'ascii'
#         ).strip()
#         headers = {'Authorization': 'Basic ' + auth}
#
#         ''' FIND THE LATEST FILE NAME'''
#         print(url)
#         req = urllib.request.Request(url, headers=headers)
#         response = urllib.request.urlopen(req)
#         html = response.read()
#         soup = BeautifulSoup(html, features="html.parser")
#         last_link = soup.find_all('a', href=True)[-1]
#         latest_file = last_link['href']
#
#         filepath = local_dir
#         os.chdir(filepath)
#         # file_url = url + latest_file
#
#         ''' Download the binary file from Jfrog'''
#         path = ArtifactoryPath(url, auth=(cicd_user, cicd_pw))
#         path.touch()
#         for file in path:
#             print('File =', file)
#
#         path = ArtifactoryPath(file, auth=(cicd_user, cicd_pw))
#         print("file to be downloaded :", latest_file)
#         print("File Path:", file)
#         with path.open() as des:
#             with open(latest_file, "wb") as out:
#                 out.write(des.read())
#         des.close()
#         print("Extract the tar.gz file and upgrade the AP ")
#         housing_tgz = tarfile.open(latest_file)
#         housing_tgz.extractall()
#         housing_tgz.close()
#         return "pass"
#         print("Extract the tar file, and copying the file to  Linksys AP directory")
#         # with open("/Users/syamadevi/Desktop/syama/ea8300/ap_sysupgrade_output.log", "a") as output:
#         #   subprocess.call("scp /Users/syamadevi/Desktop/syama/ea8300/openwrt-ipq40xx-generic-linksys_ea8300-squashfs-sysupgrade.bin root@192.100.1.1:/tmp/openwrt-ipq40xx-generic-linksys_ea8300-squashfs-sysupgrade.bin",shell=True, stdout=output,
#         #                 stderr=output)
#
#         print('SSH to Linksys and upgrade the file')
#
#         '''
#
#         ssh = SSHClient()
#         ssh.load_system_host_keys()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(hostname='192.100.1.1',
#                     port='22',
#                     username='root',
#                     password='Dadun123$',
#                     look_for_keys=False,
#                     pkey='load_key_if_relevant')
#
#         # SCPCLient takes a paramiko transport as its only argument
#         scp = SCPClient(ssh.get_transport())
#
#         scp.put('test.txt', 'testD.txt')
#         scp.close()
#
#
#
#        # client = paramiko.SSHClient()
#         #client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         #client.connect('192.100.1.1', username='syama', password='Dadun123$')
#
#         stdin, stdout, stderr = ssh.exec_command('sysupgrade /tmp/openwrt-ipq40xx-generic-linksys_ea8300-squashfs-sysupgrade.bin')
#
#         for line in stdout:
#             print (line.strip('\n'))
#         client.close()
#         '''
#
#     def run_opensyncgw_in_docker(self):
#         # user_password = 'fepv6nj9guCPeEHC'
#         # my_env = os.environ.copy()
#         # my_env["userpass"] = user_password
#         # my_command = 'python --version'
#         # subprocess.Popen('echo', env=my_env)
#         with open(local_dir + "docker_jfrog_login.log", "a") as output:
#             subprocess.call(
#                 "docker login --username" + cicd_user + "--password" + cicd_pw + " https://tip-tip-wlan-cloud-docker-repo.jfrog.io",
#                 shell=True, stdout=output,
#                 stderr=output)
#         with open(local_dir + "opensyncgw_upgrade.log", "a") as output:
#             subprocess.call(
#                 "docker pull tip-tip-wlan-cloud-docker-repo.jfrog.io/opensync-gateway-and-mqtt:0.0.1-SNAPSHOT",
#                 shell=True, stdout=output,
#                 stderr=output)
#         with open(local_dir + "opensyncgw.log", "a") as output:
#             subprocess.call("docker run --rm -i -p 1883:1883 -p 6640:6640 -p 6643:6643 -p 4043:4043 \
#   -v ~/mosquitto/data:/mosquitto/data \
#   -v ~/mosquitto/log:/mosquitto/log \
#   -v ~/wlan-pki-cert-scripts:/opt/tip-wlan/certs \
#   -v ~/app/log:/app/logs \
#   -v ~//app/config:/app/config \
#   -e OVSDB_CONFIG_FILE='/app/config/config_2_ssids.json' \
#   tip-tip-wlan-cloud-docker-repo.jfrog.io/opensync-gateway-and-mqtt:0.0.1-SNAPSHOT", shell=True, stdout=output,
#                             stderr=output)
#             print("opensync Gateway is running")
#             return "pass"
#
#     def run_opensyncgw_in_aws(self):
#         try:
#             s = pxssh.pxssh()
#
#             os.chdir(local_dir)
#             print("AWS OPENSYNC GW UPGRADE VIA HELM")
#             print(
#                 'Helm upgrades the latest image in the GW if a new image is found from jfrog and the AWS gateway is not upto date ')
#             # makesure the client key file is in the fame directory to login to AWS VM
#             s.login(aws_host, aws_user, ssh_key='id_key.pem')
#             s.sendline('kubectl get pods')
#
#             # run a command
#             s.prompt()  # match the prompt
#             print(s.before)  # print everything before the prompt.
#             s.sendline(
#                 'helm upgrade tip-wlan wlan-cloud-helm/tip-wlan/ -n default -f wlan-cloud-helm/tip-wlan/resources/environments/dev-amazon.yaml')
#             s.prompt()  # match the prompt
#             print(s.before)  # print everything before the prompt.
#             s.sendline('kubectl get pods')
#
#             # run a command
#             s.prompt()  # match the prompt
#             print(s.before)  # print everything before the prompt.
#             s.logout()
#             return "pass"
#
#         except pxssh.ExceptionPxssh as e:
#             print("ALERT !!!!!! pxssh failed on login.")
#             print(e)
#
#
# class openwrt_ap:
#
#     def ap_upgrade(src, user2, host2, tgt, pwd, opts='', timeout=60):
#         ''' Performs the scp command. Transfers file(s) from local host to remote host '''
#         print("AP Model getting upgarded is :", apModel)
#         if apModel == "ecw5410":
#             ap_firmware = 'openwrt-ipq806x-generic-edgecore_ecw5410-squashfs-nand-sysupgrade.bin'
#             AP_IP = '10.10.10.207'
#         else:
#             if apModel == "ea8300":
#                 ap_firmware = 'openwrt-ipq40xx-generic-linksys_ea8300-squashfs-sysupgrade.bin'
#                 AP_IP = '10.10.10.208'
#         host2 = AP_IP
#         src = src + ap_firmware
#         print("src =", src)
#         print("AP IP ", AP_IP)
#         print("AP USER =", ap_user)
#         print("AP PASSWORD =", ap_pw)
#         cmd = f'''/bin/bash -c "scp {opts} {src} {user2}@{AP_IP}:{tgt}"'''
#         print("Executing the following cmd:", cmd, sep='\n')
#
#         tmpFl = '/tmp/scp.log'
#         fp = open(tmpFl, 'wb')
#         print(tmpFl)
#         childP = pexpect.spawn(cmd, timeout=timeout)
#         try:
#             childP.sendline(cmd)
#             childP.expect([f"{user2}@{host2}'s password:"])
#             childP.sendline(pwd)
#             childP.logfile = fp
#             childP.expect(pexpect.EOF)
#             childP.close()
#             fp.close()
#             fp = open(tmpFl, 'r')
#             stdout = fp.read()
#             fp.close()
#
#             if childP.exitstatus != 0:
#                 raise Exception(stdout)
#         except KeyboardInterrupt:
#             childP.close()
#             fp.close()
#             return
#         print(stdout)
#
#         try:
#             s = pxssh.pxssh()
#             s.login(host2, user2, pwd)
#             # s.sendline('sysupgrade /tmp/openwrt-ipq40xx-generic-linksys_ea8300-squashfs-sysupgrade.bin&')
#             s.sendline('sysupgrade /tmp/openwrt-ipq806x-generic-edgecore_ecw5410-squashfs-nand-sysupgrade.bin&')
#             # s.logout()
#             # s.prompt()  # match the prompt
#             print(s.before)  # print everything before the prompt.
#             sleep(100)
#             # s.login(host2, user2, pwd)
#             s.prompt()
#             # os.system(f"scp {local_dir}/cacert.pem root@10.10.10.207:/usr/plume/certs/ca.pem")
#             # os.system(f"scp {local_dir}/clientcert.pem root@10.10.10.207:/usr/plume/certs/client.pem")
#             # os.system(f"scp {local_dir}/clientkey_dec.pem  root@10.10.10.207:/usr/plume/certs/client_dec.key")
#             # s.sendline('service opensync restart')
#             # s.prompt()  # match the prompt
#             # print(s.before)  # print everything before the prompt.
#             s.logout()
#             return "pass"
#         except pxssh.ExceptionPxssh as e:
#             print("ALERT !!!!!! pxssh failed on login.")
#             print(e)
#
#     def apCopyCert(src, user2, host2, tgt, pwd, opts='', timeout=60):
#
#         print("Copying the AP Certs")
#         '''
#         s = pxssh.pxssh()
#         print(src, users2,pwd)
#         s.login(host2, user2, pwd)
#         s.prompt()  # match the prompt
#         print("Copying ca.pem")
#         os.system(f"scp {src}/cacert.pem root@10.10.10.207:/usr/plume/certs/ca.pem")
#         print("Copying the client.pem")
#         os.system(f"scp {src}/clientcert.pem root@10.10.10.207:/usr/plume/certs/client.pem")
#         print("Copying the client_dec.key")
#         os.system(f"scp {src}/clientkey_dec.pem  root@10.10.10.207:/usr/plume/certs/client_dec.key")
#         s.sendline('service opensync restart')
#         s.prompt()  # match the prompt
#         print(s.before)  # print everything before the prompt.
#         s.logout()
#         '''
#         cacert = src + "ca.pem"
#         clientcert = src + "client.pem"
#         clientkey = src + "client_dec.key"
#         tgt = "/usr/plume/certs"
#         ap_pw
#
#         print("src =", src)
#         print("AP IP ", host2)
#         print("AP USER =", ap_user)
#         print("AP PASSWORD =", ap_pw)
#         # cmd = f'''/bin/bash -c "scp {opts} {src} {user2}@{AP_IP}:{tgt}"'''
#         # cmd = f'''/bin/bash -c "scp {opts} {cacert} {user2}@{AP_IP}:{tgt}"'''
#         # cmd = f'''/bin/bash -c "scp {opts} {clientcert} {user2}@{AP_IP}:{tgt}"'''
#         cmd = f'''/bin/bash -c "scp {opts} {cacert} {clientcert} {clientkey} {user2}@{host2}:{tgt}"'''
#         print("Executing the following cmd:", cmd, sep='\n')
#         tmpFl = '/tmp/cert.log'
#         fp = open(tmpFl, 'wb')
#         print(tmpFl)
#         childP = pexpect.spawn(cmd, timeout=timeout)
#         try:
#             childP.sendline(cmd)
#             childP.expect([f"{user2}@{host2}'s password:"])
#             childP.sendline(ap_pw)
#             childP.logfile = fp
#             childP.expect(pexpect.EOF)
#             fp.close()
#             fp = open(tmpFl, 'r')
#             stdout = fp.read()
#             fp.close()
#
#             if childP.exitstatus != 0:
#                 # raise Exception(stdout)
#                 print("there is an excess status non 0")
#         except KeyboardInterrupt:
#             childP.close()
#             fp.close()
#             return
#         print(stdout)
#
#     def restartGw(src, user2, host2, tgt, pwd, opts='', timeout=60):
#         print("Restarting opensync GW")
#         s = pxssh.pxssh()
#         s.login(host2, user2, pwd)
#         # s.sendline('sysupgrade /tmp/openwrt-ipq40xx-generic-linksys_ea8300-squashfs-sysupgrade.bin&')
#         s.sendline('service opensync restart')
#         # s.logout()
#         # s.prompt()  # match the prompt
#         print(s.before)  # print everything before the prompt.
#         s.prompt()
#         s.logout()
#
#
# class RunTest:
#     def TestCase_938(self, rid):
#         '''SINGLE CLIENT CONNECTIVITY'''
#         staConnect = StaConnect("10.10.10.201", 8080, _debugOn=False)
#         staConnect.sta_mode = 0
#         staConnect.upstream_resource = 1
#         staConnect.upstream_port = "eth2"
#         staConnect.radio = "wiphy1"
#         staConnect.resource = 1
#         staConnect.dut_ssid = "autoProvisionedSsid-5u"
#         # staConnect.dut_passwd = "4C0nnectUS!"
#         staConnect.dut_passwd = "12345678"
#         staConnect.dut_security = "wpa2"
#         staConnect.station_names = ["sta01010"]
#         staConnect.runtime_secs = 30
#         staConnect.cleanup_on_exit = True
#         staConnect.run()
#         run_results = staConnect.get_result_list()
#         for result in run_results:
#             print("test result: " + result)
#         # result = 'pass'
#         print("Single Client Connectivity :", staConnect.passes)
#         if staConnect.passes() == True:
#             client.update_testrail(case_id=938, run_id=rid, status_id=1,
#                                    msg='client Connectivity to 5GHZ Open SSID is Passed ')
#         else:
#             client.update_testrail(case_id=938, run_id=rid, status_id=5,
#                                    msg='client connectivity to 5GHZ OPEN SSID is Failed')
#
#     def TestCase_941(self, rid):
#         # MULTI CLIENT CONNECTIVITY
#         staConnect = StaConnect("10.10.10.201", 8080, _debugOn=False)
#         staConnect.sta_mode = 0
#         staConnect.upstream_resource = 1
#         staConnect.upstream_port = "eth2"
#         staConnect.radio = "wiphy1"
#         staConnect.resource = 1
#         staConnect.dut_ssid = "autoProvisionedSsid-5u"
#         # staConnect.dut_passwd = "4C0nnectUS!"
#         staConnect.dut_passwd = "12345678"
#         staConnect.dut_security = "wpa2"
#         staConnect.station_names = ["sta0020", 'sta0021', 'sta0022', 'sta0023']
#         staConnect.runtime_secs = 20
#         staConnect.cleanup_on_exit = True
#         staConnect.run()
#         run_results = staConnect.get_result_list()
#         for result in run_results:
#             print("test result: " + result)
#         if staConnect.passes() == True:
#             client.update_testrail(case_id=941, run_id=rid, status_id=1,
#                                    msg='client Connectivity to 5GHZ Open SSID is Passed ')
#         else:
#             client.update_testrail(case_id=941, run_id=rid, status_id=5,
#                                    msg='client connectivity to 5GHZ OPEN SSID is Failed')
#
#     # Check for externally run test case results.
#     def TestCase_LF_External(self, rid):
#         # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
#         results = glob.glob("%s/*_CICD_RESULTS.txt" % external_results_dir)
#         for r in results:
#             rfile = open(r, 'r')
#             lines = rfile.readlines()
#
#             # File contents looks something like:
#             # CASE_ID 9999
#             # RUN_ID 15
#             # STATUS 1
#             # MSG Test passed nicely
#             # MSG Build ID:  deadbeef
#             # MSG Results:  http://cicd.telecominfraproject.com
#
#             _case_id = -1
#             _status_id = 1  # Default to pass
#             _msg = ""
#             _rid = rid
#
#             for line in Lines:
#                 m = re.search(r'(\S+) (.*)', line)
#                 k = m.group(0);
#                 v = m.group(1);
#
#                 if k == "CASE_ID":
#                     _case_id = v
#                 if k == "RUN_ID":
#                     _rid = v
#                 if k == "STATUS":
#                     _status_id = v
#                 if k == "MSG":
#                     if _msg == "":
#                         _msg == v
#                     else:
#                         _msg += "\n"
#                         _msg += v
#             if _case_id != -1:
#                 client.update_testrail(case_id=_case_id, run_id=_rid, status_id=_status_id, msg=_msg)
#             os.unlink(r)
#
#     def TestCase_939(self, rid):
#         ''' Client Count in MQTT Log'''
#         try:
#             print("Counting clients in MQTT")
#             s = pxssh.pxssh()
#             # aws_host = os.getenv(AWS_HOST)
#             # aws_user=os.getenv(AWS_USER)
#             os.chdir(local_dir)
#             # makesure the client key file is in the fame directory to login to AWS VM
#             s.login(aws_host, aws_user, ssh_key='id_key.pem')
#             s.sendline('kubectl cp tip-wlan-opensync-gw-static-f795d45-ctb5z:/app/logs/mqttData.log mqttData.log')
#             # run a command
#             s.prompt()  # match the prompt
#             print(s.before)  # print everything before the prompt.
#             s.sendline()
#             s.logout()
#             # return "pass"
#             print(aws_host, aws_user)
#             ssh = paramiko.SSHClient()
#             ssh.load_system_host_keys()
#             ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#             k = paramiko.RSAKey.from_private_key_file('id_key.pem')
#             ssh.connect(aws_host, username=aws_user, pkey=k)
#             print("Connected")
#             scp = SCPClient(ssh.get_transport())
#             scp.get("mqttData.log")
#             scp.close()
#             # Get the client Count
#             ClientCount = subprocess.getoutput(
#                 'grep \'{\"nodeID\"\' mqttData.log | grep clientList | tail -1 |cut -d \'=\' -f 3 | json_pp | grep macAddres | grep \'04:F0:21:55\' | tr -d , | sort | uniq | wc -l ')
#             print("client count =", ClientCount)
#             if (int(ClientCount) >= 1):
#                 client.update_testrail(case_id=939, run_id=rid, status_id=1,
#                                        msg=ClientCount + ' Client/Clients Connected ')
#             else:
#                 client.update_testrail(case_id=939, run_id=rid, status_id=5,
#                                        msg='No Client Connected')
#         except pxssh.ExceptionPxssh as e:
#             print("ALERT !!!!!! pxssh failed on login.")
#             print(e)
#
#
# params = {
#     'src': local_dir,
#     'user2': ap_user,
#     'host2': '10.10.10.207',
#     'tgt': '/tmp/',
#     'pwd': ap_pw,
#     'opts': ''
# }
# apModel = "ecw5410"
#
# url = 'https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/'
# url = url + apModel
# projId = client.get_project_id(project_name='WLAN')
# print("TIP WLAN Project ID Is :", projId)
#
# rid = client.get_run_id(test_run_name='TIP-DEMO4')
# print(rid)
# Test: RunTest = RunTest()
# Build: GetBuild = GetBuild()
# '''
# binary_fetch_result = Build.get_latest_image(url)
# print("UPDATING TEST RAIL WITH TEST RESULT FOR CASE_ID 940: Download latest openwrt image from Jfrog")
#
# if binary_fetch_result == 'pass':
#     client.update_testrail(case_id=940, run_id=rid, status_id=1, msg='latest firmware downloaded')
# else:
#     client.update_testrail(case_id=940, run_id=rid, status_id=5, msg='Firmware Download failed')
#
# sleep(10)
# print("Upgrading AP with latest image downloaded")
# ap_upgrade_result = openwrt_ap.ap_upgrade(**params)
# sleep(10)
# print("UPDATING TEST RAIL WITH TEST RESULT FOR CASE_ID 937")
# sleep(10)
# if ap_upgrade_result == 'pass':
#     client.update_testrail(case_id=937, run_id=rid, status_id=1, msg='AP upgraded with latest Firmware')
# else:
#     client.update_testrail(case_id=937, run_id=rid, status_id=5, msg='Firmware upgrade failed in AP ')
# print("Upgrading AWS Opensync gateway with latest docker image from Jfrog")
# OpensyncGw_UpgResult = Build.run_opensyncgw_in_aws()
# if OpensyncGw_UpgResult == 'pass':
#     client.update_testrail(case_id=936, run_id=rid, status_id=1, msg='Opensync GW upgraded with latest Firmware')
# else:
#     client.update_testrail(case_id=936, run_id=rid, status_id=5, msg='Firmware upgrade failed in Opensync Gateway')
# sleep(10)
# '''
# pprint.pprint(params)
# ap_cert_result = openwrt_ap.apCopyCert(**params)
# print("Executing TestCase 938: single Client Connectivity test")
# openwrt_ap.restartGw(**params)
# Test.TestCase_938(rid)
#
# print("Executing TestCase 941: Multi Client Connectivity test")
# Test.TestCase_941(rid)
# sleep(100)
# print("Executing TestCase 939:Counting The number of Clients Connected from MQTT")
# Test.TestCase_939(rid)
#
#
#
#
