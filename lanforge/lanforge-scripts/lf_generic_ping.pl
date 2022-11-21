#!/usr/bin/perl -w
#
# Use this script to generate a batch of Generic lfping endpoints
#
# Examples:
# ./lf_generic_ping.pl --mgr 192.168.1.100 --resource 1 --dest 10.1.1.1 -i wlan0 -i sta1 -i eth1
# You should be able to place 1000 interfaces in the list
#
# Or all interfaces on a radio
# ./lf_generic_ping.pl --mgr $mgr --resource 1 --dest 10.1.1.1 --radio wiphy0
#
# Or all macvlan on an ethernet port
# ./lf_generic_ping.pl --mgr $mgr --resource 1 --dest 10.1.1.1 --parent eth1
#
# Or all interfaces matching a prefix:
# ./lf_generic_ping.pl -m $mgr -r 1 -d 10.1.1.1 --match sta3
#
# The default name will be lfping_$endp name, use the --name
# switch to alter the generic endpoint name, This allows multiple
# generic connections to be created per port:
#
# for n in one two three four five six seven eight nine ten; do
#  ./lf_generic_ping.pl -m 192.168.1.100 -r 1 -d 10.1.1.1 --match sta -name $n
# done
package main;
use strict;
use warnings;
use diagnostics;
use Carp;
use Data::Dumper;
$SIG{ __DIE__ }   = sub { Carp::confess( @_ )};
$SIG{ __WARN__ }  = sub { Carp::confess( @_ )};
use Getopt::Long;
use Cwd qw(getcwd);
my $cwd = getcwd();

# use lib prepends to @INC, so put lower priority first
# This is before run-time, so cannot condition this with normal 'if' logic.
use lib '/home/lanforge/scripts';
use lib "./";

use List::Util qw(first);
use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils qw(fmt_cmd);
use Net::Telnet ();

our $dest_ip_addr = "0.0.0.0";
our $log_cli = "unset"; # use ENV{'LOG_CLI'}

our $usage = qq(Usage:
$0 --mgr {host-name | IP}
   --mgr_port {ip port}
   --resource {resource}
   --dest {destination IP}
   --interface|-intf|-int|-i {source interface}
    # You should be able to place 1000 interfaces in the list
   --radio {wiphy} | --parent {eth}
   --match {simple prefix, no stars or questions marks}
   --cmd {"double quoted command"} # can contain special parameters
   --name {prefix to name connection, appended with padded number}

 Examples:
  $0 --mgr localhost --resource 1 --dest 192.168.0.1 -i wlan0 -i sta3000 --name "wlan_ping"
  This will match just sta3000

 All interfaces on a parent radio or MAC VLANs on parent Ethernet port:
  $0 --mgr localhost --resource 1 --dest 192.168.0.1 --radio wiphy0
  This will match all stations whos parent is wiphy0: sta3 wlan0

  $0 --mgr localhost --resource 1 --dest 192.168.0.1 --parent eth1
  This will match all MAC VLANs with parent eth1: eth1#0 eth1#1 eth1#2

 All interfaces matching a prefix:
  $0 -m localhost -r 1 -d 192.168.0.1 --match sta3
  This will match sta3 sta30 sta31 sta3000

 Please don't put single quotes in a command. A command can have these expansions:
   %d destination ip or hostname
   %i port IPv4 address
   %p port name

 Example with curl wrapper provides better feedback to LANforge:
 $0 --mgr cholla-f19 -r 2 -n curl_ex_ --match 'eth2#' \\
   --cmd './scripts/lf_curl.sh -n 10 -o /tmp/curl_%p.out -i %i -p %p -d %d' --dest http://localhost/

 Example curl command doesn't provide good feedback to LANforge:
 $0 --cmd "curl -sqL --dns-ipv4-addr %i --dns-interface %p \\
   --interface %p --localaddr %i -o /tmp/results-%p http://%d/"

 The default name of the generic endpoints given will be "lfping_[port]".
 You can create multiple generic connections per port by altering
 the endpoint name with the --name switch.
 Example of creating multiple connections per port in a loop:
  for n in one two three four five six seven eight nine ten; do
   $0 -m localhost -r 1 -d 10.1.1.1 --match sta -name \$n
  done

 Example iperf3 server on eth1, 10.1.1.2:
      iperf3 --forceflush --format k --precision 4 -s \\
        --bind_dev %p -i 1 --pidfile /tmp/lf_helper_iperf_%p.pid

 Example iperf3 client on sta0 as 10.1.1.3:
      iperf3 --forceflush --format k --precision 4 -c %d -t 60 --tos 0 -b 1K \\
        --bind_dev %p -i 1 --pidfile /tmp/lf_helper_iperf_%p.pid

 If only a few of your generic commands start, check journalctl for
 errors containing: 'cgroup: fork rejected by pids controller'
 You want to set DefaultTasksMax=65535 in /etc/systemd/system.conf
 then do a systemctl daemon-reload.
 https://www.novell.com/support/kb/doc.php?id=7018594
);

