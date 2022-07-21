import importlib

setup_lib = importlib.import_module("SetupLibrary")
SetupLibrary = setup_lib.SetupLibrary


class APLIBS:

    def __init__(self):
        pass

    def run_generic_command(self):
        pass

    def get(self):
        pass


if __name__ == '__main__':
    obj = SetupLibrary(remote_ip="192.168.52.89",
                       remote_ssh_port=22,
                       pwd="")

    obj.setup_serial_environment()
    obj.check_serial_connection(tty="/dev/ttyUSB0")
    obj.kill_all_minicom_process(tty="/dev/ttyUSB0")
