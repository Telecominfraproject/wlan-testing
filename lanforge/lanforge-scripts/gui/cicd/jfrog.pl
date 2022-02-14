#!/usr/bin/perl

# Query jfrog URL and get list of builds.
# This will be run on the test-bed orchestrator
# Run this in directory that contains the testbed_$hw/ directories
# Assumes cicd.class is found in ~/git/lanforge-scripts/gui/

use strict;
use warnings;
use Getopt::Long;

my $user = "cicd_user";
my $passwd = "";
my $url = "https://myco.jfrog.io/artifactory/wlan-ap-firmware";
my @platforms = ("ea8300", "ecw5410");  # Add more here as we have test beds that support them.
my $files_processed = "jfrog_files_processed.txt";
my $tb_url_base = "cicd_user\@myco.cicd.cloud.com/testbeds";  # Used by SSH: scp -R results_dir cicd_user@myco.cicd.cloud.com/testbeds/
my $help = 0;
my $cicd_prefix = "CICD_TEST";
my $kpi_dir = "/home/greearb/git/lanforge-scripts/gui/";
my @ttypes = ("fast", "basic");
my $duplicate_work = 1;

my $ul_host = "www";
my $ul_dir = "candela_html/examples/cicd/"; # used by scp
my $ul_dest = "$ul_host:$ul_dir"; # used by scp
my $other_ul_dest = ""; # used by scp
my $result_url_base = "http://localhost/myco/cicd";