our $shelf_num    = 1;
our $report_timer = 1000;
our $test_mgr     = "default_tm";
our $resource     = 1;
our $lfmgr_host   = "localhost";
our $lfmgr_port   = 4001;
our $quiet        = "yes";
our $quiesce      = 3;
our $clear_on_start = 0;
our $dest_ip;
our @interfaces   = ();
our $radio        = '';
our $pattern      = '';
our $name_pref    = "lfping";
our $ref_cmd      = ''; # user supplied command
our $ref_name     = '';
our $verbose      = ((defined $ENV{'DEBUG'}) && ($ENV{'DEBUG'} eq "1")) ? 1:0;
my $help;

if (@ARGV < 2) {
   print $usage;
   exit 0;
}
GetOptions
(
  'mgr|m=s'                   => \$::lfmgr_host,
  'mgr_port|p=i'              => \$::lfmgr_port,
  'resource|r=i'              => \$::resource,
  'quiet|q'                   => \$::quiet,
  'verbose|v'                 => \$::verbose,
  'radio|parent|o=s'          => \$::radio,
  'match=s'                   => \$::pattern,
  'interface|intf|int|i=s'    => \@::interfaces,
  'dest_ip|dest|d=s'          => \$::dest_ip,
  'name_pref|name|n=s'        => \$::name_pref,
  'cmd|c=s'                   => \$::ref_cmd,
  'help|h|?'                  => \$help,
) || (print($usage), exit(1));

#print "radio: $::radio, match: $::pattern, $::quiet, $::resource, $::dest_ip\n";

if ($help) {
   print($usage) && exit(0);
}
if ($::quiet eq "0") {
   $::quiet = "no";
}
elsif ($::quiet eq "1") {
   $::quiet = "yes";
}

# Open connection to the LANforge server.
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

# Configure our utils.
our $utils = new LANforge::Utils();
$::utils->connect($lfmgr_host, $lfmgr_port);
# $utils->telnet($t);         # Set our telnet object.

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

our @ports_lines = split("\n", $::utils->doAsyncCmd("nc_show_ports 1 $::resource ALL"));
chomp(@ports_lines);
our %eid_map = ();
my ($eid, $card, $port, $type, $mac, $dev, $parent, $ip);
foreach my $line (@ports_lines) {
  # collect all stations on that radio add them to @interfaces
  if ($line =~ /^Shelf: /) {
    $card = undef; $port = undef;
    $type = undef; $parent = undef;
    $eid = undef; $mac = undef;
    $dev = undef;
    $ip = undef;
  }

  # careful about that comma after card!
  # NO EID for Shelf: 1, Card: 1, Port: 2  Type: WIFI-Radio  Alias:
  ($card, $port, $type) = $line =~ m/^Shelf: 1, Card: (\d+),\s+Port: (\d+)\s+Type: (\w+)/;
  if ((defined $card) && ($card ne "") && (defined $port) && ($port ne "")) {
    $eid = "1.${card}.${port}";
    my $rh_eid = {
      eid => $eid,
      type => $type,
      parent => undef,
      dev => undef,
    };
    $::eid_map{$eid} = $rh_eid;
    #print "\nfound eid $eid\n";
  }
  #elsif ($line =~ /^Shelf/) {
  #  #print "NO EID for $line\n";
  #}

  if (!(defined $eid) || ($eid eq "")) {
    #print "NO EID for $line\n";
    next;
  }
  ($mac, $dev) = $line =~ / MAC: ([0-9:a-fA-F]+)\s+DEV: (\S+)/;
  if ((defined $mac) && ($mac ne "")) {
   #print "$eid MAC: $line\n";
    $::eid_map{$eid}->{mac} = $mac;
    $::eid_map{$eid}->{dev} = $dev;
  }

  ($parent) = $line =~ / Parent.Peer: (\S+) /;
  if ((defined $parent) && ($parent ne "")) {
    #print "$eid PARENT: $line\n";
    $::eid_map{$eid}->{parent} = $parent;
  }

  ($ip) = $line =~ m/ IP: *([^ ]+) */;
  if ((defined $ip) && ($ip ne "")) {
    #print "$eid IP: $line\n";
    $::eid_map{$eid}->{ip} = $ip;
  }
} # foreach

#foreach $eid (keys %eid_map) {
#  print "eid $eid ";
#}


if (defined $::radio) {
  while (my ($eid, $rh_eid) = each %::eid_map) {
    if ((defined $rh_eid->{parent}) && ($rh_eid->{parent} eq $::radio)) {
      push(@interfaces, $rh_eid->{dev});
    }
  }
}

if (defined $::pattern && $pattern ne "") {
   my $pat = $::pattern;
   $pat =~ s/[+]//g;
   # collect all stations on that resource add them to @interfaces
   while (my($eid, $rh_eid) = each %::eid_map) {
     if ((defined $rh_eid->{dev}) && ($rh_eid->{dev} =~ /$pat/)) {
       push(@interfaces, $rh_eid->{dev});
     }
   }
}

if (@interfaces < 1) {
   print STDERR "One or more interfaces required.\n";
   print $usage;
   exit(1);
}

print "Creating generic lfping endpoints using these interfaces: \n";
print " ".join(", ", @interfaces)."\n";

