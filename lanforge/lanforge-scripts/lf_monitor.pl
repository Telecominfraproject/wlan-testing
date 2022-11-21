#!/usr/bin/perl -w
# This program is used to monitor and manage Layer4 connections
#
# Written by Candela Technologies Inc.

use strict;
use warnings;
use Carp;
# Un-buffer output
$| = 1;
use lib '/home/lanforge/scripts';
use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
use Net::Telnet ();
use Getopt::Long;

use constant      NA => "NA";
use constant      NL => "\n";
our $shelf_num        = 1;
our $utils;
# Default values for ye ole cmd-line args.
our $resource         = 1;
our $quiet            = "yes";
our $cx_name          = "";
our $do_cmd           = NA;
our $action           = "show_port";
our $lfmgr_host       = "localhost";
our $lfmgr_port       = 4001;
our $cx_vals          = undef;
our $stop_at          = "";
our $fail_msg         = "";
our $interval         = 10;
our $reqs_sufx        = qq<reqs*|requests*|urls*>;
our $bytes_sufx       = qq<bytes*>;
our $secs_sufx        = qq<secs*|seconds*>;
our $known_suffixes   = qq<$reqs_sufx|$bytes_sufx|$secs_sufx>;

our $rx_bytes   = 0;
our $url_count  = 0;
our $runtime    = 0;
our $is_running = 0;

########################################################################
# Nothing to configure below here, most likely.
########################################################################
# nice but not requested
# show_endp output can be narrowed with key-value arguments
#[--cx_vals {key,key,key,key}]
# Examples:
# --action show_cx --cx_vals MinTxRate,DestMAC,Avg-Jitter

my $usage = "$0  --action { show_cx | watch_cx | list_cx  } ]
                 [--mgr {host-name | IP}]
                 [--mgr_port {ip port}]
                 [--cx_name {name}]
                 [--resource {number}]
                 [--interval {number of seconds}]
                 [--stop_at {[seconds]sec | [requests]req | [transferred]bytes}
                     req can also be: requests reqs url urls
                 [--quiet { yes | no }]

Example:
 $0 --mgr jedtest --action watch_cx --cx_name gl4g00 --interval 2 --stop_at 3urls
";

my $i = 0;

GetOptions
(
        'action|a=s'    => \$action,
        'cx_name|e=s'   => \$cx_name,
        'cx_vals|o=s'   => \$cx_vals,
        'mgr|m=s'       => \$lfmgr_host,
        'mgr_port|p=i'  => \$lfmgr_port,
        'resource|r=i'  => \$resource,
        'quiet|q=s'     => \$quiet,
        'stop_at|s=s'   => \$stop_at,
        'interval|i=i'  => \$interval,
) || do_err_exit("$usage");

if ($do_cmd ne "NA") {
  $action = "do_cmd";
}

if (!(($action eq "show_cx") ||
      ($action eq "watch_cx") ||
      ($action eq "list_cx") ||
      ($action eq "list_ports"))) {
  do_err_exit("Invalid action: $action\n$usage\n");
}

do_err_exit("mgr should not be empty; $usage")                if ("$lfmgr_host" eq "" );
do_err_exit("mgr_port should not be empty; $usage")           if ("$lfmgr_port" eq "" );
do_err_exit("resource should not be empty; $usage")           if ("$resource"   eq "" );

if ($action eq "show_cx") {
   do_err_exit("cx_name should not be empty; $usage")            if ("$cx_name" eq "" );
}
elsif( $action eq "watch_cx") {
   do_err_exit("stop_at should be greater than zero; $usage")    if ("$stop_at" eq "");
   do_err_exit("interval should be greater than zero; $usage")   if ($interval < 1 );
   do_err_exit("cx_name should not be empty; $usage")            if ("$cx_name" eq "" );

   if ($stop_at !~ /^\d+($known_suffixes)$/) {
      do_err_exit("stop_at should not have spaces and should end with $known_suffixes; $usage");
   }
}

## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
sub do_err_exit {
   my $errmsg = shift;
   print $errmsg.NL;
   exit(1);
}

## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
# Open connection to the LANforge server.
# Wait up to 20 seconds when requesting info from LANforge.
sub init {
   my $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/',
            Timeout => 20);

   $t->open(Host    => $lfmgr_host,
            Port    => $lfmgr_port,
            Timeout => 10);

   $t->waitfor("/btbits\>\>/");

   $::utils = new LANforge::Utils();
   $::utils->connect($lfmgr_host, $lfmgr_port);
}
## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
sub stop_cx {
   my $_name = $::cx_name;
   $_name = "CX_".$::cx_name if ( $::cx_name !~ /^CX_/);
   my $result = $utils->doAsyncCmd("set_cx_state default_tm $_name STOPPED");
   print $result.NL;
}
## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
sub summarize_cx {
   my $name          = $::cx_name;
   do_err_exit("please call summarize_cx() with endpoint name") if (!defined $name || "$name" eq "");

   $name          = "CX_".$::cx_name if ( $::cx_name !~ /^CX_/);
   my @lines      = split(NL, $::utils->doAsyncCmd("show_cxe default_tm $name"));

   for my $line (@lines) {
      chomp $line;
      if ( $line =~ /^L4Endp /) {
         ($line =~ /^L4Endp .*? \((\w+)\)/);
         $::is_running = ("$1" eq "RUNNING") ? 1 : 0;
      }
      if ( $line =~ / RunningFor: /) {
         ($::runtime) = ($line =~ / RunningFor: (\d+s) /);
      }
      if ( $line =~ / URLs Processed: / ) {
         ($::url_count) = ($line =~ / Total: (\d+) /);
      }
      if ( $line =~ / Bytes Read: / ) {
         ($::rx_bytes) = ($line =~ / Total: (\d+) /);
      }
   }
}
## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----



## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
##
##    M A I N
##
## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

# begin our connection.
init();

## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
if( $action eq "list_cx") {
   my @lines      = split(NL, $utils->doAsyncCmd("show_endpoints"));
   my $msg        = "";
   my $l4_flag    = 0;
   my $print_flag = 0;
   for my $line (@lines) {
      chomp $line;

      $l4_flag = 1 if ( $line =~ /^L4Endp /);
      next if (! $l4_flag);

      if ( $line =~ /^L4Endp /) {
         ($msg) = ($line =~ /^L4Endp (.*)$/);
      }
      if ( $line =~ /^\s+URL: /) {
         (my $u) = ($line =~ /^\s+URL: \S+ (\S+) /);
         $msg        .= " $u";
         $print_flag    = 1;
      }
      if ( $print_flag ) {
         print $msg . NL;
         $l4_flag       = 0;
         $print_flag    = 0;
         $msg           = '';
      }
   }
   exit 0;
}

## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
if ($action eq "show_cx") {
   my $_name = $::cx_name;
   $_name = "CX_".$::cx_name if ( $::cx_name !~ /^CX_/);
   print $utils->doAsyncCmd("show_cxe default_tm $_name") . NL;
   exit 0;
}

if( $action eq "watch_cx") {
   my $thresh;
   ($thresh) = ( $stop_at =~ /^(\d+)\w+$/);
   do_err_exit("stop_at should be greater than zero; $usage")    if ("$stop_at" eq "");
   do_err_exit("stop_at should be greater than zero; $usage")    if ($thresh    < 1);
   do_err_exit("interval should be greater than zero; $usage")   if ($interval  < 1 );
   do_err_exit("cx_name should not be empty; $usage")            if ("$cx_name" eq "" );

   summarize_cx( $cx_name );
   my $continue = 1;
   while ($continue) {
      sleep $interval;
      summarize_cx( $cx_name );
      print "$cx_name: " .($is_running ? "active":"inactive");
      print " $::runtime, $::url_count urls, $::rx_bytes bytes\n";

      # now check for bailout
      #print "Thresh $thresh | $stop_at | runtime $::runtime urls $::url_count rx $::rx_bytes\n";
      if (  $stop_at =~ /^\d+$secs_sufx$/ ) {
         my ($rtime) = ($::runtime =~ /^(\d+)s/);
         if ($rtime >= $thresh) {
            $continue = 0;
         }
      }
      elsif ( $stop_at =~ /^\d+($reqs_sufx)$/) {
         if ($::url_count >= $thresh) {
            $continue = 0;
         }
      }
      elsif ( $stop_at =~ /^\d+$bytes_sufx*$/ ) {
         if ($::rx_bytes >= $thresh) {
            $continue = 0;
         }
      }
   }
   stop_cx();
   print "connection $cx_name stopped.\n";
}

#eof
