from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.driver_context import InitCommandContext, ResourceCommandContext, AutoLoadResource, \
    AutoLoadAttribute, AutoLoadDetails, CancellationContext
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.api.cloudshell_api import CloudShellAPISession
from cloudshell.helpers.scripts.cloudshell_scripts_helpers import get_api_session, get_reservation_context_details
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext 
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help
import cloudshell.helpers.scripts.cloudshell_dev_helpers as dev_helpers
# from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
# from cloudshell.shell.core.context import InitCommandContext, ResourceCommandContext
import mock
from data_model import *
# run 'shellfoundry generate' to generate data model classes
import subprocess
import sys
import os
import importlib
import paramiko
from scp import SCPClient
import requests
import datetime
import os

# command = "./lanforge-scripts/py-scripts/update_dependencies.py"
# print("running:[{}]".format(command))
# process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
# outs, errs = process.communicate()
# print(outs)
# print(errs)

# if 'lanforge-scripts' not in sys.path:
#     sys.path.append('./lanforge-scripts')

# create_wanlink = importlib.import_module("lanforge-scripts.py-json.create_wanlink")
# create_l3 = importlib.import_module("lanforge-scripts.py-scripts.create_l3")
# CreateL3 = create_l3.CreateL3
class LanforgeResourceDriver (ResourceDriverInterface):

    def __init__(self):
        """
        ctor must be without arguments, it is created with reflection at run time
        """
        pass

    def initialize(self, context):
        """
        Initialize the driver session, this function is called everytime a new instance of the driver is created
        This is a good place to load and cache the driver configuration, initiate sessions etc.
        :param InitCommandContext context: the context the command runs on
        """
        pass

    def cleanup(self):
        """
        Destroy the driver session, this function is called everytime a driver instance is destroyed
        This is a good place to close any open sessions, finish writing to log files
        """
        pass

    def get_inventory(self, context):
        """
        Discovers the resource structure and attributes.
        :param AutoLoadCommandContext context: the context the command runs on
        :return Attribute and sub-resource information for the Shell resource you can return an AutoLoadDetails object
        :rtype: AutoLoadDetails
        """
        # See below some example code demonstrating how to return the resource structure and attributes
        # In real life, this code will be preceded by SNMP/other calls to the resource details and will not be static
        # run 'shellfoundry generate' in order to create classes that represent your data model

        '''
        resource = LanforgeResource.create_from_context(context)
        resource.vendor = 'specify the shell vendor'
        resource.model = 'specify the shell model'

        port1 = ResourcePort('Port 1')
        port1.ipv4_address = '192.168.10.7'
        resource.add_sub_resource('1', port1)

        return resource.create_autoload_details()
        '''
        return AutoLoadDetails([], [])

    def orchestration_save(self, context, cancellation_context, mode, custom_params):
        """
        Saves the Shell state and returns a description of the saved artifacts and information
        This command is intended for API use only by sandbox orchestration scripts to implement
        a save and restore workflow
        :param ResourceCommandContext context: the context object containing resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str mode: Snapshot save mode, can be one of two values 'shallow' (default) or 'deep'
        :param str custom_params: Set of custom parameters for the save operation
        :return: SavedResults serialized as JSON
        :rtype: OrchestrationSaveResult
        """

        # See below an example implementation, here we use jsonpickle for serialization,
        # to use this sample, you'll need to add jsonpickle to your requirements.txt file
        # The JSON schema is defined at:
        # https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/saved_artifact_info.schema.json
        # You can find more information and examples examples in the spec document at
        # https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/save%20%26%20restore%20standard.md
        '''
            # By convention, all dates should be UTC
            created_date = datetime.datetime.utcnow()

            # This can be any unique identifier which can later be used to retrieve the artifact
            # such as filepath etc.

            # By convention, all dates should be UTC
            created_date = datetime.datetime.utcnow()

            # This can be any unique identifier which can later be used to retrieve the artifact
            # such as filepath etc.
            identifier = created_date.strftime('%y_%m_%d %H_%M_%S_%f')

            orchestration_saved_artifact = OrchestrationSavedArtifact('REPLACE_WITH_ARTIFACT_TYPE', identifier)

            saved_artifacts_info = OrchestrationSavedArtifactInfo(
                resource_name="some_resource",
                created_date=created_date,
                restore_rules=OrchestrationRestoreRules(requires_same_resource=True),
                saved_artifact=orchestration_saved_artifact)

            return OrchestrationSaveResult(saved_artifacts_info)
      '''
        pass

    def orchestration_restore(self, context, cancellation_context, saved_artifact_info, custom_params):
        """
        Restores a saved artifact previously saved by this Shell driver using the orchestration_save function
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str saved_artifact_info: A JSON string representing the state to restore including saved artifacts and info
        :param str custom_params: Set of custom parameters for the restore operation
        :return: None
        """
        '''
        # The saved_details JSON will be defined according to the JSON Schema and is the same object returned via the
        # orchestration save function.
        # Example input:
        # {
        #     "saved_artifact": {
        #      "artifact_type": "REPLACE_WITH_ARTIFACT_TYPE",
        #      "identifier": "16_08_09 11_21_35_657000"
        #     },
        #     "resource_name": "some_resource",
        #     "restore_rules": {
        #      "requires_same_resource": true
        #     },
        #     "created_date": "2016-08-09T11:21:35.657000"
        #    }

        # The example code below just parses and prints the saved artifact identifier
        saved_details_object = json.loads(saved_details)
        return saved_details_object[u'saved_artifact'][u'identifier']
        '''
        pass

    def attach_file(self, report_server, resid, file_path, user, password, domain, filename):

        # st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        data = {
            'username': user,
            'password': password,
            'domain': domain
        }
        qq = 'Basic ' + requests.put(
            url='http://' + report_server + ':9000/API/Auth/Login',
            data=data
        ).text[1:-1]
        head = {
            'Authorization': qq,
        }
        dat_json ={
            "reservationId": resid,
            "saveFileAs": filename,
            "overwriteIfExists": "true",
        }

        with open(file_path, 'rb') as upload_file:
            xx = requests.post(
                url='http://' + report_server + ':9000/API/Package/AttachFileToReservation',
                headers=head,
                data=dat_json,
                files={'QualiPackage': upload_file}
            )
        return xx

    def send_command(self, context, cmd):
        
        msg = ""
        resource = LanforgeResource.create_from_context(context)
        session = CloudShellAPISession(host=context.connectivity.server_address,
                                       token_id=context.connectivity.admin_auth_token,
                                       domain=context.reservation.domain)
        resource_model_name = resource.cloudshell_model_name
        terminal_ip = context.resource.address
        terminal_user = context.resource.attributes[f'{resource_model_name}.User']
        terminal_pass = session.DecryptPassword(context.resource.attributes[f'{resource_model_name}.Password']).Value

        msg += f"Initializing SSH connection to {terminal_ip}, with user {terminal_user} and password {terminal_pass}\n"
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=terminal_ip, username=terminal_user, password=terminal_pass)

        print(f"running:[{cmd}]")
        (stdin, stdout, stderr) = s.exec_command(cmd)

        output = ''
        errors = ''
        for line in stdout.readlines():
            output += line
        for line in stderr.readlines():
            errors += line
        msg += output + errors
        s.close()
        return msg

    def example_command(self, context):
        """
        this is my example command
        :param ResourceCommandContext context
        :return: str
        """
        resource = LanforgeResource.create_from_context(context)
        session = CloudShellAPISession(host=context.connectivity.server_address,
                                       token_id=context.connectivity.admin_auth_token,
                                       domain=context.reservation.domain)

        resource_model_name = resource.cloudshell_model_name
        password = session.DecryptPassword(context.resource.attributes[f'{resource_model_name}.Password']).Value
        username = context.resource.attributes[f'{resource_model_name}.User']

        msg = f"My resource {resource.name} at address {context.resource.address} has model name {resource_model_name}. "
        msg += f"The username is {username} and password is {password}."
        return msg


    def create_wanlink(self, context, name, latency, rate):
        
        cmd = "/home/lanforge/lanforge-scripts/py-json/create_wanlink.py --host {host} --port_A {port_A} --port_B {port_B} --name \"{name}\" --latency \"{latency}\" --latency_A \"{latency_A}\" --latency_B \"{latency_B}\" --rate {rate} --rate_A {rate_A} --rate_B {rate_B} --jitter {jitter} --jitter_A {jitter_A} --jitter_B {jitter_B} --jitter_freq_A {jitter_freq_A} --jitter_freq_B {jitter_freq_B} --drop_A {drop_A} --drop_B {drop_B}".format(
            host="localhost",
            port_A="eth1",
            port_B="eth2",
            name=name,
            latency=latency,
            latency_A=latency,
            latency_B=latency,
            rate=rate,
            rate_A=rate,
            rate_B=rate,
            jitter="0",
            jitter_A="0",
            jitter_B="0",
            jitter_freq_A="0",
            jitter_freq_B="0",
            drop_A="0",
            drop_B="0"
        )

        output = self.send_command(context, cmd)
        print(output)
        return output

    def create_l3(self, context, name, min_rate_a, min_rate_b, endp_a, endp_b):

        cmd = f"/home/lanforge/lanforge-scripts/py-scripts/create_l3.py --endp_a \"{endp_a}\" --endp_b \"{endp_b}\" --min_rate_a \"{min_rate_a}\" --min_rate_b \"{min_rate_b}\""

        output = self.send_command(context, cmd)
        print(output)
        return output

    def pull_reports(self, hostname="", port=22,
                     username="lanforge", password="lanforge",
                     report_location="/home/lanforge/html-reports/",
                     report_dir="./"):
        
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname="juicer", username=username, password=password, port=port, allow_agent=False, look_for_keys=False)

        with SCPClient(ssh.get_transport()) as scp:
            scp.get(remote_path=report_location, local_path=report_dir, recursive=True)
            scp.close()
        
    def dataplane_test(self, context, instance_name, upstream, station, duration, download_speed, upload_speed, traffic_types, local_lf_report_dir, output_report_dir, mgr):

        cmd = '''/home/lanforge/lanforge-scripts/py-scripts/lf_dataplane_test.py --mgr {mgr} --port 8080 --lf_user lanforge --lf_password lanforge \
                --instance_name {instance_name} --config_name test_con \
                --upstream {upstream} --station {station} --duration {duration}\
                --download_speed {download_speed} --upload_speed {upload_speed} \
                --raw_line 'pkts: 256;1024' \
                --raw_line 'directions: DUT Transmit' \
                --raw_line 'traffic_types: {traffic_types}' \
                --test_rig juicer --pull_report \
                --local_lf_report_dir {local_lf_report_dir}'''.format(
                    instance_name=instance_name,
                    mgr=mgr,
                    upstream=upstream,
                    station=station,
                    duration=duration,
                    download_speed=download_speed,
                    upload_speed=upload_speed,
                    traffic_types=traffic_types,
                    local_lf_report_dir=local_lf_report_dir
                )

        output = self.send_command(context, cmd)
        print(output)
        
        resource = LanforgeResource.create_from_context(context)
        session = CloudShellAPISession(host=context.connectivity.server_address,
                                       token_id=context.connectivity.admin_auth_token,
                                       domain=context.reservation.domain)
        terminal_ip = context.resource.address
        resource_model_name = resource.cloudshell_model_name
        terminal_pass = session.DecryptPassword(context.resource.attributes[f'{resource_model_name}.Password']).Value
        terminal_user = context.resource.attributes[f'{resource_model_name}.User']
        reservation_id = context.reservation.reservation_id
        api = CloudShellSessionContext(context).get_api()
        cwd = os.getcwd()
        # session.AttachFileToReservation(context.reservation.reservation_id, f"C:/Users/Administrator/{output_report_dir}", "C:/Users/Administrator/AppData/Local/Temp", True)
        self.pull_reports(hostname=context.resource.address, port=22,
                          username=terminal_user, password=terminal_pass,
                          report_location="/home/lanforge/html-reports/",
                          report_dir=f"C:/Users/Administrator/{output_report_dir}")

        # api = get_api_session()
        # api.WriteMessageToReservationOutput(reservation_id, f"Attaching report to sandbox.")
        api.WriteMessageToReservationOutput(reservation_id, f"The current working directory is {cwd}")
        self.attach_file(
            report_server=context.connectivity.server_address,
            resid=context.reservation.reservation_id,
            user='admin',
            password='admin',
            domain=context.reservation.domain,
            file_path="C:/Users/Administrator/Desktop/My_Reports/html-reports/dataplane-2021-10-13-03-32-40/dataplane-report-2021-10-13-03-31-50.pdf",
            filename="C:/Users/Administrator/Desktop/test_report.txt"
        )
        return output

    def scenario(self, context, load):
        cmd = f"/home/lanforge/lanforge-scripts/py-scripts/scenario.py --load {load}"

        output = self.send_command(context, cmd)
        print(output)
        return output