my $usage = qq($0
  [--user { jfrog user (default: cicd_user) }
  [--passwd { jfrog password }
  [--result_url_base { http://foo.com/myco/cicd }
  [--url { jfrog URL, default is OpenWrt URL: https://myco.jfrog.io/artifactory/wlan-ap-firmware/ }
  [--files_processed { text file containing file names we have already processed }
  [--tb_url_base { Where to report the test results? }

Example:

# Use MY-CO jfrog repo
$0 --user cicd_user --passwd secret --url https://myco.jfrog.io/artifactory/wlan-ap-firmware/ \\
   --files_processed jfrog_files_processed.txt \\
   --tb_url_base cicd_user\@myco.cicd.cloud.com/testbeds

# Download images from candelatech.com web site (for developer testing and such)
$0 --tb_url_base greearb@192.168.100.195:/var/www/html/myco/testbeds/ \\
   --url http://www.candelatech.com/downloads/myco/test_images

);

GetOptions
(
  'user=s'                 => \$user,
  'passwd=s'               => \$passwd,
  'url=s'                  => \$url,
  'files_processed=s'      => \$files_processed,
  'tb_url_base=s'          => \$tb_url_base,
  'result_url_base=s'      => \$result_url_base,
  'help|?'                 => \$help,
) || (print($usage) && exit(1));

if ($help) {
  print($usage) && exit(0);
}

#if ($passwd eq "") {
#   print("ERROR:  You must specify jfrog password.\n");
#   exit(1);
#}

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
         my $process = $1;  # For example: ben-home/reports/fast
         my $completed = `cat $ln`;  # Contents of the results file
         chomp($completed);
         if ($ln =~ /(.*)\/reports\/$ttype\/NEW_RESULTS/) {
            my $tbed = $1;
            my $cmd;
            my $caseid = "";

            print "Processing new results, line: $ln  process: $process  completed: $completed  testbed: $tbed\n";

            # Figure out the new directory from the work-item.
            my $wi = `cat ./$tbed/pending_work/$completed`;

            `mv ./$tbed/pending_work/$completed /tmp/`;

            if ($wi =~ /CICD_CASE_ID=(\S+)/) {
               $caseid = "--caseid $1";
            }

            if ($wi =~ /CICD_RPT_NAME=(.*)/) {
               my $widir = $1;

               # Ensure we have a place to copy the new report
               $cmd = "ssh $ul_host \"mkdir -p $ul_dir/$tbed/$ttype\"";
               print "Ensure directory exists: $cmd\n";
               `$cmd`;

               # Upload the report directory
               $cmd = "scp -C -r $process/$widir $ul_dest/$tbed/$ttype/";
               print "Uploading: $cmd\n";
               `$cmd`;

               $caseid .= " --results_url $result_url_base/$tbed/$ttype/$widir";
            }
            else {
               print "WARNING:  No CICD_RPT_NAME line found in work-item contents:\n$wi\n";
            }

            $cmd = "cd $kpi_dir && java kpi $caseid --dir \"$pwd/$process\" && cd -";
            print ("Running kpi: $cmd\n");
            `$cmd`;
            `rm $ln`;
            $cmd = "scp -C $process/*.png $process/*.html $process/*.csv $process/*.ico $process/*.css $ul_dest/$tbed/$ttype/";
            print "Uploading: $cmd";
            `$cmd`;

            # This might need similar partial-upload logic as that above, if it is ever actually
            # enabled.
            if ($other_ul_dest ne "") {
               $cmd = "scp -C -r $process $other_ul_dest/$tbed/";
               print "Uploading to secondary location: $cmd";
               `$cmd`;
            }
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

my $z;
for ($z = 0; $z<@platforms; $z++) {
   my $pf = $platforms[$z];
   my $cmd = "curl -u $user:$passwd $url/$pf/";
   print ("Calling command: $cmd\n");
   $listing = `$cmd`;
   @lines = split(/\n/, $listing);
   for ($i = 0; $i<@lines; $i++) {
      my $ln = $lines[$i];
      chomp($ln);

      #print("ln -:$ln:-\n");

      if (($ln =~ /href=\"(.*)\">(.*)<\/a>\s+(.*)\s+\S+\s+\S+/)
          || ($ln =~ /class=\"indexcolname\"><a href=\"(.*.tar.gz)\">(.*)<\/a>.*class=\"indexcollastmod\">(\S+)\s+.*/)) {
         my $fname = $1;
         my $name = $2;
         my $date = $3;

         # Skip header
         if ($ln =~ /Last modified/) {
            next;
         }

         # Skip parent-dir
         if ($ln =~ /Parent Directory/) {
            next;
         }

         #print("line matched -:$ln:-\n");
         #print("fname: $fname  name: $name  date: $date\n");

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
         } else {
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
            if (!hw_matches($tb_hw_type, $hw)) {
               print "Skipping test bed $dname, jfrog hardware type: -:$hw:-  testbed hardware type: -:$tb_hw_type:-\n";
               next;
            }
            print "Checking testbed $dname backlog..\n";
            my $bklog = `ls $dname/pending_work/$cicd_prefix-*`;
            my $bklog_count = split(/\n/, $bklog);
            if ($best_tb eq "") {
               $best_tb = $dname;
               $best_backlog = $bklog_count;
            } else {
               if ($best_backlog > $bklog_count) {
                  $best_tb = $dname;
                  $best_backlog = $bklog_count;
               }
            }
         }

         if ($best_tb eq "") {
            print "ERROR:  No test bed found for hardware type: $hw\n";
            last;
         }

         my $fname_nogz = $fname;
         if ($fname =~ /(.*)\.tar\.gz/) {
            $fname_nogz = $1;
         }

         my @tbs = ($best_tb);

         # For more test coverage, send work to rest of the available test beds as well.
         if ($duplicate_work) {
            for ($di = 0; $di<@dira; $di++) {
               my $dname = $dira[$di];
               chomp($dname);
               if (! -d $dname) {
                  next;
               }
               if ($dname eq $best_tb) {
                  next;            # processed this one above
               }
               if (! -f "$dname/TESTBED_INFO.txt") {
                  next;
               }

               my $tb_info = `cat $dname/TESTBED_INFO.txt`;
               my $tb_hw_type = "";
               if ($tb_info =~ /TESTBED_HW=(.*)/g) {
                  $tb_hw_type = $1;
               }

               if (!hw_matches($tb_hw_type, $hw)) {
                  print "Skipping test bed $dname, jfrog hardware type: -:$hw:-  testbed hardware type: -:$tb_hw_type:-\n";
                  next;
               }

               push(@tbs, "$dname");
            }
         }

         my $q;
         for ($q = 0; $q < @tbs; $q++) {
            $best_tb = $tbs[$q];
            my $caseid_fast = "";
            my $caseid_basic = "";

            my $tb_info = `cat $best_tb/TESTBED_INFO.txt`;
            if ($tb_info =~ /TESTBED_CASEID_FAST=(.*)/g) {
               $caseid_fast = $1;
            }
            if ($tb_info =~ /TESTBED_CASEID_BASIC=(.*)/g) {
               $caseid_basic = $1;
            }

            my $ttype = "fast";
            my $work_fname = "$best_tb/pending_work/$cicd_prefix-$fname_nogz-$ttype";
            my $work_fname_a = $work_fname;

            system("mkdir -p $best_tb/pending_work");
            system("mkdir -p $best_tb/reports/$ttype");

            open(FILE, ">", "$work_fname");

            print FILE "CICD_TYPE=$ttype\n";
            print FILE "CICD_RPT_NAME=$fname_nogz\n";
            print FILE "CICD_RPT_DIR=$tb_url_base/$best_tb/reports/$ttype\n";

            print FILE "CICD_HW=$hw\nCICD_FILEDATE=$fdate\nCICD_GITHASH=$githash\n";
            print FILE "CICD_URL=$url/$pf\nCICD_FILE_NAME=$fname\nCICD_URL_DATE=$date\n";
            if ($caseid_fast ne "") {
               print FILE "CICD_CASE_ID=$caseid_fast\n";
            }

            close(FILE);

            print("Next: File Name: $fname  Display Name: $name  Date: $date  TType: $ttype\n");
            print("Work item placed at: $work_fname\n");


            $ttype = "basic";
            $work_fname = "$best_tb/pending_work/$cicd_prefix-$fname_nogz-$ttype";

            system("mkdir -p $best_tb/reports/$ttype");

            open(FILE, ">", "$work_fname");

            print FILE "CICD_TYPE=$ttype\n";
            print FILE "CICD_RPT_NAME=$fname_nogz\n";
            print FILE "CICD_RPT_DIR=$tb_url_base/$best_tb/reports/$ttype\n";

            print FILE "CICD_HW=$hw\nCICD_FILEDATE=$fdate\nCICD_GITHASH=$githash\n";
            print FILE "CICD_URL=$url/$pf\nCICD_FILE_NAME=$fname\nCICD_URL_DATE=$date\n";
            if ($caseid_basic ne "") {
               print FILE "CICD_CASE_ID=$caseid_basic\n";
            }

            close(FILE);

            print("Next: File Name: $fname  Display Name: $name  Date: $date TType: $ttype\n");
            print("Work item placed at: $work_fname\n");
            #print("To download: curl --location -o /tmp/$fname -u $user:$passwd $url/$pf/$fname\n");
         }                         # for all testbeds

         # Note this one is processed
         `echo -n "$fname " >> $files_processed`;
         `date >> $files_processed`;
      }

      #print "$ln\n";
   }# for all lines in a directory listing
}# for all URLs to process

exit 0;


sub hw_matches {
   my $a = shift;
   my $b = shift;

   # Normalize equivalent HW types.
   if ($a eq "mr8300") {
      $a = "ea8300";
   }
   if ($b eq "mr8300") {
      $b = "ea8300";
   }

   if ($a eq $b) {
      return 1;
   }
   return 0;
}
