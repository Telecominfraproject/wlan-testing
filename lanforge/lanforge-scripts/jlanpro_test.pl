#!/usr/bin/perl -w
#
# Data should be 500 bytes
# Test rig is one upstream wired system, which will be the manager as well as resource
# One ct523b as resource2, and a stand-by ct523b as resource3
# WPA2 PSK encryption

# 3x3 client testing:
# 20 clients uploading for 30 sec
# 20 clients downloading 30 sec
# 40 clients upload + download 1 minute
# Quiesce and wait 30 seconds

# 2x2:  Same
# 1x2:  Same

# Mixed mode:  10 3x3, 15 2x2, 15 1x1  (Same data pattern)

# WiFi Capacit test notes:
#  Mix of TCP and UDP, using MTU sized frames
#  All 64 stations are on one 4x4 radio

# Mixed With interference: Same as mixed mode
# Assume other test EQ is doing interference?

# Each ct523b has 4 radios.  We will spread stations among them.
# This script can work on systems with fewer radios as well, see comments
# below about naming the 3a,3b,4a,4b radios with duplicate names.

use strict;
use warnings;
use diagnostics;
use Getopt::Long;
use Socket;
use POSIX;
our $pld_size = 500;
our $ssid = "wlanpro";
our $psk = "wlanpro_passwd";
# Default radio setup for 523b with 2ac, 2ac2.
# For something like a 522 with 2 radios, set 3a, 3b to wiphy0, and
# 4a 4b to wiphy1.
our $radio_3a = "wiphy0";
our $radio_3b = "wiphy1";
our $radio_4a = "wiphy2";
our $radio_4b = "wiphy3";
our $sta_max = 40; # For upload/download tests
our $wct_sta_max = 64; # For wifi-capacity-test on single radio (4a)
our $gui_host = "127.0.0.1"; # auto-wifi-cap script will not work properly if not run on same machine as GUI
our $gui_port = 7777;
our $resource = 2;
our $speed_dl_tot = 1000000000;
our $speed_ul_tot = 1000000000;
our $speed_ul_bi_tot = 200000000; # 200Mbps upload speed when in bi-directional mode
our $testcase = -1;
our $manager = "localhost";
our $log_name = "";

our $endp_type = "lf_udp";
our $security = "wpa2";
our $upstream_resource = 1;
our $upstream_port = "eth1";
our $multicon = "1";
our $rest_time = 20;
our $quiet = "yes";
our $report_timer = 1000; # 1 second report timer
our $rpt_timer_wct = 3000; # 3-second rpt timer for wifi-capacity test
our $settle_timer_wct = 10000; # 10-sec wait for connections to get running before clearing and starting the test proper
our $wct_duration_sec = 20; # Duration for each iteration
our $one_way_test_time = 30;
our $bi_test_time = 30;
our $interferer_cx = "inteferer_cx";
our $ip = "DHCP";
our $netmask = "255.255.0.0";
our $ipn = 0;

my $usage = "$0
  [--pld_size { bytes } ]
  [--ssid {ssid}]
  [--passphrase {password}]
  [--3a {wiphy-radio-3x3-a}]
  [--3b {wiphy-radio-3x3-b}]
  [--4a {wiphy-radio-4x4-a}]
  [--4b {wiphy-radio-4x4-b}]
  [--resource {resource-number}]
  [--upstream_resource {resource-number}]
  [--upstream_port {port}]
  [--speed_ul_tot {speed-bps (default: $speed_ul_tot)}]
  [--speed_dl_tot {speed-bps (default: $speed_dl_tot)}]
  [--speed_ul_bi_tot {speed-bps for upload in bi-directional test (default: $speed_ul_bi_tot)}]
  [--security {open | wpa2}]
  [--manager {manager-machine IP or hostname}]
  [--testcase {test-case:  -1: all except cleanup, 0: setup, 1: 3x3 ul/dl,
     2: 2x2 ul/dl 3: 1x1 ul/dl, 4: mix ul/dl, 5: mix ul/dl + interference,
     6: wifi-capacity-test, 100: cleanup}]
  [--log_name {log-file-name}]
  [--rest_time {seconds to sleep between rest runs, dfault is $rest_time}]
  [--gui_host  {LANforge gui_host (127.0.0.1): Must be same as where this script runs.}]
  [--gui_port  {LANforge gui_port (7777):  Start your GUI with -cli-port 7777}]
  [--interferer_cx { name of existing LANforge interferer-cx that we should start for the interference test }]
  [--ip { DHCP | starting IP address.  Default is to use DHCP. }]
  [--netmask { Ignored if using DHCP, otherwise something like 255.255.255.0.  Default is $netmask. }]
  [--sta_max {max num stations}]
  [--wct_sta_max {max num stations for capacity test}]
  [--multicon {0: off|1: default|-1: auto}]

NOTE:  The total speed will be multiplied by 1.0 for 3x3 and mixed tests, 0.75 for 2x2 testing,
   and 0.5 for 1x1 testing.  This should still attempt near theoretical throughput without
   over-driving the DUT too badly.

For the interference test, it is expected that the user create a CX of the proper name in
LANforge, associated to a wifi station, etc, and this script will simply start and stop it.
That will simplify this script and will give more flexibility on how the interferer is
configured.  By default, the intereferer CX name will be 'interferer_cx'.

Example command:

# Run test case 5, assumes test case 0 (setup) has already been run.
./wlanpro_test.pl --ssid mu-mimo-5G --passphrase hello123 --resource 2 --upstream_resource 1 \
  --upstream_port eth4 --manager 192.168.100.182 --gui_port 7777 --interferer_cx inter_r3_w0 --testcase 5

