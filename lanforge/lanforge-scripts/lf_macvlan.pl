#!/usr/bin/perl

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# This script sets up connections of types:
# lf, lf_udp, lf_tcp, custom_ether, custom_udp, custom_tcp, l4 (http, https, ftp and fileIO)
# across real ports and MACVLAN ports on one or more machines.
# It then continously starts and stops the connections.

# Un-buffer output
$| = 1;

use strict;
#use Switch;  

use Net::Telnet ();
use LANforge::Port;
use LANforge::Utils;

my $script_speed = 25;      # Increase to issue commands faster.
my $pause = 0;              # Increase delay (seconds) if experiencing problems on slow systems.

my $INIT = 0;               # If true, removes all previous tests and ports!!!
my $create_only = 1;        # If true, only create tests, i.e. do not automatically run them.

my $mac_init   = 0;         # Set to 1 to start MAC address from zero when running looped test.
my $ip_init    = 0;         # Set to 1 to start IP addresses from zero when running looped test.
my $init_once  = 0;         # Set to 1 to only initialize test creation once.
my $init_net   = 1;         # Set to 0 to disable reconfiguring MAC and IP addresses.
my $init_tests = 1;         # Set to 0 to disable reconfiguring tests.
my $first_run  = 1;         # Set to 0 to disable initial configurations.
my $name_id    = 0;         # First index of name of endpoints and CXs.
my $name_id_len = 0;        # Override for length of $name_id.
my $loop_max   = 100;
my $start_stop_loops = 2;
my $run_for_time  = 120;    # Run for XX seconds..then will be stopped again
my $stop_for_time = 5;      # Run for XX seconds..then will be stopped again
my $ignore_phys_ports = 1;  # If true, just muck with mac-vlans.

my $one_cx_per_port = 0;    # If zero, will have one of EACH of the cx types on each port.

my $cx_types_from_file = 0; # If true, will rotate through the @cx_types_files
                            # when creating tests instead of using @cx_types array.
#cx_types files must be CSV.
my @cx_types_files = ("/tmp/cx_type-foo.txt", "/tmp/cx_type-foo1.txt");

#my @cx_types =     ("lf", "lf_udp", "lf_tcp", "custom_udp", "custom_tcp", "l4", "voip");
#my @min_pkt_szs =  (64,   1,        1,         1,            1,            0);
#my @max_pkt_szs =  (1514, 12000,    13000,     2048,         2048,         0);

#my @cx_types =     ("lf_udp");
my @cx_types =     ("lf_tcp");
#my @cx_types =     ("l4", "l4", "l4", "l4", "l4", "l4", "l4", "l4", "l4", "l4");
#my @cx_types =     ("l4");
#my @cx_types = (
#"lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp"
#,"l4");


my $test_mgr = "ben_tm";
my $report_timer = 8000;       # Set report timer for all tests created in ms, i.e. 8 seconds

my $lfmgr_host = undef;
my $lfmgr_port = 4001;

my $shelf = 1;

# This sets up connections.
my $lf1 = 1;  # Minor Resource EID of first LANforge resource.
my $lf2 = ""; # Set to "" if we have no second machine.  Or set to second Resource
              # minor EID to create mac-vlans on it.


# Port pairs.  These are the ports that should be talking to each other.
# i.e. the third column in lf1_ports talks to the third column in lf2_ports.
# EIDs or aliases can be used.
# Port pairs must match on each shelf - will enhance to allow any pair on each shelf.
#my @lf1_ports = (1); #, 2, 3);
#my @lf2_ports = (2); #, 2, 3);
my @lf1_ports = (       "eth0",        "eth1");
my @lf2_ports = ("");
my @ip_base   = (    "192.168",      "172.16");
my @ip_c      = (           2 ,            1 );
my @ip_lsb    = (           2 ,            2 );
my @msk       = ("255.255.0.0", "255.255.0.0");
my @ip_gw     = ("192.168.2.1",  "172.16.1.1");

#my $ip_base1 = "172.16";    # Use this set.
#my $ip_c1 = 2;              #
#my $ip_lsb1 = 2;            #
#my $msk1 = "255.255.0.0"; #
#my $ip_gw1 = "0.0.0.0";     #

my $mac1 = 0x00;         # Starting MAC address 00:m5:m4:m3:m2:m1 where:
my $mac2 = 0x00;         # m5 is shelf EID, m4 is card EID, m3 is $mac3, 
my $mac3 = 0x00;         # m2 is $mac2 and m1 is $mac1.

my $mvl = 1;
my $start_mvlan = 0;
my $num_mvlans = 9;
my $num_cxs = 10;

#my @min_rate = (100000);# bps
#my @max_rate = (100000);# bps
my @min_rate = (9600, 64000, 1000000, 9600);   # bps
my @max_rate = (9600, 64000, 1000000, 1000000);# bps
#my @min_pkt_szs =  (0); # bytes
#my @max_pkt_szs =  (0); # bytes
my @min_pkt_szs =  (40, 548, 1472, 40); # bytes
my @max_pkt_szs =  (40, 548, 1472, 1472); # bytes


################
# Layer-4 Only #
################

my $url_dl = 1;               # If true, test will download from URL.  False will upload to URL.
#my $l4_dl_path = "/tmp";     # Path to save downloaded file.
#my $l4_dl_path = "NUL";      # Windows equivalent of *nix /dev/null.
my $l4_dl_path = "/dev/null"; # Improve performance by saving downloaded file to /dev/null.

#my @l4_urls = (
# "http://192.168.100.3/index.html", "ftp://192.168.100.3/file", "http://192.168.100.3/index.html", "ftp://192.168.100.3/file"
#,"http://192.168.100.3/index.html", "ftp://192.168.100.3/file", "http://192.168.100.3/index.html", "ftp://192.168.100.3/file"
#,"http://192.168.100.3/index.html", "ftp://192.168.100.3/file", "http://192.168.100.3/index.html", "ftp://192.168.100.3/file"
#,"http://192.168.100.3/index.html", "ftp://192.168.100.3/file", "http://192.168.100.3/index.html", "ftp://192.168.100.3/file"
#,"http://192.168.100.3/index.html", "ftp://192.168.100.3/file", "http://192.168.100.3/index.html", "ftp://192.168.100.3/file"
#);
my @l4_urls = ("http://192.168.100.3/index.html");
#my @l4_urls = ("ftp://192.168.100.3/file");

