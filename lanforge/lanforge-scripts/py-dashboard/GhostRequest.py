#!/usr/bin/env python3
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Class holds default settings for json requests to Ghost     -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys
import os
import importlib
import requests
import jwt
from datetime import datetime
import json
import subprocess
from scp import SCPClient
import paramiko
import time
from collections import Counter
import shutil
import itertools

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

GrafanaRequest = importlib.import_module("py-dashboard.GrafanaRequest")
InfluxRequest = importlib.import_module("py-dashboard.InfluxRequest")
RecordInflux = InfluxRequest.RecordInflux


class CSVReader:
    @staticmethod
    def read_csv(file,
                 sep='\t'):
        df = open(file).read().split('\n')
        rows = list()
        for x in df:
            if len(x) > 0:
                rows.append(x.split(sep))
        return rows

    @staticmethod
    def get_column(df,
                   value):
        index = df[0].index(value)
        values = []
        for row in df[1:]:
            values.append(row[index])
        return values

    @staticmethod
    def get_columns(df, targets):
        target_index = []
        for item in targets:
            target_index.append(df[0].index(item))
        results = []
        for row in df:
            row_data = []
            for x in target_index:
                row_data.append(row[x])
            results.append(row_data)
        return results

    @staticmethod
    def to_html(df):
        html = ''
        html = html + ('<table style="border:1px solid #ddd">'
                       '<colgroup>'
                       '<col style="width:25%">'
                       '<col style="width:25%">'
                       '<col style="width:50%">'
                       '</colgroup>'
                       '<tbody>'
                       '<tr>')
        for row in df:
            for item in row:
                html = html + ('<td style="border:1px solid #ddd">%s</td>' % item)
            html = html + '</tr>\n<tr>'
        html = html + ('</tbody>'
                       '</table>')
        return html

    @staticmethod
    def filter_df(df, column, expression, target):
        target_index = df[0].index(column)
        counter = 0
        targets = [0]
        for row in df[1:]:
            try:
                if expression == 'less than':
                    if float(row[target_index]) < target:
                        targets.append(counter)
                if expression == 'greater than':
                    if float(row[target_index]) > target:
                        targets.append(counter)
                if expression == 'greater than or equal to':
                    if float(row[target_index]) >= target:
                        targets.append(counter)
            finally:
                pass
            counter += 1
        return list(map(df.__getitem__, targets))

    @staticmethod
    def concat(dfs):
        return list(itertools.chain.from_iterable(dfs))


