#!/usr/bin/env python3

"""TestRail API binding for Python 3.x.

"""

import base64
import json

import requests
from pprint import pprint
import os
tr_user = os.getenv('TR_USER')
tr_pw=os.getenv('TR_PW')



class APIClient:
    def __init__(self, base_url):
        self.user = tr_user
        self.password = tr_pw
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/api/v2/'


    def send_get(self, uri, filepath=None):
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for 'get_attachment/:attachment_id'.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request('GET', uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri

        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {'Authorization': 'Basic ' + auth}
        print("Method =" , method)

        if method == 'POST':
            if uri[:14] == 'add_attachment':    # add_attachment API method
                files = {'attachment': (open(data, 'rb'))}
                response = requests.post(url, headers=headers, files=files)
                files['attachment'].close()
            else:
                headers['Content-Type'] = 'application/json'
                payload = bytes(json.dumps(data), 'utf-8')
                response = requests.post(url, headers=headers, data=payload)
        else:
            headers['Content-Type'] = 'application/json'
            response = requests.get(url, headers=headers)
            print("headers = ", headers)
            print("resonse=", response)
            print("response code =", response.status_code)

        if response.status_code > 201:

            try:
                error = response.json()
            except:     # response.content not formatted as JSON
                error = str(response.content)
            #raise APIError('TestRail API returned HTTP %s (%s)' % (response.status_code, error))
            print('TestRail API returned HTTP %s (%s)' % (response.status_code, error))
            return
        else:
            print(uri[:15])
            if uri[:15] == 'get_attachments':   # Expecting file, not JSON
                try:
                    print('opening file')
                    print (str(response.content))
                    open(data, 'wb').write(response.content)
                    print('opened file')
                    return (data)
                except:
                    return ("Error saving attachment.")
            else:

                try:
                    return response.json()
                except: # Nothing to return
                    return {}
    def get_project_id(self, project_name):
        "Get the project ID using project name"
        project_id = None
        projects = client.send_get('get_projects')
        pprint(projects)
        for project in projects:
            if project['name']== project_name:
                project_id = project['id']
                # project_found_flag=True
                break
                print("project Id =",project_id)
        return project_id

    def get_run_id(self, test_run_name):
        "Get the run ID using test name and project name"
        run_id = None
        project_id = client.get_project_id(project_name='WLAN')

        try:
            test_runs = client.send_get('get_runs/%s' % (project_id))
            print("------------TEST RUNS----------")
            pprint(test_runs)

        except Exception:
            print
            'Exception in update_testrail() updating TestRail.'
            return None
        else:
            for test_run in test_runs:
                if test_run['name'] == test_run_name:
                    run_id = test_run['id']
                    print("run Id in Test Runs=",run_id)
                    break
            return run_id

    def update_testrail(self, case_id, run_id, status_id, msg):
        "Update TestRail for a given run_id and case_id"
        update_flag = False
        # Get the TestRail client account details
        # Update the result in TestRail using send_post function.
        # Parameters for add_result_for_case is the combination of runid and case id.
        # status_id is 1 for Passed, 2 For Blocked, 4 for Retest and 5 for Failed
        #status_id = 1 if result_flag else 5

        print("result status is = ", status_id)
        print("case id=", case_id)
        print("run id passed to update is ", run_id, case_id)
        if run_id is not None:
            try:
                result = client.send_post(
                    'add_result_for_case/%s/%s' % (run_id, case_id),
                    {'status_id': status_id, 'comment': msg})
                print("result in post",result)
            except Exception:
                print
                'Exception in update_testrail() updating TestRail.'

            else:
                print
                'Updated test result for case: %s in test run: %s with msg:%s' % (case_id, run_id, msg)

        return update_flag



client: APIClient = APIClient('https://telecominfraproject.testrail.com')

'''
case = client.send_get('get_case/1')
print("---------TEST CASE 1---------")
pprint(case)
case = client.send_get('get_case/2')
print("---------TEST CASE 2---------")
pprint(case)
print ("----------TEST Project ID----------")
proj_id = client.get_project_id(project_name= "WLAN")
pprint(proj_id)

#REST API POSTMAN PROJECT
projId = client.get_project_id(project_name= "REST-API-POSTMAN")
pprint("REST API POSTMAN PROJECT ID IS :", projId)

#print("---------TEST RUN ID-----------")
#rid = client.get_run_id(test_run_name='Master',project_name='WLAN')
rid=client.get_run_id(test_run_name= 'Master-Run3')
pprint(rid)

result: bool= client.update_testrail(case_id = 1, run_id=rid, status_id = 5, msg ='Test Failed')

#result = client.send_get('get_attachment/:1', '/Users/syamadevi/Desktop/syama/python-test/TestRail/testreport.pdf')
#print(result)
#project_report= client.send_get("get_reports/:%s" %proj_id)
#print(project_report)
'''
class APIError(Exception):
    pass