my $urls_10m = 100;           # How many URLs to process every 10 minutes.
my $l4_timeout = 10000;       # How long to wait for a connection, in milliseconds.


#############
# VoIP Only #
#############
my $codec = "G711U"; # Other options:  G711U, g729a, SPEEX, g726-16, g726-24, g726-32, g726-40
my $jB_size = 1;     # Set jitter buffer size in 20ms packets.  Default value is 8 packets, 160ms.
my $tos = 0xBE;      # Set ToS/QoS for VoIP can be decimal or 0xNN for hexadecimal but values will display in decimal in the GUI.

my $mn_icg = 3;            # minimum intercall gap
my $mx_icg = 3;            # maximum intercall gap
my $min_call_duration = 0; # set to zero for 'file'
my $max_call_duration = 0; # Set to zero for 'file'

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

my $peer_to_peer_voip = 1; # Don't register with SIP proxy, but just call peer to peer.

my @src_sound_files = ("media/female_voice_8khz.wav");

################
# File-IO Only #
################
my $fio_base = "/mnt/fio_base";
my $fio_targ_dir = "";
my $fsrw = "write";


my $DEBUG = 0;
my $D_PAUSE = 3;

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

if ($lfmgr_host eq undef) {
  print "\nYou must define a LANforge Manager!!!\n\n"
      . "For example:\n"
      . "./$script_name mgr=localhost\n"
      . "OR\n"
      . "./$script_name mgr=192.168.1.101\n\n";
  printHelp();
  exit (1);
}

my $foundL4 = 0;
for ($i = 0; $i<@cx_types; $i++) {
  if ($cx_types[$i] eq "l4") {
    $foundL4 = 1;
    last;
  }
}
if ($lf2 == "" && @lf1_ports < 2 && !$foundL4) {
  die ("Must have more than one port with only one resource.");
}


if (!$num_mvlans) { $mvl=0; }


#if (!$start_mvlan && !$num_mvlan && $num_cxs) {
#  die ("Must have either number of MACVLANs (num_mvl) or cross-connects (num_cxs) > 0.");
#}

print
    "\nStarting script with the following arguments:"
  . "\ninit: $INIT"
  . "\nmanager: $lfmgr_host\n"
  . "\nlf1: $lf1\nlf2: $lf2\n"
  . "\nlf1_ports: " . join(" ", @lf1_ports)
  . "\nlf2_ports: " . join(" ", @lf2_ports) . "\n"
  . "\nstart_macvlans: $start_mvlan"
  . "\nnum_mvlans: $num_mvlans\n"
  . "\nmin_rates: " . join(" ", @min_rate)
  . "\nmax_rates: " . join(" ", @max_rate) 
  . "\nmin_pkt_sizes: " . join(" ", @min_pkt_szs)
  . "\nmax_pkt_sizes: " . join(" ", @max_pkt_szs) . "\n"
  . "\ncx_types: " . join(" ", @cx_types)
  . "\nnum_cxs: $num_cxs\n"
  . "\none_cx_per_port: $one_cx_per_port\n\n";

if ($DEBUG) { sleep ($D_PAUSE); }


# Determine total port and endpoint counts and make sorting by name easier in the GUI :P

my @num = ();    # Formatted index number for name sorting in GUI.
my $t_num = 0;
my $t_ports = 0;
my $ni=0;
my $nj=0;

my @lf1orig_ports = @lf1_ports;
my @lf2orig_ports = @lf2_ports;
my $lf2orig = $lf2;
 
if ($lf2 == "") {
  $lf2 = $lf1;
  if ($foundL4) {
    @lf2_ports = undef;
  }
  else {
    # Put every other port into @lf2_ports to fake out lf2 info which makes the
    # script work later.
    # TODO: Stop faking out too early since we end up probing the same ports multiple times
    #       because of $num_cxs.  This needs to move to below utils->updatePort @all_ports1
    #       and @all_ports2
    @lf1_ports = undef;
    @lf2_ports = undef;
    $i=0;
    if ($mvl) {
      for ($ni=0; $ni<@lf1orig_ports; $ni++) {
        $lf1_ports[$i] = $lf1orig_ports[$ni];
        $lf2_ports[$i] = $lf1orig_ports[++$ni];
        $i++;
      }  
    } else {
      for ($nj=0; $nj<($num_cxs*2); $nj++) {
        for ($ni=0; $ni<(@lf1orig_ports); $ni++) {
          $lf1_ports[$i] = $lf1orig_ports[$ni];
          $lf2_ports[$i] = $lf1orig_ports[++$ni];
          $i++;
        }
      }
    } # if mvl 
  } # if foundL4
} # if lf2 = ""

if ($DEBUG) { printArgs(); sleep ($D_PAUSE); }

# Check that ip_base address pairs aren't the same.
for ($ni = 0; $ni<@ip_base; $ni++) {
  if ($ip_base[$ni] == $ip_base[$ni+1]) {
    die ("ERROR: Base IP addresses cannot be the same.");
  }
  $ni++;
}

my @cxts = ("lf", "lf_udp", "lf_tcp", "custom_udp", "custom_tcp", "l4",
            "fileIONFS", "fileIOCIFS");
my @t_cxts = ();
for ($ni=0; $ni<@cxts; $ni++) {
  @t_cxts[$ni] = 0;
}

if ($lf2orig ne "") {
  if ($ignore_phys_ports) {
    $t_ports = $num_mvlans;
  }
  else {
    $t_ports = @lf1_ports + @lf2_ports + ($num_mvlans);
    if (@lf2_ports eq undef) { $t_ports--; }
  }
}
elsif ($num_mvlans) {
  if ($ignore_phys_ports) {
    $t_ports = $num_mvlans;
  }
  else {
    $t_ports = @lf1_ports + ($num_mvlans);
  }
}
else {
  $t_ports = @lf1_ports + @lf2_ports;
  if (@lf2_ports eq undef) { $t_ports--; }
  $t_ports *= $num_cxs;
}

my $t_cxtypes = @cx_types;
my $t_urls = @l4_urls;

if (@min_rate != @max_rate ) {
  die("Number of elements in min_rate does not match number of elements in max_rate.");
}
else {
  my $t_rate = @min_rate + @max_rate;
}
if (@min_pkt_szs != @max_pkt_szs ) {
  die("Number of elements in min_pkt_szs does not match number of elements in max_pkt_szs.");
}
else {
  my $t_pkt_szs = @min_pkt_szs + @max_pkt_szs;
}

