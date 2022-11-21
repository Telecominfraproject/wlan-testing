""" This script is used for DFS Test Report generation 
    it has generic methods inside which can be used for other test report generation 
    date - 11- feb - 2021
    -Nikita Yadav
"""
import os.path
import sys

print(sys.path)
sys.path.append('/home/lanforge/.local/lib/python3.6/site-packages')
import pdfkit

# dev complete
def report_banner(date):
    banner_data = """
                   <!DOCTYPE html>
                    <html lang='en'>
                    <head>
                    <meta charset='UTF-8'>
                    <meta name='viewport' content='width=device-width, initial-scale=1' />
                    <title>LANforge Report</title>                        

                    </head>

                    <title>DFS TEST </title></head>
                    <body>
                    <div class='Section report_banner-1000x205' style='background-image:url("/home/lanforge/LANforgeGUI_5.4.3/images/report_banner-1000x205.jpg");background-repeat:no-repeat;padding:0;margin:0;min-width:1000px; min-height:205px;width:1000px; height:205px;max-width:1000px; max-height:205px;'>
                    <br>
                    <img align='right' style='padding:25;margin:5;width:200px;' src="/home/lanforge/LANforgeGUI_5.4.3/images/CandelaLogo2-90dpi-200x90-trans.png" border='0' />


                    <div class='HeaderStyle'>
                    <br>
                    <h1 class='TitleFontPrint' style='color:darkgreen;'>  Dynamic Frequency Selection  </h1>
                    <h3 class='TitleFontPrint' style='color:darkgreen;'>""" + date + """</h3>
                    </div>
                    </div>

                    <br><br>

                 """
    return str(banner_data)

# dev complete
def test_objective(objective="The DFS Test is designed to test the Performance of the Netgear Access Point.Dynamic frequency selection is a technology that is designed to ensure that wireless devices operating in the unlicensed WLAN 5 GHz bands are able to detect when they may be interfering with military and weather radar systems and automatically switch over to another frequency where they will not cause any disturbance. "):
    test_objective = """
                    <!-- Test Objective -->
                    <h3 align='left'>Objective</h3> 
                    <p align='left' width='900'>""" + str(objective) + """</p>
                    <br>
                    """
    return str(test_objective)

def radar_detect_discription(data= " This Table will give you results in YES or NO if the AP detects the Radar"):
    test_radar = """
                    <!-- Radar Detect status -->
                    <h3 align='left'>Radar Detection Detail</h3> 
                    <p align='left' width='900'>""" + str(data) + """</p>
                    <br>
                """
    return str(test_radar)

def client_connection_detail(data = "This Table will give you results in seconds which is measured value of the time taken by the client to connect and generate traffic after Radar detection"):
    test_client = """
                        <!-- client connection time -->
                        <h3 align='left'>Client Connection Details</h3> 
                        <p align='left' width='900'>""" + str(data) + """</p>
                        <br>
                    """
    return str(test_client)

def detection_time_details(data= "This Table will give you results in seconds which is measured value of the time difference when the radar was sent and detected"):
    test_detection = """
                            <!-- detection time -->
                            <h3 align='left'>Detection Time Details</h3> 
                            <p align='left' width='900'>""" + str(data) + """</p>
                            <br>
                        """
    return  str(test_detection)

def switched_channel_details(data = "This Table will give you result value of channel number to which the client switches after radar detection X - channel never set in AP AUTO - State when we cannot determine the channel at which the client is associated"):
    switch_channel = """
                                <!-- switched channe;l -->
                                <h3 align='left'>Switcing Channel Details</h3> 
                                <p align='left' width='900'>""" + str(data) + """</p>
                                <br>
                            """
    return str(switch_channel)