class GhostRequest:
    def __init__(self,
                 _ghost_json_host,
                 _ghost_json_port,
                 _api_token=None,
                 _overwrite='false',
                 debug_=False,
                 die_on_error_=False,
                 influx_host=None,
                 influx_port=8086,
                 influx_org=None,
                 influx_token=None,
                 influx_bucket=None):
        self.debug = debug_
        self.die_on_error = die_on_error_
        self.ghost_json_host = _ghost_json_host
        self.ghost_json_port = _ghost_json_port
        self.ghost_json_url = "http://%s:%s/ghost/api/v3" % (_ghost_json_host, _ghost_json_port)
        self.data = dict()
        self.data['overwrite'] = _overwrite
        self.ghost_json_login = self.ghost_json_url + '/admin/session/'
        self.api_token = _api_token
        self.images = list()
        self.webpages = list()
        self.pdfs = list()
        self.influx_host = influx_host
        self.influx_port = influx_port
        self.influx_org = influx_org
        self.influx_token = influx_token
        self.influx_bucket = influx_bucket

    def encode_token(self):

        # Split the key into ID and SECRET
        key_id, secret = self.api_token.split(':')

        # Prepare header and payload
        iat = int(datetime.now().timestamp())

        header = {'alg': 'HS256', 'typ': 'JWT', 'kid': key_id}
        payload = {
            'iat': iat,
            'exp': iat + 5 * 60,
            'aud': '/v3/admin/'
        }
        token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)
        return token

    def create_post(self,
                    title=None,
                    text=None,
                    status="published"):
        ghost_json_url = self.ghost_json_url + '/admin/posts/?source=html'
        post = dict()
        posts = list()
        datastore = dict()
        datastore['html'] = text
        datastore['title'] = title
        datastore['status'] = status
        posts.append(datastore)
        post['posts'] = posts

        headers = dict()

        token = self.encode_token()
        headers['Authorization'] = 'Ghost {}'.format(token)
        response = requests.post(ghost_json_url, json=post, headers=headers)
        if self.debug:
            print(datastore)
            print(ghost_json_url)
            print('\n')
            print(post)
            print('\n')
            print(headers)
            print(response.headers)

    def upload_image(self,
                     image):
        if self.debug:
            print(image)
        ghost_json_url = self.ghost_json_url + '/admin/images/upload/'

        token = self.encode_token()
        bash_command = "curl -X POST -F 'file=@%s' -H \"Authorization: Ghost %s\" %s" % (image, token, ghost_json_url)

        proc = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.read().decode('utf-8')
        if self.debug:
            print(output)
        self.images.append(json.loads(output)['images'][0]['url'])

    def upload_images(self,
                      folder):
        for image in os.listdir(folder):
            if 'kpi' in image:
                if 'png' in image:
                    self.upload_image(folder + '/' + image)
        if self.debug:
            print('images %s' % self.images)

    def custom_post(self,
                    folder,
                    title='custom'):
        self.upload_images(folder)
        head = '''This is a custom post created via a script'''
        for picture in self.images:
            head = head + '<img src="%s"></img>' % picture
        head = head + '''This is the end of the example'''
        self.create_post(title=title,
                         text=head)

    def kpi_to_ghost(self,
                     folders,
                     parent_folder=None,
                     title=None,
                     ghost_host=None,
                     port=22,
                     user_push=None,
                     password_push=None,
                     customer=None,
                     testbed=None,
                     test_run=None,
                     target_folders=None,
                     grafana_token=None,
                     grafana_host=None,
                     grafana_port=3000,
                     grafana_datasource='InfluxDB',
                     grafana_bucket=None):

        now = datetime.now()

        text = ''
        csvreader = CSVReader()
        if self.debug:
            print('Folders: %s' % folders)

        ssh_push = paramiko.SSHClient()
        ssh_push.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
        ssh_push.connect(ghost_host,
                         port,
                         username=user_push,
                         password=password_push,
                         allow_agent=False,
                         look_for_keys=False)
        scp_push = SCPClient(ssh_push.get_transport())

        if parent_folder is not None:
            files = os.listdir(parent_folder)
            if self.debug:
                print("parent_folder %s" % parent_folder)
                print(files)
            for file in files:
                if os.path.isdir(parent_folder + '/' + file) is True:
                    if os.path.exists(file):
                        shutil.rmtree(file)
                    shutil.copytree(parent_folder + '/' + file, file)
                    target_folders.append(file)
            if self.debug:
                print('Target folders: %s' % target_folders)
        else:
            for folder in folders:
                if self.debug:
                    print(folder)
                target_folders.append(folder)

        testbeds = list()
        web_pages_and_pdfs = list()
        high_priority_list = list()
        low_priority_list = list()
        images = list()
        times = list()
        test_pass_fail = list()
        subtest_pass_fail = list()
        subtest_pass_total = 0
        subtest_fail_total = 0
        test_tag_1 = list()
        columns = ['test-rig', 'dut-hw-version', 'dut-sw-version',
                   'dut-model-num', 'dut-serial-num']
        duts = dict()

        for target_folder in target_folders:
            try:
                target_file = '%s/kpi.csv' % target_folder
                df = csvreader.read_csv(file=target_file, sep='\t')
                test_id = csvreader.get_column(df, 'test-id')[0]
                for column in columns:
                    try:
                        column_data = csvreader.get_column(df, column)[0]
                        duts[column] = column_data
                    except:
                        print('no column named %s' % column)
                    test_tag_1.append([test_id, list(set(csvreader.get_column(df, 'test-tag')))])
                pass_fail = Counter(csvreader.get_column(df, 'pass/fail'))
                test_pass_fail.append(pass_fail)
                subtest_pass = csvreader.get_column(df, 'Subtest-Pass')
                subtest_fail = csvreader.get_column(df, 'Subtest-Fail')
                for result in subtest_pass:
                    subtest_pass_total += int(result)
                for result in subtest_fail:
                    subtest_fail_total += int(result)
                subtest_pass_fail_list = dict()
                subtest_pass_fail_list['PASS'] = subtest_pass_total
                subtest_pass_fail_list['FAIL'] = subtest_fail_total
                subtest_pass_fail.append(subtest_pass_fail_list)
                times_append = csvreader.get_column(df, 'Date')
                if len(times_append) == 0:
                    print(LookupError("%s/kpi.csv has no time points" % target_folder))
                    break
                for target_time in times_append:
                    times.append(float(target_time) / 1000)
                if pass_fail['PASS'] + pass_fail['FAIL'] > 0:
                    text = text + 'Tests passed: %s<br />' % pass_fail['PASS']
                    text = text + 'Tests failed: %s<br />' % pass_fail['FAIL']
                    text = text + 'Percentage of tests passed: %s<br />' % (
                            pass_fail['PASS'] / (pass_fail['PASS'] + pass_fail['FAIL']))
                else:
                    text = text + 'Tests passed: 0<br />' \
                                  'Tests failed : 0<br />' \
                                  'Percentage of tests passed: Not Applicable<br />'
                testbeds.append(duts['test-rig'])
                if testbed is None:
                    testbed = duts['test-rig']

                if test_run is None:
                    test_run = now.strftime('%B-%d-%Y-%I-%M-%p-report')
                local_path = '/home/%s/%s/%s/%s' % (user_push, customer, testbed, test_run)

                transport = paramiko.Transport(ghost_host, port)
                transport.connect(None, user_push, password_push)
                sftp = paramiko.sftp_client.SFTPClient.from_transport(transport)

                if self.debug:
                    print(local_path)
                    print(target_folder)

                try:
                    sftp.mkdir('/home/%s/%s/%s' % (user_push, customer, testbed))
                except:
                    pass

                try:
                    sftp.mkdir(local_path)
                except:
                    pass
                scp_push.put(target_folder, local_path, recursive=True)
                files = sftp.listdir(local_path + '/' + target_folder)
                pdfs = list()
                webpages = list()
                for file in files:
                    if 'pdf' in file:
                        url = 'http://%s/%s/%s/%s/%s/%s' % (
                            ghost_host, customer.strip('/'), testbed, test_run, target_folder, file)
                        pdfs.append('<a href="%s">PDF</a>' % url)
                if 'index.html' in files:
                    url = 'http://%s/%s/%s/%s/%s/%s' % (
                        ghost_host, customer.strip('/'), testbed, test_run, target_folder, 'index.html')
                    webpages.append('<a href="%s">HTML</a>' % url)
                web_pages_and_pdfs_append = dict()
                web_pages_and_pdfs_append[test_id] = pdfs + webpages
                web_pages_and_pdfs.append(web_pages_and_pdfs_append)
                scp_push.close()
                self.upload_images(target_folder)
                for image in self.images:
                    if 'kpi-' in image:
                        if '-print' not in image:
                            images.append('<img src="%s"></img>' % image)
                self.images = []

                results = csvreader.get_columns(df, ['short-description', 'numeric-score', 'test details', 'pass/fail',
                                                     'test-priority'])

                results[0] = ['Short Description', 'Score', 'Test Details', 'Pass or Fail', 'test-priority']
                for row in results:
                    try:
                        row[1] = round(float(row[1]), 2)
                    except:
                        pass

                low_priority = csvreader.filter_df(results, 'test-priority', 'less than', 94)
                if self.debug:
                    print('Low Priority results %s' % len(low_priority))
                high_priority = csvreader.filter_df(results, 'test-priority', 'greater than or equal to', 95)
                high_priority_list.append(high_priority)
                low_priority_list.append(low_priority)

            except:
                print("Failed to process %s" % target_folder)
                target_folders.remove(target_folder)
                failuredict = dict()
                failuredict[target_folder] = ['Failure']
                web_pages_and_pdfs.append(failuredict)
        test_tag = dict()
        for x in list(set([x[0] for x in test_tag_1])):
            l3 = list()
            for sublist in test_tag_1:
                if sublist[0] == x:
                    l3 += sublist[1]
            test_tag[x] = l3
        if len(times) == 0:
            return ArithmeticError("There are no datapoints in any folders passed into Ghost")

        test_pass_fail_results = sum((Counter(test) for test in test_pass_fail), Counter())
        subtest_pass_fail_results = sum((Counter(test) for test in subtest_pass_fail), Counter())

        if self.debug:
            print(times)
        end_time = max(times)
        start_time = '2021-07-01'
        end_time = datetime.utcfromtimestamp(end_time)
        now = time.time()
        offset = datetime.fromtimestamp(now) - datetime.utcfromtimestamp(now)
        end_time = end_time + offset

        high_priority = csvreader.concat(high_priority_list)
        low_priority = csvreader.concat(low_priority_list)

        if len(high_priority) > 0:
            high_priority = csvreader.get_columns(high_priority,
                                                  ['Short Description', 'Score', 'Test Details'])
        low_priority = csvreader.get_columns(low_priority,
                                             ['Short Description', 'Score', 'Test Details'])
        high_priority.append(['Total Passed', test_pass_fail_results['PASS'], 'Total subtests passed during this run'])
        high_priority.append(['Total Failed', test_pass_fail_results['FAIL'], 'Total subtests failed during this run'])
        high_priority.append(
            ['Subtests Passed', subtest_pass_fail_results['PASS'], 'Total subtests passed during this run'])
        high_priority.append(
            ['Subtests Failed', subtest_pass_fail_results['FAIL'], 'Total subtests failed during this run'])

        if title is None:
            title = end_time.strftime('%B %d, %Y %I:%M %p report')

        # create Grafana Dashboard
        target_files = []
        for folder in target_folders:
            target_file = folder.split('/')[-1] + '/kpi.csv'
            try:
                open(target_file)
                target_files.append(target_file)
            except:
                pass
        if self.debug:
            print('Target files: %s' % target_files)

        text = 'Testbed: %s<br />' % testbeds[0]
        if self.influx_token is not None:
            influxdb = RecordInflux(_influx_host=self.influx_host,
                                    _influx_port=self.influx_port,
                                    _influx_org=self.influx_org,
                                    _influx_token=self.influx_token,
                                    _influx_bucket=self.influx_bucket)
            try:
                short_description = 'Tests passed'  # variable name
                numeric_score = test_pass_fail_results['PASS']  # value
                tags = dict()
                if self.debug:
                    print(datetime.utcfromtimestamp(max(times)))
                tags['testbed'] = testbeds[0]
                tags['script'] = 'GhostRequest'
                tags['Graph-Group'] = 'PASS'
                date = datetime.utcfromtimestamp(max(times)).isoformat()
                influxdb.post_to_influx(short_description, numeric_score, tags, date)

                short_description = 'Tests failed'  # variable name
                numeric_score = test_pass_fail_results['FAIL']  # value
                tags = dict()
                tags['testbed'] = testbeds[0]
                tags['script'] = 'GhostRequest'
                tags['Graph-Group'] = 'FAIL'
                date = datetime.utcfromtimestamp(max(times)).isoformat()
                influxdb.post_to_influx(short_description, numeric_score, tags, date)

                short_description = 'Subtests passed'  # variable name
                numeric_score = subtest_pass_fail_results['PASS']  # value
                tags = dict()
                if self.debug:
                    print(datetime.utcfromtimestamp(max(times)))
                tags['testbed'] = testbeds[0]
                tags['script'] = 'GhostRequest'
                tags['Graph-Group'] = 'Subtest PASS'
                date = datetime.utcfromtimestamp(max(times)).isoformat()
                influxdb.post_to_influx(short_description, numeric_score, tags, date)

                short_description = 'Subtests failed'  # variable name
                numeric_score = subtest_pass_fail_results['FAIL']  # value
                tags = dict()
                tags['testbed'] = testbeds[0]
                tags['script'] = 'GhostRequest'
                tags['Graph-Group'] = 'Subtest FAIL'
                date = datetime.utcfromtimestamp(max(times)).isoformat()
                influxdb.post_to_influx(short_description, numeric_score, tags, date)
            except Exception as err:
                influx_error = err
                text += '''InfluxDB Error: %s<br />
                Influx Host: %s<br />
                Influx Port: %s<br />
                Influx Organization: %s<br />
                Influx Bucket: %s<br />''' % (
                    influx_error, self.influx_host, self.influx_port, self.influx_org, self.influx_bucket)

        raw_test_tags = list()
        test_tag_table = ''
        for tag in test_tag.values():
            for value in tag:
                raw_test_tags.append(value)
        for value in list(set(raw_test_tags)):
            test_tag_table += (
                    '<tr><td style="border-color: gray; border-style: solid; border-width: 1px; ">Test Tag</td><td colspan="3" style="border-color: gray; border-style: solid; border-width: 1px; ">%s</td></tr>' % value)
        dut_table_column_names = {'test-rig': 'Testbed',
                                  'dut-hw-version': 'DUT HW',
                                  'dut-sw-version': 'DUT SW',
                                  'dut-model-num': 'DUT Model',
                                  'dut-serial-num': 'DUT Serial'}
        dut_table_columns = ''
        for column in columns:
            if column in dut_table_column_names.keys():
                column_name = dut_table_column_names[column]
            else:
                column_name = column
            dut_table_columns += (
                    '<tr><td style="border-color: gray; border-style: solid; border-width: 1px; ">%s</td><td colspan="3" style="border-color: gray; border-style: solid; border-width: 1px; ">%s</td></tr>' %
                    (column_name, duts[column])
            )

        dut_table = '<table width="700px" border="1" cellpadding="2" cellspacing="0" ' \
                    'style="border-color: gray; border-style: solid; border-width: 1px; "><tbody>' \
                    '<tr><th colspan="2">Test Information</th></tr>' \
                    '%s' \
                    '%s' \
                    '<tr><td style="border-color: gray; border-style: solid; border-width: 1px; ">Tests passed</td>' \
                    '<td colspan="3" style="border-color: gray; border-style: solid; border-width: 1px; ">%s</td></tr>' \
                    '<tr><td style="border-color: gray; border-style: solid; border-width: 1px; ">Tests failed</td>' \
                    '<td colspan="3" style="border-color: gray; border-style: solid; border-width: 1px; ">%s</td></tr>' \
                    '<tr><td style="border-color: gray; border-style: solid; border-width: 1px; ">Subtests passed</td>' \
                    '<td colspan="3" style="border-color: gray; border-style: solid; border-width: 1px; ">%s</td></tr>' \
                    '<tr><td style="border-color: gray; border-style: solid; border-width: 1px; ">Subtests failed</td>' \
                    '<td colspan="3" style="border-color: gray; border-style: solid; border-width: 1px; ">%s</td></tr>' \
                    '</tbody></table>' % (
                        dut_table_columns, test_tag_table, test_pass_fail_results['PASS'],
                        test_pass_fail_results['FAIL'], subtest_pass_total, subtest_fail_total)
        text = text + dut_table

        for dictionary in web_pages_and_pdfs:
            text += list(dictionary.keys())[0] + ' report: '
            for value in dictionary.values():
                for webpage in value:
                    text += webpage
                    if value.index(webpage) + 1 != len(value):
                        text += ' | '
            text += '<br />'

        for image in images:
            text = text + image

        text = text + 'High priority results: %s' % csvreader.to_html(high_priority)

        if grafana_token is not None:
            grafana = GrafanaRequest(grafana_token,
                                     grafana_host,
                                     grafanajson_port=grafana_port,
                                     debug_=self.debug
                                     )
            if self.debug:
                print('Test Tag: %s' % test_tag)
            try:
                grafana.create_custom_dashboard(target_csvs=target_files,
                                                title=title,
                                                datasource=grafana_datasource,
                                                bucket=grafana_bucket,
                                                from_date=start_time,
                                                to_date=end_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                pass_fail='GhostRequest',
                                                testbed=testbeds[0],
                                                test_tag=test_tag)
                # get the details of the dashboard through the API, and set the end date to the youngest KPI
                grafana.list_dashboards()

                grafana.create_snapshot(title='Testbed: ' + title)
                time.sleep(3)
                snapshot = grafana.list_snapshots()[-1]
                text = text + '<iframe src="http://%s:3000/dashboard/snapshot/%s" width="100%s" height=1500></iframe><br />' % (
                    grafana_host, snapshot['key'], '%')
            except Exception as err:
                grafana_error = err
                text = text + '''Grafana Error: %s<br />
                Grafana credentials:<br />
                Grafana Host: %s<br />
                Grafana Bucket: %s<br />
                Grafana Database: %s<br />''' % (grafana_error, grafana_host, grafana_bucket, grafana_datasource)

        text = text + 'Low priority results: %s' % csvreader.to_html(low_priority)

        self.create_post(title=title,
                         text=text)
