#!/usr/bin/perl

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# This script sets up connections to load-test pairs of ports.
# The user does not need to give many details..the script attempts
# to configure connections with optimal values for maximum throughput.

# Un-buffer output
$| = 1;

# This breaks Net::Telnet...gah!
#use bigint;

use strict;
#use Switch;  

use Net::Telnet ();
use LANforge::Port;
use LANforge::Utils;

my @cx_types = ();

my $test_mgr = "netoptics_tm";
my $report_timer = 1000;       # Set report timer for all tests created in ms, i.e. 8 seconds

my $lfmgr_host = "127.0.0.1";
my $lfmgr_port = 4001;

my $shelf = 1;

# This sets up connections.
my $lf1 = 1;  # Minor Resource EID of first LANforge resource.

my @lf1_ports = ();

my $num_vlans = 3; # .1q vlans per physical port
my $vid = "RANDOM";
my $vlan_mac = "RANDOM";
my $num_mvlans = 3; # mac-vlans per .1q vlan
my $mvlan_mac = "RANDOM";
my $num_cxs = 5;  # CXs per MVL pair (or endpoints per MVL)
my $ipaddr = "DHCP";
my $mask = "255.255.0.0";
my $subnet_per_vl = 1;

my $multicon = "AUTO";
my $duration = 10 * 60 * 1000; # 10 minutes by default
my $max_rate = 10000000000;
my $max_pkt_sz = "AUTO";
my $dbname = "netoptics-scr";
my $clear_port_on_start = 1;
my $group_prefix = "L3";

########################################################################
# Nothing to configure below here, most likely.
########################################################################

my $ports_rpt = "Interface VID MAC IP\n";

# Parse cmd-line args
my $i;
for ($i = 0; $i<@ARGV; $i++) {
  my $var = $ARGV[$i];
  if ($var =~ m/(\S+)=(.*)/) {
    my $arg = $1;
    my $val = $2;
    handleCmdLineArg($arg, $val);
  }
  else {
    handleCmdLineArg($var);
  }
}

if (@cx_types == 0) {
  @cx_types = ("lf_tcp");
}

if (@lf1_ports < 2) {
  print("ERROR:  Must specify two base ports, ie:  --portA=eth1 --portB=eth2\n");
  exit(1);
}

if ($lfmgr_host eq undef) {
  print "\nYou must define a LANforge Manager!!!\n\n"
      . "For example:\n"
      . "./lf_netoptics.pl --mgr=localhost\n"
      . "OR\n"
      . "./lf_netoptics.pl --mgr=192.168.1.101\n\n";
  printHelp();
  exit (1);
}

print
    "\nStarting script with the following arguments:"
  . "\nmanager: $lfmgr_host:$lfmgr_port"
  . "\nlf1: $lf1"
  . "\nlf1_ports: " . join(" ", @lf1_ports)
  . "\nipaddr: $ipaddr"
  . "\nsubnet-per-vlan: $subnet_per_vl"
  . "\nnum_mvlans: $num_mvlans"
  . "\nmax_rate: $max_rate"
  . "\nmax_pkt_size: $max_pkt_sz"
  . "\ncx_types: " . join(" ", @cx_types)
  . "\nnum_cxs: $num_cxs\n\n";

# Run some logic tests.
if (1) {
  my $tst_ip = "99.99.99.2";
  my $tsti = toIpString($tst_ip);
  my $tips = toStringIp($tsti);
  if ($tst_ip ne $tips) {
    print ("tst-ip: $tst_ip  as-integer: $tsti  as-string-again: $tips\n");
    die("bug");
  }
}

# Open connection to the LANforge server.
my $t = new Net::Telnet(Timeout => 15,
			#Dump_Log => "lf_netoptics.log",
                        Prompt => '/default\@btbits\>\>/');

$t->telnetmode(0); # Not true telnet protocol
$t->max_buffer_length(1024 * 1024 * 10); # 10M buffer

$t->open(Host    => $lfmgr_host,
         Port    => $lfmgr_port,
         Timeout => 45);