# dev complete
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
                                  """ + var + """
                                </table>
                              </td>
                            </tr>
                        </table>

                        <br>
                        """
    return str(setup_information)


# yet to test on dev level
def graph_html(graph_path=""):
    graph_html_obj = """
    <!-- Detection Time Graph -->
    <h3>Detection Time Graph</h3> 
      <img align='center' style='padding:15;margin:5;width:1000px;' src=""" + graph_path + """ border='1' />
    <br><br>
    """
    return str(graph_html_obj)


def bar_plot(ax, data, x_axis_info=[], colors=None, total_width=0.8, single_width=1, legend=True):
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
        # print(values)

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])
        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys(), bbox_to_anchor=(1.1, 1.05))

    ax.set_ylabel('Time in seconds')
    ax.set_xlabel('Channels')
    # ax.set_xticks(1)
    x_data = x_axis_info
    idx = np.asarray([i for i in range(len(x_data))])
    ax.set_xticks(idx)

    ax.set_xticklabels(x_data)


def generate_graph(result_data, x_axis_info, graph_path):
    detection_data = dict.fromkeys(result_data.keys())
    for i in detection_data:
        try:
            detection_data[i] = result_data[i]['detection_time_lst']
        except:
            detection_data[i] = []
    print(detection_data)

    fig, ax = plt.subplots()
    bar_plot(ax, detection_data, x_axis_info=x_axis_info, total_width=.8, single_width=1.2)

    my_dpi = 96
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(18, 6)

    # when saving, specify the DPI
    str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
    plt.savefig(graph_path + "/image.png", dpi=my_dpi)
    return str(graph_html(graph_path + "/image.png"))


# yet to test on dev level
def add_radar_table(result_data, row_head_list=None, col_head_list=None):
    var_row = "<th></th>"
    for row in col_head_list:
        var_row = var_row + "<th>" + row + "</th>"

    radar_html_struct = dict.fromkeys(list(result_data.keys()))
    for fcc in list(result_data.keys()):
        fcc_type = result_data[fcc]["radar_lst"]
        final_data = ""
        for i in fcc_type:
            if i == "YES":
                final_data = final_data + "<td colspan='1' bgcolor='#90EE90'>YES</td>"

            else:
                final_data = final_data + "<td colspan='1' bgcolor='orange'>NO</td>"
        radar_html_struct[fcc] = final_data

    var_col = ""
    for col in row_head_list:
        var_col = var_col + "<tr><td>" + str(col) + "</td><!-- Add Variable Here -->" + str(
            radar_html_struct[col]) + "</tr>"

    radar_html = """
                <!--  Radar Detected Table -->
                <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                  <tr>
                    <th colspan='2'>Radar Detected </th>
                  </tr>
                  <table width='1000px' border='1' >
                    <tr>
                        """ + var_row + """
                    </tr>
                    """ + var_col + """
                 </table>
                </table>
                <br><br><br><br><br><br><br>
                """
    return str(radar_html)


# yet to test on dev level
def add_client_cx_table(result_data, row_head_list, col_head_list):
    var_row = "<th></th>"
    for row in col_head_list:
        var_row = var_row + "<th>" + row + "</th>"

    client_html_struct = dict.fromkeys(list(result_data.keys()))
    for fcc in list(result_data.keys()):
        fcc_type = result_data[fcc]["connection_time_lst"]
        final_data = ""
        for i in fcc_type:
            if i == 0:
                final_data = final_data + "<td colspan='1'bgcolor='pink'>" + str(i) + "</td>"
            else:
                final_data = final_data + "<td colspan='1' bgcolor='yellow'>" + str(i) + "</td>"

        client_html_struct[fcc] = final_data

    var_col = ""
    for col in row_head_list:
        var_col = var_col + "<tr><td>" + str(col) + "</td><!-- Add Variable Here -->" + str(
            client_html_struct[col]) + "</tr>"
    client_cx_html = """
                    <!--  Radar Detected Table -->
                    <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                      <tr>
                        <th colspan='2'>Client Connection Time (sec) </th>
                      </tr>
                      <table width='1000px' border='1' >
                        <tr>
                            """ + var_row + """
                        </tr>
                        """ + var_col + """
                     </table>
                    </table>
                    <br><br><br><br><br><br><br>
                    """
    return str(client_cx_html)


# yet to test on dev level
def add_detection_table(result_data, row_head_list, col_head_list):
    var_row = "<th></th>"
    for row in col_head_list:
        var_row = var_row + "<th>" + row + "</th>"

    detection_html_struct = dict.fromkeys(list(result_data.keys()))
    for fcc in list(result_data.keys()):
        fcc_type = result_data[fcc]["detection_time_lst"]
        final_data = ""
        for i in fcc_type:
            if i == 0:
                final_data = final_data + "<td colspan='1' bgcolor='GREEN'>" + str(i) + " </td>"
            else:
                final_data = final_data + "<td colspan='1'bgcolor='BLUE'>" + str(i) + " </td>"

        detection_html_struct[fcc] = final_data

    var_col = ""
    for col in row_head_list:
        var_col = var_col + "<tr><td>" + str(col) + "</td><!-- Add Variable Here -->" + str(
            detection_html_struct[col]) + "</tr>"

    detection_html = """
                    <!--  Radar Detected Table -->
                    <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                      <tr>
                        <th colspan='2'>Detection Time (sec) </th>
                      </tr>
                      <table width='1000px' border='1' >
                        <tr>
                            """ + var_row + """
                        </tr>
                        """ + var_col + """
                     </table>
                    </table>
                    <br><br><br><br><br><br><br>
                    """
    return detection_html


# yet to test on dev level
def add_switched_channel_table(result_data, row_head_list, col_head_list):
    var_row = "<th></th>"
    for row in col_head_list:
        var_row = var_row + "<th>" + row + "</th>"

    switched_html_struct = dict.fromkeys(list(result_data.keys()))
    for fcc in list(result_data.keys()):
        fcc_type = result_data[fcc]["switched_ch_lst"]
        final_data = ""
        for i in fcc_type:
            if i == "X" or i == "AUTO":
                final_data = final_data + "<td colspan='1'bgcolor='#C6FECC'>" + str(i) + "</td>"
            elif i == " - ":
                final_data = final_data + "<td colspan='1'bgcolor='#CCC6FE'>" + str(i) + "</td>"

            else:
                final_data = final_data + "<td colspan='1'bgcolor=' #FEE8C6'>" + str(i) + "</td>"

        switched_html_struct[fcc] = final_data

    var_col = ""
    for col in row_head_list:
        var_col = var_col + "<tr><td>" + str(col) + "</td><!-- Add Variable Here -->" + str(
            switched_html_struct[col]) + "</tr>"

    switched_data = """
                    <!--  Radar Detected Table -->
                    <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                      <tr>
                        <th colspan='2'>Switched Channel </th>
                      </tr>
                      <table width='1000px' border='1' >
                        <tr>
                            """ + var_row + """
                        </tr>
                        """ + var_col + """
                     </table>
                    </table>
                    <br><br><br><br><br><br><br>
                    """

    return switched_data

'''def input_usedinformation(ip ="", user="", passwd="", radio= "", help= ""):
    setup_information = """
                        <!-- Input Used Information -->
                        <table width='700px' border='1' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                            <tr>
                              <th colspan='2'>Input Given Information</th>
                            </tr>
                            <tr>
                              <td>Input used in script</td>
                              <td>
                                <table width='100%' border='0' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                                  <tr>
                                    <td>AP ip</td>
                                    <td colspan='3'>""" + ip + """</td>
                                  </tr>
                                  <tr>
                                    <td>user name</td>
                                    <td colspan='3'>""" + user + """</td>
                                  </tr>
                                  <tr>
                                    <td>password</td>
                                    <td colspan='3'>""" + passwd + """</td>
                                  </tr>
                                  <tr>
                                    <td>radio</td>
                                    <td colspan='3'>""" + radio + """</td>
                                  </tr>
                                  <tr>
                                    <td>help</td>
                                    <td colspan='3'>""" + help + """</td>
                                  </tr>
                                </table>
                              </td>
                            </tr>
                        </table>

                        <br>
                        """
    return str(setup_information)'''
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
                                  """ + var + """
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
                    input_setup_info = {},
                    test_channel=None,

                    graph_path="/home/lanforge/html-reports/dfs"):
    # Need to pass this to test_setup_information()
    input_setup_info = input_setup_info
    test_setup_data = test_setup_info
    test_chal = test_channel

    # test_setup_data = {
    #     "AP Name": "TestAP",
    #     "SSID": "NETGEAR",f
    #     "Number of Stations": "1",
    #     "Test Duration": "5:00 Mins"
    # }

    """result_data = {'FCC0': {'switched_ch_lst': ["1"], 'detection_time_lst': [1, 5], 'radar_lst': ['NO', 'YES'],
                            'connection_time_lst': [0, 65]}
                   }"""
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
                  generate_graph(result_data, test_chal, graph_path=reports_root) + \
                  radar_detect_discription() + \
                  add_radar_table(result_data, result_data.keys(), test_chal) + \
                  client_connection_detail() + \
                  add_client_cx_table(result_data, result_data.keys(), test_chal) + \
                  detection_time_details() + \
                  add_detection_table(result_data, result_data.keys(), test_chal) + \
                  switched_channel_details() + \
                  add_switched_channel_table(result_data, result_data.keys(), test_chal) + \
                  input_setup_info_table(input_setup_info)




    # write the html_report into a file in /home/lanforge/html_reports in a directory named DFS_TEST and html_report name should be having a timesnap with it
    f = open(reports_root + "/report.html", "a")
    # f = open("report.html", "a")
    f.write(html_report)
    f.close()
    # write logic to generate pdf here
    pdfkit.from_file(reports_root + "/report.html", reports_root + "/report.pdf")


# test blocks from here
if __name__ == '__main__':
    generate_report()
    # generate_graph()









""" This script is used for DFS Test Report generation 
    it has generic methods inside which can be used for other test report generation 
    date - 11- feb - 2021
    -Nikita Yadav
