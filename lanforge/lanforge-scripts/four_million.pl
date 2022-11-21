#!/usr/bin/perl
use strict;
use warnings;
use diagnostics;
use Carp;
#$SIG{ __DIE__  } = sub { Carp::confess( @_ ) };
#$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };
use POSIX qw(ceil floor);
use Scalar::Util; #::looks_like_number;
use Getopt::Long;
use Socket;
use Cwd qw(getcwd);
my $cwd = getcwd();


package main;

# Un-buffer output
$| = 1;

# use lib prepends to @INC, so put lower priority first
# This is before run-time, so cannot condition this with normal 'if' logic.
use lib '/home/lanforge/scripts';
use lib "./";

use List::Util qw(first);
use LANforge::Endpoint;
use LANforge::Utils;
use Net::Telnet ();

my $lfmgr_host = "jedway3";
my $lfmgr_port = 4001;

our $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/',
          Timeout => 20);
$t->open(Host    => $lfmgr_host,
         Port    => $lfmgr_port,
         Timeout => 10);
$t->waitfor("/btbits\>\>/");

# Configure our utils.
our $utils = new LANforge::Utils();
$utils->telnet($t);         # Set our telnet object.
our $quiet = 1;
if ($utils->isQuiet()) {
  if (defined $ENV{'LOG_CLI'} && $ENV{'LOG_CLI'} ne "") {
    $utils->cli_send_silent(0);
  }
  else {
    $utils->cli_send_silent(1); # Do not show input to telnet
  }
  $utils->cli_rcv_silent(1);  # Repress output from telnet
}
else {
  $utils->cli_send_silent(0); # Show input to telnet
  $utils->cli_rcv_silent(0);  # Show output from telnet
}
$utils->log_cli("# $0 ".`date "+%Y-%m-%d %H:%M:%S"`);


my $num_connects = 4000;
my $num_vlans = 1000;
my @connections = ();

my $index = 0;
my $portnum = 0;

my $n = 0;
for (my $c = 1; $c <= $num_connects; $c++) {
   $n = (10 * $num_connects) + $c;
   push(@::connections, "con".substr("$n", 1));
}
my @cmds = ();
foreach my $con_name (@::connections) {
   @cmds = (
   "add_endp ${con_name}-A 1 1 rd0a#$portnum lf_tcp -1 NO 2400 2400 NO 300 300 increasing",
   "set_endp_report_timer ${con_name}-A 15000",
   "set_endp_details ${con_name}-A 8912 8912",
   "add_endp ${con_name}-B 1 1 rd1b lf_tcp -1 NO 2400 2400 NO 300 300 increasing",
   "set_endp_report_timer ${con_name}-B 15000",
   "set_endp_details ${con_name}-B 8912 8912",
   "add_cx ${con_name} default_tm ${con_name}-A ${con_name}-B",
   "set_cx_report_timer default_tm ${con_name} 15000 cxonly",
   );
   foreach my $cmd (@cmds) {
      $utils->doCmd($cmd);
      print ".";
      #sleep 1;
   }
   print "0";
}
#
