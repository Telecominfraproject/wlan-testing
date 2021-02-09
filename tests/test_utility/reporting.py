import os
from datetime import date, datetime
from shutil import copyfile
import json


class Reporting:

    def __init__(self, reports_root="../reports/"):

        self.reports_root = reports_root
        self.report_id = self.create_report_id()
        self.report_path = self.reports_root + self.report_id
        self.templates_root = os.path.abspath(self.reports_root + "../templates")
        try:
            os.mkdir(self.report_path)
            print("Successfully created the directory %s " % self.report_path)
        except OSError:
            print("Creation of the directory %s failed" % self.report_path)

        try:
            copyfile(self.templates_root + "/report_template.php", self.report_path + '/report.php')
        except:
            print("No report template created. Report data will still be saved. Continuing with tests...")

    def create_report_id(self):
        today = str(date.today())
        now = str(datetime.now()).split(" ")[1].split(".")[0].replace(":", "-")
        id = today + "-" + now
        return id

    def update_json_report(self, report_data):
        try:
            with open(self.report_path + '/report_data.json', 'w') as report_json_file:
                json.dump(report_data, report_json_file)
            report_json_file.close()
        except Exception as e:
            print(e)


def main():
    Reporting()


if __name__ == '__main__':
    main()