"""

from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
import os.path
from os import path
import sys

print(sys.path)
sys.path.append('/home/lanforge/.local/lib/python3.6/site-packages')
import pdfkit

# dev complete
def report_banner(date):
    banner_data = """
                   <!DOCTYPE html>
                    <html lang='en'>
                    <head>
                    <meta charset='UTF-8'>
                    <meta name='viewport' content='width=device-width, initial-scale=1' />
                    <title>LANforge Report</title>                        

                    </head>

                    <title>DFS TEST </title></head>
                    <body>
                    <div class='Section report_banner-1000x205' style='background-image:url("/home/lanforge/LANforgeGUI_5.4.3/images/report_banner-1000x205.jpg");background-repeat:no-repeat;padding:0;margin:0;min-width:1000px; min-height:205px;width:1000px; height:205px;max-width:1000px; max-height:205px;'>
                    <br>
                    <img align='right' style='padding:25;margin:5;width:200px;' src="/home/lanforge/LANforgeGUI_5.4.3/images/CandelaLogo2-90dpi-200x90-trans.png" border='0' />


                    <div class='HeaderStyle'>
                    <br>
                    <h1 class='TitleFontPrint' style='color:darkgreen;'>  Dynamic Frequency Selection  </h1>
                    <h3 class='TitleFontPrint' style='color:darkgreen;'>""" + date + """</h3>
                    </div>
                    </div>

                    <br><br>

                 """
    return str(banner_data)

# dev complete
def test_objective(objective="The DFS Test is designed to test the Performance of the Netgear Access Point.Dynamic frequency selection is a technology that is designed to ensure that wireless devices operating in the unlicensed WLAN 5 GHz bands are able to detect when they may be interfering with military and weather radar systems and automatically switch over to another frequency where they will not cause any disturbance. "):
    test_objective = """
                    <!-- Test Objective -->
                    <h3 align='left'>Objective</h3> 
                    <p align='left' width='900'>""" + str(objective) + """</p>
                    <br>
                    """
    return str(test_objective)

def radar_detect_discription(data= " This Table will give you results in YES or NO if the AP detects the Radar"):
    test_radar = """
                    <!-- Radar Detect status -->
                    <h3 align='left'>Radar Detection Detail</h3> 
                    <p align='left' width='900'>""" + str(data) + """</p>
                    <br>
                """
    return str(test_radar)

def client_connection_detail(data = "This Table will give you results in seconds which is measured value of the time taken by the client to connect and generate traffic after Radar detection"):
    test_client = """
                        <!-- client connection time -->
                        <h3 align='left'>Client Connection Details</h3> 
                        <p align='left' width='900'>""" + str(data) + """</p>
                        <br>
                    """
    return str(test_client)

def detection_time_details(data= "This Table will give you results in seconds which is measured value of the time difference when the radar was sent and detected"):
    test_detection = """
                            <!-- detection time -->
                            <h3 align='left'>Detection Time Details</h3> 
                            <p align='left' width='900'>""" + str(data) + """</p>
                            <br>
                        """
    return  str(test_detection)

def switched_channel_details(data = "This Table will give you result value of channel number to which the client switches after radar detection X - channel never set in AP AUTO - State when we cannot determine the channel at which the client is associated"):
    switch_channel = """
                                <!-- switched channe;l -->
                                <h3 align='left'>Switcing Channel Details</h3> 
                                <p align='left' width='900'>""" + str(data) + """</p>
                                <br>
                            """
    return str(switch_channel)



# dev complete
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
                                  """ + var + """
                                </table>
                              </td>
                            </tr>
                        </table>

                        <br>
                        """
    return str(setup_information)