for ($ni=0; $ni<@cx_types; $ni++) {
  for ($nj=0; $nj<@cxts; $nj++) {
    if ( $cx_types[$ni] eq $cxts[$nj] ) {
      $t_cxts[$nj]++;
    }
  }
}

for ($nj=0; $nj<@cxts; $nj++) {
  if ( $cxts[$nj] eq "l4") {
    $t_num += ($t_ports * (2 * ($t_cxts[$nj] * $t_urls)));
  }
  else {
    $t_num += ($t_ports * (2 * $t_cxts[$nj]));
  }
}
$t_num += $name_id;

my $num_len;
if ($name_id_len) {
  if (length($name_id) > $name_id_len || length($t_num) > $name_id_len) {
    print "\nWARNING: id_len specifies a string length less that first_name_id or less that total number of endpoints\n";
  }
  $num_len = $name_id_len;
}
else {
  $num_len = length ($t_num);
}
$t_num -= $name_id;
my $i = 0;

# !!! DO NOT Reimplement Switch/Case since the following will cause switch/case to fail:
# !!! for ($nj=0; $nj<($num_cxs / @lf1orig_ports); $nj++) {
# !!! Why? DUNNO!

#switch ($num_len) {
#  case 1 {
#    for ($i ; $i<$t_num; $i++) {
#      $num[$i] = sprintf("%01d", $name_id + $i);
#    }
#  }
#  case 2 {
#    for ($i ; $i<$t_num; $i++) {
#      $num[$i] = sprintf("%02d", $name_id + $i);
#    }
#  }
#  case 3 {
#    for ($i ; $i<$t_num; $i++) {
#      $num[$i] = sprintf("%03d", $name_id + $i);
#    }
#  }
#  case 4 {
#    for ($i ; $i<$t_num; $i++) {
#      $num[$i] = sprintf("%04d", $name_id + $i);
#    }
#  }
#  case 5 {
#    for ($i ; $i<$t_num; $i++) {
#      $num[$i] = sprintf("%05d", $name_id + $i);
#    }
#  }
#  case 6 {
#    for ($i ; $i<$t_num; $i++) {
#      $num[$i] = sprintf("%06d", $name_id + $i);
#    }
#  }
#  else {
#    for ($i ; $i<$t_num; $i++) {
#      $num[$i] = $name_id + $i;
#    }
#  }
#}

if ($num_len == 1) {
  for ($i ; $i<$t_num; $i++) {
      $num[$i] = sprintf("%01d", $name_id + $i);
  }
}
elsif ($num_len == 2) {
  for ($i ; $i<$t_num; $i++) {
    $num[$i] = sprintf("%02d", $name_id + $i);
  }
}
elsif ($num_len == 3) {
  for ($i ; $i<$t_num; $i++) {
    $num[$i] = sprintf("%03d", $name_id + $i);
  }
}
elsif ($num_len == 4) {
  for ($i ; $i<$t_num; $i++) {
    $num[$i] = sprintf("%04d", $name_id + $i);
  }
}
elsif ($num_len == 5) {
  for ($i ; $i<$t_num; $i++) {
    $num[$i] = sprintf("%05d", $name_id + $i);
  }
}
elsif ($num_len == 6) {
  for ($i ; $i<$t_num; $i++) {
    $num[$i] = sprintf("%06d", $name_id + $i);
  }
}
else {
  for ($i ; $i<$t_num; $i++) {
    $num[$i] = $name_id + $i;
  }
}

if ($DEBUG > 99) {
  $i = 0;
  print "name_id: $name_id, t_num: $t_num, num_len: $num_len :-\n";
  for ($i ; $i<$t_num; $i++) {
    print $num[$i] . " ";
  }
  print "\n";
  sleep ($D_PAUSE);
}
if ($DEBUG) { printArgs(); sleep ($D_PAUSE); }

# Open connection to the LANforge server.
my $t = new Net::Telnet(Timeout => 15,
                        Prompt => '/default\@btbits\>\>/');

$t->open(Host    => $lfmgr_host,
         Port    => $lfmgr_port,
         Timeout => 45);

$t->waitfor("/btbits\>\>/");
$t->max_buffer_length(1024 * 1024 * 10); # 10M buffer

# Configure our utils.
my $utils = new LANforge::Utils();
$utils->telnet($t);         # Set our telnet object.
$utils->cli_send_silent(0); # Do show input to CLI
$utils->cli_rcv_silent(0);  # Repress output from CLI ??

my $dt = getDate();
my $dt_start = $dt;

my @endpoint_names = (); #will be added to as they are created
my @cx_names = ();

