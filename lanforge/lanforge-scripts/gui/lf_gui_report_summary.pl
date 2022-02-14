#!/usr/bin/perl -w
# Generate HTML summary page for a collection of GUI reports (with kpi.csv)
# (C) 2020 Candela Technologies Inc.
#

use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{ __DIE__  } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };

# Un-buffer output
$| = 1;

# use lib prepends to @INC, so put lower priority first
# This is before run-time, so cannot condition this with normal 'if' logic.
use lib '/home/lanforge/scripts';
use lib "../";
use lib "./";

use Getopt::Long;
use HTML::Entities;

our $dir = "";
our $notes = "";
our $gitlog = "";
our $dutgitlog = "";
our $title = "Automated test results.";


########################################################################
# Nothing to configure below here, most likely.
########################################################################

our $usage = <<"__EndOfUsage__";
$0 [ --dir directory-to-process --notes testbed-notes-file.html --dutgitlog dut-gitlog-output.html --gitlog gitlog-output.html ] < html_template.html

Example:
 cat html-template | $0 --dir ~/tmp/results --title "My Title" --notes testbeds/my_testbed/testbed_notes.html --dutgitlog /tmp/dgitlog.html --gitlog /tmp/gitlog.html
__EndOfUsage__

my $i = 0;
my $show_help = 0;

GetOptions
(
   'dir|d=s'            => \$::dir,
   'notes|n=s'          => \$::notes,
   'gitlog|g=s'         => \$::gitlog,
   'dutgitlog=s'        => \$::dutgitlog,
   'title|t=s'          => \$::title,
   'help|h'             => \$show_help,
) || die("$::usage");

if ($show_help) {
   print $usage;
   exit 0;
}

my $testbed_notes = "";
if (-f "$notes") {
   $testbed_notes .= "<b>Test Bed Notes.</b><br>\n";
   $testbed_notes .= `cat $notes`;
}

if (-f "$dutgitlog") {
   $testbed_notes .= "<P>\n";
   $testbed_notes .= `cat $dutgitlog`;
   $testbed_notes .= "<p>\n";
}

if (-f "$gitlog") {
   $testbed_notes .= "<P>\n";
   $testbed_notes .= `cat $gitlog`;
   $testbed_notes .= "<p>\n";
}

$testbed_notes .= "<p><b>Top lanforge-scripts commits.</b><br><pre>\n";
$testbed_notes .= `git log -n 8 --oneline`;
$testbed_notes .= "</pre>\n";


chdir($dir);

my @files = `ls`;
chomp(@files);

my $line;

# Find some html helpers and copy them to current dir.
foreach $line (@files) {
   if ( -d $line) {
      if ( -f "$line/canvil.ico") {
         `cp $line/canvil.ico ./`;
         `cp $line/*.css ./`;
         `cp $line/candela_swirl* ./`;
         `cp $line/CandelaLogo* ./`;
         last;
      }
   }
}

my $dut_tr = "";
my $kpi_tr = "";
my $tests_tr = "";

# TODO:  Add git commit history for other repositories perhaps?

foreach my $line (@files) {
   if ( -d $line) {
      #print "Checking report: $line\n";
      if ( -d "$line/logs") {
         processLogs("$line/logs");
         my $log_links = "";
         my $li = 0;
         my $iline;
         my @ifiles = `ls $line/logs/*-idx.html`;
         chomp(@ifiles);
         foreach $iline (@ifiles) {
            $log_links .= " <a href=$iline>[$li]</a>";
         }
         if ($log_links ne "") {
            $log_links = "Errors: $log_links";
         }
         $tests_tr .= "<tr><td><a href=\"$line/index.html\">$line</a></td><td><a href=\"$line/logs\">Logs</a> $log_links</td></tr>\n";
      }
      else {
         $tests_tr .= "<tr><td><a href=\"$line/index.html\">$line</html></td><td></td></tr>\n";
      }

      if ( -f "$line/kpi.csv") {
         my @kpi = `cat $line/kpi.csv`;
         chomp(@kpi);
         my $i = 0;
         foreach my $k (@kpi) {
            $i++;
            if ($i == 1) {
               next; # skip header
            }

            my @cols = split(/\t/, $k);
            if ($dut_tr eq "") {
               $dut_tr = "<tr><td>$cols[1]</td><td>$cols[2]</td><td>$cols[3]</td><td>$cols[4]</td><td>$cols[5]</td></tr>\n";
            }

            my $nval = $cols[10];
            if  ( $nval =~ /^[+-]?(?=\.?\d)\d*\.?\d*(?:e[+-]?\d+)?\z/i ) {
               $nval = sprintf("%.2f", $nval);
            }

            my $s_passed = "0";
            my $s_failed = "0";
            if (@cols >= 16) {
               $s_passed = $cols[14];
               $s_failed = $cols[15];
            }

            $kpi_tr .= "<tr><td>$cols[7]</td><td>$cols[8]</td><td>$cols[9]</td><td>$s_passed</td><td>$s_failed</td><td>$nval</td><td>$cols[11]</td></tr>\n";
         }
      }
   }
}

my $date = `date`;

