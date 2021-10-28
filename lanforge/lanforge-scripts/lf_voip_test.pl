#!/usr/bin/perl

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# This script sets up VoIP connections.
# It then continously starts and stops the connections.

# Un-buffer output
$| = 1;

use strict;
use Switch;

use Net::Telnet ();
use LANforge::Port;
use LANforge::Utils;

my $script_speed = 25; # Increase to issue commands faster

my $lfmgr_host = undef;
my $lfmgr_port = 4001;

my $shelf = 1;

my $INIT = 1;           # If true, removes all previous tests!!!

# This sets up connections between 2 LANforge machines with minor EIDs of 4 and 15
#my $lf1 = 4; my $lf2 = 15; my @lf1_ports = (0); my @lf2_ports = (0);

# This sets up connections between 2 ports of a single machine;
# $lf1 and $lf2 are the minor number of the EIDs of the resource/card.
#my $lf1 = 4; my $lf2 = 4; my @lf1_ports = ("eth1"); my @lf2_ports = ("eth2");
#my $lf1 = 1; my $lf2 = 2; my @lf1_ports = ("ad0"); my @lf2_ports = ("ad0");
my $lf1 = 1; my $lf2 = 1; my @lf1_ports = ("eth1"); my @lf2_ports = ("eth2");

my $ignore_phys_ports = 0;  # If 1, just muck with mac-vlans instead.
my $mac1 = 0x00;         # Starting MAC address 00:m5:m4:m3:m2:m1 where:
my $mac2 = 0x00;         # m5 is shelf EID, m4 is card EID, m3 is $mac3, 
my $mac3 = 0x00;         # m2 is $mac2 and m1 is $mac1.
my $ip_base = "10.0";
my $ip_c = 1;
my $ip_lsb = 10;
my $msk = "255.0.0.0";
my $default_gw = "0.0.0.0";

my $start_mvlan = 0; # Starting MACVLAN index for VoIP endpoints.
my $num_cxs = 70;     # Overrides $num_mvlans.
my $num_mvlans = 0;  # Only used if $num_cxs is zero:  The number of MACVLANs per interface.
                     # Representing the total number of VoIP CXs. VoIP CXs are created
                     # across the two physical interfaces + the MACVLANs per interface.


my $codec = "G711U"; # Other options:  G711U, g729a, SPEEX, g726-16, g726-24, g726-32, g726-40
my $jB_size = 1;     # Set jitter buffer size in 20ms packets.  Default value is 8 packets, 160ms.
my $tos = 0xBE;      # Set ToS/QoS for VoIP can be decimal or 0xNN for hexadecimal but values will display in decimal in the GUI.


my $mn_icg = 3;            # minimum intercall gap
my $mx_icg = 3;            # maximum intercall gap
my $min_call_duration = 0; # set to zero for 'file'
my $max_call_duration = 0; # Set to zero for 'file'

my $start_dly = 3;         # seconds to delay call start
my $start_dly_inc = 0;     # seconds to increase delay by for each test

my $no_send_rtp = 0;      # Set to zero to send RTP traffic, 1 to suppress RTP
my $use_VAD = 0;          # Set to zero to not use VAD, 1 to use VAD
my $vad_timer = 500;      # how much silence (ms) before we start VAD (Silence Suppression)
my $vad_fs = 3000;        # how often (ms) to force an rtp pkt send even if we are in VAD
my $use_PESQ = 0;         # Set to 1 for PESQ, zero for not PESQ
my $pesq_server = "127.0.0.1";
my $pesq_server_port = 3998;
my $vproto = "SIP";       # set $vproto = "H323"; for H.323
my $bsip_port_a = "5066"; # Base SIP port for endpoint-A
my $bsip_port_b = "5067"; # Base SIP port for endpoint-B
my $i_sip_port_a = 0;     # If zero, do not increment, otherwise increment by assigned value.
my $i_sip_port_b = 0;     # If zero, do not increment, otherwise increment by assigned value.
my $brtp_port = "AUTO";   # Base RTP port
my $i_rtp_port = 0;       # If zero, do not increment, otherwise increment by assgined value


