import allure


class Reporting:

    def __init__(self):
        self.rid = None
        pass

    def update_testrail(self, case_id=None, run_id=None, status_id=1, msg=None):
        allure.attach(name=str(msg), body="")
        pass
