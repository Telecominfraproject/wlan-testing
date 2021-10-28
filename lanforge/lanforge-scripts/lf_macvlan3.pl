#!/usr/bin/perl

# This program is used to test the max TCP connections allowed through a firewall, 
# and may be used as an example for others who wish to automate LANforge tests.

# This script sets up 1 UDP connection and as many TCP connections as specified
# by $num_macvlans.  Each connection is started and verified that it is passing
# traffic before starting the next connection.  As each TCP connection is started
# the UDP connection is checked for any dropped packets.  As soon as dropped packets
# are detected on the UDP connection, the number of TCP connections is recorded
# and the entire test is repeated for $loop_max times.  An average number of TCP
# connections is calculated and reported at the conclusion of all the test runs.

# Un-buffer output
$| = 1;

use strict;

use Net::Telnet ();
use LANforge::Port;
use LANforge::Utils;
use LANforge::Endpoint;

my $lfmgr_host = "localhost";
my $lfmgr_port = 4001;

my $shelf = 1;

my $script_speed = 25; # Increase to issue commands faster.

# The LANforge resources
my $lf1 = 1;  # Minor Resource EID.
my $lf2 = ""; # Set to "" if we have no second machine.  Or set to second Resource
              # minor EID to create mac-vlans on it.

# Port pairs.  These are the ports that should be talking to each other.
# i.e. the third column in lf1_ports talks to the third column in lf2_ports.
# EIDs or aliases can be used.
# Port pairs must match on each shelf - will enhance to allow any pair on each shelf.
#my @lf1_ports = (1); #, 2, 3);
#my @lf2_ports = (2); #, 2, 3);
my @lf1_ports = ("eth0"); #, "eth2");
my @lf2_ports = ("eth1"); #, "eth3");

my $mac1 = 0x00;            # Starting MAC address 00:m5:m4:m3:m2:m1 where:
my $mac2 = 0x00;            # m5 is shelf EID, m4 is card EID, m3 is $mac3, 
my $mac3 = 0x00;            # m2 is $mac2 and m1 is $mac1.

my $ip_base1 = "192.168";   #
my $ip_c1 = 2;              #
my $ip_lsb1 = 2;            #
my $msk1 = "255.255.255.0"; #
my $ip_gw1 = "192.168.2.1"; #

my $ip_base2 = "172.1";     #
my $ip_c2 = 1;              #
my $ip_lsb2 = 2;            #
my $msk2 = "255.255.255.0"; #
my $ip_gw2 = "172.1.1.1";   #


my $num_macvlans = 200; # Number of mac vlans per port, or the number of connections
my $pause_min = 3;      # Depends on $num_macvlans and how well your LANforge system runs

my $one_cx_per_port = 1;# If zero, will have one of EACH of the cx types on each port.

#my @cx_types =     ("lf", "lf_udp", "lf_tcp", "custom_udp", "custom_tcp", "l4");
#my @min_pkt_szs =  (64,   1,        1,         1,            1,            0);
#my @max_pkt_szs =  (1514, 12000,    13000,     2048,         2048,         0);

my @cx_types =     ("lf_tcp");
my @min_pkt_szs =  (1472);
my @max_pkt_szs =  (1472);

my $min_rate = 9600;
my $max_rate = 9600;

my $test_mgr = "mac_tm";

my $mac_init = 0;        # Set to 1 to initialize IPs when running looped test.
my $ip_init = 0;         # Set to 1 to initialize IPs when running looped test.
my $loop_max = 3;        # Number of times the test will be run before calculating average TCP connections
my $report_timer = 1000; # 1 second, must be set higher when using > 500 mac vlans
my $cxcnt = 0;
my $avg_cxcnt = 0;


########################################################################
# Nothing to configure below here, most likely.
########################################################################

my @endpoint_names = (); #will be added to as they are created
my @cx_names = ();

# Open connection to the LANforge server.

my $t = new Net::Telnet(Timeout => 15,
                        Prompt => '/default\@btbits\>\>/');

my $timeout = 60;

$t->open(Host    => $lfmgr_host,
     Port    => $lfmgr_port,
     Timeout => $timeout);

