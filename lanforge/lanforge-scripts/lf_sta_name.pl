#!/usr/bin/perl -w
#
# This program is used to modify the LANforge virtual station aliases
#
# (C) 2016 Candela Technologies Inc.
#

use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };

# Un-buffer output
$| = 1;

use lib '/home/lanforge/scripts';
use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
use Net::Telnet ();
use Getopt::Long;
our $shelf_num     = 1;
our $resource      = 1;
our $quiet         = "yes";
our $do_cmd        = "NA";
our $lfmgr_host    = "localhost";
our $lfmgr_port    = 4001;

########################################################################
# Nothing to configure below here, most likely.
########################################################################
our $usage = qq<
$0  --action { set_alias | reset_alias } ]
     [--mgr          {host-name | IP} default: $::lfmgr_host]
     [--resource     {lanforge resource id}]
     [--mgr_port     {ip port}]

     [--first_dev    {actual device name with suffix number}]
     [--last_dev     {actual device name with suffix number}]
     [--new_prefix   {phrase to replace 'sta' with}]
     [--old_prefix   {old prefix}]
     [--quiet { yes | no }]
      # spaces and punctuation are prohibitied in aliases!
      
Examples:
   # alias sta100-sta149 as truck100-truck149
 $0 --mgr 192.168.100.138 --action set_alias --first_dev sta100 --last_dev sta149 --new_prefix truck
 
   # reset truck* stations to original sta* names
 $0 --mgr 192.168.100.138 --action reset_alias --old_prefix truck
 
   # reset a series of station aliases to original names
 $0 --mgr 192.168.100.138 --action reset_alias --first_sta truck100 --last_sta truck110
>;

GetOptions 
(
  'action|a=s'       => \$::action,
  'cmd|c=s'          => \$::do_cmd,
  'mgr|m=s'          => \$::lfmgr_host,
  'mgr_port|p=i'     => \$::lfmgr_port,
  'resource|r=i'     => \$::resource,
  'quiet|q=s'        => \$::quiet,
  'new_prefix=s'     => \$::new_prefix,
  'old_prefix=s'     => \$::old_prefix,
  'first_dev=s'      => \$::first_dev,
  'last_dev=s'       => \$::last_dev,
) || (print($usage) && exit(1));

die ("Please specify manager address. $::usage")
   if (!defined $::lfmgr_host || "$::lfmgr_host" eq "" );
   
die ("Please specify resource id. $::usage")
   if (!defined $::resource || "$::resource" eq "" );

die ("Please tell me what to do with --action. " )
   if (!defined $::action || "$::action" eq "");
   
if ($::action eq "set_alias" ) {
   die( "Please specify the first station device. $::usage") 
      if (!defined $::first_dev || "$::first_dev" eq "" );
   die( "Please specify the last station device. $::usage") 
      if (!defined $::last_dev || "$::last_dev" eq "" );
   die( "Please specify the new prefix. $::usage") 
      if (!defined $::new_prefix || "$::new_prefix" eq "" );
}
elsif ($::action eq "reset_alias" && !defined $::first_dev) {
   die( "Please specify the old prefix. $::usage")
      if (!defined $::old_prefix || "$::old_prefix" eq "");
}


# Open connection to the LANforge server.

our $telnet = new Net::Telnet(Prompt => '/default\@btbits\>\>/',
         Timeout => 20);

$::telnet->open( Host    => $::lfmgr_host,
          Port    => $::lfmgr_port,
          Timeout => 10);

$::telnet->waitfor("/btbits\>\>/");


# Configure our utils.
our $utils = new LANforge::Utils();
$::utils->telnet($::telnet);         # Set our telnet object.
if ($::quiet eq "yes") {
   $::utils->cli_send_silent(1); # Do show input to CLI
   $::utils->cli_rcv_silent(1);  # Repress output from CLI ??
}
else {
   $utils->cli_send_silent(0); # Do show input to CLI
   $utils->cli_rcv_silent(0);  # Repress output from CLI ??
}

my $in_bounds = 0;
my @port_names = ();
my @sorted_names;
my @matching_devices = ();
my %port_map = ();
my $port_name;
my $port;
my $cmd;
my $alias;
my @ports;
if ($::action eq "set_alias" || $::action eq "reset_alias") {
   @ports = $::utils->getPortListing($::shelf_num, $::resource);
}
else {
   die("Actions are set_alias and reset_alias.");
}

for (my $i = 0; $i<@ports; $i++) {
   $port_name              = $ports[$i]->dev();
   push(@port_names, $port_name);
   $port_map{ $port_name } = $i;
}
@sorted_names = sort { lc($a) cmp lc($b) } @port_names;
for $port_name (@sorted_names) {
   my $i    = $port_map{ $port_name };
   $port    = $ports[ $i ];
   $alias   = $port->alias();
   if (defined $::first_dev && defined $::last_dev) {
      if ($port_name eq $::first_dev || $alias eq $::first_dev) {
         $in_bounds = 1;
      }
      if ($in_bounds) {
         push(@matching_devices, $port);
      }
      if ($port_name eq $::last_dev || $alias eq $::last_dev) {
         $in_bounds = 0;
      }
   }
   if (defined $::old_prefix && "$::old_prefix" ne "") {
      print "\nchecking $port_name ($alias)" if ($quiet eq "no");
      if ($alias =~ /^$::old_prefix\d+/) {
         print "* " if ($quiet eq "no");
         push(@matching_devices, $port);
      }
   }
}

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- # 
## Note that alias is for mvlans, nothing will be found              #
## $cmd = $::utils->fmt_cmd("set_port_alias", $::shelf_num,          #
##                         $::resource, $parname, $mac, $alias);     #
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

for $port (@matching_devices) {
   $port_name     = $port->dev();
   my $portno     = $port->port_id();
   my ($suffix)   = $port_name =~/^.*?(\d+)$/;

   if ($::action eq "set_alias" ) {
      $alias      = "$::new_prefix$suffix";
   }
   else {
      $alias      = $port->dev();
   }
   # set_port shelf resource port ip_addr netmask gateway 
   # cmd_flags current_flags MAC MTU tx_queue_len alias interest
   $cmd = $::utils->fmt_cmd("set_port", $::shelf_num, $::resource, $portno,
                           "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA",
                           $alias, 0x1000);
   $::utils->doCmd($cmd);
}

#
