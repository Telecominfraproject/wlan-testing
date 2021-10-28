#!/usr/bin/perl

use strict;

# Clean up routing tables

remove_local_routing_table("rddC1");
remove_local_routing_table("rddA2");
remove_local_routing_table("rddA1");
remove_local_routing_table("rddB1");
remove_local_routing_table("rddD1");
remove_local_routing_table("rddD2");
remove_local_routing_table("rddE1");
remove_routing_table(1001);
remove_routing_table(1002);
remove_routing_table(1003);

do_cmd("ip ru show");
do_cmd("ip route show table 1001");
do_cmd("ip route show table 1002");

# Set up router 1001
set_ip("rddC1", "10.0.4.1", "10.0.4.0", "24", "10.0.4.255", "10.0.4.2", 1001);
set_ip("rddA2", "10.0.3.1", "10.0.3.0", "24", "10.0.3.255", "10.0.3.2", 1001);
set_ip("rddD1", "10.0.5.1", "10.0.5.0", "24", "10.0.5.255", "10.0.5.2", 1001);
do_cmd("ip rule add to 10.0.5.1 iif rddC1 lookup local pref 10"); # use local routing table if it arrives here and is destined to peer.
do_cmd("ip rule add to 10.0.5.1 iif rddA2 lookup local pref 10"); # use local routing table if it arrives here and is destined to peer.
do_cmd("ip rule add to 10.0.3.1 iif rddC1 lookup local pref 10"); # use local routing table if it arrives here and is destined to peer.
do_cmd("ip rule add to 10.0.3.1 iif rddD1 lookup local pref 10"); # use local routing table if it arrives here and is destined to peer.
do_cmd("ip rule add to 10.0.4.1 iif rddA2 lookup local pref 10"); # use local routing table if it arrives here and is destined to peer.
do_cmd("ip rule add to 10.0.4.1 iif rddD1 lookup local pref 10"); # use local routing table if it arrives here and is destined to peer.

# Set up router 1002
set_ip("rddA1", "10.0.3.2", "10.0.3.0", "24", "10.0.3.255", "10.0.3.1", 1002);
set_ip("rddB1", "10.0.2.1", "10.0.2.0", "24", "10.0.2.255", "10.0.2.2", 1002);
do_cmd("ip rule add to 10.0.3.2 iif rddB1 lookup local pref 10"); # use local routing table if it arrives here and is destined to peer.
do_cmd("ip rule add to 10.0.2.1 iif rddA1 lookup local pref 10"); # use local routing table if it arrives here and is destined to peer.

# Set up router 1003
set_ip("rddD2", "10.0.5.2", "10.0.5.0", "24", "10.0.5.255", "10.0.5.1", 1003);
set_ip("rddE1", "10.0.6.1", "10.0.6.0", "24", "10.0.6.255", "10.0.6.2", 1003);
do_cmd("ip rule add to 10.0.5.2 iif rddE1 lookup local pref 10"); # use local routing table if it arrives here and is destined to peer.
do_cmd("ip rule add to 10.0.6.1 iif rddD2 lookup local pref 10"); # use local routing table if it arrives here and is destined to peer.


add_subnet_route("10.0.2.0/24", "10.0.3.2", "rddA2", 1001);
add_subnet_route("10.0.6.0/24", "10.0.5.2", "rddD1", 1001);

add_subnet_route("10.0.4.0/24", "10.0.3.1", "rddA1", 1002);
add_subnet_route("10.0.5.0/24", "10.0.3.1", "rddA1", 1002);
add_subnet_route("10.0.6.0/24", "10.0.3.1", "rddA1", 1002);

add_subnet_route("10.0.4.0/24", "10.0.5.1", "rddD2", 1003);
add_subnet_route("10.0.3.0/24", "10.0.5.1", "rddD2", 1003);
add_subnet_route("10.0.2.0/24", "10.0.5.1", "rddD2", 1003);


sub add_subnet_route {
  my $sn = shift;
  my $sn_gw = shift;
  my $dev = shift;
  my $rt = shift;

  do_cmd("ip route add $sn via $sn_gw dev $dev table $rt"); # subnet route
}


sub set_ip {
  my $dev = shift; # network device name
  my $ip = shift; # ip
  my $sn = shift; # subnet addr
  my $mbits = shift; # mask bits (ie, 24)
  my $bcast = shift; # broadcast addr
  my $sn_gw = shift; # next hot for this subnet route
  my $rt = shift; # routing table

  # Set it's IP address.
  do_cmd("ip link set $dev down");
  do_cmd("ip link set $dev up");
  do_cmd("ip addr flush dev $dev");
  do_cmd("ip addr add $ip/$mbits broadcast $bcast dev $dev");
  do_cmd("ip rule add to $ip iif $dev lookup local pref 10"); # use local routing table if it arrives here and is destined here.
  do_cmd("ip rule add iif $dev lookup $rt pref 20"); # use this table for pkts rx on this interface.
  do_cmd("ip rule add from $ip/32 table $rt pref 30"); # use this table for pkts from this IP
  do_cmd("ip route add $sn/$mbits via $ip table $rt"); # subnet route
  #  Do default gateway on a per-router basis, not per-interface.

  # Enable arp filtering.
  do_cmd("echo 1 > /proc/sys/net/ipv4/conf/$dev/arp_filter");
}


sub remove_routing_table {
  my $tid = shift;

  my $listing = `ip ru list`;
  my @listings = split(/\n/, $listing);
  my $q = 0;
  for ($q = 0; $q<@listings; $q++) {
    my $line = $listings[$q];
    chomp($line);
    #print "Processing ip-ru-list line -:$line:-\n";
    my $num;
    my $from;
    my $arg;
    my @rest;
	
    if ($line =~ /\S+:\s+\S+\s+(\S+)\s+.*lookup\s+(\S+)/) {
      my $a = $1;
      my $mtid = $2;

      if ($a eq "all") {
	$a = "0/0";
      }

      if ($tid eq $mtid) {
	my $cmd = "ip ru del from $a lookup $tid";
	do_cmd("$cmd");
      }
    }
  }

  $listing = `ip route show table $tid`;
  @listings = split(/\n/, $listing);
  $q = 0;
  for ($q = 0; $q<@listings; $q++) {
    my $line = $listings[$q];
    chomp($line);
    #print "Processing ip-ru-list line -:$line:-\n";

    if ($line =~ /(\S+)\s+/) {
      my $key = $1;

      if ($a eq "all") {
	$a = "0/0";
      }

      my $cmd = "ip route del $key table $tid";
      do_cmd("$cmd");
    }
  }

}


sub remove_local_routing_table {
  my $dev = shift;

  my $listing = `ip ru list`;
  my @listings = split(/\n/, $listing);
  my $q = 0;
  for ($q = 0; $q<@listings; $q++) {
    my $line = $listings[$q];
    chomp($line);
    #print "Processing ip-ru-list line -:$line:-\n";
    my $num;
    my $from;
    my $arg;
    my @rest;

    if ($line =~ /.*\s+iif $dev\s+.*/) {
      if ($line =~ /\S+:\s+\S+\s+(\S+)\s+(.*)lookup local/) {
	my $a = $1;
	my $match = $2;
	
	if ($a eq "all") {
	  $a = "0/0";
	}
	
	my $cmd = "ip ru del from $a $match lookup local";
	do_cmd("$cmd");
      }
    }
  }
}

sub do_cmd {
  my $cmd = shift;
  print "$cmd\n";
  system("$cmd");
}
