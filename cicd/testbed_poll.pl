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

my $usage = qq($0
  [--jfrog_user { jfrog user (default: cicd_user) }
  [--jfrog_passwd { jfrog password }
  [--user { for accessing URL }
  [--passwd { for accessing URL }
  [--url { test-orchestrator URL for this test bed }
  [--next_info { output text file containing info about the next test to process }

Example:
$0 --user to_user --passwd secret --jfrog_user cicd_user --jfrog_passwd secret2 \
   --url https://tip.cicd.mycloud.com/testbed-ferndale-01/ \
   --next_info jfrog_files_next.txt

);

GetOptions
(
  'jfrog_user=s'           => \$jfrog_user,
  'jfrog_passwd=s'         => \$jfrog_passwd,
  'user=s'                 => \$user,
  'passwd=s'               => \$passwd,
  'url=s'                  => \$url,
  'next_info=s'            => \$next_info,
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

my $i;

my $cuser = "-u $user:$passwd";
if ($user eq "") {
   $cuser = "";
}

my $cmd = "curl $cuser $url";

print ("Calling command: $cmd\n");
$listing = `$cmd`;
@lines = split(/\n/, $listing);
for ($i = 0; $i<@lines; $i++) {
   my $ln = $lines[$i];
   chomp($ln);

   if ($ln =~ /href=\"(CICD_TEST_.*)\">(.*)<\/a>\s+(.*)\s+\S+\s+\S+/) {
      my $fname = $1;
      my $name = $2;
      my $date = $3;

      # Grab that test file
      $cmd = "curl --location $cuser -o $next_info $url/$fname";
      system($cmd);

      # Read in that file
      my $jurl = "";
      my $jfile = "";
      my $report_to = "";
      my $listing = `cat $next_info`;
      my @lines = split(/\n/, $listing);
      for ($i = 0; $i<@lines; $i++) {
         my $ln = $lines[$i];
         chomp($ln);
         if ($ln =~ /^CICD_URL=(.*)/) {
            $jurl = $1;
         }
         elsif ($ln =~ /^CICD_FILE_NAME=(.*)/) {
            $jfile = $1;
         }
      }

      if ($jurl eq "") {
         print("ERROR: No CICD_URL found, cannot download file.\n");
         exit(1);
      }
      if ($jfile eq "") {
         print("ERROR: No CICD_FILE_NAME found, cannot download file.\n");
         exit(1);
      }

      my $cmd = "curl --location -o $jfile -u $jfrog_user:$jfrog_passwd $jurl/$jfile";
      system($cmd);

      # Next steps here are to put the OpenWrt file on the LANforge system
      # and then get it onto the DUT, reboot DUT, re-configure as needed,
      # and then kick off automated regression test.
      # When complete, upload the results to the requested location.

      exit(0);
   }

   #print "$ln\n";
}

exit 0;
