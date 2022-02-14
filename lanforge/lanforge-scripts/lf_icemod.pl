#!/usr/bin/perl -w

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# Written by Candela Technologies Inc.
#  Updated by: greearb@candelatech.com
#
#

use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };
our $q = q(');
our $Q = q(");
# Un-buffer output
$| = 1;

# use lib prepends to @INC, so put lower priority first
# This is before run-time, so cannot condition this with normal 'if' logic.
use lib '/home/lanforge/scripts';
use lib "./";

use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
use Net::Telnet ();
use Getopt::Long;

my $shelf_num = 1;
my $lfmgr_host = "localhost";
my $lfmgr_port = 4001;
my $report_timer = 1000; # XX/1000 seconds

# Default values for ye ole cmd-line args.
my $port = "";
my $endp_name = "";
my $speed = "";
my $latency = "";
my $max_jitter = "";
my $reorder_freq = "";
my $extra_buffer = "";
my $drop_pm = "";
my $dup_pm = "";
my $jitter_freq = "";
my $min_drop_amt = "";
my $max_drop_amt = "";
my $min_reorder_amt = "";
my $max_reorder_amt = "";
my $max_lateness = "";
my $switch = "";
my $pcap = "";
my $load = "";
my $state = "";
my $cx = "";
our $quiet = 0;
my $description = "";
my $fail_msg = "";
my $manual_check = 0;
my $cpu_id = "NA";
my $wle_flags = 0;

########################################################################
# Nothing to configure below here, most likely.
########################################################################

my $usage = qq($0  [--manager { hostname or address of LANforge manager } ]
                 [--resource { resource number } ]
                 [--port {port name} ]
                 [--endp_name { name } ]
                 [--description { ${Q}stuff in quotes${Q} } ]
                 [--cx { name } ]
                 [--speed { speed in bps } ]
                 [--latency { 0 - 1000000 }        # in milliseconds ]
                 [--max_jitter { 0 - 1000000 }     # in milliseconds ]
                 [--reorder_freq { 0 - 1000000 }   # packets per million ]
                 [--extra_buffer { -1 - 1000000 }  # extra bytes to buffer, -1: AUTO, units of 1024 ]
                 [--drop_pm { 0 - 1000000 }        # drop packets per million ]
                 [--dup_pm { 0 - 1000000 }         # duplication packets per million ]
                 [--jitter_freq { 0 - 10000000 }   # jitter these many packets per million ]
                 [--min_drop_amt { 1 - 1000 }     # drop at least this many packets in a row, default 1
                 [--max_drop_amt { 1 - 1000 }     # drop at most this many packets in a row, default 1
                 [--min_reorder_amt { 1 - 1000 }   # reorder at least this many packets, default 1
                 [--max_reorder_amt { 1 - 1000 }   # reorder at most this many packets, default 10
                 [--max_lateness { -1 - 1000000 }  # maximum amount of unintentional delay before pkt is dropped -1=AUTO
                 [--switch new_cx_to_run ]         # activate named CX
                 [--pcap { dir-name | off } ]      # specify a packet capture to replay
                 [--load { db-name } ]             # load a database
                 [--state { running | switch | quiesce | stopped | deleted } ]

Example:
 lf_icemod.pl --manager lanforge1 --new_endp t1-A --speed 256000 --drop_pm 100 --latency 35 --description ${Q}link one${Q}
 lf_icemod.pl --mgr lanforge1 --new_cx "t1" --endps t1-A,t1-B
 lf_icemod.pl --mgr lanforge1 --endp_name t1-A --speed 154000 --drop_pm 10000 --latency 35
 lf_icemod.pl --mgr 192.168.100.223 --switch t3
 lf_icemod.pl --state running --cx t3
 lf_icemod.pl --pcap /tmp/endp-a --endp_name t1-A
 lf_icemod.pl --load my_db
);

if (@ARGV < 2) {
   print "$usage\n";
   exit 0;
}

my $i = 0;
my $show_help;
my $resource = 1;
my $new_endp = "";
my $new_cx = "";
my $endps = "";

GetOptions (
   'help|h'                => \$show_help,
   'manager|mgr|m=s'       => \$lfmgr_host,
   'card|resource|r=i'     => \$resource,
   'endp_name|e=s'         => \$endp_name,
   'desc|description=s'    => \$description,
   'cx|c=s'                => \$cx,
   'speed|s=i'             => \$speed,
   'latency|l=i'           => \$latency,
   'max_jitter=i'          => \$max_jitter,
   'reorder_freq=i'        => \$reorder_freq,
   'extra_buffer=i'        => \$extra_buffer,
   'drop_pm|d=i'           => \$drop_pm,
   'dup_pm=i'              => \$dup_pm,
   'jitter_freq|j=i'       => \$jitter_freq,
   'min_drop_amt=i'        => \$min_drop_amt,
   'max_drop_amt=i'        => \$max_drop_amt,
   'min_reorder_amt=i'     => \$min_reorder_amt,
   'max_reorder_amt=i'     => \$max_reorder_amt,
   'max_lateness=i'        => \$max_lateness,
   'switch|w=s'            => \$switch,
   'new_endp=s'            => \$new_endp,
   'new_cx=s'              => \$new_cx,
   'endps=s'               => \$endps,
   'port=s'                => \$port,
   'pcap|p=s'              => \$pcap,
   'load|o=s'              => \$load,
   'state|a=s'             => \$state,
   'wle_flags=i'           => \$wle_flags,
   'quiet|q=i'             => \$quiet,
) || die("$usage");

if ($show_help) {
   print $usage;
   exit 0;
}

# Open connection to the LANforge server.
my $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/',
         Timeout => 20);

$t->open( Host    => $lfmgr_host,
          Port    => $lfmgr_port,
          Timeout => 10);

$t->waitfor("/btbits\>\>/");

my $dt = "";

my $utils = new LANforge::Utils();
$utils->connect($lfmgr_host, $lfmgr_port);

my $cmd;

$speed = "NA" if ($speed eq "");
$latency = "NA" if ($latency eq "");
$max_jitter = "NA" if ($max_jitter eq "");
$reorder_freq = "NA" if ($reorder_freq eq "");
$extra_buffer = "NA" if ($extra_buffer eq "");
$drop_pm = "NA" if ($drop_pm eq "");
$dup_pm = "NA" if ($dup_pm eq "");
$pcap = "NA" if ($pcap eq "");
$jitter_freq = "NA" if ($jitter_freq eq "");
$min_drop_amt = "NA" if ($min_drop_amt eq "");
$max_drop_amt = "NA" if ($max_drop_amt eq "");
$min_reorder_amt = "NA" if ($min_reorder_amt eq "");
$max_reorder_amt = "NA" if ($max_reorder_amt eq "");
$max_lateness = "NA" if ($max_lateness eq "");



if (($load ne "") && ($load ne "NA")) {
  $cmd = "load $load overwrite";
  $utils->doCmd($cmd);
  my @rslt = $t->waitfor("/LOAD-DB:  Load attempt has been completed./");
  if (!($quiet & 0x1)) {
    print @rslt;
    print "\n";
  }
  exit(0);
}

if (($new_cx ne "") && ($new_cx ne "NA")) {
   die("please set the endpoints for new wanlink cx; $usage")
      unless ((defined $endps) && ($endps ne ""));

   die("please specify two endpoints joined by a comma: end1-A,end1-B; $usage")
      unless ($endps =~ /^\S+,\S+$/);
   my @ends= split(',', $endps);
   $cmd = $utils->fmt_cmd("add_cx", $new_cx, "default_tm", $ends[0], $ends[1]);
   $utils->doCmd($cmd);
   exit(0);
}

if (($new_endp ne "") && ($new_endp ne "NA")) {
   die("please set the resource for new wanlink endpoint; $usage")
      unless ((defined $resource) && ($resource ne ""));
   die("please set latency for new wanlink endpoint; $usage")
      unless ((defined $latency) && ($latency ne ""));
   die("please set drop_pm for new wanlink endpoint; $usage")
      unless ((defined $drop_pm) && ($drop_pm ne ""));
   die("please set port for new wanlink endpoint; $usage")
      unless ((defined $port) && ($port ne ""));

   $wle_flags = "NA" if (($wle_flags == 0) || ($wle_flags eq ""));
   $cpu_id = "NA" if ($cpu_id eq "");
   $description = "NA" if ($description eq "");

   $cmd = $utils->fmt_cmd("add_wl_endp", $new_endp, 1, $resource, $port,
      $latency, $speed, $description, $cpu_id, $wle_flags);
   $utils->doCmd($cmd);

   $cmd = $utils->fmt_cmd("set_wanlink_info", $new_endp, $speed, $latency,
      $max_jitter, $reorder_freq, $extra_buffer, $drop_pm, $dup_pm, $pcap,
      $jitter_freq, $min_drop_amt, $max_drop_amt, $min_reorder_amt,
      $max_reorder_amt, $max_lateness );
   $utils->doCmd($cmd);
   exit(0);
}

if (($switch ne "") && ($switch ne "NA")) {
  $cmd = "set_cx_state all $switch SWITCH";
  $utils->doCmd($cmd);
  exit(0);
}

if ((length($endp_name) == 0) && (length($cx) == 0)) {
  print "ERROR:  Must specify endp or cx name.\n";
  die("$usage");
}

if ((defined $pcap) && ($pcap ne "")&& ($pcap ne "NA")) {
   print STDERR "pcap has value??? [$pcap]\n";
  if ($pcap =~ /^OFF$/i) {
    $cmd = "set_wanlink_pcap $endp_name off";
  }
  else {
    $cmd = "set_wanlink_pcap $endp_name ON $pcap";
  }
  $utils->doCmd($cmd);
  exit(0);
}

if (($state ne "") || ($state ne "NA")){
  $cmd = "set_cx_state all $cx $state";
  $utils->doCmd($cmd);
  exit(0);
}


die ("requires endp_name to be set")
   unless ((defined $endp_name) && ($endp_name ne ""));
# Assumes that the endpoint already exists.
$cmd = Utils::fmt_cmd("set_wanlink_info", $endp_name, $speed, $latency,
   $max_jitter, $reorder_freq, $extra_buffer, $drop_pm, $dup_pm, $pcap,
   $jitter_freq, $min_drop_amt, $max_drop_amt, $min_reorder_amt,
   $max_reorder_amt, $max_lateness );
$utils->doCmd($cmd);

exit(0);