# yet to test on dev level
def graph_html(graph_path=""):
    graph_html_obj = """
    <!-- Detection Time Graph -->
    <h3>Detection Time Graph</h3> 
      <img align='center' style='padding:15;margin:5;width:1000px;' src=""" + graph_path + """ border='1' />
    <br><br>
    """
    return str(graph_html_obj)


def bar_plot(ax, data, x_axis_info=[], colors=None, total_width=0.8, single_width=1, legend=True):
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
        # print(values)

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])
        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys(), bbox_to_anchor=(1.1, 1.05))

    ax.set_ylabel('Time in seconds')
    ax.set_xlabel('Channels')
    # ax.set_xticks(1)
    x_data = x_axis_info
    idx = np.asarray([i for i in range(len(x_data))])
    ax.set_xticks(idx)

    ax.set_xticklabels(x_data)


def generate_graph(result_data, x_axis_info, graph_path):
    detection_data = dict.fromkeys(result_data.keys())
    for i in detection_data:
        try:
            detection_data[i] = result_data[i]['detection_time_lst']
        except:
            detection_data[i] = []
    print(detection_data)

    fig, ax = plt.subplots()
    bar_plot(ax, detection_data, x_axis_info=x_axis_info, total_width=.8, single_width=1.2)

    my_dpi = 96
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(18, 6)

    # when saving, specify the DPI
    str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
    plt.savefig(graph_path + "/image.png", dpi=my_dpi)
    return str(graph_html(graph_path + "/image.png"))


