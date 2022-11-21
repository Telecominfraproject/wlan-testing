Potential polling method for CICD integration.

* Polling should decrease network security head-aches such as setting
  up VPN access for all test beds.

***

Implementation:

* Web server accessible to all CICD test beds runs a 'test orchestrator' logic, henceforth TO
  *  This TO will periodically query jfrog for latest openwrt builds (see jfrog.pl)
  *  If new build is found, a work-item file containing pertinent info, including the HW platform
     will be created, example:

CICD_TYPE=fast
CICD_RPT_NAME=ea8300
CICD_RPT_DIR=greearb@192.168.100.195:/var/www/html/myco/testbeds//ferndale-basic-01/reports
CICD_HW=ea8300
CICD_FILEDATE=
CICD_GITHASH=
CICD_URL=https://myco.jfrog.io/artifactory/wlan-ap-firmware/
CICD_FILE_NAME=ea8300
CICD_URL_DATE=24-Apr-2020 16:32 

  *  TO has manually configured list of test-beds, with some info about each test
     bed, including the DUT HW platform and testing capabilities.
  *  It picks a test bed that matches the new build HW.
  *  That test bed will have a URL directory for it and it alone.
  *  The TO writes a new test configuration file into this directory.
     The test configuration file will have the info above, and also have other
     info including the tests to run and where to upload results when complete.
  *  TO looks for any completed results, and removes the work-item if result is found.
  *  TO will re-calculate historical charts and publish those if new results are found for a testbed.
     It could generate email and/or poke the results into testrails or similar at this point.
  *  TO should run periodically every 1 minute or so to check on progress.


* Test bed polling:
  *  The test-bed (hence forth TB) will poll its directory on the TO web server to look for new jobs.
  *  When new job is found, the TB will download the test config file, and use scp to upload a file
     to the TO to indicate it is working on the test.
  *  When test is complete, TB will upload results to TO server.  TO now knows test bed is available
     for more jobs.
  *  TB should pause for 2 minutes after uploading results to make sure TO notices the new results and
     removes the old work item so that TB does not re-test the same work item.



*************   Installation / Usage ***************

The jfrog.pl runs on the web server.  This is the Test Orchestrator.
Create a directory structure looking similar to this:

[greearb@ben-dt4 html]$ find myco -name "*" -print
myco
myco/testbeds
myco/testbeds/ferndale-basic-01
myco/testbeds/ferndale-basic-01/pending_work
myco/testbeds/ferndale-basic-01/reports

Copy the TESTBED_INFO from testbeds directory to the myco/testbeds directory:

[greearb@ben-dt4 testbeds]$ pwd
/var/www/html/myco/testbeds
cp -ar /home/greearb/git/lanforge-scripts/gui/cicd/ferndale-basic-01/ ./


Run the jfrog.pl script from the myco/testbeds directory:

/home/greearb/git/lanforge-scripts/gui/cicd/cicd/jfrog.pl --passwd secret --tb_url_base greearb@192.168.100.195:/var/www/html/myco/testbeds/

A work-item file will be created as needed, in my case, it is here:

[greearb@ben-dt4 testbeds]$ cat ferndale-basic-01/pending_work/fast/CICD_TEST-ea8300
CICD_TEST=fast
CICD_RPT_DIR=greearb@192.168.100.195:/var/www/html/myco/testbeds//ferndale-basic-01/reports/fast
CICD_RPT_NAME=ea8300
CICD_HW=ea8300
CICD_FILEDATE=
CICD_GITHASH=
CICD_URL=https://myco.jfrog.io/artifactory/wlan-ap-firmware/
CICD_FILE_NAME=ea8300
CICD_URL_DATE=24-Apr-2020 16:32 



************  Installation / Usage on Test Controller **************

# This runs on the test controller or Jump-Box.

# Set up OS
sudo needs to work w/out password.

sudo chmod a+rwx /dev/ttyUSB*
sudo pip3 install pexpect-serial

Run testbed_poll.pl from the cicd testbed directory:

The 192.168.100.195 system is the jfrog / Orchestrator machine.  The jfrog
password is so that it can download the OpenWrt binary file from jfrog.

cd ~/git/lanforge-scripts/gui/cicd/ferndale-basic-01

../testbed_poll.pl --jfrog_passwd secret --url http://192.168.100.195/myco/testbeds/testbed-ferndale-01/pending_work/
