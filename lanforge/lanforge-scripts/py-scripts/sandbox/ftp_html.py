#!/usr/bin/env python3

from matplotlib import pyplot as plt
import numpy as np
import os.path
from os import path
import sys
import pdfkit
sys.path.append('/home/lanforge/.local/lib/python3.6/site-packages')
def report_banner(date):
    banner_data = """
                   <!DOCTYPE html>
                    <html lang='en'>
                    <head>
                    <meta charset='UTF-8'>
                    <meta name='viewport' content='width=device-width, initial-scale=1' />
                    <title>LANforge Report</title>                        
                    </head>
                    <title>FTP Test </title></head>
                    <body>
                    <div class='Section report_banner-1000x205' style='background-image:url("/home/lanforge/LANforgeGUI_5.4.3/images/report_banner-1000x205.jpg");background-repeat:no-repeat;padding:0;margin:0;min-width:1000px; min-height:205px;width:1000px; height:205px;max-width:1000px; max-height:205px;'>                
                    <br>
                    <img align='right' style='padding:25;margin:5;width:200px;' src="/home/lanforge/LANforgeGUI_5.4.3/images/CandelaLogo2-90dpi-200x90-trans.png" border='0' />                
                    <div class='HeaderStyle'>
                    <br>
                    <h1 class='TitleFontPrint' style='color:darkgreen;'>  FTP Test  </h1>
                    <h3 class='TitleFontPrint' style='color:darkgreen;'>""" + str(date) + """</h3>
                    </div>
                    </div>
                    <br><br>
                 """
    return str(banner_data)
def test_objective(objective= 'This FTP Test is used to "Verify that N clients connected on Specified band and can simultaneously download some amount of file from FTP server and measuring the time taken by client to Download/Upload the file."'):
    test_objective = """
                    <!-- Test Objective -->
                    <h3 align='left'>Objective</h3> 
                    <p align='left' width='900'>""" + str(objective) + """</p>
                    <br>
                    """
    return str(test_objective)
def test_setup_information(test_setup_data=None):
    if test_setup_data is None:
        return None
    else:
        var = ""
        for i in test_setup_data:
            var = var + "<tr><td>" + i + "</td><td colspan='3'>" + str(test_setup_data[i]) + "</td></tr>"

    setup_information = """
                        <!-- Test Setup Information -->
                        <table width='700px' border='1' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                            <tr>
                              <th colspan='2'>Test Setup Information</th>
                            </tr>
                            <tr>
                              <td>Device Under Test</td>
                              <td>
                                <table width='100%' border='0' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                                  """ + str(var) + """
                                </table>
                              </td>
                            </tr>
                        </table>
                        <br>
                        """
    return str(setup_information)


def pass_fail_description(data=" This Table will give Pass/Fail results. "):
    pass_fail_info = """
                        <!-- Radar Detect status -->
                        <h3 align='left'>PASS/FAIL Results</h3> 
                        <p align='left' width='900'>""" + str(data) + """</p>
                        <br>
                    """
    return str(pass_fail_info)


def download_upload_time_description(data=" This Table will FTP Download/Upload Time of Clients."):
    download_upload_time= """
                    <!-- Radar Detect status -->
                    <h3 align='left'>File Download/Upload Time (sec)</h3> 
                    <p align='left' width='900'>""" + str(data) + """</p>
                    <br>
                """
    return str(download_upload_time)


def add_pass_fail_table(result_data, row_head_list, col_head_list):
    var_row = "<th></th>"
    for row in col_head_list:
        var_row = var_row + "<th>" + str(row) + "</th>"
    list_data = []
    dict_data = {}
    bands = result_data[1]["bands"]
    file_sizes = result_data[1]["file_sizes"]
    directions = result_data[1]["directions"]
    for b in bands:
        final_data = ""
        for size in file_sizes:
            for d in directions:
                for data in result_data.values():
                    if data["band"] == b and data["direction"] == d and data["file_size"] == size:
                        if data["result"] == "Pass":
                            final_data = final_data + "<td style='background-color:Green'>Pass</td>"
                        elif data["result"] == "Fail":
                            final_data = final_data + "<td style='background-color:Red'>Fail</td>"

        list_data.append(final_data)

    #print(list_data)
    j = 0
    for i in row_head_list:
        dict_data[i] = list_data[j]
        j = j + 1
    #print(dict_data)
    var_col = ""
    for col in row_head_list:
        var_col = var_col + "<tr><td>" + str(col) + "</td><!-- Add Variable Here -->" + str(
            dict_data[col]) + "</tr>"

    pass_fail_table = """
                      <!--  Radar Detected Table -->
                      <table width='1000px' border='1' cellpadding='2' cellspacing='0' >

                        <table width='1000px' border='1' >
                          <tr>
                              """ + str(var_row) + """
                          </tr>
                          """ + str(var_col) + """
                       </table>
                      </table>
                      <br><br><br><br><br><br><br>
                      """
    return pass_fail_table