# If zero, will have one of EACH of the cx types on each port.
#my $one_cx_per_port = 1;
#my $one_cx_per_port = 0;

#my @cx_types =     ("", "lf_udp", "lf_tcp", "custom_udp", "custom_tcp", "l4");
#my @min_pkt_szs =  (64,   1,        1,         1,            1,            0);
#my @max_pkt_szs =  (1514, 12000,    13000,     2048,         2048,         0);

# Layer-4 only
#my @cx_types =     ("l4", "l4");
#my @min_pkt_szs =  (0, 0);
#my @max_pkt_szs =  (0, 0);

# VOIP only
#my @cx_types =     ("voip", "voip", "voip", "voip");
#my @min_pkt_szs =  (0, 0, 0, 0);
#my @max_pkt_szs =  (0, 0, 0, 0);
#my @cx_types =     ("voip");
#my @min_pkt_szs =  (0);
#my @max_pkt_szs =  (0);

my $peer_to_peer_voip = 1; # Don't register with SIP proxy, but just call peer to peer.

my @src_sound_files = ("media/female_voice_8khz.wav");

# URL will be acted on from machine $lf1
#my $l4_url = "http://172.1.5.75";
#my $l4_url = "http://172.1.2.3"; # not used in lf_voip.pl script but makes it work

#my $min_rate = 64000; # not used in lf_voip.pl script but makes it work
#my $max_rate = 512000; # not used in lf_voip.pl script but makes it work

my $test_mgr = "voip_tm";

my $STARTSTOP_LOOP = 0; # set $STARTSTOP_LOOP = 1; to start and stop ALL endpoints 
                        # after script finishes populating the database.
my $loop_max = 100;
my $start_stop_iterations = 100;
my $run_for_time = 1200; # Run for XX seconds..then will be stopped again
my $stop_for_time = 5;   # Run for XX seconds..then will be stopped again
my $report_timer = 5000; # 8 seconds


########################################################################
# Nothing to configure below here, most likely.
########################################################################
my $script_name = $0;

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

if ($lfmgr_host == undef) {
  print "\nYou must define a LANforge Manager!!!\n\n"
      . "For example:\n"
      . "./$script_name mgr=locahost\n"
      . "OR\n"
      . "./$script_name mgr=192.168.1.101\n\n";
  printHelp();
  exit (1);
}

my @num = (); #make sorting by name easier :P
my $num_len = 0;
my $total = 0;

if ($num_mvlans == 0 && $num_cxs == 0) {
  printHelp();
  print "\nYou must specify a non-zero value for:  num_cxs: $num_cxs  OR  num_mvl: $num_mvlans\n\n";
  exit (1);
}

if ($num_cxs != 0) {
  $total = $num_cxs*2;
  $num_len = length ($total);
  $num_mvlans = $num_cxs-1;
}
else {
  $total = (($num_mvlans+1)*2);
  $num_len = length ($total);
}

my $i = 0;
switch ($num_len) {
  case 1 {
    for ($i=0;$i<$total;$i++) {
      $num[$i] = sprintf("%01d", $i);
    }
  }
  case 2 {
    for ($i=0;$i<$total;$i++) {
      $num[$i] = sprintf("%02d", $i);
    }
  }
  case 3 {
    for ($i=0;$i<$total;$i++) {
      $num[$i] = sprintf("%03d", $i);
    }
  }
  case 4 {
    for ($i=0;$i<$total;$i++) {
      $num[$i] = sprintf("%04d", $i);
    }
  }
  else { print '***** Error Invalid Number of MAC VLANS i.e. >10,000 !!!!'; }
}


print
  . "init: $INIT\n"
  . "\nmanager: $lfmgr_host\n"
  . "\nlf1: $lf1\nlf2: $lf2\n"
  . "\nlf1_ports: " . join(" ", @lf1_ports)
  . "\nlf2_ports: " . join(" ", @lf2_ports) . "\n"
  . "\nstart_macvlans: $start_mvlan"
  . "\nnum_mvlans: $num_mvlans\n\n";