$t->waitfor("/btbits\>\>/");
$t->max_buffer_length(1024 * 1024 * 10); # 10M buffer

# Configure our utils.
my $utils = new LANforge::Utils();
$utils->telnet($t);         # Set our telnet object.
$utils->cli_send_silent(0); # Do show input to CLI
$utils->cli_rcv_silent(0);  # Repress output from CLI ??

if ($lf2 == "") { $lf2 = $lf1; }
my $start_mvlan = 0;
my $num_mvlans = $num_macvlans;


my $i_c1   = $ip_c1;
my $i_lsb1 = $ip_lsb1;
my $i_c2   = $ip_c2;
my $i_lsb2 = $ip_lsb2;

my $dt = "";

my $loop = 0;
for ($loop = 0; $loop<$loop_max; $loop++) {
  $dt = `date`;
  chomp($dt);
  print "\n\n*****  Starting loop: $loop at: $dt  *****\n\n";

  @endpoint_names = ();
  @cx_names = ();
  $cxcnt = 0;

  initToDefaults();
  #exit(0);

  # Now, add back the test manager we will be using
  doCmd("add_tm $test_mgr");
  doCmd("tm_register $test_mgr default");  #Add default user
  doCmd("tm_register $test_mgr default_gui");  #Add default GUI user

  addMacVlans();

  # Add some IP addresses to the ports
  initIpAddresses();

  # Add our endpoints
  addCrossConnects();

  print "Done adding CXs.\n";
  print "Pause $pause_min minutes for ports to update.\n";
  for (my $n=1; $n<=$pause_min; $n++) {
     print "$n of $pause_min\n";
     sleep(60);
  }

  # Start Cross-Connects
  my $p = 0;
  for (my $q=0; $q<@cx_names; $q++) {
    my $cmd = "set_cx_state $test_mgr " . $cx_names[$q] . " RUNNING";
    doCmd($cmd);
    $p = $q+$q;

    # check that the CX is passing packets
    my $endp = new LANforge::Endpoint();
    $utils->updateEndpoint($endp, $endpoint_names[$p]);
    my $en = $endp->rx_pkts();

    my $slp=0;
    while ($en == 0) {
       # sleep to allow CX to connect
       sleep(1);
       $slp++;
       $utils->updateEndpoint($endp, $endpoint_names[$p]);
       $en = $endp->rx_pkts();
       if ($slp > 14) {
          # too long
          print "WARNING: Waited too long on endp $q\n";
          last;
       }
    }

    # check UDP CX for dropped packets
    my $endp1 = new LANforge::Endpoint();
    $utils->updateEndpoint($endp1, $endpoint_names[0]);
    my $en1 = $endp1->rx_dropped_pkts();

    my $endp2 = new LANforge::Endpoint();
    $utils->updateEndpoint($endp2, $endpoint_names[1]);
    my $en2 = $endp2->rx_dropped_pkts();

    if ($en1 != 0 || $en2 != 0) { # If there are ANY dropped packets on UDP CX
       $avg_cxcnt = $avg_cxcnt + $cxcnt; # Average calculated later
       last;       
    }
    elsif ($q > 0) {
       # Successfully added TCP CX, count it
       $cxcnt++;
    }
  } #for $q
} #for $loop_max

if ($avg_cxcnt == 0) {
   print "$cxcnt TCP connections were made.\n";
   print "No dropped packets were detected on the UDP connection.\n";
   print "Try increasing the number of connections.\n";
}
else {
   $avg_cxcnt = int($avg_cxcnt / $loop_max);
   print "$loop_max test loops completed.\n";
   print "Average number of simultaneous TCP connections: $avg_cxcnt\n";
}

$dt = `date`;
chomp($dt);
print "Done at: $dt\n\n";
exit(0);


sub initToDefaults {
  # Clean up database if stuff exists

  doCmd("rm_cx $test_mgr all");
  doCmd("rm_endp YES_ALL");
  doCmd("rm_test_mgr $test_mgr");

  initPortsToDefault();

}#initToDefaults

my $lsb1 = sprintf("%d", $mac1);
my $lsb2 = sprintf("%d", $mac2);
my $lsb3 = sprintf("%d", $mac3);