# Run all test cases with Fixed IP addresses (instead of DHCP)
./wlanpro_test.pl --ssid mu-mimo-5G --passphrase hello123 --resource 2 --upstream_resource 1 --upstream_port eth4 --manager 192.168.100.182 --gui_host 192.168.100.149 --gui_port 7777 --interferer_cx inter_r3_w0 --testcase -1 --ip 5.5.5.1 --netmask 255.255.255.0


Interesting bugs:

While testing with a netgear r7800, I noticed that the RX encoding rate received from the AP
can be NSS 2 even when the station is configured for NSS 1.  I double-checked that the association
request is using NSS 1 info, so this appears to be a bug in the Netgear.  But, since the LANforge
radio can actually decode NSS 2 frames, then the packets are actually received and the Netgear gets
better performance than is warranted in this configuration.  This appears to be a bug in the Netgear.

";

my $usage_notes = "
Errors reported by the LANforge-GUI that you should be able to ignore:

* ERROR:  Cannot change MAC address with the 'add-vwifi' command.
     Reason: Existing MAC would be fine anyway.

";

my $script_start = time();

GetOptions (
	    'pld_size=i'     => \$pld_size,
	    'ssid=s'         => \$ssid,
	    'passphrase=s'   => \$psk,
	    '3a=s'           => \$radio_3a,
	    '3b=s'           => \$radio_3b,
	    '4a=s'           => \$radio_4a,
	    '4b=s'           => \$radio_4b,
	    'resource=i'     => \$resource,
	    'upstream_resource=i' => \$upstream_resource,
	    'upstream_port=s' => \$upstream_port,
	    'rest_time=i'    => \$rest_time,
	    'speed_ul_tot=s' => \$speed_ul_tot,
	    'speed_ul_bi_tot=s' => \$speed_ul_bi_tot,
	    'speed_dl_tot=s' => \$speed_dl_tot,
	    'security=s'     => \$security,
	    'manager=s'      => \$manager,
	    'mgr=s'          => \$manager,
	    'testcase=i'     => \$testcase,
	    'log_name=s'     => \$log_name,
	    'gui_host=s'     => \$gui_host,
	    'gui_port=i'     => \$gui_port,
	    'interferer_cx=s' => \$interferer_cx,
	    'ip=s'           => \$ip,
	    'netmask=s'      => \$netmask,
            'sta_max=i'       => \$sta_max,
            'wct_sta_max=i'   => \$wct_sta_max,
            'multicon=s'      => \$multicon,
	   ) || (print($usage) && exit(1));

if ($log_name eq "") {
  $log_name = "wlanpro_log_" . $ssid . "_" . time() . ".txt";
}
my @radios = ($radio_3a, $radio_3b, $radio_4a, $radio_4b);
my $radio_count = @radios;
my $i;
my $cmd;
my $log_prefix = "LANforge wlanpro-test\nConfiguration:\n" .
  "  SSID: $ssid  passphrase: $psk  security: $security  resource: $resource\n" .
  "  speed_dl_request: $speed_dl_tot  speed_ul_request: $speed_ul_tot  payload-size: $pld_size  traffic-type: $endp_type\n" .
  "  speed_ul_bi_request: $speed_ul_bi_tot  interferer: $interferer_cx\n" .
  "  Test started at: " . `date` . "\n\n";
my $brief_log = "$log_prefix";
my $summary_text = "$log_prefix";
my $mini_summary_text = "$log_prefix";

if ($ip ne "DHCP") {
  $ipn = ip2ipn($ip);
}

# Initial setup for test cases, create $sta_max stations
my @cxs = ();
my @stations = ();
my @stations4a = ();
my $sta_on_4a = 0;

$SIG{'INT'} = sub {
  print "Caught ctrl-C, exiting!\n";
  exit 1;
};

open(LOGF, ">$log_name") or die("Could not open log file: $log_name $!\n");

logp($log_prefix);

# Stop any running tests.
stop_all_cx();

# Delete any wifi-capacity generated connections at this time, it will clean things
# up, and it will make parsing reporting data faster.
sub remove_cxs {
   my @cx_dump = `./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"show_cx\"`;
   for (my $i = 0; $i<@cx_dump; $i++) {
     my $line = $cx_dump[$i];
     chomp($line);
     #print "looking for $upstream_resource, $upstream_port **** $line ****\n";
     # also match udp--1.eth4-02.sta102-B
     if ($line =~ /CX:\s+((tcp|udp)\-\-$upstream_resource\.[^-]+-\S+)\b/) {
       my $cxn = $1;
       $cmd = "./lf_firemod.pl --mgr $manager --action delete_cxe --cx_name $cxn";
       do_cmd($cmd);
     }
   }
}

remove_cxs();
# Stop the interferer, just in case it is already running for some reason
$cmd = "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"set_cx_state default_tm $interferer_cx STOPPED\"";
do_cmd($cmd);

# Set upstream port to DHCP or fixed IP as requested.
$cmd = "./lf_portmod.pl --quiet $quiet --manager $manager --card $upstream_resource --port_name $upstream_port --ip $ip --netmask $netmask";
do_cmd($cmd);

# Set radios to 3x3 mode.
if ($testcase == -1 || $testcase == 0) {
  for ($i = 0; $i<$radio_count; $i++) {
    my $radio = $radios[$i];
    my $set_cmd = "set_wifi_radio 1 $resource $radio NA NA NA NA NA NA NA NA NA 7";
    $cmd = "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"$set_cmd\"";
    do_cmd($cmd);
  }
}

# Find wlanX for 4a radio.
if ($radio_4a =~ /\S+(\d+)/) {
  my $sta_name = "wlan$1";
  @stations4a = (@stations4a, $sta_name);
  my $radio = $radio_4a;
  $sta_on_4a++;
  if ($testcase == -1 || $testcase == 0 || $testcase == 6) {
    my $_ip = incr_ip();
    $cmd = "./lf_vue_mod.sh --mgr $manager --create_sta --resource $resource --name $sta_name  --radio $radio --security $security --ssid $ssid --passphrase $psk --ip $_ip --netmask $netmask";
    do_cmd($cmd);

    # Set to maximum mode.  The stations might have been
    # previously set to a different mode on an earlier run of this script.
    $cmd = "./lf_portmod.pl  --quiet $quiet --manager $manager --card $resource --port_name $sta_name --wifi_mode 8 --set_speed DEFAULT --set_ifstate up";
    do_cmd($cmd);
  }
}