$t->waitfor('/.*btbits\>\>.*/');

# Configure our utils.
my $utils = new LANforge::Utils();
$utils->telnet($t);         # Set our telnet object.
$utils->cli_send_silent(0); # Do show input to CLI
$utils->cli_rcv_silent(0);  # Repress output from CLI ??

my $dt = getDate();
my $dt_start = $dt;


initToDefaults();

doCmd("add_tm $test_mgr");
doCmd("tm_register $test_mgr default");     # Add default user
doCmd("tm_register $test_mgr default_gui"); # Add default GUI user
doCmd("tm_register $test_mgr Admin");

my $i;
my $p;
my $q;
my $m;
my $ip;

# For each port, add .1q vlans.
# For each .1q vlan, add mac-vlans

# Create list of IP addresses, one for each mac-vlan.
if ($ipaddr eq "RANDOM") {
  # basically, just randomize the middle two octets
  $ip = (10 << 24) + int(rand(1<<23));
  $ip &= 0xffffff00;
  $ip |= 2;
}
else {
  if ($ipaddr eq "DHCP") {
    $ip = 0;
  }
  else {
    $ip = toIpString($ipaddr);
    print "IP-addr: $ipaddr  (as int: $ip)\n";
  }
}
my @vl_ips = ();
for ($q = 0; $q<$num_vlans; $q++) {
  @vl_ips = (@vl_ips, $ip);
  if ($subnet_per_vl) {
    if ($ipaddr eq "RANDOM") {
      # basically, just randomize the middle two octets
      $ip = (10 << 24) + int(rand(1<<23));
      $ip &= 0xffffff00;
      $ip |= 2;
    }
    else {
      if ($ipaddr eq "DHCP") {
	$ip = 0;
      }
      else {
	my $maski = toIpString($mask);
	print "maski: $maski  ip: $ip\n";
	$ip += ~$maski;
	$ip &= $maski;
	$ip |= 2;
	print "after: ip: $ip\n";
      }
    }
  }
  else {
    $ip++;
  }
}

my @ips = ();
for ($p = 0; $p<@lf1_ports; $p++) {
  for ($q = 0; $q<$num_vlans; $q++) {
    for ($m = 0; $m<$num_mvlans; $m++) {
      if ($subnet_per_vl) {
	my $ip = $vl_ips[$q];
	@ips = (@ips, $ip);
	$ip++;
	$vl_ips[$q] = $ip;
      }
      else {
	@ips = (@ips, $ip);
	$ip++;
      }
    }
  }
}

my $total_mvlans = @lf1_ports * $num_vlans * $num_mvlans;

# Build list of VIDs, we want same VID on each different
# physical/base port.
my $myvid;
if ($vid eq "RANDOM") {
  $myvid = int(rand(4094));
  if ($myvid <= 0) {
    $myvid = 1;
  }
}
else {
  $myvid = $vid;
}

my @vids = ($myvid);
for ($q = 0; $q < ($num_vlans - 1); $q++) {
  my $myvid;
  if ($vid eq "RANDOM") {
    $myvid = int(rand(4094));
    if ($myvid <= 0) {
      $myvid = 1;
    }
  }
  else {
    $vid++;
    $myvid = $vid;
  }
  @vids = (@vids, $myvid);
}


my $do_simple_names = (@lf1_ports == 2);

