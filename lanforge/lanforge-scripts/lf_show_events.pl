#!/usr/bin/perl -w
# This program is used to create a hunt-script 
# # used for matrix load emulation on LANforge
# # (C) Candela Technologies 2015

use strict;
use warnings;
#use Carp;
#$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };

# Un-buffer output
$| = 1;
use lib '/home/lanforge/scripts';
use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
use Net::Telnet ();
use Getopt::Long;


# Default values for ye ole cmd-line args.
#our $resource         = 1;
our $quiet            = "yes";
our $lfmgr_host       = "localhost";
our $lfmgr_port       = 4001;
our $do_clear         = 0;
our $do_alerts        = 0;
# ########################################################################
# # Nothing to configure below here, most likely.
# ########################################################################
our $usage = qq($0 ...
   [--mgr          {host-name | IP}]
   [--mgr_port     {ip port}]
   [--resource     {number}]
   [--quiet        { yes | no }]
   [--clear]       # or -c; clear events. Alerts cannot be cleared.
   [--alerts]      # or -a; show alerts instead of events
);
my $i = 0;
my $cmd;
die($::usage) if (@ARGV < 2);

GetOptions
(
     'mgr|m=s'          => \$::lfmgr_host,
     'mgr_port|p=i'     => \$::lfmgr_port,
     'quiet|q=s'        => \$::quiet,
     'alerts|a'         => \$::do_alerts,
     'clear|c'          => \$::do_clear,
) || die("$::usage");

my $utils = new LANforge::Utils();
my $t     = new Net::Telnet(Prompt => '/default\@btbits\>\>/',
                           Timeout => 20);
$t->open( Host    => $lfmgr_host,
          Port    => $lfmgr_port,
          Timeout => 10);
$t->waitfor("/btbits\>\>/");

$utils->telnet($t);
if ($quiet eq "yes") {
  $utils->cli_send_silent(1);
  $utils->cli_rcv_silent(1);
}
else {
  $utils->cli_send_silent(0);
  $utils->cli_rcv_silent(0);
}

if ($do_alerts) {
  print $utils->doAsyncCmd("show_alerts");
}
else {
  print $utils->doAsyncCmd("show_events");
}
print "\n";

if ($do_clear) {
   $utils->doAsyncCmd("rm_event all");
}

exit(0);
#
