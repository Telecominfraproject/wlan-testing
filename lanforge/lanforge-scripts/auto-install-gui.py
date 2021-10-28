#!/usr/bin/env python3
from html.parser import HTMLParser
import urllib.request
from html.entities import name2codepoint
import re
import datetime
import argparse
import os
import time
import glob
import sys
import subprocess


#===========ARGUMENT PARSING==============
parser = argparse.ArgumentParser()
parser.add_argument("--versionNumber", type=str, help="Specify version number to search for")

args = parser.parse_args()
if args.versionNumber != None:
	ver = args.versionNumber
else:
	parser.print_help()
	parser.exit()

#=============HTML PARSING================
url = "http://jed-centos7/pld/"
with urllib.request.urlopen(url) as response:
	html = response.read()

webpage = html.decode('utf-8')
#print(webpage)

searchPattern = '(LANforgeGUI_(\d+\.\d+\.\d+)_Linux64.tar.bz2)<\/a><\/td><td align="right">(\d+\-\d+\-\d+\ \d+\:\d+)'
searchResults = re.findall(searchPattern, webpage)

webFiles = []

for file in searchResults:
	if ver == file[1]:
		webFiles.append({'filename':file[0], 'timestamp': datetime.datetime.strptime(file[2], "%Y-%m-%d %H:%M")})
if len(webFiles) == 0:
	print("Failed to find webfile with version number %s" % (ver))
	sys.exit(1)


#=========CHECK DIR FOR FILES=============
filePath = "/home/lanforge/Downloads/"
dir = glob.glob(filePath + "LANforgeGUI_%s*" % ver)
dirFiles = []

for file in dir:
	if ver in file:
		fileTime = datetime.datetime.strptime(time.ctime(os.stat(file).st_ctime), "%a %b %d %H:%M:%S %Y") # Fri May  8 08:31:43 2020
		dirFiles.append({'filename':file[25:], 'timestamp':fileTime})

if len(dirFiles) == 0:
	print("Unable to find file in {filePath} with version %s" % ver)
	#sys.exit(1)

#============FIND NEWEST FILES============
def findNewestVersion(filesArray):
	newest = filesArray[0]
	if len(filesArray) > 0:
		for file in filesArray:
			if file['timestamp'] > newest['timestamp']:
				newest = file

	return newest

newestWebFile = findNewestVersion(webFiles)
if len(dirFiles) != 0:
	newestDirFile = findNewestVersion(dirFiles)
else:
	newestDirFile = {'filename':'placeholder', 'timestamp': datetime.datetime.strptime("0", "%H")}


#=======COMPARE WEB AND DIR FILES=========
if newestWebFile['timestamp'] > newestDirFile['timestamp']:
	try:
		if newestDirFile['filename'] != 'placeholder':
			subprocess.call(["rm", "%s%s" % (filePath, newestDirFile['filename'])])
			print("No file found")
			print("Downloading newest %s from %s" % (newestWebFile['filename'], url))
		else:
			print("Found newer version of GUI")
			print("Downloading %s from %s" % (newestWebFile['filename'], url))
#=====ATTEMPT DOWNLOAD AND INSTALL=========
		subprocess.call(["curl", "-o", "%s%s" % (filePath, newestWebFile['filename']), "%s%s" % (url, newestWebFile['filename'])])
		time.sleep(5)
	except Exception as e:
		print("%s Download failed. Please try again." % e)
		sys.exit(1)
	try:
		print("Attempting to extract files")
		subprocess.call(["tar", "-xf", "%s%s" % (filePath, newestWebFile['filename']), "-C", "/home/lanforge/"])
	except Exception as e:
		print("%s\nExtraction failed. Please try again" % e)
		sys.exit(1)

	#time.sleep(90)
	try:
		if "/home/lanforge/.config/autostart/LANforge-auto.desktop" not in glob.glob("/home/lanforge/.config/autostart/*"):
			print("Copying LANforge-auto.desktop to /home/lanforge/.config/autostart/")
			subprocess.call(["cp", "/home/lanforge/%s/LANforge-auto.desktop" % (newestWebFile['filename'][:len(newestWebFile)-18]), "/home/lanforge/.config/autostart/"])
	except Exception as e:
		print("%s\nCopy failed. Please try again" % e)
		sys.exit(1)

	try:
		print("Attempting to install %s at /home/lanforge" % newestWebFile['filename'])
		os.system("cd /home/lanforge/%s; sudo bash lfgui_install.bash" % (newestWebFile['filename'][:len(newestWebFile)-18]))
	except Exception as e:
		print("%s\nInstallation failed. Please Try again." % e)
		sys.exit(1)
#=========ATTEMPT TO RESTART GUI==========
#	try:
#		print("Killing current GUI process")
#		os.system("if pgrep java; then pgrep java | xargs kill -9 ;fi")
#	except Exception as e:
#		print("%s\nProcess kill failed. Please try again" % e)
#		sys.exit(1)

else:
	print("Current GUI version up to date")
	sys.exit(0)