my $ip_idx = 0;
for ($p = 0; $p<@lf1_ports; $p++) {
  for ($q = 0; $q<$num_vlans; $q++) {
    # Create .1q vlan
    my $myvid = $vids[$q];
    my $vname = $lf1_ports[$p] . ".$myvid";
    doCmd("add_vlan $shelf $lf1 $lf1_ports[$p] $myvid $vname 8000");

    if ($vlan_mac ne "PARENT") {
      my $mac_addr;
      if ($vlan_mac eq "RANDOM") {
	$mac_addr = getNextMac($vlan_mac);
      }
      else {
	$mac_addr = $vlan_mac;
      }
      doCmd("set_port $shelf $lf1 $vname NA NA NA NA NA $mac_addr");
      if ($vlan_mac ne "RANDOM") {
	$vlan_mac = getNextMac($vlan_mac);
      }
    }

    # Create mac-vlans
    for ($m = 0; $m<$num_mvlans; $m++) {

      my $mac_addr;
      if ($mvlan_mac eq "RANDOM") {
	$mac_addr = getNextMac($mvlan_mac);
      }
      else {
	$mac_addr = $mvlan_mac;
      }

      my $mvname = "$vname#$m";
      doCmd("add_mvlan $shelf $lf1 $vname $mac_addr $m $mvname");

      my $ips = toStringIp($ips[$ip_idx]);
      $ip_idx++;
      my $masks = $mask;
      my $interest_flags = 0x4000 | 0x4 | 0x8 ; # dhcp, IP, Mask
      my $cur_flags = 0;
      if ($ipaddr eq "DHCP") {
	$masks = "0.0.0.0";
	$cur_flags = 0x80000000; # use-dhcp
      }

      # Set up IP addressing on the mac-vlan
      doCmd("set_port $shelf $lf1 $mvname $ips $masks NA NA $cur_flags NA NA NA NA $interest_flags");

      $ports_rpt .= "$mvname $myvid $mac_addr $ips\n";

      # Now, create endpoints on this port.
      my $e;
      for ($e = 0; $e < $num_cxs; $e++) {
	my $burst = "NO";
        my $szrnd = "NO";
        my $pattern = "increasing";
        my $ep1 = "$group_prefix-$p.$q#$m-$e";
	my $etype = $cx_types[$e % @cx_types];
	my $rate = int($max_rate / $num_cxs);
	my $pdu_sz = getPduSize($etype, $max_rate);
	my $mcon = $multicon;
	if ($mcon eq "AUTO") {
	  if ($max_rate > 1000000000) {
	    $mcon = 1;
	  }
	  else {
	    $mcon = 0;
	  }
	}
        my $cmd = "add_endp $ep1 $shelf $lf1 $mvname $etype -1 $burst $rate $rate $szrnd $pdu_sz $pdu_sz $pattern NO NA NA $mcon";
        doCmd($cmd);
	if ($clear_port_on_start) {
	  doCmd("set_endp_flag $ep1 ClearPortOnStart 1");
	}
      }

      if ($mvlan_mac ne "RANDOM") {
	$mvlan_mac = getNextMac($mvlan_mac);
      }
    }
  }
}#for all ports

my $pdu_sz = getPduSize($cx_types[0], $max_rate);
my $flags = 4; # symmetric
my $script_body = "my-script $flags Script2544 '$duration 5000 bps,$max_rate $pdu_sz 50000,100000,500000,100000,0 bps,$max_rate $pdu_sz 0 NONE' ALL 0";

# Add cross-connects between the endpoints on port-pairs.
for ($p = 0; $p<@lf1_ports; $p += 2) {
  # Add test-group for this port-pair
  my $pgname = "$group_prefix-$p";
  if ($do_simple_names) {
    $pgname = "$group_prefix-all";
  }
  doCmd("add_group $pgname 4 4");
  doCmd("set_script $pgname $script_body");

  for ($q = 0; $q<$num_vlans; $q++) {
    my $myvid = $vids[$q];

    # Add test-group for this vlan-pair
    my $vgname = "$group_prefix-$p.v$myvid";
    if ($do_simple_names) {
      $vgname = "$group_prefix-all-v$myvid";
    }

    doCmd("add_group $vgname 4 4");
    doCmd("set_script $vgname $script_body");

    for ($m = 0; $m<$num_mvlans; $m++) {

      # Add test-group for this mvlan pair
      my $gname = "$group_prefix-$p.$q#$m";
      if ($do_simple_names) {
	$gname = "$group_prefix-v$myvid#$m";
      }
      doCmd("add_group $gname 4 4");
      doCmd("set_script $gname $script_body");

      my $e;
      for ($e = 0; $e < $num_cxs; $e++) {
	# Now, add the cross-connects
	my $pp = int($p / 2);
	my $p2 = $p+1;
        my $ep1 = "$group_prefix-$p.$q#$m-$e";
        my $ep2 = "$group_prefix-$p2.$q#$m-$e";
	my $cx_name = "$group_prefix-$pp.$q.$m-$e";
	if ($do_simple_names) {
	  $cx_name = "$group_prefix-$myvid#$m-$e";
	}

	my $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
	doCmd($cmd);
	doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

	# Add to groups
	doCmd("add_tgcx $gname $cx_name");
	doCmd("add_tgcx $vgname $cx_name");
	doCmd("add_tgcx $pgname $cx_name");

	# TODO:  Add 2544 scripts to test-groups
      }
    }
  }
};

