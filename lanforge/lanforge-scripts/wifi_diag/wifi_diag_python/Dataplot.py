import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os
import datetime

time = (datetime.datetime.now().time())
name = "WIFI_Diag"
name += str(time)
name += "/"

name = name.replace(":","_")
if not os.path.exists(str(name)):
    os.makedirs(str(name))


class Plot:
    def __init__(self):
        # print("In Plot")
        pass

    def bar(self, datax="", datay=" ", title="Temp", xaxis="yaxis", yaxis="xaxis",figname="temp"):
        # fig = plt.figure()
        self.tmpfile = BytesIO()

        plt.xlabel(xaxis)
        plt.ylabel(yaxis)

        plt.title(title)
        plt.xticks(rotation=90)
        plt.rc('xtick', labelsize=8)
        plt.rc('ytick', labelsize=8)
        plt.bar(datax, datay)
        path =  plt.savefig(str(name)+str(figname)+".png",bbox_inches='tight')
        # plt.savefig(str(title)+".png")
        plt.savefig(self.tmpfile, format='png')
        self.encoded = base64.b64encode(self.tmpfile.getvalue()).decode('utf-8')
        # print("self.encoded",path)
        plt.clf()
        return str(name)+str(figname)+".png"


