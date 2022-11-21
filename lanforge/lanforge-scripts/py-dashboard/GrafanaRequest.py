#!/usr/bin/env python3

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Class holds default settings for json requests to Grafana     -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import requests

import json
import string
import random


class CSVReader:
    def __init__(self):
        self.shape = None

    def read_csv(self,
                 file,
                 sep='\t'):
        df = open(file).read().split('\n')
        rows = list()
        for x in df:
            if len(x) > 0:
                rows.append(x.split(sep))
        length = list(range(0, len(df[0])))
        columns = dict(zip(df[0], length))
        self.shape = (length, columns)
        return rows

    def get_column(self,
                   df,
                   value):
        index = df[0].index(value)
        values = []
        for row in df[1:]:
            values.append(row[index])
        return values


class GrafanaRequest:
    def __init__(self,
                 _grafana_token,
                 _grafanajson_host,
                 grafanajson_port=3000,
                 _folderID=0,
                 _headers=dict(),
                 _overwrite='false',
                 debug_=False,
                 die_on_error_=False):
        self.debug = debug_
        self.die_on_error = die_on_error_
        self.headers = _headers
        self.headers['Authorization'] = 'Bearer ' + _grafana_token
        self.headers['Content-Type'] = 'application/json'
        self.grafanajson_host = _grafanajson_host
        self.grafanajson_port = grafanajson_port
        self.grafanajson_token = _grafana_token
        self.grafanajson_url = "http://%s:%s" % (_grafanajson_host, grafanajson_port)
        self.data = dict()
        self.data['overwrite'] = _overwrite
        self.csvreader = CSVReader()
        self.units = dict()

    def create_bucket(self,
                      bucket_name=None):
        # Create a bucket in Grafana
        if bucket_name is not None:
            pass

    def list_dashboards(self):
        url = self.grafanajson_url + '/api/search'
        print(url)
        return json.loads(requests.get(url, headers=self.headers).text)

    def create_dashboard(self,
                         dashboard_name=None,
                         ):
        grafanajson_url = self.grafanajson_url + "/api/dashboards/db"
        datastore = dict()
        dashboard = dict()
        dashboard['id'] = None
        dashboard['title'] = dashboard_name
        dashboard['tags'] = ['templated']
        dashboard['timezone'] = 'browser'
        dashboard['schemaVersion'] = 27
        dashboard['version'] = 4
        datastore['dashboard'] = dashboard
        datastore['overwrite'] = False
        data = json.dumps(datastore, indent=4)
        return requests.post(grafanajson_url, headers=self.headers, data=data, verify=False)

    def delete_dashboard(self,
                         dashboard_uid=None):
        grafanajson_url = self.grafanajson_url + "/api/dashboards/uid/" + dashboard_uid
        return requests.post(grafanajson_url, headers=self.headers, verify=False)

    def create_dashboard_from_data(self,
                                   json_file=None):
        grafanajson_url = self.grafanajson_url + '/api/dashboards/db'
        datastore = dict()
        dashboard = dict(json.loads(open(json_file).read()))
        datastore['dashboard'] = dashboard
        datastore['overwrite'] = False
        data = json.dumps(datastore, indent=4)
        return requests.post(grafanajson_url, headers=self.headers, data=data, verify=False)

    def create_dashboard_from_dict(self,
                                   dictionary=None,
                                   overwrite=False):
        grafanajson_url = self.grafanajson_url + '/api/dashboards/db'
        datastore = dict()
        dashboard = dict(json.loads(dictionary))
        datastore['dashboard'] = dashboard
        datastore['overwrite'] = overwrite
        data = json.dumps(datastore, indent=4)
        return requests.post(grafanajson_url, headers=self.headers, data=data, verify=False)

    def get_graph_groups(self, target_csvs):  # Get the unique values in the Graph-Group column
        dictionary = dict()
        for target_csv in target_csvs:
            if len(target_csv) > 1:
                csv = self.csvreader.read_csv(target_csv)
                # Unique values in the test-id column
                scripts = list(set(self.csvreader.get_column(csv, 'test-id')))
                # we need to make sure we match each Graph Group to the script it occurs in
                for script in scripts:
                    # Unique Graph Groups for each script
                    graph_groups = self.csvreader.get_column(csv, 'Graph-Group')
                    dictionary[script] = list(set(graph_groups))
                    units = self.csvreader.get_column(csv, 'Units')
                    self.units[script] = dict()
                    for index in range(0, len(graph_groups)):
                        self.units[script][graph_groups[index]] = units[index]
                subtests = 0
                for score in list(self.csvreader.get_column(csv, 'Subtest-Pass')):
                    subtests += int(score)
                for score in list(self.csvreader.get_column(csv, 'Subtest-Fail')):
                    subtests += int(score)
                if subtests > 0:
                    dictionary[script].append('Subtests passed')
                    dictionary[script].append('Subtests failed')
                print(subtests)
                for item in dictionary[script]:
                    print('%s, %s' % (item, type(item)))
        print(dictionary)
        return dictionary

    def maketargets(self,
                    bucket,
                    scriptname,
                    groupBy,
                    index,
                    graph_group,
                    testbed,
                    test_tag=None):
        query = (
                'from(bucket: "%s")\n  '
                '|> range(start: v.timeRangeStart, stop: v.timeRangeStop)\n  '
                '|> filter(fn: (r) => r["script"] == "%s")\n   '
                '|> group(columns: ["_measurement"])\n '
                % (bucket, scriptname))
        queryend = ('|> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)\n  '
                    '|> yield(name: "mean")\n  ')
        if graph_group is not None:
            graphgroup = ('|> filter(fn: (r) => r["Graph-Group"] == "%s")\n' % graph_group)
            query += graphgroup
        if test_tag is not None and len(test_tag) > 0:
            graphgroup = ('|> filter(fn: (r) => r["Test Tag"] == "%s")\n' % test_tag)
            query += graphgroup
        if testbed is not None:
            query += ('|> filter(fn: (r) => r["testbed"] == "%s")\n' % testbed)
        targets = dict()
        targets['delimiter'] = ','
        targets['groupBy'] = groupBy
        targets['header'] = True
        targets['ignoreUnknown'] = False
        targets['orderByTime'] = 'ASC'
        targets['policy'] = 'default'
        targets['query'] = query + queryend
        targets['refId'] = dict(enumerate(string.ascii_uppercase, 1))[index + 1]
        targets['resultFormat'] = "time_series"
        targets['schema'] = list()
        targets['skipRows'] = 0
        targets['tags'] = list()
        return targets

    def groupby(self, params, grouptype):
        dic = dict()
        dic['params'] = list()
        dic['params'].append(params)
        dic['type'] = grouptype
        return dic

    def create_custom_dashboard(self,
                                scripts=None,
                                title=None,
                                bucket=None,
                                graph_groups=None,
                                graph_groups_file=None,
                                target_csvs=None,
                                testbed=None,
                                datasource='InfluxDB',
                                from_date='now-1y',
                                to_date='now',
                                graph_height=8,
                                graph_width=12,
                                pass_fail=None,
                                test_tag=None):
        options = string.ascii_lowercase + string.ascii_uppercase + string.digits
        uid = ''.join(random.choice(options) for i in range(9))
        input1 = dict()
        annotations = dict()
        annotations['builtIn'] = 1
        annotations['datasource'] = '-- Grafana --'
        annotations['enable'] = True
        annotations['hide'] = True
        annotations['iconColor'] = 'rgba(0, 211, 255, 1)'
        annotations['name'] = 'Annotations & Alerts'
        annotations['type'] = 'dashboard'
        annot = dict()
        annot['list'] = list()
        annot['list'].append(annotations)

        templating = dict()
        templating['list'] = list()

        timedict = dict()
        timedict['from'] = from_date
        timedict['to'] = to_date

        panels = list()
        index = 1
        if graph_groups_file:
            print("graph_groups_file: %s" % graph_groups_file)
            target_csvs = open(graph_groups_file).read().split('\n')
            graph_groups = self.get_graph_groups(
                target_csvs)  # Get the list of graph groups which are in the tests we ran
        if target_csvs:
            print('Target CSVs: %s' % target_csvs)
            graph_groups = self.get_graph_groups(
                target_csvs)  # Get the list of graph groups which are in the tests we ran
        if pass_fail is not None:
            graph_groups[pass_fail] = ['PASS', 'FAIL']

        print('Test Tag in Grafana: %s' % test_tag)

        for scriptname in graph_groups.keys():
            print(scriptname)
            if scriptname in test_tag.keys():
                for tag in test_tag[scriptname]:
                    print('Script: %s, Tag: %s' % (scriptname, tag))
                    panel = self.create_panel(graph_groups,
                                              graph_height,
                                              graph_width,
                                              scriptname,
                                              bucket,
                                              testbed,
                                              tag,
                                              datasource,
                                              index)
                    panels.append(panel)
                    index = index + 1
            else:
                panel = self.create_panel(graph_groups,
                                          graph_height,
                                          graph_width,
                                          scriptname,
                                          bucket,
                                          testbed,
                                          None,
                                          datasource,
                                          index)
                panels.append(panel)
                index = index + 1

        input1['annotations'] = annot
        input1['editable'] = True
        input1['gnetId'] = None
        input1['graphTooltip'] = 0
        input1['links'] = list()
        input1['panels'] = panels
        input1['refresh'] = False
        input1['schemaVersion'] = 27
        input1['style'] = 'dark'
        input1['tags'] = list()
        input1['templating'] = templating
        input1['time'] = timedict
        input1['timepicker'] = dict()
        input1['timezone'] = ''
        input1['title'] = ("Testbed: %s" % title)
        input1['uid'] = uid
        input1['version'] = 11
        return self.create_dashboard_from_dict(dictionary=json.dumps(input1))

    def create_panel(self,
                     graph_groups,
                     graph_height,
                     graph_width,
                     scriptname,
                     bucket,
                     testbed,
                     test_tag,
                     datasource,
                     index):
        print('Test Tag: %s' % test_tag)
        for graph_group in graph_groups[scriptname]:
            panel = dict()

            gridpos = dict()
            gridpos['h'] = graph_height
            gridpos['w'] = graph_width
            gridpos['x'] = 0
            gridpos['y'] = 0

            legend = dict()
            legend['avg'] = False
            legend['current'] = False
            legend['max'] = False
            legend['min'] = False
            legend['show'] = True
            legend['total'] = False
            legend['values'] = False

            options = dict()
            options['alertThreshold'] = True

            groupBy = list()
            groupBy.append(self.groupby('$__interval', 'time'))
            groupBy.append(self.groupby('null', 'fill'))

            targets = list()
            counter = 0
            try:
                new_target = self.maketargets(bucket,
                                              scriptname,
                                              groupBy,
                                              counter,
                                              graph_group,
                                              testbed,
                                              test_tag=test_tag)
            except:
                new_target = self.maketargets(bucket, scriptname, groupBy, counter, graph_group, testbed)
            targets.append(new_target)

            fieldConfig = dict()
            fieldConfig['defaults'] = dict()
            fieldConfig['overrides'] = list()

            transformation = dict()
            transformation['id'] = "renameByRegex"
            transformation_options = dict()
            transformation_options['regex'] = "(.*) value.*"
            transformation_options['renamePattern'] = "$1"
            transformation['options'] = transformation_options

            xaxis = dict()
            xaxis['buckets'] = None
            xaxis['mode'] = "time"
            xaxis['name'] = None
            xaxis['show'] = True
            xaxis['values'] = list()

            yaxis = dict()
            yaxis['format'] = 'short'
            try:
                yaxis['label'] = self.units[scriptname][graph_group]
            except:
                pass
            yaxis['logBase'] = 1
            yaxis['max'] = None
            yaxis['min'] = None
            yaxis['show'] = True

            yaxis1 = dict()
            yaxis1['align'] = False
            yaxis1['alignLevel'] = None

            panel['aliasColors'] = dict()
            panel['bars'] = False
            panel['dashes'] = False
            panel['dashLength'] = 10
            panel['datasource'] = datasource
            panel['fieldConfig'] = fieldConfig
            panel['fill'] = 0
            panel['fillGradient'] = 0
            panel['gridPos'] = gridpos
            panel['hiddenSeries'] = False
            panel['id'] = index
            panel['legend'] = legend
            panel['lines'] = True
            panel['linewidth'] = 1
            panel['nullPointMode'] = 'null'
            panel['options'] = options
            panel['percentage'] = False
            panel['pluginVersion'] = '7.5.4'
            panel['pointradius'] = 2
            panel['points'] = True
            panel['renderer'] = 'flot'
            panel['seriesOverrides'] = list()
            panel['spaceLength'] = 10
            panel['stack'] = False
            panel['steppedLine'] = False
            panel['targets'] = targets
            panel['thresholds'] = list()
            panel['timeFrom'] = None
            panel['timeRegions'] = list()
            panel['timeShift'] = None

            if graph_group is not None:
                scriptname = '%s: %s' % (scriptname, graph_group)
            if test_tag is not None:
                scriptname = '%s: %s' % (scriptname, test_tag)
            scriptname = '%s: %s' % (scriptname, testbed)
            panel['title'] = scriptname

            if self.debug:
                print(panel['title'])
            panel['transformations'] = list()
            panel['transformations'].append(transformation)
            panel['type'] = "graph"
            panel['xaxis'] = xaxis
            panel['yaxes'] = list()
            panel['yaxes'].append(yaxis)
            panel['yaxes'].append(yaxis)
            panel['yaxis'] = yaxis1
            return panel

    def create_snapshot(self, title):
        print('create snapshot')
        grafanajson_url = self.grafanajson_url + '/api/snapshots'
        data = self.get_dashboard(title)
        data['expires'] = False
        data['external'] = False
        data['timeout'] = 15
        if self.debug:
            print(data)
        return requests.post(grafanajson_url, headers=self.headers, json=data, verify=False).text

    def list_snapshots(self):
        grafanajson_url = self.grafanajson_url + '/api/dashboard/snapshots'
        print(grafanajson_url)
        return json.loads(requests.get(grafanajson_url, headers=self.headers, verify=False).text)

    def get_dashboard(self, target):
        dashboards = self.list_dashboards()
        print(target)
        for dashboard in dashboards:
            if dashboard['title'] == target:
                uid = dashboard['uid']
        grafanajson_url = self.grafanajson_url + '/api/dashboards/uid/' + uid
        print(grafanajson_url)
        return json.loads(requests.get(grafanajson_url, headers=self.headers, verify=False).text)

    def get_units(self, csv):
        df = self.csvreader.read_csv(csv)
        units = self.csvreader.get_column(df, 'Units')
        test_id = self.csvreader.get_column(df, 'test-id')
        maxunit = max(set(units), key=units.count)
        maxtest = max(set(test_id), key=test_id.count)
        d = dict()
        d[maxunit] = maxtest
        print(maxunit, maxtest)
        return d