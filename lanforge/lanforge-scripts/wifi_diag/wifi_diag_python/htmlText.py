import datetime
import matplotlib.pyplot as plt
import base64
from io import BytesIO

html = open("wifi_diag.html", 'w')

def htmlstart():
    start = """<!DOCTYPE html> 
        <!-- This is for Banner --> 
        <body> 
        <title> WIFI Diag Report </title> <link rel='shortcut icon' href='canvil.ico' type='image/x-icon' /> 
        <link rel='stylesheet' href='report.css' /> 
        <link rel='stylesheet' href='custom.css' /> 
        <style> 
         pre {   
            overflow: auto; 
         } 
         img { 
            width: 100%; 
            max-width: 8in; 
         } 
        </style> 
        </head> 
        
        <div class='Section report_banner-1000x205' style='background-image:url("report_banner-1000x205.jpg");background-repeat:no-repeat;padding:0;margin:0;min-width:1000px; min-height:205px;width:1000px; height:205px;max-width:1000px; max-height:205px;'>
        <img align='right' style='padding:0;margin:5;width:200px;' src='CandelaLogo2-90dpi-200x90-trans.png' border='0' />
        <div class='HeaderStyle'>
        <h1 class='TitleFontPrint'>WIFI Diag Report</h1><br/><h3 class='TitleFontPrintSub'></h3><br><br/>
        <h4 class='TitleFontPrintSub'><br><br></br></br>"""
    html.write(start)
    html.write(str(datetime.datetime.now()))
    html.write("</h4></div></div></body>")


def downloadBtn():
    text =  """<tr><p align="right">
            <td><input class="btn" type="submit"  value="Print" name="Submit" id="printbtn" onclick="window.print()" /></td>
            </tr></p>"""
    html.write(text)

def htmlobj(text):
    html.write("<h2> Objecitve </h2>")
    html.write("<p>")
    html.write(str(text))
    html.write("</p>")

def htmlpointview():
    pointview = """
<!--For Point view -->
<meta name="viewport" content="width=device-width, initial-scale=1">\n
<style>\n
ul, #myUL {\n
  list-style-type: none;\n
}\n

#myUL {\n
  margin: 0;\n
  padding: 0;\n
}\n

.box {\n
  cursor: pointer;\n
  -webkit-user-select: none; /* Safari 3.1+ */\n
  -moz-user-select: none; /* Firefox 2+ */\n
  -ms-user-select: none; /* IE 10+ */\n
  user-select: none;\n
}\n

.box::before {\n
  content: "\\2610";\n
  color: black;\n
  display: inline-block;\n
  margin-right: 6px;\n
}\n

.check-box::before {\n
  content: "\\2611";\n
  color: dodgerblue;\n
}\n

.nested {\n
  display: none;\n
}\n

.active {\n
  display: block;\n
}\n

* {\n
  box-sizing: border-box;\n
}\n

.column {\n
  float: left;\n
  width: 100%;\n

}\n

.row::after {\n
  content: "";\n
  clear: both;\n
  display: table;\n
}\n

.borderexample {\n
 border-style:solid;\n
 border-color: hsl(0, 0%, 73%);\n
}\n
.btn {\n
  background-color: DodgerBlue;\n
  border: none;\n
  color: white;\n
  padding: 12px 30px;\n
  cursor: pointer;\n
  font-size: 20px;\n
}\n

/* Darker background on mouse-over */
.btn:hover {\n
  background-color: RoyalBlue;\n
}\n
</style>\n
</head>\n
"""
    html.write(str(pointview))

def htmlTableSummary(Summary):
    tableSummary = "<body><!-- This is heading and Summary --><h2> About: </h2> \n \
    <p>"+str(Summary)+"</p> \n"

    html.write(str(tableSummary))

def myUL():
    html.write("<ul id='myUL'> \n")


def htmlSpanBox(Table):
    tablespan = "<li><span class= 'box borderexample'>"+str(Table)+"</span> <ul class='nested'> \n"
    html.write(tablespan)

def htmlSpanBox1():
    tablespan = "<li><span class='box'> Table </span> <ul class='nested'> \n"
    html.write(tablespan)

def htmltable(Heading,data,image1,image2,image3,summary):
    # htmlBreak(1)
    htmlSpanBox(Heading)
    htmlTableSummary(str(summary)+"\n")
    # htmlSpanBox1()
    html.write("<li><span> ")
    html.write(str(data))
    html.write("</span></li> ")
    htmltableimage(image1,image2,image3)


def htmltableimage(image1, image2, image3):
    if image1 != "0":
        imagePre = "<div class='column'>  \
               <img style='padding:0;margin:3;width:450px;' src="
        html.write(imagePre)
        html.write(image1)
        imagepost = " border='0' /> \
            </div>"
        html.write(imagepost)

    if image2 != "0":
        imagePre = "<div class='column'> \
               <img style='padding:0;margin:3;width:450px;' src="
        html.write(imagePre)
        html.write(image2)
        imagepost = " border='0' /> \
            </div>\n"
        html.write(imagepost)

    if image3 != "0":
        imagePre = "<div class='column'> \
               <img style='padding:0;margin:3;width:450px;' src="
        html.write(imagePre)
        html.write(image2)
        imagepost = " border='0' /> \
            </div>"
        html.write(imagepost)

    html.write("</ul></ul></li><br>")


def closemyUl():
    html.write("</ul>\n")


def htmlclose():
    data = """    
        <script>\n
        var toggler = document.getElementsByClassName("box");\n
        var i;\n

        for (i = 0; i < toggler.length; i++) {\n
          toggler[i].addEventListener("click", function() {\n
            this.parentElement.querySelector(".nested").classList.toggle("active");\n
            this.classList.toggle("check-box");\n
          });\n
        }\n
        </script>

        </body>
        """
    html.write(data)

    html.write("</html>")


def htmlBreak(lines):
    for i in range(lines):
        html.write("<br></br>")


def htmlSpace(space):
    Space = """<style> 
        .tab1 { 
            tab-size:""" + str(space) + """; 
        } 
    </style>"""
    html.write(Space)

def htmlText(text):
    data = "<p>" + str(text) + "<p/>"
    html.write(data)



#htmlstart()
#htmlobjective()
#htmlpointview()
#htmlsummary()
#myUl
#htmlspanbox()
#htmltable
#closemyul()
#htmlclose()

