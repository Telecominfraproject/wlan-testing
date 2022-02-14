#!/usr/bin/env python3
'''
NAME: lf_report_test.py

PURPOSE:
Common file for testing lf_report and lf_graph Library generates html and pdf output

SETUP:
/lanforge/html-reports directory needs to be present or output generated in local file

EXAMPLE:
./lf_report_test.py : currently script does not accept input

COPYWRITE
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
'''
import sys
import os
import importlib
import pandas as pd
import random
import argparse


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lf_report = importlib.import_module("py-scripts.lf_report")
lf_report = lf_report.lf_report
lf_graph = importlib.import_module("py-scripts.lf_graph")
lf_bar_graph = lf_graph.lf_bar_graph
lf_scatter_graph = lf_graph.lf_scatter_graph
lf_stacked_graph = lf_graph.lf_stacked_graph
lf_horizontal_stacked_graph = lf_graph.lf_horizontal_stacked_graph

# Unit Test


def main():
    # Testing: generate data frame
    parser = argparse.ArgumentParser(
        prog="lf_report_test.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description='''\
-----------------
NAME: lf_report_test.py

PURPOSE:
Common file for testing lf_report and lf_graph Library generates html and pdf output

SETUP:
/lanforge/html-reports directory needs to be present or output generated in local file

EXAMPLE:
./lf_report_test.py : currently script does not accept input

COPYWRITE
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
''')

    parser.add_argument(
        '--mgr',
        '--lfmgr',
        dest='lfmgr',
        help='sample argument: where LANforge GUI is running',
        default='localhost')
    # the args parser is not really used , this is so the report is not generated when testing
    # the imports with --help
    args = parser.parse_args()
    print("LANforge manager {lfmgr}".format(lfmgr=args.lfmgr))

    dataframe = pd.DataFrame({
        'product': ['CT521a-264-1ac-1n', 'CT521a-1ac-1ax', 'CT522-264-1ac2-1n', 'CT523c-2ac2-db-10g-cu',
                    'CT523c-3ac2-db-10g-cu', 'CT523c-8ax-ac10g-cu', 'CT523c-192-2ac2-1ac-10g'],
        'radios': [1, 1, 2, 2, 6, 9, 3],
        'MIMO': ['N', 'N', 'N', 'Y', 'Y', 'Y', 'Y'],
        'stations': [200, 64, 200, 128, 384, 72, 192],
        '1 mbps': [300, 300, 300, 10000, 10000, 10000, 10000]
    })

    print(dataframe)

    # Testing: generate data frame
    dataframe2 = pd.DataFrame({
        'station': [1, 2, 3, 4, 5, 6, 7],
        'time_seconds': [23, 78, 22, 19, 45, 22, 25]
    })

    # report = lf_report(_dataframe=dataframe)
    report = lf_report()

    report_path = report.get_path()
    report_path_date_time = report.get_path_date_time()

    print("path: {}".format(report_path))
    print("path_date_time: {}".format(report_path_date_time))

    report.set_title("Banner Title One")
    report.build_banner()

    # report.set_title("Banner Title Two")
    # report.build_banner()

    report.set_table_title("Title One")
    report.build_table_title()

    report.set_table_dataframe(dataframe)
    report.build_table()

    report.set_table_title("Title Two")
    report.build_table_title()

    report.set_table_dataframe(dataframe2)
    report.build_table()
    set_xaxis = []
    y_set1 = []
    y_set2 = []
    y_set3 = []
    for i in range(0, 30):
        set_xaxis.append(i)
        y_set1.append(random.randint(1, 50))
        y_set2.append(random.randint(1, 50))
        y_set3.append(random.randint(1, 50))

    # test lf_graph in report
    dataset = [y_set1, y_set2, y_set3]
    x_axis_values = set_xaxis

    report.set_graph_title("Graph Title")
    report.build_graph_title()

    graph = lf_bar_graph(_data_set=dataset,
                         _xaxis_name="stations",
                         _yaxis_name="Throughput 2 (Mbps)",
                         _xaxis_categories=x_axis_values,
                         _graph_image_name="Bi-single_radio_2.4GHz",
                         _label=["bi-downlink", "bi-uplink", 'uplink'],
                         _color=['darkorange', 'forestgreen', 'blueviolet'],
                         _color_edge='red',
                         _grp_title="Throughput for each clients",
                         _xaxis_step=5,
                         _show_bar_value=True,
                         _text_font=7,
                         _text_rotation=45,
                         _xticks_font=7,
                         _legend_loc="best",
                         _legend_box=(1, 1),
                         _legend_ncol=1,
                         _legend_fontsize=None,
                         _enable_csv=True)

    graph_png = graph.build_bar_graph()

    print("graph name {}".format(graph_png))

    report.set_graph_image(graph_png)
    # need to move the graph image to the results
    report.move_graph_image()
    if graph.enable_csv:
        report.set_csv_filename(graph_png)
        report.move_csv_file()
    report.build_graph()
    set1 = [1, 2, 3, 4]
    set2 = [[45, 67, 45, 34], [34, 56, 45, 34], [45, 78, 23, 45]]
    graph2 = lf_scatter_graph(_x_data_set=set1, _y_data_set=set2, _xaxis_name="x-axis", _values=None,
                              _yaxis_name="y-axis",
                              _graph_image_name="image_name1",
                              _color=None,
                              _label=["s1", "s2", "s3"],
                              _enable_csv=False)
    graph_png = graph2.build_scatter_graph()

    print("graph name {}".format(graph_png))

    report.set_graph_image(graph_png)
    report.move_graph_image()

    report.build_graph()
    # this will generate graph which is independent,we can customize the value
    # with different colors
    graph2 = lf_scatter_graph(_x_data_set=set1, _y_data_set=[45, 67, 45, 34], _values=[0, 0, 0, 1],
                              _xaxis_name="x-axis",
                              _yaxis_name="y-axis",
                              _graph_image_name="image_name_map",
                              _color=None,
                              _label=["s1", "s2"],
                              _enable_csv=False)
    graph_png = graph2.build_scatter_graph()

    print("graph name {}".format(graph_png))

    report.set_graph_image(graph_png)
    report.move_graph_image()

    report.build_graph()
    dataset = [["1", "2", "3", "4"], [12, 45, 67, 34],
               [23, 67, 23, 12], [25, 45, 34, 23]]
    graph = lf_stacked_graph(_data_set=dataset,
                             _xaxis_name="Stations",
                             _yaxis_name="Login PASS/FAIL",
                             _label=['Success', 'Fail', 'both'],
                             _graph_image_name="login_pass_fail1",
                             _color=None,
                             _enable_csv=False)

    graph_png = graph.build_stacked_graph()

    print("graph name {}".format(graph_png))

    report.set_graph_image(graph_png)
    report.move_graph_image()
    report.build_graph()

    graph = lf_horizontal_stacked_graph(_seg=2,
                                        _yaxis_set=('A', 'B'),
                                        _xaxis_set1=[12, 65],
                                        _xaxis_set2=[23, 34],
                                        _unit="",
                                        _xaxis_name="Stations",
                                        _label=['Success', 'Fail'],
                                        _graph_image_name="image_name_pass_fail",
                                        _color=["r", "g"],
                                        _figsize=(9, 4),
                                        _enable_csv=False)

    graph_png = graph.build_horizontal_stacked_graph()

    print("graph name {}".format(graph_png))

    report.set_graph_image(graph_png)
    report.move_graph_image()
    report.build_graph()
    # report.build_all()

    html_file = report.write_html()
    print("returned file {}".format(html_file))
    print(html_file)

    # try other pdf formats
    # report.write_pdf()
    # report.write_pdf(_page_size = 'A3', _orientation='Landscape')
    # report.write_pdf(_page_size = 'A4', _orientation='Landscape')
    report.write_pdf(_page_size='Legal', _orientation='Landscape')
    # report.write_pdf(_page_size = 'Legal', _orientation='Portrait')

    # report.generate_report()
if __name__ == "__main__":
    main()