# yet to test on dev level
def add_radar_table(result_data, row_head_list=None, col_head_list=None):
    var_row = "<th></th>"
    for row in col_head_list:
        var_row = var_row + "<th>" + row + "</th>"

    radar_html_struct = dict.fromkeys(list(result_data.keys()))
    for fcc in list(result_data.keys()):
        fcc_type = result_data[fcc]["radar_lst"]
        final_data = ""
        for i in fcc_type:
            if i == "YES":
                final_data = final_data + "<td colspan='1' bgcolor='#90EE90'>YES</td>"

            else:
                final_data = final_data + "<td colspan='1' bgcolor='orange'>NO</td>"
        radar_html_struct[fcc] = final_data

    var_col = ""
    for col in row_head_list:
        var_col = var_col + "<tr><td>" + str(col) + "</td><!-- Add Variable Here -->" + str(
            radar_html_struct[col]) + "</tr>"

    radar_html = """
                <!--  Radar Detected Table -->
                <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                  <tr>
                    <th colspan='2'>Radar Detected </th>
                  </tr>
                  <table width='1000px' border='1' >
                    <tr>
                        """ + var_row + """
                    </tr>
                    """ + var_col + """
                 </table>
                </table>
                <br><br><br><br><br><br><br>
                """
    return str(radar_html)