#my $junk=0;
#for ($junk=0;$junk<$total;$junk++) {
#  printf "$num[$junk],";
#}
#printf "\n";
#exit(0);

my @endpoint_names = (); #will be added to as they are created
my @cx_names = ();

# Open connection to the LANforge server.

my $t = new Net::Telnet(Timeout => 45,
                        Prompt  => '/default\@btbits\>\>/');


$t->open(Host    => $lfmgr_host,
         Port    => $lfmgr_port,
         Timeout => 45);

$t->waitfor("/btbits\>\>/");

# Configure our utils.
my $utils = new LANforge::Utils();
$utils->telnet($t);         # Set our telnet object.
$utils->cli_send_silent(0); # Do show input to CLI
$utils->cli_rcv_silent(0);  # Repress output from CLI ??


my $dt = "";

my $loop = 0;
for ($loop = 0; $loop<$loop_max; $loop++) {
  $dt = `date`;
  chomp($dt);
  print "\n\n*****  Starting loop: $loop at: $dt  *****\n\n";

  if ($INIT) {
    initToDefaults();
  }
  #exit(0);

  # Now, add back the test manager we will be using
  doCmd("add_tm $test_mgr");
  doCmd("tm_register $test_mgr default");  #Add default user
  doCmd("tm_register $test_mgr default_gui");  #Add default GUI user

  if ($num_mvlans != 0) {
    addMacVlans();
    # Add some IP addresses to the ports
    initIpAddresses();
  }

  # Add our endpoints
  addCrossConnects();

  if ($STARTSTOP_LOOP) {
    my $rl = 0;
    for ($rl = 0; $rl<$start_stop_iterations; $rl++) {
      if (($rl % 2) == 0) {
        doCmd("set_cx_state $test_mgr all RUNNING");
      }
      else {
        # Do one at a time
        my $q = 0;
        for ($q = 0; $q<@cx_names; $q++) {
      my $cmd = "set_cx_state $test_mgr " . $cx_names[$q] . " RUNNING";
      doCmd($cmd);
        }
      }

      print "Done starting endpoints...sleeping $run_for_time seconds.\n";
      sleep($run_for_time);

      # Now, stop them...

      if (($rl % 2) == 0) {
        doCmd("set_cx_state $test_mgr all STOPPED");
      }
      else {
        # Do one at a time
        my $q = 0;
        for ($q = 0; $q<@cx_names; $q++) {
      my $cmd = "set_cx_state $test_mgr " . $cx_names[$q] . " STOPPED";
      doCmd($cmd);
        }
      }
      sleep($stop_for_time);
    }# For some amount of start_stop iterations...
  }# STARTSTOP_LOOP
  else {
    $dt = `date`;
    chomp($dt);
    print "Done at: $dt\n\n";
    exit(0);
  }# STARTSTOP_LOOP
}# for some amount of loop iterations

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

  # Wait until we discover all the ports...

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

    for ($i = 0; $i<$num_mvlans; $i++) {
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
  $utils->updatePort($p1, $s, $c, 0);
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
  if (!$ignore_phys_ports) {
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
  for ($i = 0; $i<@lf1_ports; $i++) {
    if ($ip_lsb > 250) {
      $ip_c++;
      $ip_lsb = 2;
    }

    my $tmp = $lf1_ports[$i];
    my $tmp2 = $lf2_ports[$i];
    my $cmd = "";
    if (!$ignore_phys_ports) {
      $cmd = "set_port $shelf $lf1 $tmp $ip_base.$ip_c.$ip_lsb $msk " .
             "$default_gw NA NA NA";
      doCmd($cmd);
      $ip_lsb++;

      if ($lf2 ne "") {
      $cmd = "set_port $shelf $lf2 $tmp2 $ip_base.$ip_c.$ip_lsb $msk " .
             "$default_gw NA NA NA";
      doCmd($cmd);
      $ip_lsb++;
      }
    }

    my $p1 = new LANforge::Port();
    $utils->updatePort($p1, $shelf, $lf1, $tmp);
    my $pname = $p1->{dev};

    my $q;
    my $throttle = $script_speed;
    my $since_throttle = 0;
    for ($q = 0; $q<$num_mvlans; $q++) {
      $cmd = "set_port $shelf $lf1 $pname\#$q $ip_base.$ip_c.$ip_lsb $msk "
           . "$default_gw NA NA NA NA 400";
      doCmd($cmd);
      $ip_lsb++;

      if ($ip_lsb > 250) {
        $ip_c++;
        $ip_lsb = 2;
      }

      if ($since_throttle++ > $throttle) {
        my $p1 = new LANforge::Port();
        $utils->updatePort($p1, $shelf, $lf1, "$pname\#$q");
        $since_throttle = 0;
      }
    }

    $ip_lsb++;

    if ($lf2 ne "") {
      $p1 = new LANforge::Port();
      $utils->updatePort($p1, $shelf, $lf2, $tmp2);
      $pname = $p1->{dev};

      for ($q = 0; $q<$num_mvlans; $q++) {
        $cmd = "set_port $shelf $lf2 $pname\#$q $ip_base.$ip_c.$ip_lsb $msk "
             . "$default_gw NA NA NA NA 400";
        doCmd($cmd);
        $ip_lsb++;

        if ($ip_lsb > 250) {
          $ip_c++;
          $ip_lsb = 2;
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
  my $cx = 0;
  my $i = 0;

  my $voip_phone = 3000; # Start here and count on up as needed.
  my $rtp_port = 10000;  # Starting RTP port.
  my $sound_file_idx = 0;
  my $sip_port_a = $bsip_port_a;
  my $sip_port_b = $bsip_port_b;


  my @all_ports1 = @lf1_ports;
  my $j;
  my $pname;
  for ($j = 0; $j<@lf1_ports; $j++) {
    my $p1 = new LANforge::Port();
    $utils->updatePort($p1, $shelf, $lf1, $lf1_ports[$j]);
    $pname = $p1->{dev};

    my $q;
    my $q_end = 0;

    if ($num_mvlans == 0) {
      $q_end = $num_cxs;
    }
    else {
      $q_end = $num_mvlans;
    }

    for ($q = 0; $q<$q_end; $q++) {
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
      my $q_end = 0;

      if ($num_mvlans == 0) {
        $q_end = $num_cxs;
      }
      else {
        $q_end = $num_mvlans;
      }

      for ($q = 0; $q<$q_end; $q++) {
        @all_ports2 = (@all_ports2, "$pname\#$q");
      }
    }
  }

  print "About to start endpoints, all_ports1:\n" . join(" ", @all_ports1) .
        "\nall_ports2: " . join(" ", @all_ports2) . "\n\n";

# if ($one_cx_per_port) {
#   my $j = 0;
#   my $cxcnt = 0;
#   for ($j ; $j<@all_ports1; $j++) {
#     my $i = $cxcnt % @cx_types;
#     $cxcnt++;
#
#     my $cxt = $cx_types[$i];
#     if ($cxt eq "l4") {
#       # Create layer-4 endpoint
#
#       my $ep1 = "l4e-${ep}-TX";
#       $ep++;
#       my $ep2 = "D_l4e-${ep}-TX";
#       $ep++;
#       
#       @endpoint_names = (@endpoint_names, $ep1, $ep2);
#       
#       # Add the dummy endpoint
#       my $cmd = "add_l4_endp $ep2 $shelf $lf1 " . $all_ports1[$j] . " l4_generic  0 0 0 ' ' ' '";
#       doCmd($cmd);
#       $cmd = "set_endp_flag $ep2 unmanaged 1";
#       doCmd($cmd);
#       
#       $cmd = "add_l4_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " l4_generic 0 10000 100 '" .
#         "dl $l4_url /tmp/$ep1' ' '";
#       doCmd($cmd);
#       
#       # Now, add the cross-connects
#       my $cx_name = "l4-cx-${cx}";
#       $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
#       doCmd($cmd);
#       doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");
#       
#       $cx++;
#       
#       @cx_names = (@cx_names, $cx_name);
#     }
#     elsif ($cxt eq "voip") {
#       # Create VOIP endpoint
#       
#       my $ep1 = "rtpe-${num[$ep]}-TX";
#       $ep++;
#       my $ep2 = "rtpe-${num[$ep]}-RX";
#       $ep++;
#       
#       @endpoint_names = (@endpoint_names, $ep1, $ep2);
#       
#       my $cmd = "add_voip_endp $ep2 $shelf $lf2 " . $all_ports2[$j] .
#                 " $voip_phone $rtp_port AUTO " .
#             $src_sound_files[$sound_file_idx % @src_sound_files] .
#                         " " . $src_sound_files[$sound_file_idx % @src_sound_files] .
#             ".$ep2 $vad_timer $vad_fs";
#       doCmd($cmd);
#       
#       $cmd = "set_voip_info $ep2 NA $mn_icg $mx_icg NA $codec $vproto NA NA $min_call_duration $max_call_duration /dev/null 20000 $sip_port_b $pesq_server $pesq_server_port NA $jB_size";
#       doCmd($cmd);
#       
#       if ($i_sip_port_b != 0) {
#         $sip_port_b = $sip_port_b + $i_sip_port_b;
#       }
#       
#       $cmd = "set_endp_flag $ep2 SavePCM 0";
#       doCmd($cmd);
#       
#       $cmd = "set_endp_tos $ep2 ${tos} 0";
#       doCmd($cmd);
#       
#       if ($peer_to_peer_voip) {
#         $cmd = "set_endp_flag $ep2 DoNotRegister 1";
#         doCmd($cmd);
#         $cmd = "set_endp_flag $ep2 BindSIP 1";
#         doCmd($cmd);
#       }
#       if ($no_send_rtp) {
#         $cmd = "set_endp_flag $ep2 nosendrtp 1";
#                 doCmd($cmd);
#               }
#       
#       if ($use_VAD) {
#         $cmd = "set_endp_flag $ep2 VAD 1";
#                 doCmd($cmd);
#               }
#       
#       if ($use_PESQ) {
#         $cmd = "set_endp_flag $ep2 pesq 1";
#                 doCmd($cmd);
#       }
#       
#       $voip_phone++;
#       $rtp_port += 2;
#       $sound_file_idx++;
#       
#       doCmd($cmd);
#       
#       $cmd = "add_voip_endp $ep1 $shelf $lf1 " . $all_ports1[$j] .
#              " $voip_phone $rtp_port AUTO " .
#              $src_sound_files[$sound_file_idx % @src_sound_files] .
#              " " . $src_sound_files[$sound_file_idx % @src_sound_files] .
#              ".$ep1 $vad_timer $vad_fs";
#       doCmd($cmd);
#       
#       $cmd = "set_voip_info $ep1 NA $mn_icg $mx_icg NA $codec $vproto NA NA $min_call_duration $max_call_duration /dev/null 20000 $sip_port_a $pesq_server $pesq_server_port NA $jB_size";
#       doCmd($cmd);
#       
#       if ($i_sip_port_a != 0) {
#         $sip_port_a = $sip_port_a + $i_sip_port_a;
#       }
#       
#       $cmd = "set_endp_flag $ep1 SavePCM 0";
#       doCmd($cmd);
#       
#       $cmd = "set_endp_tos $ep1 ${tos} 0";
#       doCmd($cmd);
#       
#       if ($peer_to_peer_voip) {
#         $cmd = "set_endp_flag $ep1 DoNotRegister 1";
#         doCmd($cmd);
#         $cmd = "set_endp_flag $ep1 BindSIP 1";
#         doCmd($cmd);
#       }
#       if ($no_send_rtp) {
#         $cmd = "set_endp_flag $ep1 nosendrtp 1";
#         doCmd($cmd);
#       }
#       if ($use_VAD) {
#         $cmd = "set_endp_flag $ep1 VAD 1";
#                 doCmd($cmd);
#       }
#       
#       if ($use_PESQ) {
#         $cmd = "set_endp_flag $ep1 pesq 1";
#                 doCmd($cmd);
#       }
#       
#       $voip_phone++;
#       $rtp_port += 2;
#       $sound_file_idx++;
#       
#       # Now, add the cross-connects
#       my $cx_name = "rtp-cx-${num[$cx]}";
#       $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
#       doCmd($cmd);
#       doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");
#       
#       $cx++;
#       
#       @cx_names = (@cx_names, $cx_name);
#     }
#     else {
#       my $burst = "NO";
#       if ($min_rate != $max_rate) {
#         $burst = "YES";
#       }
#       my $szrnd = "NO";
#       if ($min_pkt_szs[$i] != $max_pkt_szs[$i]) {
#         $szrnd = "YES";
#       }
#       
#       my $pattern = "increasing";
#       if ($cx_types[$i] =~ /custom/) {
#         $pattern = "custom";
#       }
#       
#       my $ep1 = "l3e-${ep}-TX";
#       $ep++;
#       my $ep2 = "l3e-${ep}-RX";
#       $ep++;
#       
#       @endpoint_names = (@endpoint_names, $ep1, $ep2);
#       
#       my $cmd = "add_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " " . @cx_types[$i] .
#           " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " . $max_pkt_szs[$i] .
#           " $pattern NO";
#       doCmd($cmd);
#       
#       
#       if ($lf2 == "") {
#         die("Must lave lf2 defined if using non-l4 endpoints.");
#       }
#       
#       $cmd =    "add_endp $ep2 $shelf $lf2 " . $all_ports2[$j] . " " . @cx_types[$i] .
#           " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " .
#           $max_pkt_szs[$i] . " $pattern NO";
#       doCmd($cmd);
#       
#       # Now, add the cross-connects
#       my $cx_name = "l3-cx-${cx}";
#       $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
#       doCmd($cmd);
#       doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");
#       
#       $cx++;
#       
#       @cx_names = (@cx_names, $cx_name);
#     }
#   }#for all ports
# }#one_cx_per_port
# else {
    my $j = 0;
    for ($j ; $j<@all_ports1; $j++) {
#      for ($i = 0; $i<@cx_types; $i++) {
#       my $cxt = $cx_types[$i];
#
#       if ($cxt eq "l4") {
#         # Create layer-4 endpoint
#
#         my $ep1 = "l4e-${ep}-TX";
#         $ep++;
#         my $ep2 = "D_l4e-${ep}-TX";
#         $ep++;
#
#         @endpoint_names = (@endpoint_names, $ep1, $ep2);
#
#         # Add the dummy endpoint
#         my $cmd = "add_l4_endp $ep2 $shelf $lf1 " . $all_ports1[$j] . " l4_generic  0 0 0 ' ' ' '";
#         doCmd($cmd);
#         $cmd = "set_endp_flag $ep2 unmanaged 1";
#         doCmd($cmd);
#
#         $cmd = "add_l4_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " l4_generic 0 10000 100 '" .
#              "dl $l4_url /tmp/$ep1' ' '";
#         doCmd($cmd);
#
#         # Now, add the cross-connects
#         my $cx_name = "l4-cx-${cx}";
#         $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
#         doCmd($cmd);
#         doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");
#
#         $cx++;
#
#         @cx_names = (@cx_names, $cx_name);
#       } # cx type l4
#       elsif ($cxt eq "voip") {
          # Create VOIP endpoint

          my $ep1 = "RTPE-${num[$ep]}-TX";
          $ep++;
          my $ep2 = "RTPE-${num[$ep]}-RX";
          $ep++;

          @endpoint_names = (@endpoint_names, $ep1, $ep2);

          my $cmd = "add_voip_endp $ep2 $shelf $lf2 " . $all_ports2[$j] .
                    " $voip_phone $rtp_port AUTO " .
                $src_sound_files[$sound_file_idx % @src_sound_files] .
                        " " . $src_sound_files[$sound_file_idx % @src_sound_files] .
                ".$ep2 $vad_timer $vad_fs";
          doCmd($cmd);
          $voip_phone++;
          $rtp_port += 2;
          $sound_file_idx++;
          
          $cmd = "set_voip_info $ep2 $start_dly $mn_icg $mx_icg NA $codec $vproto NA NA $min_call_duration $max_call_duration /dev/null 20000 $sip_port_b $pesq_server $pesq_server_port NA $jB_size";
          doCmd($cmd);

          if ($i_sip_port_b != 0) {
            $sip_port_b = $sip_port_b + $i_sip_port_b;
          }

          $cmd = "set_endp_flag $ep2 SavePCM 0";
          doCmd($cmd);

          $cmd = "set_endp_tos $ep2 ${tos} 0";
          doCmd($cmd);

          if ($peer_to_peer_voip) {
            $cmd = "set_endp_flag $ep2 DoNotRegister 1";
            doCmd($cmd);
            $cmd = "set_endp_flag $ep2 BindSIP 1";
            doCmd($cmd);
          }

              if ($no_send_rtp) {
                $cmd = "set_endp_flag $ep2 nosendrtp 1";
                doCmd($cmd);
              }

          if ($use_VAD) {
            $cmd = "set_endp_flag $ep2 VAD 1";
            doCmd($cmd);
          }

          if ($use_PESQ) {
            $cmd = "set_endp_flag $ep2 pesq 1";
            doCmd($cmd);
          }

          my $cmd = "add_voip_endp $ep1 $shelf $lf1 " . $all_ports1[$j] .
                    " $voip_phone $rtp_port AUTO " .
                $src_sound_files[$sound_file_idx % @src_sound_files] .
                        " " . $src_sound_files[$sound_file_idx % @src_sound_files] .
                ".$ep1";
          doCmd($cmd);

          $cmd = "set_voip_info $ep1 $start_dly $mn_icg $mx_icg NA $codec $vproto NA NA $min_call_duration $max_call_duration /dev/null 20000 $sip_port_a $pesq_server $pesq_server_port NA $jB_size";
          doCmd($cmd);

          $start_dly += $start_dly_inc;

          if ($i_sip_port_a != 0) {
            $sip_port_a = $sip_port_a + $i_sip_port_a;
          }

          $cmd = "set_endp_flag $ep1 SavePCM 0";
          doCmd($cmd);

          $cmd = "set_endp_tos $ep1 ${tos} 0";
          doCmd($cmd);

          if ($peer_to_peer_voip) {
            $cmd = "set_endp_flag $ep1 DoNotRegister 1";
            doCmd($cmd);
            $cmd = "set_endp_flag $ep1 BindSIP 1";
            doCmd($cmd);
          }
              if ($no_send_rtp) {
                $cmd = "set_endp_flag $ep1 nosendrtp 1";
                doCmd($cmd);
              }

          if ($use_VAD) {
            $cmd = "set_endp_flag $ep1 VAD 1";
            doCmd($cmd);
          }

          if ($use_PESQ) {
            $cmd = "set_endp_flag $ep1 pesq 1";
            doCmd($cmd);
          }

          $voip_phone++;
          $rtp_port += 2;
          $sound_file_idx++;

          # Now, add the cross-connects
          my $cx_name = "rtp-cx-${num[$cx]}";
          $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
          doCmd($cmd);
          doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

          $cx++;

          @cx_names = (@cx_names, $cx_name);
#       }
#       else {
#         my $burst = "NO";
#         if ($min_rate != $max_rate) {
#           $burst = "YES";
#         }
#         my $szrnd = "NO";
#         if ($min_pkt_szs[$i] != $max_pkt_szs[$i]) {
#           $szrnd = "YES";
#         }
#
#         my $pattern = "increasing";
#         if ($cx_types[$i] =~ /custom/) {
#           $pattern = "custom";
#         }
#
#         my $ep1 = "l3e-${ep}-TX";
#         $ep++;
#         my $ep2 = "l3e-${ep}-RX";
#         $ep++;
#
#         @endpoint_names = (@endpoint_names, $ep1, $ep2);
#
#         my $cmd = "add_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " " . @cx_types[$i] .
#           " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " . $max_pkt_szs[$i] .
#             " $pattern NO";
#         doCmd($cmd);
#
#         if ($lf2 == "") {
#           die("Must lave lf2 defined if using non-l4 endpoints.");
#         }
#
#         $cmd =    "add_endp $ep2 $shelf $lf2 " . $all_ports2[$j] . " " . @cx_types[$i] .
#           " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " .
#             $max_pkt_szs[$i] . " $pattern NO";
#         doCmd($cmd);
#
#         # Now, add the cross-connects
#         my $cx_name = "l3-cx-${cx}";
#         $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
#         doCmd($cmd);
#         doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");
#
#         $cx++;
#
#         @cx_names = (@cx_names, $cx_name);
#       }
#     }#for cx types
    }#for each port
# }# each cx per port
}#addCrossConnects


sub doCmd {
  my $cmd = shift;

  print ">>> $cmd\n";

  $t->print($cmd);

  my @rslt = $t->waitfor('/ \>\>RSLT:(.*)/');
  print "**************\n @rslt ................\n\n";
  #sleep(1);
}


sub printHelp {
  print
    "\n$script_name\n"
  . "USAGE:  mgr=[ip-of-mgr] init=[0|1] speed=25\n"
  . "        lf1=X lf2=Y\n"
  . "        lf1_ports=[\"1 2 3\"|\"eth2 eth3\"] lf2_ports=[\"4 5 6\"|\"eth4 eth5\"]\n"
  . "        start_mvl=X num_cxs=[N|0 num_mvl=Y]\n"
  . "        mac3=0xf0 mac2=0xbe mac1=0xef\n"
  . "        ip_base=192.168 ip_c=1 ip_lsb=2 ip_msk=255.255.0.0\n"
  . "\n";

}

sub handleCmdLineArg {
  my $arg = $_[0];
  my $val = $_[1];

  if ($arg eq "mgr") {
    $lfmgr_host = $val;
  }
  elsif ($arg eq "init") {
    $INIT = $val;
  }
  elsif ($arg eq "speed") {
    $script_speed = $val;
  }
  elsif ($arg eq "lf1") {
    $lf1 = $val;
  }
  elsif ($arg eq "lf2") {
    $lf2 = $val;
    if ($lf1 == $lf2) {
      print "\nINVALID: First and second resource are the same !!!\n\n";
      exit (1);
    }
  }
  elsif ($arg eq "mac3") {
    $mac3 = $val;
  }
  elsif ($arg eq "mac2") {
    $mac2 = $val;
  }
  elsif ($arg eq "mac1") {
    $mac1 = $val;
  }  
  elsif ($arg eq "ip_base") {
    $ip_base = $val;
  }
  elsif ($arg eq "ip_lsb") {
    $ip_lsb = $val;
  }
  elsif ($arg eq "ip_c") {
    $ip_c = $val;
  }
  elsif ($arg eq "ip_msk") {
    $msk = $val;
  }
  elsif ($arg eq "lf1_ports") {
    @lf1_ports = split(/ /, $val);
  }
  elsif ($arg eq "lf2_ports") {
    if ($lf2 == "" || $lf1 == $lf2) {
      print "\nINVALID: Either second resource is not defined\nor first and second resource are the same !!!\n\n";
      exit (1);
    }
    else {
      @lf2_ports = split(/ /, $val);
    }
  }
  elsif ($arg eq "start_mvl") {
    $start_mvlan = $val;
  }
  elsif ($arg eq "num_cxs") {
    $num_cxs = $val;
  }
  elsif ($arg eq "num_mvl") {
    $num_mvlans = $val;
  }
  else {
    printHelp();
    exit(1);
  }
} # handleCmdLineArg
