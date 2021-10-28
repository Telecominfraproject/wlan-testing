#!/usr/bin/perl -w
=pod
Use this script to create a large number of L3 connections for emulating video
traffic. This script is going to assume that all the connections are going to
use the same traffic type and same traffic speed. This test will collect all the
L3 connections into a test group.
=cut

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
use lib "./";
use Data::Dumper;
use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
use Net::Telnet ();
use Getopt::Long;

our $quiet           = "yes";
our $lfmgr_host      = "localhost";
our $lfmgr_port      = 4001;
our $resource        = 1;

our $action          = "";
our $vid_mode        = "yt-sdr-1080p30";
our $buffer_size     = (3 * 1024 * 1024);
our $clear_group     = -1;
my $cmd;
our $cx_name         = "";
our $upstream        = "";

our $endp_type       = "tcp";
our $first_sta       = "";
my $log_cli          = "unset"; # use ENV{LOG_CLI} elsewhere
our $num_cx          = -1;
my $show_help        = 0;
our $speed           = 1000 * 1000 * 1000;
our $generic_test_grp;  # we will manage our generic connections using this group (l3_video_em)
our $l3_test_grp;       # the actual Layer 3 cx will live here, starting with _L3_
our $use_ports_str   = "NA";
our $use_speeds_str  = "NA";
our $use_max_speeds  = "NA";

our $usage = <<"__EndOfUsage__";
Usage: $0 # create a large group of Layer 3 creations that emulate video traffic
 --action -a      { create | destroy | start | stop }
 --buffer_size -b {bytes K|M} # size of emulated RX buffer, default 3MB
 --clear_group -z  # empty test group first
 --cx_name -c     {connection prefix}
 --endp_type -t   {tcp|udp|lf_tcp|lf_udp}
 --first_sta -i   {name}
 --log_cli        {1|filename}   # log cli commands
 --mgr -m         {lanforge server} # default localhost
 --mgr_port -p    {lanforge port} # default 4002
 --num_cx -n      {number} # default 1
 --resource -r    {station resource}
 --speed -s       {bps K|M|G} # maximum speed of tx side, default 1Gbps
 --stream --vid_mode -e {stream resolution name|list} # default yt-sdr-1080p30
                  # list of streams maintained in l3_video_em.pl
 --test_grp -g    {test group name} # all connections placed in this group
                  # default is {cx_name}_tg for the Generic connections
                  # we manage Layer 3 connections in _L3_{cx_name}_tg
 --upstream -u    {port short-EID} # video transmitter port;
                  # use 1.1.eth1 or 1.2.br0 for example
                  # upstream port does not need to be on same resource
Examples:
# create 30 stations emulating 720p HDR 60fps transmitted from resource 2:
 $0 --action create --buffer_size 8M --clear_group --cx_name yt1080p60.1 \\
   --endp_type udp --first_sta sta0000 --num_cx 30 \\
   --resource 2 --speed 200M --stream yt-hdr-720p60 --test_group yt60fps \\
   --upstream 1.2.br0

# start test group:
 $0 -a start -g yt60fps

# stop test group:
 $0 -a stop -g yt60fps

# add 30 more stations on resource 3 to group
 $0 -a create -b 8M -c yt1080p60.3 -t udp -i sta0100 -n 30 -r 3 \\
   -s 200M -e yt-hdr-720p60 -g yt60fps -u 1.2.br0

# destroy test group
 $0 -a destroy -g yt60fps
__EndOfUsage__

if (@ARGV < 2) {
   print $usage;
   exit 0;
}
our $debug = 0;
GetOptions
(
   'action|a=s'         => \$::action,
   'buffer_size|b=s'    => \$::buffer_size,
   'clear_group|z'      => \$::clear_group,
   'cx_name|c=s'        => \$::cx_name,
   'debug|d'            => \$::debug,
   'endp_type|type|t=s' => \$::endp_type,
   'first_sta|i=s'      => \$::first_sta,
   'help|h'             => \$show_help,

   'log_cli=s{0,1}'     => \$log_cli,
   'manager|mgr|m=s'    => \$::lfmgr_host,
   'mgr_port|p=i'       => \$::lfmgr_port,
   'num_cx|n=i'         => \$::num_cx,
   'quiet|q=s'          => \$::quiet,
   'resource|r=i'       => \$::resource,
   'speed|s=i'          => \$::speed,
   'stream|vid_mode|e'  => \$::vid_mode,
   'test_group|test_grp|group|g=s'       => \$::generic_test_grp,
   'upstream|u=s'       => \$::upstream,

) || die($::usage);