# Save this in a database for later retrieval.
doCmd("save $dbname");

# Print some reporting on what was configured.
print "<PORTS_CREATED>\n$ports_rpt</PORTS_CREATED>\n";


$dt = getDate();
print "Started lf_netoptics.pl script at  : $dt_start\n";
print "Completed lf_netoptics.pl script at: $dt\n\n";
exit(0);
#####################
# END lf_macvlan.pl #
#####################



sub initToDefaults {
  # Clean up database if stuff exists
  doCmd("rm_cx $test_mgr all");
  doCmd("rm_endp YES_ALL");
  doCmd("rm_test_mgr $test_mgr");
  my $rslt = doCmd("show_group");
  my @rslts = split(/\n/, $rslt);
  my $i;
  my $pat = ".*TestGroup name: (${group_prefix}-\\S+)\\s+";
  #print "pattern -:$pat:-\n";
  for ($i = 0; $i<@rslts; $i++) {
    my $ln = $rslts[$i];
    chomp($ln);
    #print "test-group-rslt-line -:$ln:-\n";
    if ($ln =~ /$pat/) {
      doCmd("rm_group $1");
    }
  }

  initPortsToDefault();
}#initToDefaults

sub getNextMac {
  my $last = shift;
  if ($last eq "RANDOM") {
    my $msb = int(rand(255)) & 0xfe; # make sure odd bit (mcast) isn't set.
    return sprintf("%02x:%02x:%02x:%02x:%02x:%02x", $msb, int(rand(255)), int(rand(255)), int(rand(255)),
		   int(rand(255)), int(rand(255)));
  }
  else {
    # Parse last, and increment.
    if ($last =~ /(\S+):(\S+):(\S+):(\S+):(\S+):(\S+)/) {
      my $dl = hex($6);
      $dl |= (hex($5) << 8);
      $dl |= (hex($4) << 16);
      $dl |= (hex($3) << 24);

      my $dh |= hex($2);
      $dh |= (hex($1) << 8);

      $dl++; # Increment mac by one.
      if ($dl == 0) {
	# Wrapped, how unlucky.
	$dh++;
      }
      return sprintf("%02x:%02x:%02x:%02x:%02x:%02x",
		     ($dh & 0xff00) >> 8,
		     ($dh & 0xff),
		     ($dl & 0xff000000) >> 24,
		     ($dl & 0xff0000) >> 16,
		     ($dl & 0xff00) >> 8,
		     ($dl & 0xff));
    }
  }
} # getNextMac


sub toIpString {
  my $ips = shift;
  if ($ips =~ /(\S+)\.(\S+)\.(\S+)\.(\S+)/) {
    my $d = int($4);
    $d += ((int($3) << 8) & 0xff00);
    $d += ((int($2) << 16) & 0xff0000);
    $d += ((int($1) << 24) & 0xff000000);
    return $d;
  }
  return 0;
}

sub toStringIp {
  my $ip = shift;
  return sprintf("%d.%d.%d.%d",
		 ($ip >> 24),
		 ($ip & 0xff0000) >> 16,
		 ($ip & 0xff00) >> 8,
		 ($ip & 0xff));
}

# Wait until the system can update a port..
sub throttleCard {
  my $s = shift;
  my $c = shift;
  my $p1 = new LANforge::Port();
  $utils->updatePort($p1, $s, $c, 1);
}#throttle

