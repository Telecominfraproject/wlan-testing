from controller.controller_3x.controller import CController
import allure
import pytest

class Fixtures_3x:

    def __init__(self, configuration={}, run_lf=False):
        self.lab_info = configuration
        # print(self.lab_info)
        print("cc.1")
        self.controller_obj = ""
        if not run_lf:
            try:
                self.controller_obj = CController(controller_data=self.lab_info["controller"], timeout="10")
            except Exception as e:
                print(e)
                allure.attach(body=str(e), name="Controller Instantiation Failed: ")
                sdk_client = False
                pytest.exit("unable to communicate to Controller" + str(e))


    def get_sdk_version(self):
        version = self.controller_obj.get_sdk_version()
        return version

    def setup_profiles(self):
        pass