# yet to test on dev level
def add_client_cx_table(result_data, row_head_list, col_head_list):
    var_row = "<th></th>"
    for row in col_head_list:
        var_row = var_row + "<th>" + row + "</th>"

    client_html_struct = dict.fromkeys(list(result_data.keys()))
    for fcc in list(result_data.keys()):
        fcc_type = result_data[fcc]["connection_time_lst"]
        final_data = ""
        for i in fcc_type:
            if i == 0:
                final_data = final_data + "<td colspan='1'bgcolor='pink'>" + str(i) + "</td>"
            else:
                final_data = final_data + "<td colspan='1' bgcolor='yellow'>" + str(i) + "</td>"

        client_html_struct[fcc] = final_data

    var_col = ""
    for col in row_head_list:
        var_col = var_col + "<tr><td>" + str(col) + "</td><!-- Add Variable Here -->" + str(
            client_html_struct[col]) + "</tr>"
    client_cx_html = """
                    <!--  Radar Detected Table -->
                    <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                      <tr>
                        <th colspan='2'>Client Connection Time (sec) </th>
                      </tr>
                      <table width='1000px' border='1' >
                        <tr>
                            """ + var_row + """
                        </tr>
                        """ + var_col + """
                     </table>
                    </table>
                    <br><br><br><br><br><br><br>
                    """
    return str(client_cx_html)


# yet to test on dev level
def add_detection_table(result_data, row_head_list, col_head_list):
    var_row = "<th></th>"
    for row in col_head_list:
        var_row = var_row + "<th>" + row + "</th>"

    detection_html_struct = dict.fromkeys(list(result_data.keys()))
    for fcc in list(result_data.keys()):
        fcc_type = result_data[fcc]["detection_time_lst"]
        final_data = ""
        for i in fcc_type:
            if i == 0:
                final_data = final_data + "<td colspan='1' bgcolor='GREEN'>" + str(i) + " </td>"
            else:
                final_data = final_data + "<td colspan='1'bgcolor='BLUE'>" + str(i) + " </td>"

        detection_html_struct[fcc] = final_data

    var_col = ""
    for col in row_head_list:
        var_col = var_col + "<tr><td>" + str(col) + "</td><!-- Add Variable Here -->" + str(
            detection_html_struct[col]) + "</tr>"

    detection_html = """
                    <!--  Radar Detected Table -->
                    <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                      <tr>
                        <th colspan='2'>Detection Time (sec) </th>
                      </tr>
                      <table width='1000px' border='1' >
                        <tr>
                            """ + var_row + """
                        </tr>
                        """ + var_col + """
                     </table>
                    </table>
                    <br><br><br><br><br><br><br>
                    """
    return detection_html