if __name__ == "__main__":
    # setup for mock-debug environment
    shell_name = "LanforgeResource"
    cancellation_context = mock.create_autospec(CancellationContext)
    context = mock.create_autospec(ResourceCommandContext)
    context.resource = mock.MagicMock()
    context.reservation = mock.MagicMock()
    context.connectivity = mock.MagicMock()
    context.reservation.reservation_id = "<RESERVATION_ID>"
    context.resource.address = "192.168.100.176"
    context.resource.name = "Lanforge_Resource"
    context.resource.attributes = dict()
    context.resource.attributes["{}.User".format(shell_name)] = "lanforge"
    context.resource.attributes["{}.Password".format(shell_name)] = "lanforge"
    context.resource.attributes["{}.SNMP Read Community".format(shell_name)] = "<READ_COMMUNITY_STRING>"

    # add information for api connectivity
    context.reservation.domain = "Global"
    context.connectivity.server_address = "192.168.100.131"
    driver = LanforgeResourceDriver()
    # print driver.run_custom_command(context, custom_command="sh run", cancellation_context=cancellation_context)
    # result = driver.example_command_with_api(context)

    # driver.create_l3(context, "my_fire", "69000", "41000", "eth1", "eth2")
    # driver.create_wanlink(context, name="my_wanlin", latency="49", rate="6000")
    driver.dataplane_test(context, "instance", "upstream", "station", "duration")
    print("done")
    
