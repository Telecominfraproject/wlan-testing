#!/usr/bin/perl

# This program is used to modify the LANforge attenuator (through
# the LANforge manager/server processes.

# Written by Candela Technologies Inc.
#  Udated by:
#
#

use strict;

# Un-buffer output
$| = 1;

use lib '/home/lanforge/scripts';
use LANforge::Utils;
use Net::Telnet ();
use Getopt::Long;
my $shelf_num = 1;

# Default values for ye ole cmd-line args.


my $resource = 1;
my $quiet = "yes";
my $atten_serno = "";
my $atten_idx = "";
my $atten_val = "";
my $action = "show_atten";
my $do_cmd = "NA";
my $lfmgr_host = "localhost";
my $lfmgr_port = 4001;


my $fail_msg = "";
my $manual_check = 0;

########################################################################
# Nothing to configure below here, most likely.
########################################################################

my $usage = "$0  --action { show_atten | set_atten | do_cmd } ]
                 [--mgr {host-name | IP}]
                 [--mgr_port {ip port}]
                 [--cmd {lf-cli-command text}]
                 [--atten_serno {serial-num}]
                 [--atten_idx { attenuator-module-index | all}]
                 [--atten_val {0-950 dDbm}]
                 [--quiet { yes | no }]

Example:
 $0 --mgr 192.168.100.138 --action set_atten --atten_serno 3 --atten_idx all --atten_val 550\n";

my $i = 0;
my $show_help = 0;

if (@ARGV < 2) {
   print $usage;
   exit 0;
}
GetOptions 
(
   'help|h'          => \$show_help,
   'atten_serno|s=s' => \$atten_serno,
   'atten_idx|i=s'   => \$atten_idx,
   'atten_val|v=s'   => \$atten_val,
   'action|a=s'      => \$action,
   'cmd|c=s'         => \$do_cmd,
   'mgr|m=s'         => \$lfmgr_host,
   'mgr_port|p=i'    => \$lfmgr_port,
   'resource|r=i'    => \$resource,
   'quiet|q=s'       => \$quiet,

) || (print($usage) && exit(1));

if ($show_help) {
   print $usage;
   exit 0;
}

if ($do_cmd ne "NA") {
  $action = "do_cmd";
}

if (!(($action eq "show_atten") ||
      ($action eq "set_atten") ||
      ($action eq "do_cmd"))) {
  die("Invalid action: $action\n$usage\n");
}

if ($action eq "set_atten") {
  if ((length($atten_serno) == 0) ||
      (length($atten_val) == 0) ||
      (length($atten_idx) == 0)) {
    print "ERROR:  Must specify atten_serno, atten_idx, and atten_val when setting attenuator.\n";
    die("$usage");
  }
}

# Open connection to the LANforge server.
# Configure our utils.
my $utils = new LANforge::Utils();
$utils->connect($lfmgr_host, $lfmgr_port);
if ($quiet eq "yes") {
  $utils->cli_send_silent(1); # Do show input to CLI
  $utils->cli_rcv_silent(1);  # Repress output from CLI ??
}
else {
  $utils->cli_send_silent(0); # Do show input to CLI
  $utils->cli_rcv_silent(0);  # Repress output from CLI ??
}

if ($action eq "show_atten") {
  print $utils->doAsyncCmd("show_atten $shelf_num $resource $atten_serno");
}
elsif ($action eq "set_atten") {
  print $utils->doAsyncCmd("set_atten $shelf_num $resource $atten_serno $atten_idx $atten_val") . "\n";
}
elsif ($action eq "do_cmd") {
  print $utils->doAsyncCmd("$do_cmd") . "\n";
}
else {
  die("Unknown action: $action\n$usage\n");
}

exit(0);