# yet to test on dev level
def add_switched_channel_table(result_data, row_head_list, col_head_list):
    var_row = "<th></th>"
    for row in col_head_list:
        var_row = var_row + "<th>" + row + "</th>"

    switched_html_struct = dict.fromkeys(list(result_data.keys()))
    for fcc in list(result_data.keys()):
        fcc_type = result_data[fcc]["switched_ch_lst"]
        final_data = ""
        for i in fcc_type:
            if i == "X" or i == "AUTO":
                final_data = final_data + "<td colspan='1'bgcolor='#C6FECC'>" + str(i) + "</td>"
            elif i == " - ":
                final_data = final_data + "<td colspan='1'bgcolor='#CCC6FE'>" + str(i) + "</td>"

            else:
                final_data = final_data + "<td colspan='1'bgcolor=' #FEE8C6'>" + str(i) + "</td>"

        switched_html_struct[fcc] = final_data

    var_col = ""
    for col in row_head_list:
        var_col = var_col + "<tr><td>" + str(col) + "</td><!-- Add Variable Here -->" + str(
            switched_html_struct[col]) + "</tr>"

    switched_data = """
                    <!--  Radar Detected Table -->
                    <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                      <tr>
                        <th colspan='2'>Switched Channel </th>
                      </tr>
                      <table width='1000px' border='1' >
                        <tr>
                            """ + var_row + """
                        </tr>
                        """ + var_col + """
                     </table>
                    </table>
                    <br><br><br><br><br><br><br>
                    """

    return switched_data

'''def input_usedinformation(ip ="", user="", passwd="", radio= "", help= ""):
    setup_information = """
                        <!-- Input Used Information -->
                        <table width='700px' border='1' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                            <tr>
                              <th colspan='2'>Input Given Information</th>
                            </tr>
                            <tr>
                              <td>Input used in script</td>
                              <td>
                                <table width='100%' border='0' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                                  <tr>
                                    <td>AP ip</td>
                                    <td colspan='3'>""" + ip + """</td>
                                  </tr>
                                  <tr>
                                    <td>user name</td>
                                    <td colspan='3'>""" + user + """</td>
                                  </tr>
                                  <tr>
                                    <td>password</td>
                                    <td colspan='3'>""" + passwd + """</td>
                                  </tr>
                                  <tr>
                                    <td>radio</td>
                                    <td colspan='3'>""" + radio + """</td>
                                  </tr>
                                  <tr>
                                    <td>help</td>
                                    <td colspan='3'>""" + help + """</td>
                                  </tr>
                                </table>
                              </td>
                            </tr>
                        </table>

                        <br>
                        """
    return str(setup_information)'''
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
                                  """ + var + """
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
                    input_setup_info = {},
                    test_channel=None,

                    graph_path="/home/lanforge/html-reports/dfs"):
    # Need to pass this to test_setup_information()
    input_setup_info = input_setup_info
    test_setup_data = test_setup_info
    test_chal = test_channel

    # test_setup_data = {
    #     "AP Name": "TestAP",
    #     "SSID": "NETGEAR",f
    #     "Number of Stations": "1",
    #     "Test Duration": "5:00 Mins"
    # }

    """result_data = {'FCC0': {'switched_ch_lst': ["1"], 'detection_time_lst': [1, 5], 'radar_lst': ['NO', 'YES'],
                            'connection_time_lst': [0, 65]}
                   }"""
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
                  generate_graph(result_data, test_chal, graph_path=reports_root) + \
                  radar_detect_discription() + \
                  add_radar_table(result_data, result_data.keys(), test_chal) + \
                  client_connection_detail() + \
                  add_client_cx_table(result_data, result_data.keys(), test_chal) + \
                  detection_time_details() + \
                  add_detection_table(result_data, result_data.keys(), test_chal) + \
                  switched_channel_details() + \
                  add_switched_channel_table(result_data, result_data.keys(), test_chal) + \
                  input_setup_info_table(input_setup_info)




    # write the html_report into a file in /home/lanforge/html_reports in a directory named DFS_TEST and html_report name should be having a timesnap with it
    f = open(reports_root + "/report.html", "a")
    # f = open("report.html", "a")
    f.write(html_report)
    f.close()
    # write logic to generate pdf here
    pdfkit.from_file(reports_root + "/report.html", reports_root + "/report.pdf")


# test blocks from here
if __name__ == '__main__':
    generate_report()
    # generate_graph()









