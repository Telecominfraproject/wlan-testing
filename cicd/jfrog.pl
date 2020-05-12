#!/usr/bin/perl

# Query jfrog URL and get list of builds.
# This will be run on the test-bed orchestrator
# Run this in directory that contains the testbed_$hw/ directories
# Assumes cicd.class is found in ~/git/tip/wlan-lanforge-scripts/gui/

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
my $kpi_dir = "/home/greearb/git/tip/wlan-lanforge-scripts/gui/";
my @ttypes = ("fast", "basic");

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

my $pwd = `pwd`;
chomp($pwd);

my $listing;
my @lines;
my $j;

# Check for any completed reports.
for ($j = 0; $j<@ttypes; $j++) {
   my $ttype = $ttypes[$j];
   $listing = `ls */reports/$ttype/NEW_RESULTS-*`;
   @lines = split(/\n/, $listing);
   for ($i = 0; $i<@lines; $i++) {
      my $ln = $lines[$i];
      chomp($ln);
      if ($ln =~ /(.*)\/NEW_RESULTS/) {
         my $process = $1;
         my $completed = `cat $ln`;
         chomp($completed);
         if ($ln =~ /(.*)\/reports\/$ttype\/NEW_RESULTS/) {
            my $tbed = $1;

            `rm ./$tbed/pending_work/$completed`;

            my $cmd = "cd $kpi_dir && java kpi --dir \"$pwd/$process\" && cd -";
            print ("Running kpi: $cmd\n");
            `$cmd`;
            `rm $ln`;
            `scp -C -r $process www:candela_html/examples/cicd/$tbed/`
         }
      }
   }
}

#Read in already_processed builds
my @processed = ();
$listing = `cat $files_processed`;
@lines = split(/\n/, $listing);
for ($i = 0; $i<@lines; $i++) {
   my $ln = $lines[$i];
   chomp($ln);
   print("Reported already processed: $ln\n");
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
         print "ERROR:  Un-handled filename syntax: $fname, assuming file-name is hardware name.\n";
         $hw = $fname;
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
         my $bklog = `ls $dname/pending_work/$cicd_prefix-*`;
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

      my $ttype = "fast";
      my $work_fname = "$best_tb/pending_work/$cicd_prefix-$fname_nogz-$ttype";

      system("mkdir -p $best_tb/pending_work");
      system("mkdir -p $best_tb/reports/$ttype");

      open(FILE, ">", "$work_fname");

      print FILE "CICD_TYPE=$ttype\n";
      print FILE "CICD_RPT_NAME=$fname_nogz\n";
      print FILE "CICD_RPT_DIR=$tb_url_base/$best_tb/reports/$ttype\n";

      print FILE "CICD_HW=$hw\nCICD_FILEDATE=$fdate\nCICD_GITHASH=$githash\n";
      print FILE "CICD_URL=$url\nCICD_FILE_NAME=$fname\nCICD_URL_DATE=$date\n";

      close(FILE);


      $ttype = "basic";
      $work_fname = "$best_tb/pending_work/$cicd_prefix-$fname_nogz-$ttype";

      system("mkdir -p $best_tb/reports/$ttype");

      open(FILE, ">", "$work_fname");

      print FILE "CICD_TYPE=$ttype\n";
      print FILE "CICD_RPT_NAME=$fname_nogz\n";
      print FILE "CICD_RPT_DIR=$tb_url_base/$best_tb/reports/$ttype\n";

      print FILE "CICD_HW=$hw\nCICD_FILEDATE=$fdate\nCICD_GITHASH=$githash\n";
      print FILE "CICD_URL=$url\nCICD_FILE_NAME=$fname\nCICD_URL_DATE=$date\n";

      close(FILE);

      print("Next: File Name: $fname  Display Name: $name  Date: $date\n");
      print("Work item placed at: $work_fname\n");
      #print("To download: curl --location -o /tmp/$fname -u $user:$passwd $url/$fname\n");

      # Note this one is processed
      `echo -n "$fname " >> $files_processed`;
      `date >> $files_processed`;

      exit(0);
   }

   #print "$ln\n";
}

exit 0;
