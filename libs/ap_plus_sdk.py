from lab_ap_info import *
from JfrogHelper import GetBuild
from ap_ssh import ssh_cli_active_fw


def get_ap_info(args):
    return ssh_cli_active_fw(args)
    pass
