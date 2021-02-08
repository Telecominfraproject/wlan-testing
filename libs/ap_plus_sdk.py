

from lab_ap_info import *
from JfrogHelper import GetBuild
from ap_ssh import ssh_cli_active_fw

def check_latest_fw(jfrog=None,
                    ap_latest_dict=None,
                    buildid=None):

        ############################################################################
        #################### Jfrog Firmware Check ##################################
        ############################################################################
        for model in ap_models:
            # cloudModel = cloud_sdk_models[model]
            ###Check Latest FW on jFrog
            jfrog_url = 'https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/'
            url = jfrog_url + model + "/dev/"
            Build: GetBuild = GetBuild(jfrog["user"], jfrog["pass"])
            latest_image = Build.get_latest_image(url, buildid)
            print(model, "Latest FW on jFrog:", latest_image)
            ap_latest_dict[model] = latest_image
        return ap_latest_dict


def get_ap_info(args):
    return ssh_cli_active_fw(args)
    pass


