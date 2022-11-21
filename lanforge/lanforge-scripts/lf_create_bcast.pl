#!/usr/bin/perl -w

# This program creates a UDP broadcast connection

# Written by Candela Technologies Inc.
#  Udated by:
#
#

use strict;
use warnings;
use Carp;
$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };

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

# Default values for ye ole cmd-line args.
our $lfmgr_host   = "localhost";
our $lfmgr_port   = 4001;

our $resource     = 1;
our $quiet        = "yes";
our $tx_bps       = 512000;
our $socket_buf   = 512000;
our $cx_name      = "";
our $endp_a       = "";
our $endp_b       = "";
our $port_a       = "";
our $mac_a        = "";
our $mac_b        = "FF FF FF FF FF FF";

########################################################################
# Nothing to configure below here, most likely.
########################################################################

sub logg {
   return if ($::quiet eq "yes");
   foreach (@_) {
      print "* ".$_."\n";
   }
}

# [--port_b       {eth0}]
our $port_b = "eth0";

our $usage = qq($0 ## creates a UDP broadcast connection
  [--mgr          {host-name | IP}]
  [--mgr_port     {ip port}]
  [--resource     {number}]
  [--quiet        { yes | no }]
  [--cx_name      {cx name}]
  [--tx_bps       { transmit bps }]
  [--port_a       {eth1}]
  [--mac_addr_a   {mac address}]
  [--ip_a         {ip addr}]
  [--netmask      {255.255.255.0}]
  [--dest_ip      {ip.255}]
  [--socket_buf   {512000}]
  [--tx_bps       {512000}]

Examples:
# set broadcast endpoint
$0 --mgr jedtest \\
   --resource_a   1                 \\
   --cx_name      cx3eth0           \\
   --port_a       eth1              \\
   --mac_a        00:00:00:32:23:11 \\
   --ip_a         10.26.1.2         \\
   --broadcast    10.26.1.255       \\
   --netmask      255.255.255.0     \\
   --socket_buf   512000            \\
   --tx_bps       512000
);

GetOptions
(
   'mgr|m=s'         => \$::lfmgr_host,
   'mgr_port|p=i'    => \$::lfmgr_port,
   'resource|r=i'    => \$::resource,
   'quiet|q=s'       => \$::quiet,
   'cx_name|c=s'     => \$::cx_name,
   'port_a|a=s'      => \$::port_a,
   'mac_addr_a|mac_a=s' => \$::mac_a,
   'tx_bps=i'        => \$::tx_bps,
   'socket_buf=i'    => \$::socket_buf
) || die("$::usage");

sub fmt_cmd {
   my $rv;
   my $mod_hunk;
   for my $hunk (@_) {
      die("fmt_cmd called with empty space or null argument, bye.") unless(defined $hunk && $hunk ne '');
      die("rv[${rv}]\n --> fmt_cmd passed an array, bye.")  if (ref($hunk) eq 'ARRAY');
      die("rv[${rv}]\n --> fmt_cmd passed a hash, bye.")    if (ref($hunk) eq 'HASH');
      $mod_hunk = $hunk;
      $mod_hunk = "0" if ($hunk eq "0" || $hunk eq "+0");

      if( $hunk eq "" ) {
         #print "hunk[".$hunk."] --> ";
         $mod_hunk = 'NA';
         #print "hunk[".$hunk."]\n";
         #print "fmt_cmd: warning: hunk was blank, now NA. Prev hunks: $rv\n"
      }
      $rv .= ( $mod_hunk =~m/ +/) ? "'$mod_hunk' " : "$mod_hunk ";
   }
   chomp $rv;
   print "cmd formatted to: $rv\n" unless($::quiet eq "yes");
   return $rv;
}

die "please specify --mgr \n$::usage"
   if ((! defined $::lfmgr_host) || "$::lfmgr_host" eq "");

die "please specify --resource\n$::usage"
   if ((! defined $::resource) || "$::resource" eq "");

die "please specify --mgr_port\n$::usage"
   if ((! defined $::lfmgr_port) || "$::lfmgr_port" eq "");

die "please specify --port_a\n$::usage"
   if ((! defined $::port_a) || "$::port_a" eq "");

die "please specify --cx_name\n$::usage"
   if ((! defined $::cx_name) || "$::cx_name" eq "");

die "please specify --tx_bps\n$::usage"
   if ((! defined $::cx_name) || "$::cx_name" eq "");


$endp_a = $::cx_name."-A";
$endp_b = $::cx_name."-B";


# Open connection to the LANforge server.
our $t = new Net::Telnet(  Prompt   => '/default\@btbits\>\>/',
                           Timeout  => 20);