for ($i = 0; $i < $sta_max; $i++) {
  my $sta_idx = $i + 100;
  my $radio_idx = $i % $radio_count;
  my $radio = $radios[$radio_idx];
  my $sta_name = "sta$sta_idx";

  if ($radio eq $radio_4a) {
    $sta_on_4a++;
    @stations4a = (@stations4a, $sta_name);
  }

  @stations = (@stations, $sta_name);

  if ($testcase == -1 || $testcase == 0) {
    my $_ip = incr_ip();
    $cmd = "./lf_vue_mod.sh --mgr $manager --create_sta --resource $resource --name $sta_name  --radio $radio --security $security --ssid $ssid --passphrase $psk --ip $_ip --netmask $netmask";
    do_cmd($cmd);

    # Set to maximum mode.  The stations might have been
    # previously set to a different mode on an earlier run of this script.
    $cmd = "./lf_portmod.pl  --quiet $quiet --manager $manager --card $resource --port_name $sta_name --wifi_mode 8 --set_speed DEFAULT --set_ifstate up";
    do_cmd($cmd);
  }
  # Create data connection
  my $cxn = "l3-${sta_name}";
  my $endpa = "$cxn-A";
  my $endpb = "$cxn-B";
  my $pkt_sz ="--min_pkt_sz $pld_size --max_pkt_sz $pld_size";
  my $gen_args = "--mgr $manager --multicon $multicon $pkt_sz --endp_type $endp_type --action create_endp --report_timer $report_timer";

  if ($testcase == -1 || $testcase == 0) {
    $cmd = "./lf_firemod.pl --resource $resource $gen_args --endp_name $endpa --speed 0 --port_name $sta_name";
    do_cmd($cmd);

    $cmd = "./lf_firemod.pl --resource $upstream_resource $gen_args --endp_name $endpb --speed 0 --port_name $upstream_port";
    do_cmd($cmd);

    $cmd = "./lf_firemod.pl --mgr $manager --action create_cx --cx_name $cxn --cx_endps $endpa,$endpb --report_timer $report_timer";
    do_cmd($cmd);
  }

  @cxs = (@cxs, $cxn);
}

# Create rest of the 4a-stations for Wifi Capacity Test
while ($sta_on_4a < $wct_sta_max) {
  my $sta_idx = $sta_on_4a + 200;
  my $radio = $radio_4a;
  my $sta_name = "sta$sta_idx";

  @stations4a = (@stations4a, $sta_name);
  $sta_on_4a++;

  if ($testcase == -1 || $testcase == 0 || $testcase == 6) {
    my $_ip = incr_ip();
    $cmd = "./lf_vue_mod.sh --mgr $manager --create_sta --resource $resource --name $sta_name  --radio $radio --security $security --ssid $ssid --passphrase $psk --ip $_ip --netmask $netmask";
    do_cmd($cmd);

    # Set to maximum mode.  The stations might have been
    # previously set to a different mode on an earlier run of this script.
    # Set them to admin-down, the wifi-capacity-test will bring them up as needed.
    $cmd = "./lf_portmod.pl  --quiet $quiet --manager $manager --card $resource --port_name $sta_name --wifi_mode 8 --set_speed DEFAULT --set_ifstate down";
    do_cmd($cmd);
  }
}

stop_all_cx();


if ($testcase == -1 || $testcase == 1) {
  wait_for_stations();
  do_test_series("3x3 station upload/download test", 1.0);
}

if ($testcase == -1 || $testcase == 2) {
  # Test case 2, set stations to 2x2 and re-test
  my $start = time();
  for ($i = 0; $i<$radio_count; $i++) {
    my $radio = $radios[$i];
    my $set_cmd = "set_wifi_radio 1 $resource $radio NA NA NA NA NA NA NA NA NA 4";
    $cmd = "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"$set_cmd\"";
    do_cmd($cmd);
  }

  wait_for_stations();
  check_more_rest($testcase, $start);
  do_test_series("2x2 station upload/download test", 0.75);
}

if ($testcase == -1 || $testcase == 3) {
  # Test case 3, set stations to 1x1 and re-test
  my $start = time();
  for ($i = 0; $i<$radio_count; $i++) {
    my $radio = $radios[$i];
    my $set_cmd = "set_wifi_radio 1 $resource $radio NA NA NA NA NA NA NA NA NA 1";
    $cmd = "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"$set_cmd\"";
    do_cmd($cmd);
  }

  wait_for_stations();
  check_more_rest($testcase, $start);
  do_test_series("1x1 station upload/download test", 0.50);
}