=pod
Example of generic created by GUI:
   add_gen_endp test-1 1 3 sta3000 gen_generic
   set_gen_cmd test-1 lfping  -p deadbeef -I sta3000 10.41.1.2
   set_endp_quiesce test-1 3
   set_endp_report_timer test-1 1000
   set_endp_flag test-1 ClearPortOnStart 0
   add_gen_endp D_test-1 1 3 sta3000 gen_generic
   set_endp_flag D_test-1 unmanaged 1
   set_endp_quiesce D_test-1 3
   set_endp_report_timer D_test-1 1000
   set_endp_flag D_test-1 ClearPortOnStart 0

Parameters that can be replaced:
   %d destination ip or hostname
   %i port IPv4 address
   %p port name

   curl -sqL --dns-ipv4-addr %i --dns-interface %p --interface %p --localaddr %i -o /dev/null http://%d/

=cut
sub create_generic {
   my ($name, $port_name, $eid)=@_;
   #print "= 1 =====================================================\n";
   #print Dumper($eid);
   my $endp_name = "${name_pref}_${port_name}";
   my $type = "gen_generic";
   my $rh_idr = $::eid_map{$eid};
   my $port_ip = $rh_idr->{'ip'};
   #print Dumper($rh_idr);
   #print Dumper($rh_idr->{'ip'});
   #print "$endp_name PORT_IP $port_ip \n";
   #print "= 2 =====================================================\n";
   my $ping_cmd = "lfping -I $port_name $::dest_ip";
   if ((defined $::ref_cmd) && ($::ref_cmd ne "")) {
      $ping_cmd = $::ref_cmd;
      my $d_ip = '';
      $d_ip = $::dest_ip if (defined $::dest_ip && $::dest_ip ne "");
      $ping_cmd =~ s/%d/$::dest_ip/g if ($ping_cmd =~ /%d/);

      if (defined $port_name && $port_name ne "") {
         $ping_cmd =~ s/%p/$port_name/g if ($ping_cmd =~ /%p/);
      }
      else {
         print "no name for port $port_name\n";
         return;
      }

      if (defined $port_ip && $port_ip ne "") {
         $ping_cmd =~ s/%i/$port_ip/g if ($ping_cmd =~ /%i/);
      }
      else {
         print "no ip for port $port_name\n";
         return;
      }
   }
   $::command_map{$eid} = $ping_cmd;

   print "CMD: $ping_cmd\n" if ($::verbose);

   $::utils->doCmd($::utils->fmt_cmd("add_gen_endp", $endp_name, 1, $::resource, $port_name, $type));
   $::utils->doCmd("set_gen_cmd $endp_name $ping_cmd");
   $::utils->doCmd("set_endp_quiesce $endp_name $::quiesce");
   $::utils->doCmd("set_endp_flag $endp_name ClearPortOnStart $::clear_on_start");
   $::utils->doCmd("set_endp_report_timer $endp_name $::report_timer");

   # we also need to add the opposite unmanaged endpoint
   $::utils->doCmd("add_gen_endp D_$endp_name 1 $::resource $port_name gen_generic");
   $::utils->doCmd("set_endp_flag D_$endp_name unmanaged 1");
   $::utils->doCmd("set_endp_quiesce D_$endp_name $::quiesce");
   $::utils->doCmd("set_endp_flag D_$endp_name ClearPortOnStart $::clear_on_start");
   $::utils->doCmd("set_endp_report_timer D_$endp_name $::report_timer");

   # tie the knot with a CX
   $::utils->doCmd("add_cx CX_$endp_name default_tm $endp_name D_$endp_name");
   $::utils->doCmd("set_cx_report_timer default_tm CX_$endp_name $::report_timer cxonly");
}

#print Dumper(\@interfaces);
#print Dumper(\%::eid_map);
our %command_map = ();
my @map_keys = sort keys %eid_map;
for my $port (sort @interfaces) {
   my $endp_name = "${name_pref}_$port";
   my $matching_eid = "";
   #print "Searching for port $port ";
   #while (my ($eid, $rh_pid) = each %eid_map) {
   for my $eid (@map_keys) {
      my $rh_pid = $eid_map{$eid};
      #print " $port/$rh_pid->{dev} ";
      if ("$port" eq "$rh_pid->{dev}") {
         #print " ** ";
         $matching_eid = $eid;
         last;
      }
   }
   if ($matching_eid eq "") {
      print "\nSkipping $port no eid [$matching_eid]\n";
      next;
   }
   #print "\n= 3 =====================================================\n";
   #print " $matching_eid => ".$eid_map{$matching_eid}->{dev}."\n";
   #print Dumper($eid_map{$matching_eid});
   #print "= 4 =====================================================\n";


   if (! (defined $eid_map{$matching_eid}->{ip})
      || $eid_map{$matching_eid}->{ip} eq ""
      || $eid_map{$matching_eid}->{ip} eq "0.0.0.0") {
      print "\nSkipping $port: ".$eid_map{$matching_eid}->{ip}."\n";
      sleep 1;
      next;
   }
   create_generic($endp_name, $port, $matching_eid);
}
#print Dumper(\%command_map);

#
