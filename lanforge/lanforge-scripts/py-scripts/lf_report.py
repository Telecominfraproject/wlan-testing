#!/usr/bin/env python3

"""
NAME: lf_report.py

PURPOSE:

This program is a helper  class for reporting results for a lanforge python script.
The class will generate an output directory based on date and time in the /home/lanforge/html-reports/ .
If the reports-data is not present then the date and time directory will be created in the current directory.
The banner and Candela Technology logo will be copied in the results directory.
The results directory may be over written and many of the other paramaters during construction.
Creating the date time directory on construction was a design choice.

EXAMPLE:

This is a helper class, a unit test is included at the bottom of the file.
To test lf_report.py and lf_graph.py together use the lf_report_test.py file

LICENSE:
    Free to distribute and modify. LANforge systems must be licensed.
    Copyright 2021 Candela Technologies Inc


INCLUDE_IN_README
"""
# CAUTION: adding imports to this file which are not in update_dependencies.py is not advised
import os
import shutil
import datetime

import pandas as pd
import pdfkit
import argparse


# internal candela references included during intial phases, to be deleted at future date
# https://candelatech.atlassian.net/wiki/spaces/LANFORGE/pages/372703360/Scripting+Data+Collection+March+2021
# base report class

class lf_report:
    def __init__(self,
                 # _path the report directory under which the report directories will be created.
                 _path="/home/lanforge/html-reports",
                 _alt_path="",
                 _date="",
                 _title="LANForge Unit Test Run Heading",
                 _table_title="LANForge Table Heading",
                 _graph_title="LANForge Graph Title",
                 _obj="",
                 _obj_title="",
                 _output_html="outfile.html",
                 _output_pdf="outfile.pdf",
                 _results_dir_name="LANforge_Test_Results_Unit_Test",
                 _output_format='html',  # pass in on the write functionality, current not used
                 _dataframe="",
                 _path_date_time="",
                 _custom_css='custom-example.css'):  # this is where the final report is placed.
        # other report paths,

        # _path is where the directory with the data time will be created
        if _path == "local" or _path == "here":
            self.path = os.path.abspath(__file__)
            print("path set to file path: {}".format(self.path))
        elif _alt_path != "":
            self.path = _alt_path
            print("path set to alt path: {}".format(self.path))
        else:
            self.path = _path
            print("path set: {}".format(self.path))

        self.dataframe = _dataframe
        self.text = ""
        self.title = _title
        self.table_title = _table_title
        self.graph_title = _graph_title
        self.date = _date
        self.output_html = _output_html
        self.path_date_time = _path_date_time
        self.write_output_html = ""
        self.write_output_index_html = ""
        self.output_pdf = _output_pdf
        self.write_output_pdf = ""
        self.banner_html = ""
        self.footer_html = ""
        self.graph_titles = ""
        self.graph_image = ""
        self.csv_file_name = ""
        self.html = ""
        self.custom_html = ""
        self.pdf_link_html = ""
        self.objective = _obj
        self.obj_title = _obj_title
        # self.systeminfopath = ""
        self.date_time_directory = ""
        self.log_directory = ""

        self.banner_directory = "artifacts"
        self.banner_file_name = "banner.png"  # does this need to be configurable
        self.logo_directory = "artifacts"
        self.logo_file_name = "CandelaLogo2-90dpi-200x90-trans.png"  # does this need to be configurable.
        self.logo_footer_file_name = "candela_swirl_small-72h.png"  # does this need to be configurable.
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.custom_css = _custom_css
        # note: the following 3 calls must be in order
        self.set_date_time_directory(_date, _results_dir_name)
        self.build_date_time_directory()
        self.build_log_directory()

        self.font_file = "CenturyGothic.woff"
        # move the banners and candela images to report path
        self.copy_banner()
        self.copy_css()
        self.copy_logo()
        self.copy_logo_footer()

    def copy_banner(self):
        banner_src_file = str(self.current_path) + '/' + str(self.banner_directory) + '/' + str(self.banner_file_name)
        banner_dst_file = str(self.path_date_time) + '/' + str(self.banner_file_name)
        # print("banner src_file: {}".format(banner_src_file))
        # print("dst_file: {}".format(banner_dst_file))
        shutil.copy(banner_src_file, banner_dst_file)

    def copy_css(self):
        reportcss_src_file = str(self.current_path) + '/' + str(self.banner_directory) + '/report.css'
        # print("copy_css: source file is: "+reportcss_src_file)
        reportcss_dest_file = str(self.path_date_time) + '/report.css'

        customcss_src_file = str(self.current_path) + '/' + str(self.banner_directory) + '/' + str(self.custom_css)
        customcss_dest_file = str(self.path_date_time) + '/custom.css'

        font_src_file = str(self.current_path) + '/' + str(self.banner_directory) + '/' + str(self.font_file)
        font_dest_file = str(self.path_date_time) + '/' + str(self.font_file)

        shutil.copy(reportcss_src_file, reportcss_dest_file)
        shutil.copy(customcss_src_file, customcss_dest_file)
        shutil.copy(font_src_file, font_dest_file)

    def copy_logo(self):
        logo_src_file = str(self.current_path) + '/' + str(self.logo_directory) + '/' + str(self.logo_file_name)
        logo_dst_file = str(self.path_date_time) + '/' + str(self.logo_file_name)
        # print("logo_src_file: {}".format(logo_src_file))
        # print("logo_dst_file: {}".format(logo_dst_file))
        shutil.copy(logo_src_file, logo_dst_file)

    def copy_logo_footer(self):
        logo_footer_src_file = str(self.current_path) + '/' + str(self.logo_directory) + '/' + str(
            self.logo_footer_file_name)
        logo_footer_dst_file = str(self.path_date_time) + '/' + str(self.logo_footer_file_name)
        # print("logo_footer_src_file: {}".format(logo_footer_src_file))
        # print("logo_footer_dst_file: {}".format(logo_footer_dst_file))
        shutil.copy(logo_footer_src_file, logo_footer_dst_file)

    def move_graph_image(self, ):
        graph_src_file = str(self.graph_image)
        graph_dst_file = str(self.path_date_time) + '/' + str(self.graph_image)
        print("graph_src_file: {}".format(graph_src_file))
        print("graph_dst_file: {}".format(graph_dst_file))
        shutil.move(graph_src_file, graph_dst_file)

    def move_csv_file(self):
        csv_src_file = str(self.csv_file_name)
        csv_dst_file = str(self.path_date_time) + '/' + str(self.csv_file_name)
        print("csv_src_file: {}".format(csv_src_file))
        print("csv_dst_file: {}".format(csv_dst_file))
        shutil.move(csv_src_file, csv_dst_file)

    def set_path(self, _path):
        self.path = _path

    def set_date_time_directory(self, _date, _results_dir_name):
        self.date = _date
        self.results_dir_name = _results_dir_name
        if self.date != "":
            self.date_time_directory = str(self.date) + str("_") + str(self.results_dir_name)
        else:
            self.date = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")).replace(':', '-')
            self.date_time_directory = self.date + str("_") + str(self.results_dir_name)

    def build_date_time_directory(self):
        if self.date_time_directory == "":
            self.set_date_time_directory()
        self.path_date_time = os.path.join(self.path, self.date_time_directory)
        print("path_date_time {}".format(self.path_date_time))
        try:
            if not os.path.exists(self.path_date_time):
                os.mkdir(self.path_date_time)
        except:
            self.path_date_time = os.path.join(self.current_path, self.date_time_directory)
            if not os.path.exists(self.path_date_time):
                os.mkdir(self.path_date_time)
        print("report path : {}".format(self.path_date_time))

    def build_log_directory(self):
        if self.log_directory == "":
            self.log_directory = os.path.join(self.path_date_time, "log")
        try:
            if not os.path.exists(self.log_directory):
                os.mkdir(self.log_directory)
        except:
            print("exception making {}".format(self.log_directory))
            exit(1)

    def set_text(self, _text):
        self.text = _text

    def set_title(self, _title):
        self.title = _title

    def set_table_title(self, _table_title):
        self.table_title = _table_title

    def set_graph_title(self, _graph_title):
        self.graph_title = _graph_title

    # sets the csv file name as graph title
    def set_csv_filename(self, _graph_title):
        fname, ext = os.path.splitext(_graph_title)
        self.csv_file_name = fname + ".csv"

    # The _date is set when class is enstanciated / created so this set_date should be used with caution, used to synchronize results
    def set_date(self, _date):
        self.date = _date

    def set_table_dataframe(self, _dataframe):
        self.dataframe = _dataframe

    def set_table_dataframe_from_csv(self, _csv):
        self.dataframe = pd.read_csv(_csv)

    def set_custom_html(self, _custom_html):
        self.custom_html = _custom_html

    def set_obj_html(self, _obj_title, _obj):
        self.objective = _obj
        self.obj_title = _obj_title

    def set_graph_image(self, _graph_image):
        self.graph_image = _graph_image

    def get_date(self):
        return self.date

    def get_path(self):
        return self.path

    def get_parent_path(self):
        parent_path = os.path.dirname(self.path)
        return parent_path

    # get_path_date_time, get_report_path and need to be the same
    def get_path_date_time(self):
        return self.path_date_time

    def get_report_path(self):
        return self.path_date_time

    def get_log_path(self):
        return self.log_directory

    def file_add_path(self, file):
        output_file = str(self.path_date_time) + '/' + str(file)
        print("output file {}".format(output_file))
        return output_file

    def write_html(self):
        self.write_output_html = str(self.path_date_time) + '/' + str(self.output_html)
        print("write_output_html: {}".format(self.write_output_html))
        try:
            test_file = open(self.write_output_html, "w")
            test_file.write(self.html)
            test_file.close()
        except:
            print("write_html failed")
        return self.write_output_html

    def write_index_html(self):
        self.write_output_index_html = str(self.path_date_time) + '/' + str("index.html")
        print("write_output_index_html: {}".format(self.write_output_index_html))
        try:
            test_file = open(self.write_output_index_html, "w")
            test_file.write(self.html)
            test_file.close()
        except:
            print("write_index_html failed")
        return self.write_output_index_html

    def write_html_with_timestamp(self):
        self.write_output_html = "{}/{}-{}".format(self.path_date_time, self.date, self.output_html)
        print("write_output_html: {}".format(self.write_output_html))
        try:
            test_file = open(self.write_output_html, "w")
            test_file.write(self.html)
            test_file.close()
        except:
            print("write_html failed")
        return self.write_output_html

    # https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
    # page_size A4, A3, Letter, Legal
    # orientation Portrait , Landscape
    def write_pdf(self, _page_size='A4', _orientation='Portrait'):
        # write logic to generate pdf here
        # wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
        # sudo apt install ./wkhtmltox_0.12.6-1.focal_amd64.deb

        options = {"enable-local-file-access": None,
                   'orientation': _orientation,
                   'page-size': _page_size}  # prevent error Blocked access to file
        self.write_output_pdf = str(self.path_date_time) + '/' + str(self.output_pdf)
        pdfkit.from_file(self.write_output_html, self.write_output_pdf, options=options)

    # https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
    # page_size A4, A3, Letter, Legal
    # orientation Portrait , Landscape
    def write_pdf_with_timestamp(self, _page_size='A4', _orientation='Portrait'):
        # write logic to generate pdf here
        # wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
        # sudo apt install ./wkhtmltox_0.12.6-1.focal_amd64.deb

        options = {"enable-local-file-access": None,
                   'orientation': _orientation,
                   'page-size': _page_size}  # prevent error Blocked access to file
        self.write_output_pdf = "{}/{}-{}".format(self.path_date_time, self.date, self.output_pdf)
        pdfkit.from_file(self.write_output_html, self.write_output_pdf, options=options)

    def get_pdf_path(self):
        pdf_link_path = "{}/{}-{}".format(self.path_date_time, self.date, self.output_pdf)
        return pdf_link_path

    def build_pdf_link(self, _pdf_link_name, _pdf_link_path):
        self.pdf_link_html = """
            <!-- pdf link -->
            <a href="{pdf_link_path}" target="_blank">{pdf_link_name}</a>
            <br>
        """.format(pdf_link_path=_pdf_link_path, pdf_link_name=_pdf_link_name)
        self.html += self.pdf_link_html

    def build_link(self, _link_name, _link_path):
        self.link = """
            <!-- link -->
            <a href="{link_path}" target="_blank">{link_name}</a>
            <br>
        """.format(link_path=_link_path, link_name=_link_name)
        self.html += self.link

    def generate_report(self):
        self.write_html()
        self.write_pdf()

    def build_all(self):
        self.build_banner()
        self.start_content_div()
        self.build_table_title()
        self.build_table()
        self.end_content_div()

    def get_html_head(self, title='Untitled'):
        return """<head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1' />
        <style>
        body {{ margin: 0; padding: 0; }}
        </style>
        <link rel='stylesheet' href='report.css' />
        <link rel='stylesheet' href='custom.css' />
        <title>{title}</title>
    </head>""".format(title=title)

    def build_banner(self):
        # NOTE: {{ }} are the ESCAPED curly braces
        # JBR removed deep indentation of html tag because it makes browser view-source is hard to debug
        # JBR suggests rename method to start_html_doc()
        self.banner_html = """<!DOCTYPE html>
<html lang='en'>
    {head_tag}
    <body>
        <div id='BannerBack'>
            <div id='Banner'>
                <br/>
                <img id='BannerLogo' align='right' src="CandelaLogo2-90dpi-200x90-trans.png" border='0'/>
                <div class='HeaderStyle'>
                    <br>
                    <h1 class='TitleFontPrint' style='color:darkgreen;'>{title}</h1>
                    <h3 class='TitleFontPrint' style='color:darkgreen;'>{date}</h3>
                </div>
            </div>
        </div>
                 """.format(
            head_tag=self.get_html_head(title=self.title),
            title=self.title,
            date=self.date,
        )
        self.html += self.banner_html

    def build_banner_left(self):
        # NOTE: {{ }} are the ESCAPED curly braces
        # JBR suggests rename method to start_html_doc()
        # This method violates DRY, if the ID of the body/div#BannerBack/div element is actually necessary
        # to specify, this needs to be made a parameter for build_banner() or start_html_doc()
        self.banner_html = """<!DOCTYPE html>
<html lang='en'>
    {head_tag}
    <body>
        <div id='BannerBack'>
            <div id='BannerLeft'>
                <br/>
                <img id='BannerLogo' align='right' src="CandelaLogo2-90dpi-200x90-trans.png" border='0'/>
                <div class='HeaderStyle'>
                    <br>
                    <h1 class='TitleFontPrint' style='color:darkgreen;'>{title}</h1>
                    <h3 class='TitleFontPrint' style='color:darkgreen;'>{date}</h3>
                </div>
            </div>
        </div>
                 """.format(
            head_tag=self.get_html_head(title=self.title),
            title=self.title,
            date=self.date,
        )
        self.html += self.banner_html

    def build_table_title(self):
        self.table_title_html = """
                    <!-- Table Title-->
                    <h3 align='left'>{title}</h3> 
                    """.format(title=self.table_title)
        self.html += self.table_title_html

    def start_content_div2(self):
        self.html += "\n<div class='contentDiv2'>\n"

    def start_content_div(self):
        self.html += "\n<div class='contentDiv'>\n"

    def build_text(self):
        # please do not use 'style=' tags unless you cannot override a class
        self.text_html = """
        <div class='HeaderStyle'>
            <h3 class='TitleFontPrint'>{text}</h3>\n
        </div>""".format(text=self.text)
        self.html += self.text_html

    def build_date_time(self):
        self.date_time = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-h-%m-m-%S-s")).replace(':', '-')
        return self.date_time

    def build_path_date_time(self):
        try:
            self.path_date_time = os.path.join(self.path, self.date_time)
            os.mkdir(self.path_date_time)
        except:
            curr_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.path_date_time = os.path.join(curr_dir_path, self.date_time)
            os.mkdir(self.path_date_time)

    def build_table(self):
        self.dataframe_html = self.dataframe.to_html(index=False,
                                                     justify='center')  # have the index be able to be passed in.
        self.html += self.dataframe_html

    def test_setup_table(self, test_setup_data, value):
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
                                  <td>""" + str(value) + """</td>
                                  <td>
                                    <table width='100%' border='0' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                                      """ + var + """
                                    </table>
                                  </td>
                                </tr>
                            </table>

                            <br>
                            """
        self.html += setup_information

    def build_footer(self):
        self.footer_html = """
    <footer class='FooterStyle'>
        <a href="https://www.candelatech.com/"><img 
            id='BannerLogoFooter' align='right' src="candela_swirl_small-72h.png" border='0'/></a>
        <p>Generated by Candela Technologies LANforge network testing tool</p>
        <p><a href="https://www.candelatech.com">www.candelatech.com</a><p>
    </footer>
        """
        self.html += self.footer_html

    def build_footer_no_png(self):
        self.footer_html = """
    <footer class='FooterStyle'>
        <p>Generate by Candela Technologies LANforge network testing tool</p>
        <p><a href="https://www.candelatech.com">www.candelatech.com</a><p>
    </footer>"""
        self.html += self.footer_html

    def copy_js(self):
        self.html += """