sub initPortsToDefault {
  clearVlanPorts($shelf, $lf1);

  throttleCard($shelf, $lf1);

  # Set all ports we are messing with to known state.
  my $i = 0;
  for ($i = 0; $i<@lf1_ports; $i++) {
    my $tmp = $lf1_ports[$i];
    doCmd("set_port $shelf $lf1 $tmp 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
  }
}

sub clearVlanPorts {
  my $s = shift;
  my $c = shift;

  my $i;
  my $found_one = 1;
  my @ports = ();
  while ($found_one) {
    $found_one = 0;
    doCmd("probe_ports");
    # Clear out any existing VLAN ports.
    $utils->error("");
    @ports = $utils->getPortListing($s, $c);
    my $mx = @ports;
    print "Found $mx ports for resource: $shelf.$lf1\n";

    if (($mx == 0) || ($utils->error() =~ /Timed out/g)) {
      # System is too backlogged to answer, wait a bit
      print " Will try listing ports again in a few seconds...system is backlogged now!\n";
      sleep(5);
      $found_one = 1;
      next;
    }

    my $throttle = 0;
    for ($i = 0; $i<$mx; $i++) {
      if (($ports[$i]->isMacVlan()) || ($ports[$i]->is8021qVlan())) {
	# See if it belongs to any of our interfaces
	my $par = $ports[$i]->parent();
	if ($par ne "") {
	  my $base;
	  if ($par =~ /(\S+)\#.*/) {
	    $base = $1; # mac-vlan
	  }
	  elsif ($par =~ /(\S+)\..*/) {
	    $base = $1; # .1q vlan
	  }
	  else {
	    $base = $par;
	  }

	  my $p;
	  for ($p = 0; $p < @lf1_ports; $p++) {
	    if ($lf1_ports[$p] eq $base) {
	      doCmd($ports[$i]->getDeleteCmd());
	      $found_one = 1;
	      last;
	    }
	  }# for all physical/base ports
	}# if found port has parent device
      }# Found a vlan device
    }# for all found ports
  }# while we found something to delete
}#clearVlanPorts

# Returns string, might want to split it to get line-by-line option
sub doCmd {
  my $cmd = shift;

  if ($cmd) {
    print ">>> $cmd\n";
    $t->print($cmd);
    my @rslt = $t->waitfor('/ \>\>RSLT:(.*)/');
    print "**************\n @rslt ................\n\n";
    return join("\n", @rslt);
  } else {
    print "\n***** doCmd (): NULL COMMAND !!! *****";
    print "\n$cmd\n\n";
    exit (1);
  }
}

sub getDate {
  my $date = `date`;
  chomp($date);
  return $date
}

sub printArgs {
  print
  . "\nModified arguments:"
  . "\nmanager: $lfmgr_host\n"
  . "\nlf1: $lf1\n"
  . "\nlf1_ports: " . join(" ", @lf1_ports)
  . "\nnum_mvlans: $num_mvlans"
  . "\nmax_rate: $max_rate"
  . "\ncx_types: " . join(" ", @cx_types)
  . "\n\n";
}

sub printHelp {
  print
  . "USAGE: --mgr=[ip-of-mgr]\n"
  . "       --testMgrName=\"ben_tm\"\n"
  . "       --resourceId=[1|n]\n"
  . "       --protocolFlags=[n]:  tcp4:1, udp4:2, tcp6:4 udp6:8\n"
  . "       --portA=\"eth1\"\n"
  . "       --portB=\"eth2\"\n"
  . "       --vlanAmt=[3|n]\n"
  . "       --macVlanAmt=[3|n]\n"
  . "       --clearPortOnStart=[0|1]\n"
  . "       --cxPerMacVlanAmt=[5|n]\n"
  . "       --vlanID=[RANDOM|n]\n"
  . "       --ip=\"DHCP|RANDOM|192.168.7.2\"\n"
  . "       --mask=\"255.255.0.0\"\n"
  . "       --subnetPerMacVlan=[0|1]\n"
  . "       --dbName=\"my_db_name\"\n"
  . "       --desiredTotalTxRate=[n]  (in bits-per-second)\n"
  . "       --pduSize=[AUTO|n]  (in bytes, payload size)\n"
  . "       --duration=[n]  (duration of script run, in miliseconds)\n"
  . "       --multicon=[AUTO|0|1|n]  (Enable multi-conn feature, or not)\n"
  . "\n";

}

sub getPduSize {
  my $etype = shift;
  my $rate = shift;

  if ($max_pkt_sz ne "AUTO") {
    return $max_pkt_sz;
  }

  my $rv;
  if ($rate > 1000000000) {
    # Use big pkts for > 1Gbps
    if ($etype =~ /.*udp.*/i) {
      return 64000;
    }
    else {
      return 200000;
    }
  }
  else {
    # Attempt to fit into 1500 byte MTU pkt
    if ($etype eq "lf_udp") {
      return 1472;
    }
    elsif ($etype eq "lf_tcp") {
      return 1460;
    }
    elsif ($etype eq "lf_udp6") {
      return 1452;
    }
    elsif ($etype eq "lf_tcp6") {
      return 1440;
    }
    else {
      print "Unknown cx type: $etype in PDU auto-cal method, returning 4000\n";
      return 4000;
    }
  }
}

sub handleCmdLineArg {
  my $arg = $_[0];
  my $val = $_[1];

  if ($arg eq "help" || $arg eq "--help" || $arg eq "-h" || $arg eq "-help" || $arg eq "-h" ) {
    printHelp();
    exit(0);
  }
  elsif ($arg eq "--mgr") {
    $lfmgr_host = $val;
  }
  elsif ($arg eq "--testMgrName") {
    $test_mgr = $val;
  }
  elsif ($arg eq "--resourceId") {
    $lf1 = $val;
  }
  elsif ($arg eq "--protocolFlags") {
    my $vi = int($val);
    if ($vi & 0x1) {
      @cx_types = (@cx_types, "lf_tcp");
    }
    if ($vi & 0x2) {
      @cx_types = (@cx_types, "lf_udp");
    }
    if ($vi & 0x4) {
      @cx_types = (@cx_types, "lf_tcp6");
    }
    if ($vi & 0x8) {
      @cx_types = (@cx_types, "lf_udp6");
    }
  }
  elsif ($arg eq "--portA") {
    @lf1_ports = (@lf1_ports, $val);
  }
  elsif ($arg eq "--portB") {
    @lf1_ports = (@lf1_ports, $val);
  }
  elsif ($arg eq "--vlanAmt") {
    $num_vlans = $val;
  }
  elsif ($arg eq "--macVlanAmt") {
    $num_mvlans = $val;
  }
  elsif ($arg eq "--vlanID") {
    $vid = $val;
  }
  elsif ($arg eq "--vlanMAC") {
    $vlan_mac = $val;
  }
  elsif ($arg eq "--macVlanMAC") {
    $mvlan_mac = $val;
  }
  elsif ($arg eq "--ip") {
    $ipaddr = $val;
  }
  elsif ($arg eq "--mask") {
    $mask = $val;
  }
  elsif ($arg eq "--subnetPerMacVlan") {
    $subnet_per_vl = $val;
  }
  elsif ($arg eq "--dbName") {
    $dbname = $val;
  }
  elsif ($arg eq "--cxPerMacVlanAmt") {
    $num_cxs = $val;
  }
  elsif ($arg eq "--clearPortOnStart") {
    $clear_port_on_start = int($val);
  }
  elsif ($arg eq "--desiredTotalTxRate") {
    $max_rate = $val;
  }
  elsif ($arg eq "--pduSize") {
    $max_pkt_sz = $val;
  }
  elsif ($arg eq "--duration") {
    $duration = int($val);
  }
  elsif ($arg eq "--multicon") {
    $multicon = $val;
  }
  else {
    print "\n\nCould not parse one or more of the arguments !!!\n"
            . "First rejected argument: $arg\n";
    printHelp();
    exit(1);
  }
}