# Mixed mode test:  10 3x3, 15 2x2, 15 1x1  (Same data pattern)
if ($testcase == -1 || $testcase == 4 || $testcase == 5) {
  # Set radio back to full antenna capacity
  my $start = time();
  for ($i = 0; $i<$radio_count; $i++) {
    my $radio = $radios[$i];
    my $set_cmd = "set_wifi_radio 1 $resource $radio NA NA NA NA NA NA NA NA NA 0";
    $cmd = "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"$set_cmd\"";
    do_cmd($cmd);
  }

   # 1/4 stations
  for ($i = 0; $i<floor($sta_max/4); $i++) {
    my $sta_name = $stations[$i];
    $cmd = "./lf_portmod.pl  --quiet $quiet --manager $manager --card $resource --port_name $sta_name --wifi_mode 8 --set_speed \"v-3 Streams /AC\"";
    do_cmd($cmd);
  }
  for ($i = floor($sta_max/4); $i<floor($sta_max*0.375); $i++) {
    my $sta_name = $stations[$i];
    $cmd = "./lf_portmod.pl --quiet $quiet --manager $manager --card $resource --port_name $sta_name --wifi_mode 8 --set_speed \"v-2 Streams /AC\"";
    do_cmd($cmd);
  }
  for ($i = floor($sta_max*0.375);$ i<$sta_max; $i++) {
    my $sta_name = $stations[$i];
    $cmd = "./lf_portmod.pl --quiet $quiet --manager $manager --card $resource --port_name $sta_name --wifi_mode 8 --set_speed \"v-1 Stream  /AC\"";
    do_cmd($cmd);
  }

  wait_for_stations();
  check_more_rest($testcase, $start);

  if ($testcase == -1 || $testcase == 4) {
    do_test_series("Mixed mode: 10 3x3, 15 2x2, 10 1x1 station upload/download test", 1.0);
    if ($testcase == -1) {
      sleep($rest_time);
    }
  }
}

# Interference mixed-mode test case
if ($testcase == -1 || $testcase == 5) {
  wait_for_stations();
  $cmd = "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"set_cx_state default_tm $interferer_cx RUNNING\"";
  do_cmd($cmd);
  do_test_series("Mixed mode: 10 3x3, 15 2x2, 10 1x1 station upload/download test with interference", 1.0);
  $cmd = "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"set_cx_state default_tm $interferer_cx STOPPED\"";
  do_cmd($cmd);
}

# WiFi capacity test
if ($testcase == -1 || $testcase == 6) {

  # Set radio back to full antenna capacity
  for ($i = 0; $i<$radio_count; $i++) {
    my $radio = $radios[$i];
    my $set_cmd = "set_wifi_radio 1 $resource $radio NA NA NA NA NA NA NA NA NA 0";
    $cmd = "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"$set_cmd\"";
    do_cmd($cmd);
  }

  for ($i = 0; $i < @stations; $i++) {
    my $sta_name = $stations[$i];
    $cmd = "./lf_portmod.pl  --quiet $quiet --manager $manager --card $resource --port_name $sta_name --wifi_mode 8 --set_speed DEFAULT --set_ifstate down";
    do_cmd($cmd);
  }

  #wait_for_stations();  WCT takes care of bringing stations up/down
  my $sta_list = join(",", @stations4a);
  # Call to automated wifi capacity test plugin
  do_cmd("./lf_auto_wifi_cap.pl --mgr $manager --resource $resource --radio $radio_4a --speed_dl $speed_dl_tot --ssid $ssid --num_sta $wct_sta_max --upstream $upstream_port --upstream_resource $upstream_resource --percent_tcp 50 --increment 1,5,10,20,30,45,64 --duration $wct_duration_sec --endp_type mix --test_name wlanpro-$ssid --test_text 'Wlan-Pro test case #6 to ssid $ssid' --multicon $multicon --use_existing_sta --use_existing_cfg --use_station $sta_list --gui_host $gui_host --gui_port $gui_port --report_timer $rpt_timer_wct --settle_timer $settle_timer_wct");
}

if ($testcase == 100) {
  # Cleanup
  for ($i = 0; $i<@stations; $i++) {
    my $sta_name = $stations[$i];
    $cmd = "./lf_portmod.pl  --quiet $quiet --mgr $manager --resource $resource --cmd delete --port_name $sta_name";
    do_cmd("$cmd\n");
  }
  
  for ($i = 0; $i<@stations4a; $i++) {
    my $sta_name = $stations4a[$i];
    $cmd = "./lf_portmod.pl  --quiet $quiet --mgr $manager --resource $resource --cmd delete --port_name $sta_name";
    do_cmd("$cmd\n");
  }


  for ($i = 0; $i<@cxs; $i++) {
    my $cxn = $cxs[$i];
    $cmd = "./lf_firemod.pl --mgr $manager --action delete_cxe --cx_name $cxn";
    do_cmd($cmd);
  }

  remove_cxs();

  # Set radio back to full antenna capacity
  for ($i = 0; $i<$radio_count; $i++) {
    my $radio = $radios[$i];
    my $set_cmd = "set_wifi_radio 1 $resource $radio NA NA NA NA NA NA NA NA NA 0";
    $cmd = "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"$set_cmd\"";
    do_cmd($cmd);
  }

}

my $now_sec = time();
my $took = ($now_sec - $script_start) / 60;
logpb("Entire run took: $took minutes.\n");
logpb("Completed test at " . `date` . "\n\n");

# Append brief log and final log to the report.

logf($brief_log);
logp($summary_text);
logp("\n\n$mini_summary_text");

exit 0;

sub check_more_rest {
  my $testcase = shift;
  my $start = shift;

  if ($testcase == -1) {
    # Running tests in series, so we need to add in our rest time
    my $now = time();
    if ($start + $rest_time > $now) {
      my $st = ($start + $rest_time) - $now;
      print "Sleeping $st seconds for rest time...";
      sleep($st);
    }
  }
}

# Wait until all stations are associated and have IP addresses.
sub wait_for_stations {
  # Wait until stations are associated, return count
  my $j;
  for ($j = 0; $j<60; $j++) {
    my $all_up = 1;
    for ($i = 0; $i<@stations; $i++) {
      my $sta_name = $stations[$i];
      $cmd = "./lf_portmod.pl  --quiet $quiet --mgr $manager --resource $resource --show_port AP,IP --port_name $sta_name";
      logp("$cmd\n");
      my @output = `$cmd`;
      if ($output[0] =~ "AP: Not-Associated") {
	logp("Station $sta_name is not associated, waiting...\n");
	sleep(1);
	$all_up = 0;
	last;
      }
      if ($output[1] =~ "IP: 0.0.0.0") {
	logp("Station $sta_name does not have an IP address, waiting...\n");
	sleep(1);
	$all_up = 0;
	last;
      }
    }

    if ($all_up) {
      last;
    }
  }
}