def download_upload_time_table(result_data, row_head_list, col_head_list):
    var_row = "<th></th>"
    for row in col_head_list:
        var_row = var_row + "<th>" + str(row) + "</th>"
    list_data = []
    dict_data = {}
    bands = result_data[1]["bands"]
    file_sizes = result_data[1]["file_sizes"]
    directions = result_data[1]["directions"]
    for b in bands:
        final_data = ""
        for size in file_sizes:
            for d in directions:
                for data in result_data.values():
                    data_time = data['time']
                    if data_time.count(0) == 0:
                        Min = min(data_time)
                        Max = max(data_time)
                        Sum = int(sum(data_time))
                        Len = len(data_time)
                        Avg = round(Sum / Len,2)
                    elif data_time.count(0) == len(data_time):
                        Min = "-"
                        Max = "-"
                        Avg = "-"
                    else:
                        data_time = [i for i in data_time if i != 0]
                        Min = min(data_time)
                        Max = max(data_time)
                        Sum = int(sum(data_time))
                        Len = len(data_time)
                        Avg = round(Sum / Len,2)
                    string_data = "Min=" + str(Min) + ",Max=" + str(Max) + ",Avg=" + str(Avg) + " (sec)"
                    if data["band"] == b and data["direction"] == d and data["file_size"] == size:
                        final_data = final_data + """<td>""" + string_data + """</td>"""

        list_data.append(final_data)

    #print(list_data)
    j = 0
    for i in row_head_list:
        dict_data[i] = list_data[j]
        j = j + 1
    #print(dict_data)
    var_col = ""
    for col in row_head_list:
        var_col = var_col + "<tr><td>" + str(col) + "</td><!-- Add Variable Here -->" + str(
            dict_data[col]) + "</tr>"

    download_upload_table = """
                        <!--  Radar Detected Table -->
                        <table width='1000px' border='1' cellpadding='2' cellspacing='0' >

                          <table width='1000px' border='1' >
                            <tr>
                                """ + str(var_row) + """
                            </tr>
                            """ + str(var_col) + """
                         </table>
                        </table>
                        <br><br><br><br><br><br><br>
                        """
    return download_upload_table
def graph_html(graph_path="",graph_name="",graph_description=""):
    graph_html_obj = """
    <h3>""" +graph_name+ """</h3> 
    <p>""" +graph_description+ """</p>
      <img align='center' style='padding:15;margin:5;width:1000px;' src=""" + graph_path + """ border='1' />
    <br><br>
    """
    return str(graph_html_obj)


def bar_plot(ax,x_axis, data, colors=None, total_width=0.8, single_width=1, legend=True):
    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys(),bbox_to_anchor=(1.1,1.05),loc='upper right')
    ax.set_ylabel('Time in seconds')
    ax.set_xlabel("stations")
    x_data = x_axis
    idx = np.asarray([i for i in range(len(x_data))])
    ax.set_xticks(idx)

    ax.set_xticklabels(x_data)

