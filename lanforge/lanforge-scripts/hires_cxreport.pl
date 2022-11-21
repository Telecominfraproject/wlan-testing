#!/usr/bin/perl
package main;
if (defined $ENV{DEBUG}) {
   use strict;
   use warnings;
   use diagnostics;
   use Carp;
   use Data::Dumper;
}
use Time::HiRes qw(usleep ualarm gettimeofday stat lstat utime);
#use Time::Format qw/%time/;

# use lib prepends to @INC, so put lower priority first
# This is before run-time, so cannot condition this with normal 'if' logic.
use lib '/home/lanforge/scripts';
use lib "./";

use LANforge::Utils;
use Net::Telnet ();
use Getopt::Long;
our $quiet = 1;

my $report_filename = "/tmp/hires_report.txt";
my $duration_sec = 60;
my $cx = "rdtest";


our $lfmgr_host = 'localhost';
our $lfmgr_port = 4001;
$| = 1;
my $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/',
                    Timeout => 60);

$t->open(Host    => $::lfmgr_host,
        Port    => $::lfmgr_port,
        Timeout => 10);

$t->max_buffer_length(16 * 1024 * 1000); # 16 MB buffer
$t->waitfor("/btbits\>\>/");

# Configure our utils.
our $utils = new LANforge::Utils();
$::utils->telnet($t);         # Set our telnet object.
if ($::utils->isQuiet()) {
 if (defined $ENV{'LOG_CLI'} && $ENV{'LOG_CLI'} ne "") {
   $::utils->cli_send_silent(0);
 }
 else {
   $::utils->cli_send_silent(1); # Do not show input to telnet
 }
 $::utils->cli_rcv_silent(1);  # Repress output from telnet
}
else {
 $::utils->cli_send_silent(0); # Show input to telnet
 $::utils->cli_rcv_silent(0);  # Show output from telnet
}
#$::utils->log_cli("# $0 ".`date "+%Y-%m-%d %H:%M:%S"`);

$SIG{'INT'} = sub {
   $::utils->doCmd("set_cx_state all $cx STOPPED");
   exit 0;
};

# start rdtest
my %times = ();
$times{gettimeofday().'_before_set_cx_state'} = gettimeofday() ." before_start_cx 0 0";
$::utils->doCmd("set_cx_report_timer all $cx 250");
$::utils->doCmd("set_cx_state all $cx RUNNING");
$times{gettimeofday().'_after_set_cx_state'} = gettimeofday() ." after_start_cx 0 0";

my $timelimit = $duration_sec + time();

my $show_cx_str = '';
my $lastline = '';
my $lasttime = 0;
my @hunks = ();
my $delta = 0;
my $tod = gettimeofday();
my $last_a = 0;
my $last_b = 0;
my $step_a = 0;
my $step_b = 0;
while ($tod < $timelimit) {
# the command below does not indicate last reported timestamp, skip it
#   $show_cx_str = $::utils->doAsyncCmd("show_cxe all $cx");
#   $times{gettimeofday()."_show_cxe"} = $show_cx_str;
   $tod = gettimeofday();
   $lastline=`tail -1 /home/lanforge/lf_reports/${cx}-A*`;
   @hunks = split(',', $lastline);
   $hunks[0] = $hunks[0]/1000 if ($hunks[0] > 0);
   $last_a = $hunks[0] if ($last_a == 0);
   if ($hunks[0] gt $last_a){
      print "\nnew report A entry!\n";
      $step_a = $hunks[0] - $last_a;
      $last_a = $hunks[0];
      $delta = $tod - $hunks[0];
      $times{"${tod}_tail_csv-A"} = "$hunks[0] $hunks[1] $step_a $delta";
   }
   $lastline=`tail -1 /home/lanforge/lf_reports/${cx}-B*`;
   @hunks = split(',', $lastline);
   $hunks[0] = $hunks[0]/1000 if ($hunks[0] > 0);
   $last_b = $hunks[0] if ($last_b == 0);
   if ($hunks[0] gt $last_b) {
      print "\nnew report B entry!\n";
      $step_b = $hunks[0] - $last_b;
      $last_b = $hunks[0];
      $delta = $tod - $hunks[0];
      $times{"${tod}_tail_csv-B"} = "$hunks[0] $hunks[1] $step_b $delta";
   }
   usleep(125);
   if (time() gt $lasttime) {
      print "\r".($timelimit - time())." sec remaining ";
      $lasttime = time();
   }
} #~while
$::utils->doCmd("set_cx_state all $cx STOPPED");
print "...collected.\n";
die unless open(my $fh, ">", $report_filename);
#print $fh "TimeKeyInput csv_record_tstampsecs endpoint sec_since_last_report seconds_lag_since_last_report\n";
print $fh "clock          csv_tstamp_secs           endpoint     sec_btwn_reports  tstamp_lag_sec\n";
foreach $key (sort {$a cmp $b} (keys %times)) {
   my ($clock) = $key =~ m/^([^_]+)/;
   @hunks = split(' ', $times{$key});
   print$fh sprintf "%14.3f %15.3f %18s %20.3f %15.3f\n", 0.0+$clock, $hunks[0], $hunks[1], $hunks[2], $hunks[3];
}
close $fh;
print "View the report at $report_filename\n";


#eof
