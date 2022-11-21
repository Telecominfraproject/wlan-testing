#!/usr/bin/perl

# Query test-bed orchestator URL to see if there are new tests for us to run.
# This is expected to be run on the test-bed controller (not orchestrator)
# One of these processes will run for each test bed controlled by the controller.

use strict;
use warnings;
use Getopt::Long;

my $user = "";
my $passwd = "";
my $jfrog_user = "cicd_user";
my $jfrog_passwd = "";
my $url = "";
my $next_info = "__next_test.txt";
my $help = 0;
my $owt_log = "";
my $log = "";

my $usage = qq($0
  [--jfrog_user { jfrog user (default: cicd_user) }
  [--jfrog_passwd { jfrog password }
  [--user { for accessing URL }
  [--passwd { for accessing URL }
  [--url { test-orchestrator URL for this test bed }
  [--next_info { output text file containing info about the next test to process }
  [--log {location}   For instance: --log stdout, for openwrt_ctl expect script.

Example:
$0 --user to_user --passwd secret --jfrog_user myco-read --jfrog_passwd myco-read \\
   --url https://myco.cicd.mycloud.com/testbed-ferndale-01/

# Use specific scenario file.
SCENARIO_CFG_FILE=/home/lanforge/git/wlan-testing/testbeds/ferndale-basic-01/scenario_small.txt \\
  ../testbed_poll.pl --jfrog_passwd myco-read --jfrog_user myco-read \\
  --url http://192.168.100.195/myco/testbeds/ferndale-basic-01/pending_work/

);

GetOptions
(
  'jfrog_user=s'           => \$jfrog_user,
  'jfrog_passwd=s'         => \$jfrog_passwd,
  'user=s'                 => \$user,
  'passwd=s'               => \$passwd,
  'url=s'                  => \$url,
  'next_info=s'            => \$next_info,
  'log=s'                  => \$log,
  'help|?'                 => \$help,
) || (print($usage) && exit(1));

if ($help) {
  print($usage) && exit(0);
}

if ($jfrog_passwd eq "") {
   print("ERROR:  You must specify jfrog password.\n");
   exit(1);
}

if ($user ne "" && $passwd eq "") {
   print("ERROR:  You must specify a password if specifying a user.\n");
   exit(1);
}

if ($log ne "") {
   $owt_log = "--log $log";
}

my $i;

my $cuser = "-u $user:$passwd";
if ($user eq "") {
   $cuser = "";
}

my $cmd = "curl $cuser $url";

print_note("Checking Test-Orchestrator for new work-items");
my $listing = do_system($cmd);
my @lines = split(/\n/, $listing);

# First, if any have 'fast' in them, they get precedence.
for ($i = 0; $i<@lines; $i++) {
   my $ln = $lines[$i];
   chomp($ln);
   my $fast = 0;
   if ($ln =~ /href=\"(CICD_TEST-.*-fast)\">(.*)<\/a>\s+(.*)\s+\S+\s+\S+/) {
      $fast = 1;
   }
   elsif ($ln =~ /href=\"(CICD_TEST-.*-fast)\">(.*)<\/a>/) {
      $fast = 1;
   }
   if ($fast) {
      @lines[0] = $ln;
      last;
   }
}

for ($i = 0; $i<@lines; $i++) {
   my $ln = $lines[$i];
   chomp($ln);

   my $fname = "";
   my $name = "";
   my $date = "";

   if ($ln =~ /href=\"(CICD_TEST-.*)\">(.*)<\/a>\s+(.*)\s+\S+\s+\S+/) {
      $fname = $1;
      $name = $2;
      $date = $3;
   }
   elsif ($ln =~ /href=\"(CICD_TEST-.*)\">(.*)<\/a>/) {
      $fname = $1;
   }

   if ($fname ne "") {
      # Grab that test file
      $cmd = "curl --location $cuser -o $next_info $url/$fname";
      do_system($cmd);

      # Read in that file
      my $jurl = "";
      my $jfile = "";
      my $report_to = "";
      my $report_name = "";
      my $swver = "";
      my $fdate = "";
      my $ttype = "";
      my $listing = do_system("cat $next_info");
      my @lines = split(/\n/, $listing);
      for ($i = 0; $i<@lines; $i++) {
         my $ln = $lines[$i];
         chomp($ln);
         if ($ln =~ /^CICD_URL=(.*)/) {
            $jurl = $1;
         }
         elsif ($ln =~ /^CICD_TYPE=(.*)/) {
            $ttype = $1;
         }
         elsif ($ln =~ /^CICD_FILE_NAME=(.*)/) {
            $jfile = $1;
         }
         elsif ($ln =~ /^CICD_RPT_DIR=(.*)/) {
            $report_to = $1;
         }
         elsif ($ln =~ /^CICD_RPT_NAME=(.*)/) {
            $report_name = $1;
         }
         elsif ($ln =~ /^CICD_GITHASH=(.*)/) {
            $swver = $1;
         }
         elsif ($ln =~ /^CICD_FILEDATE=(.*)/) {
            $fdate = $1;
         }
      }

      if ($swver eq "") {
         $swver = $fdate;
      }

      if ($swver eq "") {
         $swver = "$jfile";
      }

      if ($jurl eq "") {
         print("ERROR: No CICD_URL found, cannot download file.\n");
         exit(1);
      }
      if ($jfile eq "") {
         print("ERROR: No CICD_FILE_NAME found, cannot download file.\n");
         exit(1);
      }

      # Refresh wlan-ap repo if it exists.
      if ( -d "../../../wlan-ap") {
         do_system("cd ../../../wlan-ap && git pull && cd -");
      }

      print_note("Download latest AP Build from jfrog repository.");
      my $cmd = "curl --location -o $jfile -u $jfrog_user:$jfrog_passwd $jurl/$jfile";
      do_system($cmd);

      do_system("rm -f openwrt-*.bin");
      do_system("rm -f *sysupgrade.bin"); # just in case openwrt prefix changes.
      do_system("tar xf $jfile");

      print_note("Copy AP build to LANforge so LANforge can serve the file to AP");
      # Next steps here are to put the OpenWrt file on the LANforge system
      my $tb_info = do_system("cat TESTBED_INFO.txt");
      my $tb_dir = "";
      if ($tb_info =~ /TESTBED_DIR=(.*)/) {
         $tb_dir = $1;
      }

      my $env = do_system(". $tb_dir/test_bed_cfg.bash && env");
      my $lfmgr = "";
      my $serial = "";
      my $cloud_sdk = "";

      if ($env =~ /LFMANAGER=(.*)/) {
         $lfmgr = $1;
      }
      else {
         print("ERRROR:  Could not find LFMANAGER in environment, configuration error!\n");
         print("env: $env\n");
         exit(1);
      }

      if ($env =~ /USE_CLOUD_SDK=(\S+)/) {
         $cloud_sdk = $1;
         print("NOTE:  Using cloud controller: $cloud_sdk\n");
      }
      else {
         print("NOTE:  NOT Using cloud controller\n");
      }
      #print("env: $env");
      #exit(0);

      if ($env =~ /AP_SERIAL=(.*)/) {
         $serial = $1;
      }
      else {
         print("ERRROR:  Could not find AP_SERIAL in environment, configuration error!\n");
         exit(1);
      }

      my $gmport = "3990";
      my $gmanager = $lfmgr;
      my $scenario = "myco-auto";  # matches basic_regression.bash

      if ($env =~ /GMANAGER=(.*)/) {
         $gmanager = $1;
      }
      if ($env =~ /GMPORT=(.*)/) {
         $gmport = $1;
      }

      print_note("Restart LANforge GUI to be sure it is in known state.");
      # Restart the GUI on the LANforge system
      do_system("ssh lanforge\@$lfmgr pkill -f \"miglayout.*8080\"");

      # and then get it onto the DUT, reboot DUT, re-configure as needed,
      print_note("Request AP DUT to install the test image.");
      do_system("scp *sysupgrade.bin lanforge\@$lfmgr:myco-$jfile");


      # TODO:  Kill anything using the serial port
      do_system("sudo lsof -t $serial | sudo xargs --no-run-if-empty kill -9");

      print_note("Find AP DUT default gateway.");
      # and then kick off automated regression test.
      # Default gateway on the AP should be one of the ports on the LANforge system, so we can use
      # that to scp the file to the DUT, via serial-console connection this controller has to the DUT.
      my $ap_route = do_system("../../lanforge/lanforge-scripts/openwrt_ctl.py $owt_log --scheme serial --tty $serial --action cmd --value \"ip route show\"");
      my $ap_gw = "";
      if ($ap_route =~ /default via (\S+)/) {
         $ap_gw = $1;
      }
      if ($ap_gw eq "") {
         print("ERROR:  Could not find default gateway for AP, route info:\n$ap_route\n");
         if ($ap_route =~ /pexpect.exceptions.TIMEOUT/) {
            print("FATAL-ERROR:  DUT is in bad state, bail out.\n");
            exit(33);
         }
         # Re-apply scenario so the LANforge gateway/NAT is enabled for sure.
         my $out = do_system("../../lanforge/lanforge-scripts/lf_gui_cmd.pl --manager $gmanager --port $gmport --scenario $scenario");
         # TODO:  Use power-controller to reboot the AP and retry.
         if ($out =~ /pexpect.exceptions.TIMEOUT/) {
            print("FATAL-ERROR:  DUT is in bad state, bail out.\n");
            exit(34);
         }

         $out = do_system("../../lanforge/lanforge-scripts/openwrt_ctl.py $owt_log --scheme serial --tty $serial --action reboot");
         print ("Reboot DUT to try to recover networking:\n$out\n");
         if ($out =~ /pexpect.exceptions.TIMEOUT/) {
            print("FATAL-ERROR:  DUT is in bad state, bail out.\n");
            exit(35);
         }
         sleep(15);

         $ap_route = do_system("../../lanforge/lanforge-scripts/openwrt_ctl.py $owt_log --scheme serial --tty $serial --action cmd --value \"ip route show\"");
         if ($ap_route =~ /default via (\S+)/g) {
            $ap_gw = $1;
         }
         if ($ap_route =~ /pexpect.exceptions.TIMEOUT/) {
            print("FATAL-ERROR:  DUT is in bad state, bail out.\n");
            exit(36);
         }
         if ($ap_gw eq "") {
            exit(1);
         }
      }

      print_note("Request AP DUT to install the test image and reboot.");
      # TODO: Change this to curl download??
      my $ap_out = do_system("../../lanforge/lanforge-scripts/openwrt_ctl.py $owt_log --scheme serial --tty $serial --action sysupgrade --value \"lanforge\@$ap_gw:myco-$jfile\"");
      print ("Sys-upgrade results:\n$ap_out\n");
      if ($ap_out =~ /pexpect.exceptions.TIMEOUT/) {
         print("FATAL-ERROR:  DUT is in bad state, bail out.\n");
         exit(37);
      }
      # TODO:  Verify this (and reboot below) worked.  DUT can get wedged and in that case it will need
      # a power-cycle to continue.

      # System should be rebooted at this point.
      sleep(10); # Give it some more time

      if ($cloud_sdk eq "") {
         print_note("Initialize AP, disable OpenVsync since this is stand-alone testbed.");
         # Disable openvsync, it will re-write /etc/config/wireless
         # This code should not be used when we get cloud-sdk wired up.
         $ap_out = do_system("../../lanforge/lanforge-scripts/openwrt_ctl.py $owt_log --scheme serial --tty $serial --action cmd --value \"service opensync stop\"");
         print ("Stop openvsync:\n$ap_out\n");
         if ($ap_out =~ /pexpect.exceptions.TIMEOUT/) {
            print("FATAL-ERROR:  DUT is in bad state, bail out.\n");
            exit(38);
         }
         $ap_out = do_system("../../lanforge/lanforge-scripts/openwrt_ctl.py $owt_log --scheme serial --tty $serial --action cmd --value \"service opensync disable\"");
         print ("Disable openvsync:\n$ap_out\n");
         if ($ap_out =~ /pexpect.exceptions.TIMEOUT/) {
            print("FATAL-ERROR:  DUT is in bad state, bail out.\n");
            exit(39);
         }
      }
      else {
         print_note("Initialize AP, enable OpenVsync since this testbed is using Cloud-Controler: $cloud_sdk.");
         $ap_out = do_system("../../lanforge/lanforge-scripts/openwrt_ctl.py $owt_log --scheme serial --tty $serial --action cmd --value \"service opensync enable\"");
         print ("Enable openvsync:\n$ap_out\n");
         if ($ap_out =~ /pexpect.exceptions.TIMEOUT/) {
            print("FATAL-ERROR:  DUT is in bad state, bail out.\n");
            exit(40);
         }
      }

      # Re-apply overlay
      print_note("Apply default AP configuration for this test bed.");
      if ($cloud_sdk eq "") {
         $ap_out = do_system("cd $tb_dir/OpenWrt-overlay && tar -cvzf ../overlay_tmp.tar.gz * && scp ../overlay_tmp.tar.gz lanforge\@$lfmgr:myco-overlay.tar.gz");
      }
      else {
         # Create /etc/hosts file that points us towards correct cloud-sdk machine
         my $etc_hosts = "$tb_dir/OpenWrt-overlay/etc/hosts";
         open(FILE, ">", "$etc_hosts");
         print FILE "# Auto-Created by CICD process
127.0.0.1 localhost

::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
$cloud_sdk opensync-mqtt-broker
$cloud_sdk opensync-wifi-controller
$cloud_sdk opensync.zone1.art2wave.com
";

         # Leave 'wireless' out of the overlay since opensync will be designed to work with default config.
         $ap_out = do_system("cd $tb_dir/OpenWrt-overlay && tar -cvzf ../overlay_tmp.tar.gz --exclude etc/config/wireless * && scp ../overlay_tmp.tar.gz lanforge\@$lfmgr:myco-overlay.tar.gz");
         unlink($etc_hosts);
      }

      print ("Create overlay zip:\n$ap_out\n");

      for (my $q = 0; $q<10; $q++) {
         $ap_out = do_system("../../lanforge/lanforge-scripts/openwrt_ctl.py $owt_log --scheme serial --tty $serial --action download --value \"lanforge\@$ap_gw:myco-overlay.tar.gz\" --value2 \"overlay.tgz\"");
         print ("Download overlay to DUT:\n$ap_out\n");
         if ($ap_out =~ /ERROR:  Could not connect to LANforge/g) {
            # Try to restart the network
            $ap_out = do_system("../../lanforge/lanforge-scripts/openwrt_ctl.py $owt_log --scheme serial --tty $serial --action cmd --value \"/etc/init.d/network restart\"");
            print ("Request restart of DUT networking:\n$ap_out\n");
            if ($q == 9) {
               # We have failed to apply overlay at this point, bail out.
               print("ERROR:  Could not apply overlay to DUT, exiting test attempt.\n");
               exit(1);
            }
            print("Will retry overlay download in 10 seconds, try $q / 10\n");
            sleep(10);
         }
         else {
            last;
         }
      }
      $ap_out = do_system("../../lanforge/lanforge-scripts/openwrt_ctl.py $owt_log --scheme serial --tty $serial --action cmd --value \"cd / && tar -xzf /tmp/overlay.tgz\"");
      print ("Un-zip overlay on DUT:\n$ap_out\n");
      if ($ap_out =~ /pexpect.exceptions.TIMEOUT/) {
         print("FATAL-ERROR:  DUT is in bad state, bail out.\n");
         exit(41);
      }

      print_note("Reboot AP so that new configuration is applied.");
      $ap_out = do_system("../../lanforge/lanforge-scripts/openwrt_ctl.py $owt_log --scheme serial --tty $serial --action reboot");
      print ("Rebooted DUT so overlay takes effect:\n$ap_out\n");
      if ($ap_out =~ /pexpect.exceptions.TIMEOUT/) {
         print("FATAL-ERROR:  DUT is in bad state, bail out.\n");
         exit(42);
      }

      if ($ttype eq "fast") {
         print_note("Start 'Fast' LANforge regression test.");
         $ap_out = do_system("cd $tb_dir && DUT_SW_VER=$swver ./run_basic_fast.bash");
      }
      else {
         print_note("Start 'Fast' LANforge regression test.");
         $ap_out = do_system("cd $tb_dir && DUT_SW_VER=$swver ./run_basic.bash");
      }
      print("Regression $ttype test script output:\n$ap_out\n");

      print_note("Upload results.");

      #When complete, upload the results to the requested location.
      if ($ap_out =~ /Results-Dir: (.*)/) {
         my $rslts_dir = $1;
         if ($rslts_dir =~ /(.*)\'/) {
            $rslts_dir = $1;
         }
         print ("Found results at: $rslts_dir\n");
         do_system("rm -fr /tmp/$report_name");
         do_system("mv $rslts_dir /tmp/$report_name");
         do_system("scp -C -r /tmp/$report_name $report_to/");
         do_system("echo $fname > /tmp/NEW_RESULTS-$fname");
         do_system("scp /tmp/NEW_RESULTS-$fname $report_to/");

         # This will indirectly stop logread if it is running.
         $ap_out = do_system("../../lanforge/lanforge-scripts/openwrt_ctl.py $owt_log --scheme serial --tty $serial --action cmd --value \"uptime\"");
         if ($ap_out =~ /pexpect.exceptions.TIMEOUT/) {
            print("FATAL-ERROR:  DUT is in bad state, bail out.\n");
            exit(43);
         }
      }

      exit(0);
   }

   #print "$ln\n";
}

exit 0;

sub do_system {
   my $cmd = shift;
   print ">>> $cmd\n";
   return `$cmd 2>&1`;
}

sub print_note {
   my $n = shift;
   my $hdr = "###############################################################";
   print "\n\n\n$hdr\n### $n\n$hdr\n\n";
}