# Return a unique MAC address using last 3 octets
sub getNextMac {
  $lsb1++;
  if ($lsb1 > 255) {
    $lsb2++;
    $lsb1 = 0;
    if ($lsb2 > 255) {
      $lsb3++;
      $lsb2 = 0;
      if ($lsb3 > 255) {
        print "*** WARNING, MAC address rolling over XX:YY:ZZ:ff:ff:ff ***\n";
        $lsb3 = 0;
      }
    }
  }
  $mac1 = sprintf("%02x", $lsb1);
  $mac2 = sprintf("%02x", $lsb2);
  $mac3 = sprintf("%02x", $lsb3);
  return "$mac3:$mac2:$mac1";
} # getNextMac

sub addMacVlans {
  if ($mac_init == 1 ) {
    $lsb1 = sprintf("%d", $mac1);
    $lsb2 = sprintf("%d", $mac2);
    $lsb3 = sprintf("%d", $mac3);
  }
  my $i;
  my $q;
  my $v;
  my $throttle = $script_speed;
  my $since_throttle = 0;
  for ($q = 0; $q<@lf1_ports; $q++) {
    my $pnum1 = $lf1_ports[$q];
    my $pnum2 = $lf2_ports[$q];
    for ($i = $start_mvlan; $i<($num_mvlans + $start_mvlan); $i++) {
      
      my $shlf = sprintf("%02x", $shelf);
      my $card = sprintf("%02x", $lf1);
      my $mac_index = getNextMac();
      my $mac_addr = "00:$shlf:$card:$mac_index";
      doCmd("add_mvlan $shelf $lf1 $pnum1 $mac_addr $i");

      if ($lf2 ne "") {
        $card = sprintf("%02x", $lf2);
        $mac_index = getNextMac();
        $mac_addr = "00:$shlf:$card:$mac_index";
        doCmd("add_mvlan $shelf $lf2 $pnum2 $mac_addr $i");
      }

      # Throttle ourself so we don't over-run the poor LANforge system.
      if ($since_throttle++ > $throttle) {
        my $p1 = new LANforge::Port();
        $utils->updatePort($p1, $shelf, $lf1, $pnum1);
        if ($lf2 ne "") {
          my $p1 = new LANforge::Port();
          $utils->updatePort($p1, $shelf, $lf2, $pnum2);
        }
        $since_throttle = 0;
      }
    }
  }

  doCmd("probe_ports");

  # Wait untill we discover all the ports...

  for ($q = 0; $q<@lf1_ports; $q++) {
    my $p1 = new LANforge::Port();
    $utils->updatePort($p1, $shelf, $lf1, $lf1_ports[$q]);
    my $pname = $p1->{dev};

    my $p2 = new LANforge::Port();
    my $pname2;
    if ($lf2 ne "") {
      $utils->updatePort($p2, $shelf, $lf2, $lf2_ports[$q]);
      $pname2 = $p2->{dev};
    }

    for ($i = 0; $i<$num_macvlans; $i++) {
      while (1) {
    $utils->updatePort($p1, $shelf, $lf1, "$pname\#$i");
    if ($lf2 ne "") {
      $utils->updatePort($p2, $shelf, $lf2, "$pname2\#$i");
    }
    if ($p1->isPhantom() || (($lf2 ne "") && $p2->isPhantom())) {
      sleep(1);
    }
    else {
      last;
    }
      }
    }
  }


}#addMacVlans


# Wait untill the system can update a port..
sub throttleCard {
  my $s = shift;
  my $c = shift;
  my $p1 = new LANforge::Port();
  $utils->updatePort($p1, $s, $c, 1);   
}#throttle