sub do_one_test {
  my $speed_ul = shift;
  my $speed_dl = shift;
  my $cx_cnt = shift;
  my $sleep_sec = shift;
  my $series_desc = shift;

  # Download for X seconds
  for ($i = 0; $i<$cx_cnt; $i++) {
    my $cxn = $cxs[$i];
    my $endpa = "$cxn-A";
    my $endpb = "$cxn-B";

    $cmd = "./lf_firemod.pl --mgr $manager --action set_endp --endp_name $endpa --speed $speed_ul";
    do_cmd($cmd);

    $cmd = "./lf_firemod.pl --mgr $manager --action set_endp --endp_name $endpb --speed $speed_dl";
    do_cmd($cmd);

    $cmd = "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"set_cx_state default_tm $cxn RUNNING\"";
    do_cmd($cmd);
  }

  $cmd =  "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"clear_port_counters\"";
  do_cmd($cmd);

  my $msg = "Waiting $sleep_sec seconds for test to run, $cx_cnt connections, requested per-connection speed, UL: $speed_ul  DL: $speed_dl.\n" .
    " Test-case: $series_desc\n\n";
  logp($msg);
  $mini_summary_text .= "$cx_cnt connections, requested per-connection speed, UL: $speed_ul  DL: $speed_dl\n";

  sleep($sleep_sec);

  logp("Gathering stats for this test run...\n");

  # Gather layer-3 stats data
  my $sp;

  my $tmpfe = "wptest_endp_stats_tmp.txt";
  `./lf_portmod.pl --manager $manager --cli_cmd "nc_show_endp" > $tmpfe`;

  my $tmpf = "wptest_stats_tmp.txt";
  `./lf_portmod.pl --manager $manager --cli_cmd "nc_show_port 1 $resource" > $tmpf`;
  if ($resource != $upstream_resource) {
    `./lf_portmod.pl --manager $manager --cli_cmd "nc_show_port 1 $upstream_resource" >> $tmpf`;
  }

  # Stop the connections while we process stats.
  stop_all_cx();

  logp("Processing stats for this test run...\n");

  # Process stats
  $sp = `cat $tmpfe`;
  logf("$sp\n");

  # Open-code the report gathering for efficiency.

  # For each endpoint, see if it is one we care about, and gather reporting.  Put it
  # in a hash so we can search for it efficiently and generate ordered output.
  my %endp_rx_rate = ();
  my %endp_tx_rate = ();
  my @lines = split("\n", $sp);
  # Append dummy line to make it easier to terminate the parse logic.
  @lines = (@lines, "Endpoint [________] (NOT_RUNNING)\n");
  my $endp_text = "";
  my $ep = "";

  for ($i = 0; $i<@lines;$i++) {
    my $line = $lines[$i];
    chomp($line);
    if (($line =~ /Endpoint\s+\[(.*)\]/) ||
	($line =~ /WanLink\s+\[(.*)\]/) ||
	($line =~ /ArmEndp\s+\[(.*)\]/) ||
	# TODO: Layer-4 ?
	($line =~ /VoipEndp\s+\[(.*)\]/)) {
      my $m1 = $1;

      #print "Found starting line: $line  name: $m1  endp_name: $endp_name\n";

      if ($endp_text ne "") {
	# endp_text holds output for endpoint $ep.  Gather stats and store them in our hashes
	if ($endp_text =~ /.*RealTxRate:\s+(\S+)bps.*RealRxRate:\s+(\S+)bps/s) {
	  $endp_tx_rate{$ep} = $1;
	  $endp_rx_rate{$ep} = $2;
	  #print "Found $ep tx-rate: $1  rx-rate: $2\n";
	}
      }

      $endp_text = "$line\n";
      $ep = $m1;
    }
    else {
      if ($endp_text ne "") {
	$endp_text .= "$line\n";
      }
    }
  }

  my $tot_dl_bps = 0;
  my $tot_ul_bps = 0;
  # Our endp names are derived from cx, so use that to our advantage.
  for ($i = 0; $i<$cx_cnt; $i++) {
    my $cxn = $cxs[$i];
    my $epa = "$cxn-A";
    my $epb = "$cxn-B";

    $summary_text .= "$cxn:";
    my $tx = $endp_tx_rate{$epa};
    my $rx = $endp_rx_rate{$epa};

    $tot_dl_bps += $rx;
    $summary_text .= sprintf(" Download RX: %.3fMbps", $rx / 1000000);
    $summary_text .= sprintf(" Upload TX: %.3fMbps", $tx / 1000000);

    $tx = $endp_tx_rate{$epb};
    $rx = $endp_rx_rate{$epb};

    $tot_ul_bps += $rx;
    $summary_text .= sprintf(" Upload RX: %.3fMbps", $rx / 1000000);
    $summary_text .= sprintf(" Download TX: %.3fMbps", $tx / 1000000);
    $summary_text .= "\n";
  }
  $summary_text .= sprintf("Total Endpoint Upload RX: %.3fMbps  Download RX: %.3fMbps\n\n", $tot_ul_bps / 1000000, $tot_dl_bps / 1000000);
  $mini_summary_text .= sprintf("Total Endpoint Upload RX: %.3fMbps  Download RX: %.3fMbps\n\n", $tot_ul_bps / 1000000, $tot_dl_bps / 1000000);

  # Port
  $sp = `cat $tmpf`;
  logf("$sp\n");
  @lines = split("\n", $sp);
  # Append dummy line to make it easier to terminate the parse logic.
  @lines = (@lines, "Shelf: 9999, Card: 9999, Port: 9999  Type: STA  Alias: \n");

  my %port_mac = ();
  my %port_tx_rate_link = ();
  my %port_tx_rate = ();
  my %port_rx_rate = ();
  my %port_ssid = ();
  my %port_mode = ();
  my %port_nss = ();
  my %port_bandwidth = ();
  my %port_channel = ();
  my %port_ap = ();
  my %port_rx_rate_link = ();
  my %port_signal = ();
  my %port_activity = ();

  my $port_text = "";
  my $s = -1;
  my $c = -1;
  my $p = -1;

  for ($i = 0; $i<@lines;$i++) {
    my $line = $lines[$i];
    chomp($line);
    #print "line: $line\n";
    if ($line =~ /Shelf:\s+(\d+).*Card:\s+(\d+).*Port:\s+(\d+)/) {
      my $m1 = $1;
      my $m2 = $2;
      my $m3 = $3;

      if ($port_text ne "") {
	# port_text holds output for port $s.$c.$p.  Gather stats and store them in our hashes
	if ($port_text =~ /DEV:\s+(\S+)/) {
	  $p = $1;
	}
	my $pkey = "$s.$c.$p";
	#print "pkey: $pkey\n";
	# We want:  bps_rx,bps_tx,MAC,TX-Rate,Signal,Link-Activity,Channel,Bandwidth,NSS
	if ($port_text =~ /.*MAC:\s+(\S+).*Tx-Rate:\s+(\S+).*bps_tx:\s+(\S+)\s+bps_rx:\s+(\S+).*/s) {
	  $port_mac{$pkey} = $1;
	  $port_tx_rate_link{$pkey} = $2;
	  $port_tx_rate{$pkey} = $3;
	  $port_rx_rate{$pkey} = $4;
	}
	else {
	  print "Did not find MAC etc in text: $port_text\n";
	  exit 1;
	}

	if ($port_text =~ /.*ESSID: (.*)  Antenna.*/) {
	  $port_ssid{$pkey} = $1;
	}

	# WiFi stuff should come from the Probed section
	if ($port_text =~ /.*Probed:\s+(.*)/s) {
	  my $haystack = $1;

	  # We want:  Mode,NSS,Bandwidth,Channel,AP,RX-Rate,Signal,Link-Activity
	  if ($haystack =~ /.*Mode:\s+(\S+).* NSS:\s+(\S+).*Bandwidth: (\S+).*Channel:\s+(\S+).* AP:\s+(\S+).*RX-Rate: (\S+).*Signal: (\S+).*Link-Activity: (\S+).*/s) {
	    $port_mode{$pkey} = $1;
	    $port_nss{$pkey} = $2;
	    $port_bandwidth{$pkey} = $3;
	    $port_channel{$pkey} = $4;
	    $port_ap{$pkey} = $5;
	    $port_rx_rate_link{$pkey} = $6;
	    $port_signal{$pkey} = $7;
	    $port_activity{$pkey} = $8;
	  }
	  # Deal with no AP or Signal field reported.
	  elsif ($haystack =~ /.*Mode:\s+(\S+).* NSS:\s+(\S+).*Bandwidth: (\S+).*Channel:\s+(\S+).*RX-Rate: (\S+).*Link-Activity: (\S+).*/s) {
	    $port_mode{$pkey} = $1;
	    $port_nss{$pkey} = $2;
	    $port_bandwidth{$pkey} = $3;
	    $port_channel{$pkey} = $4;
	    $port_rx_rate_link{$pkey} = $5;
	    $port_signal{$pkey} = $6;
	    $port_activity{$pkey} = $7;
	    $port_ap{$pkey} = "NA";
	    $port_signal{$pkey} = "-1";
	  }
	  else {
	    print "Did not find probed wifi data, raw-text:\n$haystack\nFull port output:\n$port_text";
	    exit 1;
	  }
	}
      }

      $port_text = "$line\n";
      $s = $m1;
      $c = $m2;
      $p = $m3;
    }
    else {
      if ($port_text ne "") {
	$port_text .= "$line\n";
      }
    }
  }# for

  $tot_dl_bps = 0;
  $tot_ul_bps = 0;

  for ($i = 0; $i<@stations; $i++) {
    my $sta_name = $stations[$i];
    my $pkey = "1.$resource.$sta_name";
    my $mac = $port_mac{$pkey};
    my $tx_rate_link = $port_tx_rate_link{$pkey};
    my $tx_rate = $port_tx_rate{$pkey};
    my $rx_rate = $port_rx_rate{$pkey};
    my $ssid = $port_ssid{$pkey};
    my $mode = $port_mode{$pkey};
    my $nss = $port_nss{$pkey};
    my $bandwidth = $port_bandwidth{$pkey};
    my $channel = $port_channel{$pkey};
    my $ap = $port_ap{$pkey};
    my $rx_rate_link = $port_rx_rate_link{$pkey};
    my $signal = $port_signal{$pkey};
    my $activity = $port_activity{$pkey};

    $brief_log .= "Station Stats:\nMAC: $mac SSID: $ssid  Mode: $mode  NSS: $nss  Bandwidth: $bandwidth\n";
    $brief_log .= "\tChannel: $channel AP: $ap  Signal: $signal  Activity: $activity  TX-Link-Rate: $tx_rate_link  RX-Link-Rate: $rx_rate_link\n";
    $brief_log .= "\tTX-Rate: ${tx_rate}bps  RX-Rate: ${rx_rate}bps";

    $summary_text .= "$sta_name:";
    $tot_dl_bps += $rx_rate;
    $summary_text .= sprintf(" RX: %.3fMbps", $rx_rate / 1000000);

    $tot_ul_bps += $tx_rate;
    $summary_text .= sprintf(" TX: %.3fMbps", $tx_rate / 1000000);

    $summary_text .= " NSS: $nss RX-Rate: $rx_rate_link TX-Rate: $tx_rate_link  Signal: $signal\n";
  }
  $summary_text .= sprintf("Total station TX: %.3fMbps  RX: %.3fMbps\n\n", $tot_ul_bps / 1000000, $tot_dl_bps / 1000000);

  # Radio stats
  $tot_dl_bps = 0;
  $tot_ul_bps = 0;
  my @rep_ports = uniq(@radios);
  for ($i = 0; $i<@rep_ports; $i++) {
    my $sta_name = $rep_ports[$i];
    my $pkey = "1.$resource.$sta_name";

    my $mac = $port_mac{$pkey};
    my $tx_rate = $port_tx_rate{$pkey};
    my $rx_rate = $port_rx_rate{$pkey};
    my $mode = $port_mode{$pkey};
    my $nss = $port_nss{$pkey};

    $brief_log .= "Radio Stats for $sta_name:\nMAC: $mac Mode: $mode  NSS: $nss\n";
    $brief_log .= "\tTX-Rate: ${tx_rate}bps  RX-Rate: ${rx_rate}bps";

    $summary_text .= "$sta_name:";
    $tot_dl_bps += $rx_rate;
    $summary_text .= sprintf(" RX: %.3fMbps", $rx_rate / 1000000);
    $tot_ul_bps += $tx_rate;
    $summary_text .= sprintf(" TX: %.3fMbps", $tx_rate / 1000000);
    $summary_text .= " Mode: $mode  NSS: $nss\n";
  }
  $summary_text .= sprintf("Total Radio TX: %.3fMbps  RX: %.3fMbps\n\n", $tot_ul_bps / 1000000, $tot_dl_bps / 1000000);

  # Upstream port
  my $pkey = "1.$upstream_resource.$upstream_port";
  my $mac = $port_mac{$pkey};
  my $tx_rate = $port_tx_rate{$pkey};
  my $rx_rate = $port_rx_rate{$pkey};
  my $mode = $port_mode{$pkey};
  my $nss = $port_nss{$pkey};

  $brief_log .= "Upstream Port Stats for $pkey:\nMAC: $mac";
  $brief_log .= " TX-Rate: ${tx_rate}bps  RX-Rate: ${rx_rate}bps";

  $summary_text .= "$pkey:";
  $summary_text .= sprintf(" RX: %.3fMbps", $rx_rate / 1000000);
  $summary_text .= sprintf(" TX: %.3fMbps", $tx_rate / 1000000);

  # The code below works, and makes use of existing scripts to make it perhaps more
  # clear to understand, but it is quite slow.  So, will hand-code some more efficient
  # reporting. --Ben
#   my $tot_dl_bps = 0;
#   my $tot_ul_bps = 0;
#   # Our endp names are derived from cx, so use that to our advantage.
#   for ($i = 0; $i<$cx_cnt; $i++) {
#     my $cxn = $cxs[$i];
#     my $epa = "$cxn-A";
#     my $epb = "$cxn-B";

#     my $ep_stats = `./lf_firemod.pl --endp_name $epa --stats_from_file $tmpfe --endp_vals RealRxRate,RealTxRate`;
#     $brief_log .= "Endpoint Stats for $epa:\n$ep_stats\n\n";
#     $summary_text .= "$cxn:";
#     if ($ep_stats =~ /RealRxRate:\s+(\d+)/) {
#       $tot_dl_bps += $1;
#       $summary_text .= sprintf(" Download RX: %.3fMbps", $1 / 1000000);
#     }
#     if ($ep_stats =~ /RealTxRate:\s+(\d+)/) {
#       $summary_text .= sprintf(" Upload TX: %.3fMbps", $1 / 1000000);
#     }
#     $ep_stats = `./lf_firemod.pl --endp_name $epb --stats_from_file $tmpfe --endp_vals RealRxRate,RealTxRate`;
#     $brief_log .= "Endpoint Stats for $epb:\n$ep_stats\n\n";
#     if ($ep_stats =~ /RealRxRate:\s+(\d+)/) {
#       $tot_ul_bps += $1;
#       $summary_text .= sprintf(" Upload RX: %.3fMbps", $1 / 1000000);
#     }
#     if ($ep_stats =~ /RealTxRate:\s+(\d+)/) {
#       $summary_text .= sprintf(" Download TX: %.3fMbps", $1 / 1000000);
#     }
#     $summary_text .= "\n";
#   }
#   $summary_text .= sprintf("Total Endpoint Upload RX: %.3fMbps  Download RX: %.3fMbps\n\n", $tot_ul_bps / 1000000, $tot_dl_bps / 1000000);
#   $mini_summary_text .= sprintf("Total Endpoint Upload RX: %.3fMbps  Download RX: %.3fMbps\n\n", $tot_ul_bps / 1000000, $tot_dl_bps / 1000000);

#   # Port
#   $sp = `cat $tmpf`;
#   logf("$sp\n");

#   $tot_dl_bps = 0;
#   $tot_ul_bps = 0;
#   for ($i = 0; $i<@stations; $i++) {
#     my $sta_name = $stations[$i];
#     my $sta_stats = `./lf_portmod.pl --card $resource --port_name $sta_name --stats_from_file $tmpf --show_port AP,ESSID,bps_rx,bps_tx,MAC,Mode,RX-Rate,TX-Rate,Signal,Link-Activity,Channel,Bandwidth,NSS`;
#     $brief_log .= "Station Stats:\n$sta_stats\n\n";
#     $summary_text .= "$sta_name:";
#     if ($sta_stats =~ /bps_rx:\s+(\d+)/) {
#       $tot_dl_bps += $1;
#       $summary_text .= sprintf(" RX: %.3fMbps", $1 / 1000000);
#     }
#     if ($sta_stats =~ /bps_tx:\s+(\d+)/) {
#       $tot_ul_bps += $1;
#       $summary_text .= sprintf(" TX: %.3fMbps", $1 / 1000000);
#     }
#     if ($sta_stats =~ /NSS:\s+(\d+)/) {
#       $summary_text .= " NSS: $1";
#     }
#     if ($sta_stats =~ /RX-Rate:\s+(\S+)/) {
#       $summary_text .= " RX-Rate: $1";
#     }
#     if ($sta_stats =~ /TX-Rate:\s+(\S+)/) {
#       $summary_text .= " TX-Rate: $1";
#     }
#     if ($sta_stats =~ /Signal:\s+(\S+)/) {
#       $summary_text .= " Signal: $1";
#     }
#     $summary_text .= "\n";
#   }
#   $summary_text .= sprintf("Total station TX: %.3fMbps  RX: %.3fMbps\n\n", $tot_ul_bps / 1000000, $tot_dl_bps / 1000000);

#   # Radio stats
#   $tot_dl_bps = 0;
#   $tot_ul_bps = 0;
#   my @rep_ports = uniq(@radios);
#   for ($i = 0; $i<@rep_ports; $i++) {
#     my $sta_name = $rep_ports[$i];
#     my $sta_stats = `./lf_portmod.pl --card $resource --port_name $sta_name --stats_from_file $tmpf --show_port bps_rx,bps_tx,MAC,Mode,NSS`;
#     $brief_log .= "Radio Stats for $sta_name:\n$sta_stats\n\n";
#     $summary_text .= "$sta_name:";
#     if ($sta_stats =~ /bps_rx:\s+(\d+)/) {
#       $tot_dl_bps += $1;
#       $summary_text .= sprintf(" RX: %.3fMbps", $1 / 1000000);
#     }
#     if ($sta_stats =~ /bps_tx:\s+(\d+)/) {
#       $tot_ul_bps += $1;
#       $summary_text .= sprintf(" TX: %.3fMbps", $1 / 1000000);
#     }
#     if ($sta_stats =~ /Mode:\s+(\S+)/) {
#       $summary_text .= " Mode: $1";
#     }
#     $summary_text .= "\n";
#   }
#   $summary_text .= sprintf("Total Radio TX: %.3fMbps  RX: %.3fMbps\n\n", $tot_ul_bps / 1000000, $tot_dl_bps / 1000000);

#   # Upstream port
#   my $p_stats = `./lf_portmod.pl --card $upstream_resource --port_name $upstream_port --stats_from_file $tmpf --show_port bps_rx,bps_tx,MAC,RX-Rate,TX-Rate`;
#   $brief_log .= "Upstream Port Stats:\n$p_stats\n\n";
#   $summary_text .= "$upstream_port:";
#   if ($p_stats =~ /bps_rx:\s+(\d+)/) {
#     $tot_dl_bps += $1;
#     $summary_text .= sprintf(" RX: %.3fMbps", $1 / 1000000);
#   }
#   if ($p_stats =~ /bps_tx:\s+(\d+)/) {
#     $tot_ul_bps += $1;
#     $summary_text .= sprintf(" TX: %.3fMbps", $1 / 1000000);
#   }
#   if ($p_stats =~ /RX-Rate:\s+(\S+)/) {
#     $summary_text .= " RX-Rate: $1";
#   }
#   if ($p_stats =~ /TX-Rate:\s+(\S+)/) {
#     $summary_text .= " TX-Rate: $1";
#   }
  $summary_text .= "\n";
}

