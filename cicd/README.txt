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