sub initPortsToDefault {
  clearMacVlanPorts($shelf, $lf1);
  if ($lf2 ne "") {
    clearMacVlanPorts($shelf, $lf2);
  }

  throttleCard($shelf, $lf1);

  if ($lf2 ne "") {
    throttleCard($shelf, $lf2);
  }

  # Set all ports we are messing with to known state.
  my $i = 0;
  for ($i = 0; $i<@lf1_ports; $i++) {
    my $tmp = $lf1_ports[$i];
    my $tmp2 = $lf2_ports[$i];
    doCmd("set_port $shelf $lf1 $tmp 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
    if ($lf2 ne "") {
      doCmd("set_port $shelf $lf2 $tmp2 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
    }
  }
}

sub clearMacVlanPorts {
  my $s = shift;
  my $c = shift;

  my $i;
  my $found_one = 1;
  my @ports = ();
  while ($found_one) {
    $found_one = 0;
    doCmd("probe_ports");
    # Clear out any existing MAC-VLAN ports.
    $utils->error("");
    @ports = $utils->getPortListing($s, $c);
    my $mx = @ports;
    print "Found $mx ports for card: $shelf.$lf1\n";

    if (($mx == 0) || ($utils->error() =~ /Timed out/g)) {
      # System is too backlogged to answer, wait a bit
      print " Will try listing ports again in a few seconds...system is backlogged now!\n";
      sleep(5);
      $found_one = 1;
      next;
    }

    my $throttle = 0;
    for ($i = 0; $i<$mx; $i++) {
      if ($ports[$i]->isMacVlan()) {
	    doCmd($ports[$i]->getDeleteCmd());
      } #fi isMacVlan
    }
  }
}


sub initIpAddresses {
  # Set all ports we are messing with to known state.
  my $i = 0;
  # init base IP or keep rolling since rolling might stress caching in DUT/NUT.
  if ($ip_init = 1) {
    $i_c1   = $ip_c1;
    $i_lsb1 = $ip_lsb1;
    $i_c2   = $ip_c2;
    $i_lsb2 = $ip_lsb2;
  }
  for ($i = 0; $i<@lf1_ports; $i++) {
    my $tmp = $lf1_ports[$i];
    my $tmp2 = $lf2_ports[$i];
    my $cmd = "";
    $cmd = "set_port $shelf $lf1 $tmp 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA";
    doCmd($cmd);

    if ($lf2 ne "") {
      $cmd = "set_port $shelf $lf2 $tmp2 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA";
      doCmd($cmd);
    }

    my $p1 = new LANforge::Port();
    $utils->updatePort($p1, $shelf, $lf1, $tmp);
    my $pname = $p1->{dev};

    my $q;
    my $throttle = $script_speed;
    my $since_throttle = 0;
    for ($q = 0; $q<$num_macvlans; $q++) {
      $cmd = "set_port $shelf $lf1 $pname\#$q $ip_base1.$i_c1.$i_lsb1 $msk1 " .
             "$ip_gw1 NA NA NA";
      doCmd($cmd);
      $i_lsb1++;

      if ($i_lsb1 > 250) {
        $i_c1++;
        $i_lsb1 = 2;
      }

      if ($since_throttle++ > $throttle) {
        my $p1 = new LANforge::Port();
        $utils->updatePort($p1, $shelf, $lf1, "$pname\#$q");    
        $since_throttle = 0;
      }
    }

    if ($lf2 ne "") {
      $p1 = new LANforge::Port();
      $utils->updatePort($p1, $shelf, $lf2, $tmp2);
      $pname = $p1->{dev};

      for ($q = 0; $q<$num_macvlans; $q++) {
        $cmd = "set_port $shelf $lf2 $pname\#$q $ip_base2.$i_c2.$i_lsb2 $msk2 " .
               "$ip_gw2 NA NA NA";
        doCmd($cmd);
        $i_lsb2++;
    
        if ($i_lsb2 > 250) {
          $i_c2++;
          $i_lsb2 = 2;
        }
    
        if ($since_throttle++ > $throttle) {
          my $p1 = new LANforge::Port();
          $utils->updatePort($p1, $shelf, $lf2, "$pname\#$q");  
          $since_throttle = 0;
        }
      }
    }# If we have an LF-2 defined.
  }
}

sub addCrossConnects {
  my $ep = 0;
  my $cx = 1;
  my $i = 0;


  my @all_ports1 = @lf1_ports;
  my $j;
  my $pname;
  for ($j = 0; $j<@lf1_ports; $j++) {
    my $p1 = new LANforge::Port();
    $utils->updatePort($p1, $shelf, $lf1, $lf1_ports[$j]);
    $pname = $p1->{dev};

    my $q;
    for ($q = 0; $q<$num_macvlans; $q++) {
      @all_ports1 = (@all_ports1, "$pname\#$q");
    }
  }

  my @all_ports2 = @lf2_ports;
  if ($lf2 ne "") {
    for ($j = 0; $j<@lf2_ports; $j++) {
      my $p1 = new LANforge::Port();
      $utils->updatePort($p1, $shelf, $lf2, $lf2_ports[$j]);
      $pname = $p1->{dev};

      my $q;
      for ($q = 0; $q<$num_macvlans; $q++) {
    @all_ports2 = (@all_ports2, "$pname\#$q");
      }
    }
  }

  print "About to start endpoints, all_ports1:\n" . join(" ", @all_ports1) .
        "\nall_ports2: " . join(" ", @all_ports2) . "\n\n";

  if ($one_cx_per_port) {
    my $j = 1;
    my $cxs = 0;
    for ($j ; $j<@all_ports1; $j++) {
      my $i = $cxs % @cx_types;
      $cxs++;
      if ($j == 1) {
        my $burst = "NO";
        if ($min_rate != $max_rate) {
          $burst = "YES";
        }
        my $szrnd = "NO";
        if ($min_pkt_szs[$i] != $max_pkt_szs[$i]) {
          $szrnd = "YES";
        }
        
        my $pattern = "increasing";
        if ($cx_types[$i] =~ /custom/) {
          $pattern = "custom";
        }

        # Create UDP endpoints
        
        my $ep1 = "endp-${ep}-TX";
        $ep++;
        my $ep2 = "endp-${ep}-RX";
        $ep++;
        
        @endpoint_names = (@endpoint_names, $ep1, $ep2);
        
        # Add the UDP endpoints
        my $cmd = "add_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " lf_udp " .
                  " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " . $max_pkt_szs[$i] .
                  " $pattern NO";
        doCmd($cmd);
        
        if ($lf2 == "") {
          die("Must have lf2 defined if using non-l4 endpoints.");
        }
        
        $cmd = "add_endp $ep2 $shelf $lf2 " . $all_ports2[$j] . " lf_udp " .
               " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " .
               $max_pkt_szs[$i] . " $pattern NO";
        doCmd($cmd);
        
        # Now, add the cross-connects
        my $cx_name = sprintf "cx-%04d", $cx;
        $cmd = "add_cx $cx_name $test_mgr $ep2 $ep1";
        doCmd($cmd);
        doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");
        
        $cx++;
        
        @cx_names = (@cx_names, $cx_name);
      }
      else {
        my $burst = "NO";
        if ($min_rate != $max_rate) {
          $burst = "YES";
        }
        my $szrnd = "NO";
        if ($min_pkt_szs[$i] != $max_pkt_szs[$i]) {
          $szrnd = "YES";
        }
        
        my $pattern = "increasing";
        if ($cx_types[$i] =~ /custom/) {
          $pattern = "custom";
        }
        
        my $ep1 = "endp-${ep}-TX";
        $ep++;
        my $ep2 = "endp-${ep}-RX";
        $ep++;
        
        @endpoint_names = (@endpoint_names, $ep1, $ep2);
        
        my $cmd = "add_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " " . @cx_types[$i] .
            " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " . $max_pkt_szs[$i] .
            " $pattern NO";
        doCmd($cmd);
        
        if ($lf2 == "") {
          die("Must lave lf2 defined if using non-l4 endpoints.");
        }
        
        $cmd = "add_endp $ep2 $shelf $lf2 " . $all_ports2[$j] . " " . @cx_types[$i] .
               " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " .
               $max_pkt_szs[$i] . " $pattern NO";
        doCmd($cmd);
         
        # Now, add the cross-connects
        my $cx_name = sprintf "cx-%04d", $cx;
        $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
        doCmd($cmd);
        doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");
        
        $cx++;
        
        @cx_names = (@cx_names, $cx_name);
      }
    }#for all ports
  }#one_cx_per_port
}#addCrossConnects


sub doCmd {
  my $cmd = shift;

  print ">>> $cmd\n";

  $t->print($cmd);
  my @rslt = $t->waitfor(Match => '/ \>\>RSLT:(.*)/',
             Timeout => $timeout);

  print "**************\n @rslt ................\n\n";
  #sleep(1);
}
