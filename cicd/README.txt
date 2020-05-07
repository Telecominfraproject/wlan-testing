Potential polling method for CICD integration.

* Polling should decrease network security head-aches such as setting
  up VPN access for all test beds.

***

Implementation:

* Web server accessible to all CICD test beds runs a 'test orchestrator' logic, henceforth TO
  *  This TO will periodically query jfrog for latest openwrt builds (see jfrog.pl)
  *  If new build is found, a text file containing pertinent info, including the HW platform
     will be created, example:

CICD_URL=https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/
CICD_FILE_NAME=ea8300-2020-04-24-046ab4f.tar.gz
CICD_URL_DATE=24-Apr-2020 18:28 
CICD_HW=ea8300
CICD_FILEDATE=2020-04-24
CICD_GITHASH=046ab4f

  *  TO has manually configured list of test-beds, with some info about each test
     bed, including the DUT HW platform and testing capabilities.
  *  It picks a test bed that matches the new build HW.
  *  That test bed will have a URL directory for it and it alone.
  *  The TO writes a new test configuration file into this directory.
     The test configuration file will have the info above, and also have other
     info including the tests to run and where to upload results when complete.


* Test bed polling:
  *  The test-bed (hence forth TB) will poll its directory on the TO web server to look for new jobs.
  *  When new job is found, the TB will download the test config file, and use scp to upload a file
     to the TO to indicate it is working on the test.
  *  When test is complete, TB will upload results to TO server.  TO now knows test bed is available
     for more jobs.

* TO Polls periodically for results from test-beds, and when found it will re-generate historical
  graphs and reports.  If feasible, it could also email or otherwise notifiy whoever is interested in
  these results.  It could poke the results into testrails or similar at this point.


* If we can implement something like CTF, then it could cause the test config files to be placed into
  the test-bed directory, potentially with URLs pointing to user-specified locations for testing private
  builds.





*************   Installation / Usage ***************

The jfrog.pl runs on the web server.  Create a directory structure looking similar to this:

[greearb@ben-dt4 html]$ find tip -name "*" -print
tip
tip/testbeds
tip/testbeds/ferndale-basic-01
tip/testbeds/ferndale-basic-01/pending_work
tip/testbeds/ferndale-basic-01/reports

Copy the TESTBED_INFO from wlan-testing git to the tip/testbeds directory:

[greearb@ben-dt4 testbeds]$ pwd
/var/www/html/tip/testbeds
cp -ar /home/greearb/git/tip/wlan-testing/cicd/ferndale-basic-01/ ./


Run the jfrog.pl script from the tip/testbeds directory:

/ome/greearb/git/tip/wlan-testing/cicd/jfrog.pl --passwd secret --tb_url_base greearb@192.168.100.195:/var/www/html/tip/testbeds/

A work-item file will be created as needed, in my case, it is here:

[greearb@ben-dt4 testbeds]$ cat ferndale-basic-01/pending_work/CICD_TEST-ea8300
CICD_RPT=greearb@192.168.100.195:/var/www/html/tip/testbeds//ferndale-basic-01/reports/ea8300
CICD_HW=ea8300
CICD_FILEDATE=
CICD_GITHASH=
CICD_URL=https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/
CICD_FILE_NAME=ea8300
CICD_URL_DATE=24-Apr-2020 16:32 



************  Installation / Usage on Test Controller **************

# Set up OS
sudo chmod a+rwx /dev/ttyUSB*
sudo pip3 install pexpect-serial

Run testbed_poll.pl from the cicd testbed directory:

cd ~/tip/wlan-testing/cicd/ferndale-basic-01

../testbed_poll.pl --jfrog_passwd secret --url http://192.168.100.195/tip/testbeds/testbed-ferndale-01/pending_work/
