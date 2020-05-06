#!/usr/bin/perl

# Query jfrog URL and get list of builds.
# This will be run on the test-bed orchestrator
# Run this in directory that contains the testbed_$hw/ directories

use strict;
use warnings;
use Getopt::Long;

my $user = "cicd_user";
my $passwd = "";
my $url = "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/";
my $files_processed = "jfrog_files_processed.txt";
my $tb_url_base = "cicd_user\@tip.cicd.cloud.com/testbeds";  # Used by SSH: scp -R results_dir cicd_user@tip.cicd.cloud.com/testbeds/
my $help = 0;
my $cicd_prefix = "CICD_TEST";

my $usage = qq($0
  [--user { jfrog user (default: cicd_user) }
  [--passwd { jfrog password }
  [--url { jfrog URL, default is OpenWrt URL: https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/ }
  [--files_processed { text file containing file names we have already processed }
  [--tb_url_base { Where to report the test results? }

Example:
$0 --user cicd_user --passwd secret --url https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/ \
   --files_processed jfrog_files_processed.txt \
   --tb_url_base cicd_user\@tip.cicd.cloud.com/testbeds

);

GetOptions
(
  'user=s'                 => \$user,
  'passwd=s'               => \$passwd,
  'url=s'                  => \$url,
  'files_processed=s'      => \$files_processed,
  'tb_url_base=s'          => \$tb_url_base,
  'help|?'                 => \$help,
) || (print($usage) && exit(1));

if ($help) {
  print($usage) && exit(0);
}

if ($passwd eq "") {
   print("ERROR:  You must specify jfrog password.\n");
   exit(1);
}

my $i;

#Read in already_processed builds
my @processed = ();
my $listing = `cat $files_processed`;
my @lines = split(/\n/, $listing);
for ($i = 0; $i<@lines; $i++) {
   my $ln = $lines[$i];
   chomp($ln);
   print("Skipping, already processed: $ln\n");
   push(@processed, $ln);
}

my $cmd = "curl -u $user:$passwd $url";
print ("Calling command: $cmd\n");
$listing = `$cmd`;
@lines = split(/\n/, $listing);
for ($i = 0; $i<@lines; $i++) {
   my $ln = $lines[$i];
   chomp($ln);

   if ($ln =~ /href=\"(.*)\">(.*)<\/a>\s+(.*)\s+\S+\s+\S+/) {
      my $fname = $1;
      my $name = $2;
      my $date = $3;

      if ( grep( /^$fname\s+/, @processed ) ) {
         # Skip this one, already processed.
         next;
      }

      my $hw = "";
      my $fdate = "";
      my $githash = "";

      if ($fname =~ /^(\S+)-(\d\d\d\d-\d\d-\d\d)-(\S+).tar.gz/) {
         $hw = $1;
         $fdate = $2;
         $githash = $3;
      }
      else {
         print "ERROR:  Un-handled filename syntax: $fname\n";
         exit(1);
      }

      # Find the least used testbed for this hardware.
      my $dirs = `ls`;
      my @dira = split(/\n/, $dirs);
      my $best_tb = "";
      my $best_backlog = 0;
      my $di;
      for ($di = 0; $di<@dira; $di++) {
         my $dname = $dira[$di];
         chomp($dname);
         if (! -d $dname) {
            next;
         }
         if (! -f "$dname/TESTBED_INFO.txt") {
            next;
         }
         my $tb_info = `cat $dname/TESTBED_INFO.txt`;
         my $tb_hw_type = "";
         if ($tb_info =~ /TESTBED_HW=(.*)/g) {
            $tb_hw_type = $1;
         }
         if ($tb_hw_type ne $hw) {
            print "Skipping test bed $dname, jfrog hardware type: -:$hw:-  testbed hardware type: -:$tb_hw_type:-";
            next;
         }
         print "Checking testbed $dname backlog..\n";
         my $bklog = `ls $dname/$cicd_prefix-*`;
         my $bklog_count = split(/\n/, $bklog);
         if ($best_tb eq "") {
            $best_tb = $dname;
            $best_backlog = $bklog_count;
         }
         else {
            if ($best_backlog > $bklog_count) {
               $best_tb = $dname;
               $best_backlog = $bklog_count;
            }
         }
      }

      if ($best_tb eq "") {
         print "ERROR:  No test bed found for hardware type: $hw\n";
         exit(1);
      }

      my $fname_nogz = $fname;
      if ($fname =~ /(.*)\.tar\.gz/) {
         $fname_nogz = $1;
      }

      open(FILE, ">", "$best_tb/$cicd_prefix-$fname_nogz");

      system("mkdir -p $best_tb/reports");

      # In case we run different types of tests, report dir would need to be unique per test run
      print FILE "CICD_RPT=$tb_url_base/$best_tb/reports/fname_nogz\n";

      print FILE "CICD_HW=$hw\nCICD_FILEDATE=$fdate\nCICD_GITHASH=$githash\n";
      print FILE "CICD_URL=$url\nCICD_FILE_NAME=$fname\nCICD_URL_DATE=$date\n";

      close(FILE);

      print("Next: File Name: $fname  Display Name: $name  Date: $date\n");
      print("To download: curl --location -o /tmp/$fname -u $user:$passwd $url/$fname\n");
      exit(0);
   }

   #print "$ln\n";
}

exit 0;