$t->open(Host    => $lfmgr_host,
         Port    => $lfmgr_port,
         Timeout => 10);
$t->waitfor("/btbits\>\>/");

# Configure our utils.
our $utils = new LANforge::Utils();
$utils->telnet($t);         # Set our telnet object.
if ($::quiet eq "yes") {
  $utils->cli_send_silent(1); # Do show input to CLI
  $utils->cli_rcv_silent(1);  # Repress output from CLI ??
}
else {
  $utils->cli_send_silent(0); # Do show input to CLI
  $utils->cli_rcv_silent(0);  # Repress output from CLI ??
}

$resource   = 1;
$mac_a = "";

my @lines = split("\n", $::utils->doAsyncCmd(fmt_cmd("nc_show_ports", "1", "$resource", "$port_a")));
my @hunks = grep {/MAC/} @lines;
if ( @hunks < 1) {
  die("Unable to get mac addresses for port $port_a");
}

($mac_a) = $hunks[0] =~ /MAC: ([^ ]+)/;
$mac_a =~ y/:/ /;

die "please specify --mac_a since endp_a does not report it"
   if ((! defined $::mac_a) || "$::mac_a" eq "" || "$::mac_a" =~ /\s*(00[: ]){5}00\s*/);

#print "MAC is now [$::mac_a]\n";

my $rx_buf_size=512000; # default is 0, expresses OS min: 64B
my $tx_buf_size=512000; # default is 0, expresses OS min: 64B
# list of commands
our @endp_a_list = (
  qq(add_endp $endp_a 1 $resource $port_a custom_ether -1 NO $tx_bps 0 NO 64 64 CUSTOM NO 32 0 0),
  qq(set_endp_flag $endp_a ReplayOverwriteDstMac 1),
  # this sets the broadcast MAC address
  qq(set_endp_details $endp_a $rx_buf_size $tx_buf_size 4294967295 0 'ff ff ff ff ff ff' 0 0 0 0 10000 0 NA NA NA  0.0.0.0 0),
  qq(set_endp_quiesce $endp_a 3),
  # this sets the source MAC
  qq(set_endp_addr $endp_a '$mac_a' AUTO 0 0),
  qq(set_endp_flag $endp_a ReplayLoop 0),
  qq(set_endp_flag $endp_a EnableTcpNodelay 0),
  qq(set_endp_flag $endp_a EnableRndSrcIP 0),
  qq(set_endp_flag $endp_a EnableConcurrentSrcIP 0),
  qq(set_endp_flag $endp_a EnableLinearSrcIP 0),
  qq(set_endp_flag $endp_a EnableLinearSrcIPPort 0),
  qq(set_endp_flag $endp_a QuiesceAfterRange 0),
  qq(set_endp_flag $endp_a QuiesceAfterDuration 0),
  # does this require recompilation?
  qq(set_endp_payload $endp_a CUSTOM ff ff ff ff ff ff 00 90 0b 29 06 f9 08 00 45 00 00 32 53 f5 40 00 40 11 cf 91 0a 1a 01 02 0a 1a 01 ff 00 00 00 00 00 00 e8 9b 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00),
  qq(set_endp_tos $endp_a DONT-SET 0),
  qq(set_script $endp_a NA NA NONE 'NA' 0 0),
  qq(set_endp_proxy $endp_a NO),
  qq(rm_thresholds $endp_a all),
  qq(set_endp_report_timer $endp_a 5000),
  qq(set_endp_flag $endp_a ClearPortOnStart 0),
);
our @endp_b_list = (
  # this is how an *unmanaged port* appears to be created
  qq(add_endp $endp_b 1 0 eth0 custom_ether -1 NO 56000 0 NO 64 64 CUSTOM NO 32 0 0),
  qq(set_endp_flag $endp_b ReplayOverwriteDstMac 0),
  # dest mac address
  qq(set_endp_details $endp_b 0 0 4294967295 0 '$mac_a' 0 0 0 0 10000 0 NA NA NA  0.0.0.0 0),
  qq(set_endp_quiesce $endp_b 3),
  qq(set_endp_flag $endp_b unmanaged 1),
  qq(set_endp_addr $endp_b '00 00 00 00 00 00 ' AUTO 0 0),
  qq(set_endp_flag $endp_b ReplayLoop 0),
  qq(set_endp_flag $endp_b EnableTcpNodelay 0),
  qq(set_endp_flag $endp_b EnableRndSrcIP 0),
  qq(set_endp_flag $endp_b EnableConcurrentSrcIP 0),
  qq(set_endp_flag $endp_b EnableLinearSrcIP 0),
  qq(set_endp_flag $endp_b EnableLinearSrcIPPort 0),
  qq(set_endp_flag $endp_b QuiesceAfterRange 0),
  qq(set_endp_flag $endp_b QuiesceAfterDuration 0),
  qq(set_endp_payload $endp_b CUSTOM 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00),
  qq(set_endp_tos $endp_b DONT-SET 0),
  qq(set_script $endp_b NA NA NONE 'NA' 0 0),
  qq(set_endp_proxy $endp_b NO),
  qq(rm_thresholds $endp_b all),
  qq(set_endp_report_timer $endp_b 5000),
  qq(set_endp_flag $endp_b ClearPortOnStart 0)
);