<script>
function fallbackCopyTextToClipboard(text) {
  var textArea = document.createElement("textarea");
  textArea.value = text;
  
  // Avoid scrolling to bottom
  textArea.style.top = "0";
  textArea.style.left = "0";
  textArea.style.position = "fixed";

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    var successful = document.execCommand('copy');
    var msg = successful ? 'successful' : 'unsuccessful';
    console.log('Fallback: Copying text command was ' + msg);
  } catch (err) {
    console.error('Fallback: Oops, unable to copy', err);
  }
  document.body.removeChild(textArea);
}
function copyTextToClipboard(ele) {
  var text = ele.innerHTML || '';
  if (!navigator.clipboard) {
    fallbackCopyTextToClipboard(text);
    return;
  }
  navigator.clipboard.writeText(text).then(function() {
    console.log('Async: Copying to clipboard was successful!');
  }, function(err) {
    console.error('Async: Could not copy text: ', err);
  });
}
</script>
        """

    def build_custom(self):
        self.html += self.custom_html

    def build_objective(self):
        self.obj_html = """
            <!-- Test Objective -->
            <h3 align='left'>{title}</h3> 
            <p align='left' width='900'>{objective}</p>
            """.format(title=self.obj_title,
                       objective=self.objective)
        self.html += self.obj_html

    def build_graph_title(self):
        self.table_graph_html = """
            <div class='HeaderStyle'>
                <h2 class='TitleFontPrint' style='color:darkgreen;'>{title}</h2>
            """.format(title=self.graph_title)
        self.html += self.table_graph_html

    def build_graph(self):
        self.graph_html_obj = """
              <img align='center' style='padding:15px;margin:5px 5px 2em 5px;width:1000px;' src='{image}' border='1' />
            """.format(image=self.graph_image)
        self.html += self.graph_html_obj

    def end_content_div(self):
        self.html += "\n</div><!-- end contentDiv -->\n"


# Unit Test
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="lf_report.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="Reporting library Unit Test")
    parser.add_argument('--lfmgr', help='sample argument: where LANforge GUI is running', default='localhost')
    # the args parser is not really used , this is so the report is not generated when testing 
    # the imports with --help
    args = parser.parse_args()
    print("LANforge manager {lfmgr}".format(lfmgr=args.lfmgr))

    # Testing: generate data frame
    dataframe = pd.DataFrame({
        'product': ['CT521a-264-1ac-1n', 'CT521a-1ac-1ax', 'CT522-264-1ac2-1n', 'CT523c-2ac2-db-10g-cu',
                    'CT523c-3ac2-db-10g-cu', 'CT523c-8ax-ac10g-cu', 'CT523c-192-2ac2-1ac-10g'],
        'radios': [1, 1, 2, 2, 6, 9, 3],
        'MIMO': ['N', 'N', 'N', 'Y', 'Y', 'Y', 'Y'],
        'stations': [200, 64, 200, 128, 384, 72, 192],
        'mbps': [300, 300, 300, 10000, 10000, 10000, 10000]
    })

    print(dataframe)

    # Testing: generate data frame 
    dataframe2 = pd.DataFrame({
        'station': [1, 2, 3, 4, 5, 6, 7],
        'time_seconds': [23, 78, 22, 19, 45, 22, 25]
    })

    report = lf_report()
    report.set_title("Banner Title One")
    report.build_banner()

    report.set_table_title("Title One")
    report.build_table_title()

    report.set_table_dataframe(dataframe)
    report.build_table()

    report.set_table_title("Title Two")
    report.build_table_title()

    report.set_table_dataframe(dataframe2)
    report.build_table()

    # report.build_all()
    # report.build_footer()
    report.build_footer_no_png()

    html_file = report.write_html()
    print("returned file ")
    print(html_file)
    report.write_pdf()

    print("report path {}".format(report.get_path()))