while (<>) {
   my $ln = $_;
   chomp($ln);

   $ln =~ s/___TITLE___/$title/g;
   $ln =~ s/___DATE___/$date/g;
   $ln =~ s/___TR_DUT___/$dut_tr/g;
   $ln =~ s/___TR_KPI___/$kpi_tr/g;
   $ln =~ s/___TR_TESTS___/$tests_tr/g;
   $ln =~ s/___TESTBED_NOTES___/$testbed_notes/g;
   print "$ln\n";
}

exit(0);

sub processLogs {
   my $ldir = shift;

   my @files = `ls $ldir`;
   chomp(@files);

   open(CSV, ">$ldir/logs.csv");
   print CSV "FILE\tBUGS\tWARNINGS\tCRASHED\tRESTARTING\n";

   foreach $line (@files) {
      if ($line =~ /console.*\.txt$/) {

         my $bugs = 0;
         my $warnings = 0;
         my $crashed = 0;
         my $restarting = 0;

         my $tag = 0;
         my $logf = $ldir . "/" . $line;
         my $logh = $logf . ".html";
         my $loghb = $line . ".html";
         my $loghi = $logf . "-idx.html";

         #print("Processing log file: $logf\n");

         open(IFILE, "<", $logf ) or die( "could not read $logf");
         open(IDX, ">$loghi");
         open(LOGH, ">$logh");

         print IDX getHtmlHdr("Log file index: $line");
         print LOGH getHtmlHdr("Log file: $line");

         print LOGH "<pre>\n";

         print IDX "<a href=$loghb>Full Logs in HTML format</a><br>\n";
         print IDX "<a href=$line>Full Logs in Text format</a><P>\n";
         print IDX "<b>Interesting log sections.</b><br>\n";
         print IDX "<ol>\n";

         while (<IFILE>) {
            my $ln = $_;
            chomp($ln);

            #print("ln: $ln\n");
            my $enc_ln = encode_entities($ln);
            # Get rid of some funk
            $enc_ln =~ s/\&\#0\;//g;

            if (($ln =~ /WARNING:/) ||
                ($ln =~ /BUG:/) ||
                ($ln =~ /Hardware became unavailable during restart/) ||
                ($ln =~ /restarting hardware/) ||
                ($ln =~ /oom-killer/) ||
                ($ln =~ /crashed/)) {
               if ($ln =~ /WARNING:/) {
                  $warnings++;
               }
               elsif ($ln =~ /BUG:/) {
                  $bugs++;
               }
               elsif ($ln =~ /restarting hardware/) {
                  $restarting++;
               }
               elsif (($ln =~ /crashed/) || # software/firmware crashed
                      ($ln =~ /oom-killer/) || # System OOM, processes were force-killed by kernel
                      ($ln =~ /became unavailable/)) { # hardware crashed
                  $crashed++;
               }
               print IDX "<li><a href=$loghb#$tag>$enc_ln</a></li>\n";
               print LOGH "<a name='$tag'></a>\n";
               print LOGH "<pre style='color:red'>$enc_ln</pre>\n";
               $tag++;
            }
            else {
               print LOGH "$enc_ln\n";
            }
         }

         #print ("Done with file\n");

         print LOGH "</pre>\n";
         print IDX "</ol>\n";

         print LOGH getHtmlFooter();
         print IDX getHtmlFooter();

         close(IDX);
         close(LOGH);
         close(IFILE);

         print CSV "$line\t$bugs\t$warnings\t$crashed\t$restarting\n";

         if ($bugs + $warnings +$crashed + $restarting == 0) {
            # Remove index since it has no useful data
            unlink($loghi);
         }
      }
   }
   #print("Done processing logs.\n");
}

sub getHtmlHdr {
   my $title = shift;

   return "<!DOCTYPE html>\n" .
                "<html>\n" .
                "  <head>\n" .
                "    <meta charset='utf-8' />\n" .
                "    <meta name='viewport' content='width=device-width, initial-scale=1' />\n" .
                "    <title>$title</title>    <link rel='shortcut icon' href='canvil.ico' type='image/x-icon' />\n" .
                "    <link rel='stylesheet' href='../report.css' />\n" .
                "    <link rel='stylesheet' href='../custom.css' />\n" .
                "    <style>\n" .
                "     pre {\n" .
                "        overflow: auto;\n" .
                "     }\n" .
                "     img {\n" .
                "        width: 100%;\n" .
                "        max-width: 8in;\n" .
                "     }\n" .
                "    </style>\n" .
                "  </head>\n" .
                "  <body>\n" .
                "<div class='HeaderStyle'>\n" .
                "<h1 class='TitleFontPrint'>$title</h1><br/>\n" .
                "\n" .
                "<div class='contentDiv'>\n";
}

sub getHtmlFooter {
   return "</div><!--end content-div -->\n" .
         "<div class='FooterStyle'><span class='Gradient'>Generated by Candela Technologies LANforge network testing tool.<br/>\n" .
         "  <a href='https://www.candelatech.com/' target='_blank'>www.candelatech.com</a>\n" .
         "</span>\n" .
         "<a class='LogoImgLink' href='https://www.candelatech.com/' target='_blank'><img align='right' src='../candela_swirl_small-72h.png'></a></div><br/>\n" .
         "  </body>\n" .
         "</html>\n";
}

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