my $loop = 0;
for ($loop = 0; $loop<$loop_max; $loop++) {
  $dt = getDate();
  print "\n\n*****  Starting $script_name loop: $loop at: $dt  *****\n\n";

  if (!$init_once) {
    if ($INIT) { initToDefaults(); }
    
    if ($init_net) {
      if ($mvl) { addMacVlans(); }                # Add MACVLANs.
      initIpAddresses();                          # Add some IP addresses to the ports.
    }
    if ($init_tests) {
      doCmd("rm_cx $test_mgr all");
      doCmd("rm_endp YES_ALL");
      doCmd("rm_test_mgr $test_mgr");
      doCmd("add_tm $test_mgr");
      doCmd("tm_register $test_mgr default");     # Add default user
      doCmd("tm_register $test_mgr default_gui"); # Add default GUI user    
      addCrossConnects();                         # Add our endpoints.
    }
  }
  elsif ($first_run) {
    $first_run = 0;
    if ($INIT) { initToDefaults(); }
    
    if ($init_net) {
      if ($mvl) { addMacVlans(); }
      initIpAddresses();
    }
    if ($init_tests) {
      doCmd("rm_cx $test_mgr all");
      doCmd("rm_endp YES_ALL");
      doCmd("rm_test_mgr $test_mgr");
      doCmd("add_tm $test_mgr");
      doCmd("tm_register $test_mgr default");     # Add default user
      doCmd("tm_register $test_mgr default_gui"); # Add default GUI user    
      addCrossConnects();                         # Add our endpoints.
    }
  }
  
  $dt = getDate();
  print "\n\n*** Started $script_name script at        : $dt_start ***\n"
          . "*** Finished $script_name configuration at: $dt ***\n\n";
  sleep($D_PAUSE);

  if ($create_only == 1) { exit(0); }

  my $rl = 0;
  for ($rl = 0; $rl<$start_stop_loops; $rl++) {
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
}# for some amount of loop iterations

if ($DEBUG) { printArgs(); }

$dt = getDate();
print "Started $script_name script at  : $dt_start\n";
print "Completed $script_name script at: $dt\n\n";
exit(0);
#####################
# END lf_macvlan.pl #
#####################
sub addCrossConnects {
  my $ep = 0;
  my $cx = 0;
  my $i = 0;
  my $szs = 0;
  my $r = 0;
  my @all_ports1 = @lf1_ports;
#  my @all_ports1 = @lf1orig_ports;  This don't work
  my @all_ports2 = ("");
  my $j;
  my $pname;

  if ($foundL4) {  
    my $p1 = new LANforge::Port();
    my $q;
    for ($q = $start_mvlan; $q<($num_mvlans + $start_mvlan); $q++) {
      for ($j = 0; $j<@lf1_ports; $j++) {
        $utils->updatePort($p1, $shelf, $lf1, $lf1_ports[$j]);
        $pname = $p1->{dev};
        @all_ports1 = (@all_ports1, "$pname\#$q");
      }
    }
    if ($ignore_phys_ports) {
      for ($j = 0; $j<@lf1_ports; $j++) {
        shift(@all_ports1);
      }
    }
    # TODO: Fake out ports here to create num_cxs tests.
  }
  else {
    for ($j = 0; $j<@lf1_ports; $j++) {
      my $p1 = new LANforge::Port();
      $utils->updatePort($p1, $shelf, $lf1, $lf1_ports[$j]);
      $pname = $p1->{dev};
      my $q;
      for ($q = $start_mvlan; $q<($num_mvlans + $start_mvlan); $q++) {
        @all_ports1 = (@all_ports1, "$pname\#$q");
      }
    }
    @all_ports2 = @lf2_ports;
#    @all_ports2 = @lf2orig_ports;  This don't work
    for ($j = 0; $j<@lf2_ports; $j++) {
      my $p1 = new LANforge::Port();
      $utils->updatePort($p1, $shelf, $lf2, $lf2_ports[$j]);
      $pname = $p1->{dev};
      my $q;
      for ($q = $start_mvlan; $q<($num_mvlans + $start_mvlan); $q++) {
        @all_ports2 = (@all_ports2, "$pname\#$q");
      }
    }
    if ($ignore_phys_ports) {
      for ($j = 0; $j<@lf1_ports; $j++) {
       shift(@all_ports1);
      }
      for ($j = 0; $j<@lf2_ports; $j++) {
        shift(@all_ports2);
      }
    }
    # TODO: Fake out ports here to create num_cxs tests.
  } # if foundL4
      
  print "\n\n\nCreating endpoints on " . @all_ports1 . " ports:\nall_ports1: " . join(" ", @all_ports1);
  
#  if ($lf2orig ne "") {
    print "\nCreating endpoints on " . @all_ports2 . " ports:\nall_ports2: " . join(" ", @all_ports2) . "\n\n\n";
#  }

  if ($DEBUG) { sleep($D_PAUSE); }

  if ($one_cx_per_port) {
    my $j = 0;
    my $cxcnt = 0;
    my $fecnt = 0;
    for ($j ; $j<@all_ports1; $j++) {
      my $i = $cxcnt % @cx_types;
      $cxcnt++;

      my $cxt = $cx_types[$i];
      if ($cxt eq "l4") {
        # Create layer-4 endpoint

        my $ep1 = "L4-${num[$ep]}";
#        $ep++;
        my $ep2 = "D_L4-${num[$ep]}";
        $ep++;

        @endpoint_names = (@endpoint_names, $ep1, $ep2);

        # Add the dummy endpoint
        my $cmd = "add_l4_endp $ep2 $shelf $lf1 " . $all_ports1[$j]
                   . " l4_generic  0 0 0 ' ' ' '";
        doCmd($cmd);
        $cmd = "set_endp_flag $ep2 unmanaged 1";
        doCmd($cmd);

        if ($l4_dl_path = "/dev/null") {
          $cmd = "add_l4_endp $ep1 $shelf $lf1 " . $all_ports1[$j]
                  . " l4_generic 0 $l4_timeout $urls_10m 'dl ${l4_urls[0]} $l4_dl_path' ' '";
        }
        else {
          $cmd = "add_l4_endp $ep1 $shelf $lf1 " . $all_ports1[$j]
                  . " l4_generic 0 $l4_timeout $urls_10m 'dl ${l4_urls[0]} $l4_dl_path/$ep1' ' '";
        }
        doCmd($cmd);

        # Now, add the cross-connects
        my $cx_name = "L4-${num[$cx]}";
        $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
        doCmd($cmd);
        doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

        $cx++;

        @cx_names = (@cx_names, $cx_name);
      }# if L4
      elsif ($cxt eq "voip") {
      	
      	
      	
      	
      	
      }# if VoIP   
      elsif (($cxt eq "fileIONFS") || ($cxt eq "fileIOCIFS")) {
        # Create File-IO endpoint

        my $FST = "nfs";
        if ($cxt eq "fileIOCIFS") {
          $FST = "cifs";
        }

        my $ep1 = "fe-${num[$fecnt]}";
        my $ep2 = "D_$ep1";
        $fecnt++;
        $ep++;
#        $ep++;

        @endpoint_names = (@endpoint_names, $ep1, $ep2);

        # Add the dummy endpoint
        my $cmd = "add_file_endp $ep2 $shelf $lf1 " . $all_ports1[$j]
                   . " fe_generic $min_rate[$r] $max_rate[$r] $min_rate[$r] $max_rate[$r]"
                   . " increasing $fio_base/$ep2 $ep2";
        doCmd($cmd);
        $cmd = "set_endp_flag $ep2 unmanaged 1";
        doCmd($cmd);

        $cmd = "add_file_endp $ep1 $shelf $lf1 " . $all_ports1[$j]
                   . " fe_generic $min_rate[$r] $max_rate[$r] $min_rate[$r] $max_rate[$r]"
                   . " increasing \'$fio_base/$FST"
                   . "_$all_ports1[$j]" . $fio_targ_dir . "\' $ep1";
        doCmd($cmd);

        $cmd = "set_fe_info $ep1 16384 16384 10 1000000 1000000 \'$fio_base/$FST" . "_$all_ports1[$j]"
                   . $fio_targ_dir . "\' $ep1 $fsrw";
        doCmd($cmd);

        if ($r < (@min_rate - 1)) {
          $r++;
        }
        else {
          $r = 0;
        }

        # Now, add the cross-connects
        my $cx_name = "L4-${num[$cx]}";
        $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
        doCmd($cmd);
        doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

        $cx++;

        @cx_names = (@cx_names, $cx_name);
      }# elsif FIO
      else {
        # Create L3 endpoint

        my $burst = "NO";
        if ($min_rate[$r] != $max_rate[$r]) {
          $burst = "YES";
        }
        my $szrnd = "NO";
        if ($min_pkt_szs[$szs] != $max_pkt_szs[$szs]) {
          $szrnd = "YES";
        }

        my $pattern = "increasing";
        if ($cx_types[$i] =~ /custom/) {
          $pattern = "custom";
        }

        my $ep1 = "L3e-${num[$ep]}tx";
        $ep++;
        my $ep2 = "L3e-${num[$ep]}rx";
        $ep++;

        @endpoint_names = (@endpoint_names, $ep1, $ep2);

        my $cmd = "add_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " " . @cx_types[$i] .
                  " -1 $burst $min_rate[$r] $max_rate[$r] $szrnd " . $min_pkt_szs[$szs] . " " . $max_pkt_szs[$szs] .
                  " $pattern NO";
        doCmd($cmd);

        if ($lf2 ne "") {
#          die("Must have lf2 defined if using non-l4 endpoints.");
          $cmd = "add_endp $ep2 $shelf $lf2 " . $all_ports2[$j] . " " . @cx_types[$i] .
                 " -1 $burst $min_rate[$r] $max_rate[$r] $szrnd " . $min_pkt_szs[$szs] . " " .
                 $max_pkt_szs[$szs] . " $pattern NO";
        }
        else {
          $cmd = "add_endp $ep2 $shelf $lf1 " . $all_ports1[($j)] . " " . @cx_types[$i] .                     
                 " -1 $burst $min_rate[$r] $max_rate[$r] $szrnd " . $min_pkt_szs[$szs] . " " . $max_pkt_szs[$szs] .
                 " $pattern NO";                                                                                  
        }
        doCmd($cmd);

        if ($szs < (@min_pkt_szs - 1)) { $szs++; }
        else { $szs = 0; }
        if ($r < (@min_rate - 1)) { $r++; }
        else { $r = 0; }

        # Now, add the cross-connects
        my $cx_name = "L3-${num[$cx]}";
        $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
        doCmd($cmd);
        doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

        $cx++;

        @cx_names = (@cx_names, $cx_name);
      }# else L3
    }#for all ports
  }#one_cx_per_port = 1
  else {
    my $j = 0;
    my $n = 0;
    my $fecnt = 0;
    for ($j; $j<@all_ports1; $j++) {
      for ($i = 0; $i<@cx_types; $i++) {
        my $cxt = $cx_types[$i];
        if ($cxt eq "l4") {
          # Create layer-4 endpoint
          for ($n = 0; $n<@l4_urls; $n++) {
            my $ep1 = "L4-${num[$ep]}";
#            $ep++;
            my $ep2 = "D_L4-${num[$ep]}";
            $ep++;

            @endpoint_names = (@endpoint_names, $ep1, $ep2);

            # Add the dummy endpoint
            my $cmd = "add_l4_endp $ep2 $shelf $lf1 " . $all_ports1[$j] . " l4_generic  0 0 0 ' ' ' '";
            doCmd($cmd);
            $cmd = "set_endp_flag $ep2 unmanaged 1";
            doCmd($cmd);
            if ($l4_dl_path = "/dev/null") {
              $cmd = "add_l4_endp $ep1 $shelf $lf1 " . $all_ports1[$j]
                      . " l4_generic 0 $l4_timeout $urls_10m 'dl ${l4_urls[$n]} $l4_dl_path' ' '";
            }
            else {
              $cmd = "add_l4_endp $ep1 $shelf $lf1 " . $all_ports1[$j]
                      . " l4_generic 0 $l4_timeout $urls_10m 'dl ${l4_urls[$n]} $l4_dl_path/$ep1' ' '";
            }
            doCmd($cmd);

            # Now, add the cross-connects
            my $cx_name = "L4-${num[$cx]}";
            $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
            doCmd($cmd);
            doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

            $cx++;

            @cx_names = (@cx_names, $cx_name);
          } #for url_list
        }
        elsif ($cxt eq "voip") {
      	
      	
      	
      	
      	
        }# if VoIP   
        elsif (($cxt eq "fileIONFS") || ($cxt eq "fileIOCIFS")) {
          # Create File-IO endpoint
          my $FST = "nfs";
          if ($cxt eq "fileIOCIFS") {
            $FST = "cifs";
          }

          my $ep1 = "fe-${num[$fecnt]}";
          my $ep2 = "D_$ep1";
          $fecnt++;
          $ep++;
#          $ep++;

          @endpoint_names = (@endpoint_names, $ep1, $ep2);

          # Add the dummy endpoint
          my $cmd = "add_file_endp $ep2 $shelf $lf1 " . $all_ports1[$j]
                    . " fe_generic $min_rate[$r] $max_rate[$r] $min_rate[$r] $max_rate[$r]"
                    . " increasing $fio_base/$ep2 $ep2";
          doCmd($cmd);
          $cmd = "set_endp_flag $ep2 unmanaged 1";
          doCmd($cmd);

          $cmd = "add_file_endp $ep1 $shelf $lf1 " . $all_ports1[$j]
                 . " fe_generic $min_rate[$r] $max_rate[$r] $min_rate[$r] $max_rate[$r]"
                 . " increasing $fio_base/$FST" . "_$all_ports1[$j]" . $fio_targ_dir . " $ep1";
          doCmd($cmd);

          $cmd = "set_fe_info $ep1 16384 16384 10 1000000 1000000 $fio_base/$FST"
                     . "_$all_ports1[$j]" . $fio_targ_dir . " $ep1 $fsrw";
          doCmd($cmd);

          if ($r < (@min_rate - 1)) { $r++; }
          else { $r = 0; }

          # Now, add the cross-connects
          my $cx_name = "L4-${num[$cx]}";
          $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
          doCmd($cmd);
          doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

          $cx++;

          @cx_names = (@cx_names, $cx_name);
        }
        else {
          # Create L3 endpoint
          
          my $burst = "NO";
          if ($min_rate[$r] != $max_rate[$r]) {
            $burst = "YES";
          }
          my $szrnd = "NO";
          if ($min_pkt_szs[$szs] != $max_pkt_szs[$szs]) {
            $szrnd = "YES";
          }

          my $pattern = "increasing";
          if ($cx_types[$i] =~ /custom/) {
            $pattern = "custom";
          }

          my $ep1 = "L3e-${num[$ep]}tx";
          $ep++;
          my $ep2 = "L3e-${num[$ep]}rx";
          $ep++;

          @endpoint_names = (@endpoint_names, $ep1, $ep2);

          my $cmd = "add_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " " . @cx_types[$i] .
            " -1 $burst $min_rate[$r] $max_rate[$r] $szrnd " . $min_pkt_szs[$szs] . " " . $max_pkt_szs[$szs] .
              " $pattern NO";
          doCmd($cmd);


          if ($lf2 ne "") {
#            die("Must have lf2 defined if using non-l4 endpoints.");
            $cmd = "add_endp $ep2 $shelf $lf2 " . $all_ports2[$j] . " " . @cx_types[$i] .
                   " -1 $burst $min_rate[$r] $max_rate[$r] $szrnd " . $min_pkt_szs[$szs] . " " .
                   $max_pkt_szs[$szs] . " $pattern NO";
          }
          else {
            $cmd = "add_endp $ep2 $shelf $lf1 " . $all_ports1[$j+1] . " " . @cx_types[$i] .                     
                   " -1 $burst $min_rate[$r] $max_rate[$r] $szrnd " . $min_pkt_szs[$szs] . " " . $max_pkt_szs[$szs] .
                   " $pattern NO";
          }
          doCmd($cmd);

          if ($szs < (@min_pkt_szs - 1)) { $szs++; }
          else { $szs = 0; }
          if ($r < (@min_rate - 1)) { $r++; }
          else { $r = 0; }

          # Now, add the cross-connects
          my $cx_name = "L3-${num[$cx]}";
          $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
          doCmd($cmd);
          doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

          $cx++;

          @cx_names = (@cx_names, $cx_name);
        }
      }#for cx types
    }#for each port
  }##one_cx_per_port = 0
}#addCrossConnects
sub initToDefaults {
  # Clean up database if stuff exists
  if ($DEBUG) {
    print "\nsub initToDefaults\n";
  }
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
  if ($DEBUG) {
    print "\nsub addMacVlans\n";
  }
  if ($mac_init == 1 ) {
    $lsb1 = sprintf("%d", $mac1);
    $lsb2 = sprintf("%d", $mac2);
    $lsb3 = sprintf("%d", $mac3);
  }
  my $i;
  my $q;
  my $pnum1;
  my $pnum2;
  my $throttle = $script_speed;
  my $since_throttle = 0;
  for ($i = $start_mvlan; $i<($num_mvlans + $start_mvlan); $i++) {
    for ($q = 0; $q<@lf1_ports; $q++) {
      
      $pnum1 = $lf1_ports[$q];
      my $shlf = sprintf("%02x", $shelf);
      my $card = sprintf("%02x", $lf1);
      my $mac_index = getNextMac();
      my $mac_addr = "00:$shlf:$card:$mac_index";
      doCmd("add_mvlan $shelf $lf1 $pnum1 $mac_addr $i");
      
      $pnum2 = $lf2_ports[$q];
      if ($pnum2 ne "") {
        $card = sprintf("%02x", $lf2);
        $mac_index = getNextMac();
        $mac_addr = "00:$shlf:$card:$mac_index";
        doCmd("add_mvlan $shelf $lf2 $pnum2 $mac_addr $i");
      }
      if ($DEBUG > 1) { sleep($D_PAUSE); }

      # Throttle ourself so we don't over-run the poor LANforge system.
      if ($since_throttle++ > $throttle) {
        my $p1 = new LANforge::Port();
        $utils->updatePort($p1, $shelf, $lf1, $pnum1);
        if ($pnum2 ne "") {    
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
    if ($pnum2 ne "") {
      $utils->updatePort($p2, $shelf, $lf2, $lf2_ports[$q]);
      $pname2 = $p2->{dev};
    }
    
    for ($i = $start_mvlan; $i<($num_mvlans + $start_mvlan); $i++) {
      while (1) {
        $utils->updatePort($p1, $shelf, $lf1, "$pname\#$i");
        if ($pnum2 ne "") {
          $utils->updatePort($p2, $shelf, $lf2, "$pname2\#$i");
        }
        if ($p1->isPhantom() || (($pnum2 ne "") && $p2->isPhantom())) {
          sleep(1);
        }
        else {
          last;
        }
      }
    }
  }
}#addMacVlans

# Wait until the system can update a port..
sub throttleCard {
  my $s = shift;
  my $c = shift;
  my $p1 = new LANforge::Port();
  $utils->updatePort($p1, $s, $c, 1);
}#throttle

sub initPortsToDefault {
  clearMacVlanPorts($shelf, $lf1);
  if ($lf2orig ne "") {
    clearMacVlanPorts($shelf, $lf2);
  }

  throttleCard($shelf, $lf1);
  if ($lf2orig ne "") {
    throttleCard($shelf, $lf2);
  }

  # Set all ports we are messing with to known state.
  my $i = 0;
  for ($i = 0; $i<@lf1_ports; $i++) {
    my $tmp = $lf1_ports[$i];
    my $tmp2 = $lf2_ports[$i];
    if ($tmp ne "0") {
      doCmd("set_port $shelf $lf1 $tmp 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
    }
    if ($lf2orig ne "") {
      if ($tmp2 ne "0") {
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
      if ($ports[$i]->isMacVlan()) {
        doCmd($ports[$i]->getDeleteCmd());
        $found_one = 1;
      }
    }
  }
}


sub initIpAddresses {
  # Set all ports we are messing with to known state.
  my $i;
  
# TODO: This loop needs to only loop for the number of "real"/necessary ports
#       because lf1_ports is faked by num_cxs when num_mvlans is 0 and slows the
#       script down.
  for ($i = 0; $i<@lf1_ports; $i++) {
#  for ($i = 0; $i<(@lf1orig_ports + @lf2orig_ports); $i++) {

#    if ($ip_lsb[$i] > 250) {
#      $ip_c[$i]++;
#      $ip_lsb[$i] = 2;
#    }

# TODO: The whole assignment of IPs to physical ports need to be encapsulated in
#       a loop, much like the MACVLANs...

    my $ptmp = $lf1_ports[$i];
    my $ptmp2 = $lf2_ports[$i];
    my $cmd = "";
    if (!$ignore_phys_ports) {
#      $cmd = "set_port $shelf $lf1 $ptmp 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA";

#      $cmd = "set_port $shelf $lf1 $ptmp " .
#             "$ip_base[$i].$ip_c[$i].$ip_lsb[$i] $msk[$i] " .
#             "$ip_gw[$i] NA NA NA";
 
      if ($ptmp ne "") {
#        doCmd($cmd);
      }
      if ($ptmp2 ne "") {
#        $cmd = "set_port $shelf $lf2 $ptmp2 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA";

#        $cmd = "set_port $shelf $lf2 $ptmp2 " .
#               "$ip_base[$i+1].$ip_c[$i+1].$ip_lsb[$i+1] $msk[$i+1] " .
#               "$ip_gw[$i+1] NA NA NA";                        
#        doCmd($cmd);
      }
    }

# END TODO    
    
    my $p1 = new LANforge::Port();
    $utils->updatePort($p1, $shelf, $lf1, $ptmp);
    my $pname = $p1->{dev};

    my $q;
    my $throttle = $script_speed;
    my $since_throttle = 0;
 
    for ($q = $start_mvlan; $q<($num_mvlans + $start_mvlan); $q++) {
      $cmd = "set_port $shelf $lf1 $pname\#$q " .
             "$ip_base[$i].$ip_c[$i].$ip_lsb[$i] $msk[$i] " .
             "$ip_gw[$i] NA NA NA";
      doCmd($cmd);
      $ip_lsb[$i]++;
    
      if ($ip_lsb[$i] > 250) {
        $ip_c[$i]++;
        $ip_lsb[$i] = 2;
      }
    
      if ($since_throttle++ > $throttle) {
        my $p1 = new LANforge::Port();
        $utils->updatePort($p1, $shelf, $lf1, "$pname\#$q");
        $since_throttle = 0;
      }
    }
    
    if ($ptmp2 ne "") {
    $p1 = new LANforge::Port();
      $utils->updatePort($p1, $shelf, $lf2, $ptmp2);
      $pname = $p1->{dev};
      
      for ($q = $start_mvlan; $q<($num_mvlans + $start_mvlan); $q++) {
        if (@ip_base == 1) {
          $cmd = "set_port $shelf $lf2 $pname\#$q " .
                 "$ip_base[$i].$ip_c[$i].$ip_lsb[$i] $msk[$i] " .
                 "$ip_gw[$i] NA NA NA";                        
          doCmd($cmd);
          $ip_lsb[$i]++;
          
          if ($ip_lsb[$i] > 250) {
            $ip_c[$i]++;
            $ip_lsb[$i] = 2;
          }
        }
        else {
          $cmd = "set_port $shelf $lf2 $pname\#$q " .
                 "$ip_base[$i+1].$ip_c[$i+1].$ip_lsb[$i+1] $msk[$i+1] " .
                 "$ip_gw[$i+1] NA NA NA";                        
          doCmd($cmd);
          $ip_lsb[$i+1]++;
          
          if ($ip_lsb[$i+1] > 250) {
            $ip_c[$i+1]++;
            $ip_lsb[$i+1] = 2;
          }
        }
        if ($since_throttle++ > $throttle) {                   
           my $p1 = new LANforge::Port();                       
           $utils->updatePort($p1, $shelf, $lf2, "$pname\#$q"); 
           $since_throttle = 0;                                 
        } 
      } # for $q
    } # if we have an lf2_ports defined    
  }
}

sub doCmd {
  my $cmd = shift;
  
  if ($cmd) {
    print ">>> $cmd\n";
    $t->print($cmd);
    my @rslt = $t->waitfor('/ \>\>RSLT:(.*)/');
    print "**************\n @rslt ................\n\n";
  } else {
    print "\n***** doCmd (): NULL COMMAND !!! *****";
    print "\n$cmd\n\n";
    exit (1);
  }
  #sleep(1);
}

sub getDate {
  my $date = `date`;
  chomp($date);
  return $date
}

sub printArgs {
  print
    "\n$script_name"
  . "\nModified arguments:"
  . "\ninit: $INIT"
  . "\nmanager: $lfmgr_host\n"
  . "\nlf1: $lf1\nlf2: $lf2\n"
  . "\nlf1_ports: " . join(" ", @lf1_ports)
  . "\nlf2_ports: " . join(" ", @lf2_ports) . "\n"
  . "\nstart_macvlans: $start_mvlan"
  . "\nnum_mvlans: $num_mvlans"
  . "\nmvl: $mvl\n"
  . "\nmin_rates: " . join(" ", @min_rate)
  . "\nmax_rates: " . join(" ", @max_rate) 
  . "\nmin_pkt_sizes: " . join(" ", @min_pkt_szs)
  . "\nmax_pkt_sizes: " . join(" ", @max_pkt_szs) . "\n"
  . "\ncx_types: " . join(" ", @cx_types)
  . "\none_cx_per_port: $one_cx_per_port\n\n"
  . "\n"
  . "Available CX types: " . join(", ", @cxts) . "\n"
  . "Total of each CX type: " . join(", ", @t_cxts) . "\n"
  . "Total number of ports: $t_ports\n"
  . "Total number of urls: " . scalar(@l4_urls) . "\n"
  . "Total number of endpoints and CXs: $t_num\n"
  . "\n\n";
}

sub printMark {
  print
    "\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*"
   ."\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n";
}


sub printHelp {
  print
    "\n$script_name\n"
  . "USAGE: mgr=[ip-of-mgr] speed=[25|n] wait=[0|n] DEBUG=[0|1|2|...] D_PAUSE=[3|n]\n"
  . "       config_once=[0|1] init=[0|1] init_net=[1|0] init_tests=[1|0]\n"
  . "       test_mgr=\"ben_tm\" first_run=[1|0]\n"
  . "       first_name_id=[0|n] id_len=[0|n]\n"
  . "       create_only=[0|1] one_cx_per_port=[0|1] ignore_phy_ports=[1|0]\n"
  . "       lf1=[1|n] lf2=[none|n=!lf1]\n"
  . "       lf1_ports=[\"1 2 3\"|\"eth2 eth3\"] lf2_ports=[\"4 5 6\"|\"eth4 eth5\"]\n"
  . "       start_mvl=[0|n] num_mvl=[9|0]\n"
  . "       if (num_mvl=0) num_cxs_per_port=[10|n]\n"
  . "       mac3=0xf0 mac2=0xbe mac1=0xef\n"
  . "       ip_base=    \"192.168      172.16\"\n"
  . "       ip_c   =          \"2           1\"\n"
  . "       ip_lsb =          \"2           2\"\n"
  . "       ip_msk =\"255.255.0.0 255.255.0.0\"\n"
  . "       ip_gw  =\"192.168.2.1  172.16.1.1\"\n"
  . "       cx_types=\"lf lf_udp lf_tcp custom_udp custom_tcp l4 fileIONFS fileIOCIFS\"\n"
  . "       min_rates=\"9600 56000 128000\" max_rates=\"56000 128000 25600\"\n"
  . "       min_pkt_sizes=\"500 500 500\" max_pkt_sizes=\"1000 1000 1000\"\n"
  . "       url_rate=100 l4_wait=10000\n"
  . "       urls=\"http://www.candelatech.com/file ftp://www.candelatech.com/file https://www.candelatech.com/file\"\n"
  . "       fsrw=[read|write] fio_targ_dir=tmp/ fio_base=/mnt/fio_base\n"
  . "\n";

}

sub handleCmdLineArg {
  my $arg = $_[0];
  my $val = $_[1];

  if ($arg eq "help" || $arg eq "--help" || $arg eq "-h" || $arg eq "-help" || $arg eq "-h" ) {
    printHelp();
    exit(0);
  }
  elsif ($arg eq "debug" || $arg eq "DEBUG") {
    $DEBUG = $val;
  }
  elsif ($arg eq "d_pause" || $arg eq "D_PAUSE") {
    $D_PAUSE = $val;
  }  
  elsif ($arg eq "mgr") {
    $lfmgr_host = $val;
  }
  elsif ($arg eq "test_mgr") {
    $test_mgr = $val;
  }
  elsif ($arg eq "init") {
    $INIT = $val;
  }
  elsif ($arg eq "config_once") {
    $init_once = $val;
  }
  elsif ($arg eq "init_net") {
    $init_net = $val;
  }
  elsif ($arg eq "init_tests") {
    $init_tests = $val;
  }
  elsif ($arg eq "first_run") {
    $first_run = $val;
  }
  elsif ($arg eq "first_name_id") {
    $name_id = $val;
  }
  elsif ($arg eq "id_len") {
    $name_id_len = $val;
    if (length($name_id) > $name_id_len) {
      print "\nWARNING: id_len specifies a string length less that first_name_id.\n";
    }
  }
  elsif ($arg eq "speed") {
    $script_speed = $val;
  }
  elsif ($arg eq "wait") {
    $pause = $val;
  }
  elsif ($arg eq "lf1") {
    $lf1 = $val;
  }
  elsif ($arg eq "lf2") {
    $lf2 = $val;
    if ($lf1 == $lf2) {
      die("\nINVALID: First and second resource are the same !!!\n\n");
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
    @ip_base = undef;    
    @ip_base = split(/ /, $val);
  }
  elsif ($arg eq "ip_c") {
    @ip_c = undef;
    @ip_c = split(/ /, $val);
  }
  elsif ($arg eq "ip_lsb") {
    @ip_lsb = undef;
    @ip_lsb = split(/ /, $val);
  }
  elsif ($arg eq "ip_msk") {
    @msk = undef;
    @msk = split(/ /, $val);
  }
  elsif ($arg eq "ip_gw") {
    @ip_gw = undef;
    @ip_gw = split(/ /, $val);
  }
  elsif ($arg eq "lf1_ports") {
    @lf1_ports = split(/ /, $val);
  }
  elsif ($arg eq "lf2_ports") {
    if ($lf2 == "" || $lf1 == $lf2) {
      die("\nINVALID: Either second resource is not defined\nor first and second resource are the same !!!\n\n");
    }
    else {
      @lf2_ports = split(/ /, $val);
    }
  }
  elsif ($arg eq "cx_types") {
    @cx_types = split(/ /, $val);
  }
  elsif ($arg eq "min_pkt_sizes") {
    @min_pkt_szs = split(/ /, $val);
  }
  elsif ($arg eq "max_pkt_sizes") {
    @max_pkt_szs = split(/ /, $val);
  }
  elsif ($arg eq "start_mvl") {
    $start_mvlan = $val;
  }
  elsif ($arg eq "num_mvl") {
    $num_mvlans = $val;
  }
  elsif ($arg eq "num_cxs_per_port") {
    $num_cxs = $val;
  }
  elsif ($arg eq "min_rates") {
    @min_rate = split(/ /, $val);
  }
  elsif ($arg eq "max_rates") {
    @max_rate = split(/ /, $val);
  }  
  elsif ($arg eq "fsrw") {
    $fsrw = $val;
  }
  elsif ($arg eq "fio_base") {
    $fio_base = $val;
  }
  elsif ($arg eq "fio_targ_dir") {
    $fio_targ_dir = $val;
  }
  elsif ($arg eq "urls") {
    @l4_urls = split(/ /, $val);
  }
  elsif ($arg eq "url_rate") {
    $urls_10m = $val;
  }
  elsif ($arg eq "l4_wait") {
    $l4_timeout = $val;
  }
  elsif ($arg eq "one_cx_per_port") {
    $one_cx_per_port = $val;
  }
  elsif ($arg eq "ignore_phy_ports") {
    $ignore_phys_ports = $val;
  }  
  elsif ($arg eq "create_only") {
    $create_only = $val;
  }
  else {
    print "\n\nCould not parse one or more of the arguments !!!\n"
            . "First rejected argument: $arg\n";
    printHelp();
    exit(1);
  }
}