$::utils->doAsyncCmd( fmt_cmd("rm_cx", "all", $cx_name));
sleep(1);
$::utils->doAsyncCmd( fmt_cmd("rm_endp", "$endp_a"));
$::utils->doAsyncCmd( fmt_cmd("rm_endp", "$endp_b"));
sleep(1);
my $cmd;
logg("creating endp_a:");
for $cmd (@endp_a_list) {
   logg("   ".$cmd."\n");
   $::utils->doAsyncCmd( $cmd );
}
logg("creating endp_b");
for $cmd (@endp_b_list) {
   logg("   ".$cmd."\n");
   $::utils->doAsyncCmd( $cmd );
}
sleep 1;
$::utils->doAsyncCmd(fmt_cmd("add_cx", $cx_name, "default_tm", "$endp_a", "$endp_b"));


########################################################################
=pod
### REFERENCE OF COMMANDS
add_endp $endp_a 1 1 eport_a custom_ether -1 NO 512000 0 NO 64 64 CUSTOM NO 32 0 0
 set_endp_flag $endp_a ReplayOverwriteDstMac 1
 set_endp_details $endp_a 0 0 4294967295 0 'ff ff ff ff ff ff ' 0 0 0 0 10000 0 NA NA NA  0.0.0.0 0
 set_endp_quiesce $endp_a 3
 set_endp_addr $endp_a '00 90 0b 29 06 f9 ' AUTO 0 0
 set_endp_flag $endp_a ReplayLoop 0
 set_endp_flag $endp_a EnableTcpNodelay 0
 set_endp_flag $endp_a EnableRndSrcIP 0
 set_endp_flag $endp_a EnableConcurrentSrcIP 0
 set_endp_flag $endp_a EnableLinearSrcIP 0
 set_endp_flag $endp_a EnableLinearSrcIPPort 0
 set_endp_flag $endp_a QuiesceAfterRange 0
 set_endp_flag $endp_a QuiesceAfterDuration 0
 set_endp_payload $endp_a CUSTOM ff ff ff ff ff ff 00 90 0b 29 06 f9 08 00 45 00 00 32 53 f5 40 00 40 11 cf 91 0a 1a 01 02 0a 1a 01 ff 00 00 00 00 00 00 e8 9b 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
 set_endp_tos $endp_a DONT-SET 0
set_script $endp_a NA NA NONE 'NA' 0 0
 set_endp_proxy $endp_a NO
rm_thresholds $endp_a all
set_endp_report_timer $endp_a 5000
 set_endp_flag $endp_a ClearPortOnStart 0
add_endp $endp_b 1 0 eth0 custom_ether -1 NO 56000 0 NO 64 64 CUSTOM NO 32 0 0
 set_endp_flag $endp_b ReplayOverwriteDstMac 0
 set_endp_details $endp_b 0 0 4294967295 0 '00 90 0b 29 06 f9 ' 0 0 0 0 10000 0 NA NA NA  0.0.0.0 0
 set_endp_quiesce $endp_b 3
 set_endp_flag $endp_b unmanaged 1
 set_endp_addr $endp_b '00 00 00 00 00 00 ' AUTO 0 0
 set_endp_flag $endp_b ReplayLoop 0
 set_endp_flag $endp_b EnableTcpNodelay 0
 set_endp_flag $endp_b EnableRndSrcIP 0
 set_endp_flag $endp_b EnableConcurrentSrcIP 0
 set_endp_flag $endp_b EnableLinearSrcIP 0
 set_endp_flag $endp_b EnableLinearSrcIPPort 0
 set_endp_flag $endp_b QuiesceAfterRange 0
 set_endp_flag $endp_b QuiesceAfterDuration 0
 set_endp_payload $endp_b CUSTOM 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 set_endp_tos $endp_b DONT-SET 0
set_script $endp_b NA NA NONE 'NA' 0 0
 set_endp_proxy $endp_b NO
rm_thresholds $endp_b all
set_endp_report_timer $endp_b 5000
 set_endp_flag $endp_b ClearPortOnStart 0
report 'lf_reports' NO NO NO NO
=cut