if ($show_help) {
   print $usage;
   exit 0;
}

if ($::debug) {
  $ENV{DEBUG} = 1 if (!(defined $ENV{DEBUG}));
}

if ($::quiet eq "0") {
  $::quiet = "no";
}
elsif ($::quiet eq "1") {
  $::quiet = "yes";
}

if (defined $log_cli) {
  if ($log_cli ne "unset") {
    # here is how we reset the variable if it was used as a flag
    if ($log_cli eq "") {
      $ENV{'LOG_CLI'} = 1;
    }
    else {
      $ENV{'LOG_CLI'} = $log_cli;
    }
  }
}

our $utils = new LANforge::Utils;

$::utils->connect($lfmgr_host, $lfmgr_port);
#$::utils->doCmd("log_level 8");

# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
#     M  A  I  N
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------

# Apply defaults

if (!(defined $::generic_test_grp) || ("" eq $::generic_test_grp) || ("NA" eq $::generic_test_grp)) {
   # use cx_name as prefix
   if (!(defined $::cx_name) || ("" eq $::cx_name) || ("NA" eq $::cx_name)) {
      die("No test_grp or cx_name is defined. Bye.");
   }
   $::generic_test_grp = $::cx_name ."_tg";
}
$::l3_test_grp = "_L3_".$::generic_test_grp;

# get a list of test groups
my $ra_tg_list = $::utils->test_groups();
print Dumper($ra_tg_list) if ($::debug);

my $ra_l3_cx_names = $::utils->group_items($::l3_test_grp);
my $ra_generic_cx_names = $::utils->group_items($::generic_test_grp);



# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
if (($::clear_group > 0) || ($::action eq "destroy")) {
   if (@$ra_tg_list < 1) {
     print "No test groups defined, bye.";
     exit(1);
   }

   my @matches = grep {/^$::generic_test_grp$/} @$ra_tg_list;

   print Dumper(\@matches) if ($::debug);
   if (@matches < 1) {
     print "No test group matching name [$::generic_test_grp], bye.";
     exit(1);
   }
   print "will clear groups $::generic_test_grp and $::l3_test_grp\n";
   $::utils->doCmd("clear_group $::generic_test_grp");
   $::utils->doCmd("clear_group $::l3_test_grp");
}

# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
if ($::action eq "create") {
   my $re = q(^TestGroup name:\s+).$::generic_test_grp.q(\s+[\[]);
   my @matches = grep {/$re/} @$ra_tg_list;
   print Dumper(\@matches) if ($::debug);
   if (@matches < 1) {
     print "Creating test group [$::generic_test_grp]...";
     $::utils->doCmd($::utils->fmt_cmd("add_group", $::generic_test_grp));
     print "Creating test group [$::l3_test_grp]...";
     $::utils->doCmd($::utils->fmt_cmd("add_group", $::l3_test_grp));
   }

   if (!(defined $::cx_name) or ("" eq $::cx_name)) {
     $::cx_name = $::generic_test_grp."-";
   }
   if (!(defined $::buffer_size) or ($::buffer_size < 0)) {
     print ("Please set --buffer_size, bye.");
     exit(1);
   }
   if (!(defined $::endp_type) or ("" eq $::endp_type)) {
     print ("Please set --endp_type {tcp|udp}");
   }
   elsif ($::endp_type eq "tcp") {
     $::endp_type = "lf_tcp";
   }
   elsif ($::endp_type eq "udp") {
     $::endp_type = "lf_udp";
   }
   if ($::num_cx < 1) {
     print "How many connections should we create? --num_cx 1? Bye.\n";
     exit(1);
   }
   if (!(defined $::first_sta) or ("" eq $::first_sta)) {
     print "Please set first station name: --first_sta 200; bye.";
     exit(1);
   }
   if (!(defined $::upstream) or ("" eq $::upstream)) {
     print "Please set your upstream port: --upstream 1.1.eth1; bye.";
     exit(1);
   }
   elsif ($::upstream !~ /^1.\d+\.\S+$/) {
     print "Upstream port should be named 1.<resource>.<name>\n EG: --upstream 1.1.eth1\nbye.";
     exit(1);
   }

   if ( ! -x "./lf_firemod.pl" ) {
     print "I don't see ./lf_firemod.pl, bye.";
     exit(1);
   }
   my $upstream_resource = $::resource;
   my $rh_eid_map = $::utils->get_eid_map($::resource);
   die("Unable to find keys in rh_eid_map") if ((keys(%$rh_eid_map)) < 1);

   my $rh_upstream_map = $rh_eid_map;
   if ($::upstream !~ /^1\.$::resource\.\S+$/) {
     $upstream_resource = (split('.', $::upstream))[1];
     if (!(defined $upstream_resource) || ("" eq $upstream_resource)) {
       die("Problem with upstream resource name");
     }
     $rh_upstream_map = $::utils->get_eid_map($upstream_resource);
   }
   #print Dumper($rh_eid_map);

   # build a list of ports -n ports long starting at -first_port
   my @ports = ();
   my $rh_first_dev = $::utils->find_by_name($rh_eid_map, $::first_sta);
   die("Unable to find dev record for port $::first_sta on resource $::resource")
     if ($rh_first_dev == -1);
   my $parent_name = $rh_first_dev->{parent};
   die("Unable to find parent of $::first_sta, bye.")
     if (!(defined $parent_name));
   my $ra_interfaces = $::utils->ports_on_radio($rh_eid_map, $parent_name);
   while (@$ra_interfaces < $::num_cx) {
      # hack wiphy names
      my ($wi, $nu) = $parent_name =~ /^([a-z]+)(\d+)$/;
      $nu = 1 + $nu;
      $parent_name = "${wi}${nu}";
      my $ra_more = $::utils->ports_on_radio($rh_eid_map, $parent_name);
      push(@$ra_interfaces, @$ra_more);
   }
   die("Unable to find any subinterfaces of $parent_name")
     if (@$ra_interfaces < 1);

   # want a pattern that matches Qvlan and Mvlan patterns, not just stations
   # things like eth1.3 or rd0#0 or r0b#0
   my ($prefix) = $::first_sta =~ /^(.*?[^0-9]+)\d+$/i;
   #print "PREFIX IS $prefix\n";
   my @selected_list = ();

   foreach my $iface (sort @$ra_interfaces) {
     #print "iface[$iface] ";
     next if ($iface !~ /^$prefix/);
     push(@selected_list, $iface);
     last if (@selected_list >= $::num_cx);
   }
   if (@selected_list != $::num_cx) {
      my $a = @selected_list;
      print "Number of interfaces($a) does not match number of connections($::num_cx).\n"
         ." You probably don't have as many interfaces as you think.\n";
      sleep 5;
   }

   my @next_cmds = ();
   for (my $i=0; $i < @selected_list; $i++) {
     my $j = 10000 + $i;
     my $cname = "_".$::cx_name . substr("$j", 1);
     my $ports = join('.', 1, $::resource, $selected_list[$i]).",".$::upstream;

     #print "Connection name $name uses $ports\n";
     my $cmd = qq(/home/lanforge/scripts/lf_firemod.pl --mgr $::lfmgr_host --mgr_port $::lfmgr_port )
      .qq(--action create_cx --cx_name $cname --endp_type $::endp_type )
      .qq(--use_ports $ports --use_speeds 0,0 --report_timer 3000);
     #print "CMD: $cmd\n";
     `$cmd`;
     push(@next_cmds, "set_endp_flag $cname-A AutoHelper 1");
     push(@next_cmds, "set_endp_flag $cname-B AutoHelper 1");
     push(@next_cmds, $::utils->fmt_cmd("add_tgcx", $::l3_test_grp, $cname));
   }
   sleep 1;
   $::utils->doAsyncCmd("nc_show_endpoints all"); # this helps prepare us for adding next generic connections
   print "adding L3 CX to $::l3_test_grp ";
   for my $cmd (@next_cmds) {
      print ".";
      $::utils->doCmd($cmd);
   }
   print "done\n";
   print "Creating Generic connections for video emulation ";
   $::utils->sleep_ms(20);
   @next_cmds = ();
   for (my $i=0; $i < @selected_list; $i++) {
        my $j = 10000 + $i;
        my $cname = "_".$::cx_name . substr("$j", 1);
        my $ports = join('.', 1, $::resource, $selected_list[$i]).",".$::upstream;

     my $gname = $::cx_name . substr("$j", 1);
     my $gnr_cmd = qq(/home/lanforge/scripts/l3_video_em.pl --mgr $::lfmgr_host --mgr_port $::lfmgr_port )
            .qq(--cx_name $cname --max_tx 1G --buf_size $::buffer_size )
            .qq(--stream $::vid_mode --quiet yes );

     $cmd = qq(./lf_firemod.pl --mgr $::lfmgr_host --mgr_port $::lfmgr_port)
               .qq( --action create_endp --endp_name $gname --endp_type 'generic')
               .qq( --port_name ).$selected_list[$i]
               .q( --endp_cmd ").$gnr_cmd.q(");
     `$cmd`;
     print ".";
     $::utils->sleep_ms(20);
     #print "adding CX_$gname to $::generic_test_grp\n";
     push(@next_cmds, $::utils->fmt_cmd("add_tgcx", $::generic_test_grp, "CX_".$gname));
   }
   print "done\n";
   sleep 1;
   $::utils->doAsyncCmd("nc_show_endpoints all"); # this helps prepare us for adding next generic connections
   print "Adding generic connections to $::generic_test_grp ";
   for my $cmd (@next_cmds) {
      print ".";
      $::utils->doCmd($cmd);
   }
   print "done\n";

   exit 0;
}
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
if ($::action eq "destroy") {
   my @cmds = ();
   if (@$ra_generic_cx_names < 1) {
      print "No layer 3 connections in group [$::generic_test_grp], bye\n";
   }
   else {
      print "Removing generic connections ";
      foreach my $cx_name (@$ra_generic_cx_names) {
         push(@cmds, "rm_cx default_tm ".$cx_name);
      }
      foreach my $cx_name (@$ra_generic_cx_names) {
         $cx_name =~ s/^CX_/D_/;
         push(@cmds, "rm_endp ".$cx_name);
         $cx_name =~ s/^D_//;
         push(@cmds, "rm_endp ".$cx_name);
      }
      foreach my $cmd (@cmds) {
         print ".";
         $::utils->doCmd($cmd);
         $::utils->sleep_ms(30);
      }
      print "done\n";
   }
   $::utils->doCmd("rm_group $::generic_test_grp");

   if (@$ra_l3_cx_names < 1) {
      print "No layer 3 connections in group [$::l3_test_grp], bye\n";
   }
   else {
      print "Removing L3 endpoints ";
      @cmds = ();
      foreach my $cx_name (@$ra_l3_cx_names) {
         push(@cmds, "rm_cx default_tm ".$cx_name);
      }
      foreach my $cx_name (@$ra_l3_cx_names) {
         push(@cmds, "rm_endp ${cx_name}-A");
         push(@cmds, "rm_endp ${cx_name}-B");
      }
      foreach my $cmd (@cmds) {
         print ".";
         $::utils->doCmd($cmd);
         $::utils->sleep_ms(30);
      }
      print "done\n";
   }
   $::utils->doCmd("rm_group $::l3_test_grp");
   exit 0;
}
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
if ($::action eq "start") {
   if (!(defined $::generic_test_grp) || ("" eq $::generic_test_grp)) {
     print "Please specify test group to start: --test_grp foo; bye.";
     exit(1);
   }

   # collect all cx names in the test group and start up the
   # video pulser on them
   print "Starting connections...";
   $::utils->doCmd("start_group $::l3_test_grp");
   sleep 1;
   $::utils->doCmd("start_group $::generic_test_grp");

   exit 0;
}
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
if ($::action eq "stop") {
   if (!(defined $::generic_test_grp) || ("" eq $::generic_test_grp)) {
     print "Please specify test group to stop: --test_grp foo; bye.";
     exit(1);
   }

   # collect all cx names in the test group and start up the
   # video pulser on them
   print "Stopping connections...";
   $::utils->doCmd("stop_group $::generic_test_grp");
   sleep 1;
   $::utils->doCmd("stop_group $::l3_test_grp");
   exit 0;
}
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
else {
   die "What kind of action is [$::action]?";
}

# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
#END {
#   if (defined $::utils->{telnet}) {
#      print STDERR "reducing log level";
#      $::utils->doCmd("log_level 2");
#   }
#}