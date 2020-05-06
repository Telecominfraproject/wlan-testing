#!/usr/bin/perl

# Query jfrog URL and get list of builds.

use strict;
use warnings;
use Getopt::Long;

my $user = "cicd_user";
my $passwd = "";
my $url = "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/";
my $files_processed = "jfrog_files_processed.txt";
my $next_info = "jfrog_files_next.txt";
my $help = 0;

my $usage = qq($0
  [--user { jfrog user (default: cicd_user) }
  [--passwd { jfrog password }
  [--url { jfrog URL, default is OpenWrt URL: https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/ }
  [--files_processed { text file containing file names we have already processed }
  [--next_info { output text file containing info about the next file to process }

Example:
$0 --user cicd_user --passwd secret --url https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/ \
   --files_processed jfrog_files_processed.txt --next_info jfrog_files_next.txt

);

GetOptions
(
  'user=s'                 => \$user,
  'passwd=s'               => \$passwd,
  'url=s'                  => \$url,
  'files_processed=s'      => \$files_processed,
  'next_info=s'            => \$next_info,
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
   print("Already processed: $ln");
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

      open(FILE, ">", $next_info);
      print FILE "CICD_URL=$url\nCICD_FILE_NAME=$fname\nCICD_URL_DATE=$date\n";

      if ($fname =~ /^(\S+)-(\d\d\d\d-\d\d-\d\d)-(\S+).tar.gz/) {
         my $hw = $1;
         my $fdate = $2;
         my $githash = $3;
         print FILE "CICD_HW=$1\nCICD_FILEDATE=$fdate\nCICD_GITHASH=$githash\n";
      }

      close(FILE);

      print("Next: File Name: $fname  Display Name: $name  Date: $date\n");
      print("To download: curl --location -o /tmp/$fname -u $user:$passwd $url/$fname\n");
      exit(0);
   }

   #print "$ln\n";
}

exit 0;