sub stop_all_cx {
  $cmd = "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"set_cx_state all all STOPPED\"";
  do_cmd($cmd);
}

sub stop_all_my_cx {
  my $i;

  for ($i = 0; $i<@cxs; $i++) {
    my $cxn = $cxs[$i];
    $cmd = "./lf_firemod.pl --mgr $manager --action do_cmd --cmd \"set_cx_state default_tm $cxn STOPPED\"";
    do_cmd($cmd);
  }
}

sub logf {
  my $text = shift;
  print LOGF $text;
}

sub logp {
  my $text = shift;
  print LOGF $text;
  print $text; # to std-out too
}

sub logpb {
  my $text = shift;
  print LOGF $text;
  print $text; # to std-out too
  $brief_log .= "$text";
  $summary_text .= "$text"; # Even sparser summary output
}

sub do_test_series {
  my $desc = shift;
  my $speed_mult = shift;
  my $msg = "\n" . `date` . "Doing test series: $desc\n";

  logpb($msg);
  $mini_summary_text .= $msg;

  # First test case, 20 stations downloading, 3x3 mode.
  logpb("\nDoing download test with 20 stations.\n");
  do_one_test(0, floor(($speed_dl_tot * $speed_mult) / 20), 20, $one_way_test_time, $desc);
  # Upload 30 sec
  logpb("\nDoing upload test with 20 stations.\n");
  do_one_test( floor(($speed_ul_tot * $speed_mult) / 20), 0, 20, $one_way_test_time, $desc);
  # Upload/Download 1 minute sec
  logpb("\nDoing upload/download test with $sta_max stations.\n");
  do_one_test(floor(($speed_ul_bi_tot * $speed_mult) / $sta_max),
                floor(($speed_dl_tot * $speed_mult) / $sta_max),
                $sta_max,
                $bi_test_time,
                $desc);
}

sub do_cmd {
  my $cmd = shift;
  logp("$cmd\n");
  return system($cmd);
}

sub uniq {
  my %seen;
  grep !$seen{$_}++, @_;
}

sub incr_ip {
  if ($ip eq "DHCP") {
    return "DHCP";
  }
  $ipn++;
  return ipn2ip($ipn);
}

sub ip2ipn {
     return unpack 'N', inet_aton(shift);
}

sub ipn2ip {
    return inet_ntoa( pack 'N', shift );
}


my @array = qw(one two three two three);
my @filtered = uniq(@array);