def generate_graph(result_data, x_axis,band,size,graph_path):
    # bands = result_data[1]["bands"]
    # file_sizes = result_data[1]["file_sizes"]
    num_stations = result_data[1]["num_stations"]
    # for b in bands:
    #     for size in file_sizes:

    dict_of_graph = {}
    color = []
    graph_name = ""
    graph_description=""
    count = 0
    for data in result_data.values():
        if data["band"] == band and data["file_size"] == size and data["direction"] == "Download":
            dict_of_graph["Download"] = data["time"]
            color.append("Orange")
            graph_name = "File size "+ size +" " + str(num_stations) + " Clients " +band+ "-File Download Times(secs)"
            graph_description =  "Out of "+ str(data["num_stations"])+ " clients, "+ str(data["num_stations"] - data["time"].count(0))+ " are able to download " + "within " + str(data["duration"]) + " min."
            count = count + 1
        if data["band"] == band and data["file_size"] == size and data["direction"] == "Upload":
            dict_of_graph["Upload"] = data["time"]
            color.append("Blue")
            graph_name = "File size "+ size +" " + str(num_stations) + " Clients " +band+ "-File Upload Times(secs)"
            graph_description = graph_description + "Out of " + str(data["num_stations"]) + " clients, " + str(
                data["num_stations"] - data["time"].count(0)) + " are able to upload " + "within " +str(data["duration"]) + " min."
            count = count + 1
    if count == 2:
        graph_name = "File size "+ size +" " + str(num_stations) + " Clients " +band+ "-File Download and Upload Times(secs)"
    if len(dict_of_graph) != 0:
        fig, ax = plt.subplots()
        bar_plot(ax, x_axis, dict_of_graph, total_width=.8, single_width=.9, colors=color)
        my_dpi = 96
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(18, 6)

        # when saving, specify the DPI
        plt.savefig(graph_path + "/image"+band+size+".png", dpi=my_dpi)
        return str(graph_html(graph_path + "/image"+band+size+".png", graph_name,graph_description))
    else:
        return ""
def input_setup_info_table(input_setup_info=None):
    if input_setup_info is None:
        return None
    else:
        var = ""
        for i in input_setup_info:
            var = var + "<tr><td>" + i + "</td><td colspan='3'>" + str(input_setup_info[i]) + "</td></tr>"

    setup_information = """
                        <!-- Test Setup Information -->
                        <table width='700px' border='1' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                            <tr>
                              <th colspan='2'>Input Setup Information</th>
                            </tr>
                            <tr>
                              <td>Information</td>
                              <td>
                                <table width='100%' border='0' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                                  """ + str(var) + """
                                </table>
                              </td>
                            </tr>
                        </table>
                        <br>
                        """
    return str(setup_information)


def generate_report(result_data=None,
                    date=None,
                    test_setup_info={},
                    input_setup_info={},
                    graph_path="/home/lanforge/html-reports/FTP-Test"):
    # Need to pass this to test_setup_information()
    input_setup_info = input_setup_info
    test_setup_data = test_setup_info
    x_axis = []
    num_stations = result_data[1]["num_stations"]
    for i in range(1, num_stations + 1, 1):
        x_axis.append(i)
    column_head = []
    rows_head = []
    bands = result_data[1]["bands"]
    file_sizes = result_data[1]["file_sizes"]
    directions = result_data[1]["directions"]

    for size in file_sizes:
        for direction in directions:
            column_head.append(size + " " + direction)
    for band in bands:
        if band != "Both":
            rows_head.append(str(num_stations) + " Clients-" + band)
        else:
            rows_head.append(str(num_stations // 2) + "+" + str(num_stations // 2) + " Clients-2.4G+5G")

    reports_root = graph_path + "/" + str(date)
    if path.exists(graph_path):
        os.mkdir(reports_root)
        print("Reports Root is Created")

    else:
        os.mkdir(graph_path)
        os.mkdir(reports_root)
        print("Reports Root is created")
    print("Generating Reports in : ", reports_root)

    html_report = report_banner(date) + \
                  test_setup_information(test_setup_data) + \
                  test_objective() + \
                  pass_fail_description() + \
                  add_pass_fail_table(result_data, rows_head, column_head) + \
                  download_upload_time_description() + \
                  download_upload_time_table(result_data, rows_head, column_head)

    for b in bands:
        for size in file_sizes:
            html_report = html_report + \
                          generate_graph(result_data, x_axis, b, size, graph_path=reports_root)

    html_report = html_report + input_setup_info_table(input_setup_info)

    # write the html_report into a file in /home/lanforge/html_reports in a directory named FTP-Test and html_report name should be having a timesnap with it
    f = open(reports_root + "/report.html", "a")
    # f = open("report.html", "a")
    f.write(html_report)
    f.close()
    # write logic to generate pdf here
    pdfkit.from_file(reports_root + "/report.html", reports_root + "/report.pdf")


# test blocks from here
if __name__ == '__main__':
    generate_report()
