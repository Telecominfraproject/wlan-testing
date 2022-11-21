#!/usr/bin/perl -w
=pod
-------------------------------------------------------------------------------
   Use this script to survey a captive portal station:
   * check DNS settings via dig
   * check initial page redirect with curl
   ## (C) 2017, Candela Technologies Inc. support@candelatech.com
-------------------------------------------------------------------------------
=cut
package main;
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

# Un-buffer output
$| = 1;
use Cwd qw(getcwd);
my $cwd = getcwd();

 # this is pedantic necessity for the following use statements
if ( $cwd =~ q(.*LANforge-Server\scripts$)) {
   use lib '/home/lanforge/scripts'
}
else {
   use lib '/home/lanforge/scripts';
}
use List::Util qw(first);
use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
use Net::Telnet ();

my $usage = qq($0   [--mgr {host-name | IP}]
      [--mgr_port {ip port}]     # use if on non-default management port
      [--resource {resource}]    # use if multiple lanforge systems; defaults to 1
      [--quiet { yes | no }]     # debug output; -q
      [--log_cli]                # enables CLI command printing to STDOUT
                                 # same effect when setting env var LOG_CLI=STDOUT
      [--radio {name}]           # radio parent of sta1000 e.g. wiphy0
      [--sta {name}]             # station to use e.g. sta1000 or wlan0
      [--ssid {ssid}]            # ssid to set station on
      [--upstream {dev}]         # e.g. eth1 # attempt to ping upstream port from station
      [--verbose|v]
      );

if (@ARGV < 2) {
   print $usage;
   exit 0;
}
my $help;
our $lfmgr_host = "localhost";
my $lfmgr_port = 4001;
our $resource = 1;
our $quiet = "yes";
our $sta_wiphy = "wiphy0";
our $ssid = "";
our $sta;
our $upstream_port = "";
my $log_cli;
our $verbose = 0;
GetOptions
(
  'mgr|m=s'                   => \$::lfmgr_host,
  'mgr_port|p=i'              => \$lfmgr_port,
  'resource|r=i'              => \$::resource,
  'quiet|q=s'                 => \$::quiet,
  'radio|o=s'                 => \$::sta_wiphy,
  'ssid|s=s'                  => \$::ssid,
  'upstream|t=s'              => \$::upstream_port,
  'log_cli=s{0,1}'            => \$log_cli, # use ENV{LOG_CLI} elsewhere
  'sta|w=s'                   => \$::sta,
  'verbose|v=i'               => \$::verbose,
  'help|?'                    => \$help,
) || (print($usage) && exit(1));

if ($help) {
  print($usage) && exit(0);
}
$SIG{ __DIE__  } = sub { Carp::confess( @_ ) };

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

our $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/',
          Timeout => 20);
$t->open(Host    => $lfmgr_host,
         Port    => $lfmgr_port,
         Timeout => 10);
$t->waitfor("/btbits\>\>/");

# Configure our utils.
our $utils = new LANforge::Utils();
$utils->telnet($t);         # Set our telnet object.
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

# this is the --show_port options ("")
my @port_txt = ();
our $port_mac = '';
our $port_dev = '';
our $port_ip = '';
our $port_dns = '';
our $port_gateway = '';
if ((defined $::sta) && ("$sta" ne "")) {
    @port_txt = split("\n", $utils->doAsyncCmd("nc_show_port 1 $::resource $::sta"));
}
my @likely = ();
if ($::verbose > 0) {
   print "--------------------------------------------\n";
   print join("\n", @port_txt);
   print "--------------------------------------------\n";
}

@likely = grep {/MAC: .* DEV: .*/} @port_txt;
die("Unable to find port named $::sta")
   if (!@likely);
if (@likely) {
   ($port_mac) = $likely[0] =~ /MAC: ([^ ]+) /;
   $port_mac = ''
      if (!defined $port_ip);
   ($port_dev) = $likely[0] =~ /DEV: ([^ ]+) /;
   $port_dev = ''
      if (!defined $port_ip);
}

@likely = grep {/IP: .* MASK:/} @port_txt;
if (@likely) {
   ($port_ip) = $likely[0] =~ /IP: ([^ ]+) /;
   $port_ip = ''
      if (!defined $port_ip);
}

@likely = grep {/DNS Servers:/} @port_txt;
if (@likely) {
   if ($verbose) {
      print "LIKELY DNS SERVERS:\n";
      print join("\n", @likely)."\n";
   }
   ($port_dns) = $likely[0] =~ /DNS Servers: (.*)$/;
   $port_dns =''
      if (!defined $port_dns)
}
@likely = grep {/GW: /} @port_txt;
if (@likely) {
   ($port_gateway) = $likely[0] =~ /GW: ([^ ]+) /;
   $port_gateway = ''
      if (!defined $port_gateway);
}

print qq(Port name: $sta IP: $port_ip; DNS: $port_dns; GW: $port_gateway;\n\n);

if ($port_ip eq '') {
   print "\nNo tests possible, bye\n";
   exit(1);
}

if ($port_gateway ne '') {
   print "\nChecking gateway: $port_gateway\n";
   print("ping -c2 -w2 -t2 -I $port_ip $port_gateway \n");
   system("ping -c2 -w2 -t2 -I $port_ip $port_gateway");
}
else {
   print "Not checking gateway\n";
}

if ($port_dns ne '') {
   my @dns = split(',', $port_dns);
   if (@dns) {
      print "\nChecking DNS: $dns[0]\n";
      print("\nping -c2 -w2 -t2 -I $port_ip $dns[0]\n");
      system("ping -c2 -w2 -t2 -I $port_ip $dns[0]");
      print("\ndig -b $port_ip -q www.slashdot.org \@$dns[0]\n");
      system("dig -b $port_ip -q www.slashdot.org \@$dns[0]");
   }
}
else {
   print "Not checking DNS\n";
}

sub assembleCurl {
   return qq(/home/lanforge/local/bin/curl -svLki -4 -m30 --connect-timeout 15 )
         .qq( --interface $port_dev )
         .qq( --localaddr $port_ip )
         .qq( --dns-interface $port_dev )
         .qq( --dns-ipv4-addr $port_ip )
         .qq( --dns-servers $::port_dns )
         .join(" ", @_);
}
print "\nChecking redirect to http://1.1.1.1/ ...\n";
my $cmd = assembleCurl(qw("http://1.1.1.1/"));
print("\n$cmd\n");
system("$cmd");

print "\n\nChecking redirect to http://www.slashdot.org/ ...\n";
$cmd = assembleCurl(qw("http://www.slashdot.org/"));
print("\n$cmd\n");
system("$cmd");
print "\n\n";
#
