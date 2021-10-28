#!/usr/bin/perl -w
## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    LANforge server script for associating virtual stations
##    to an arbitrary SSID. You have options for creating a series
##    of Layer-3 connections per station created. Support for various
##    security modes for stations: wep, wpa, wpa2.
##
##    Install:
##    copy this script to /home/lanforge/scripts
##
##    Preparation:
##    This script expects a free radio (like wiphy0) to create
##    wifi stations on. It also expects an upstream wired port to
##    make tcp connections to. These ports should be able to
##    communicate with each other.
##
##    Usage Overview:
##    Use -h to show options.
##    There are two activities that this script presently performs:
##
##    Step1: create 1 wifi station, pass traffic to the upstream port
##       back and forth, and then disassociate. This activity could
##       be split into several steps if testing traffic up- or
##       down-stream only is desired.
##
##    Step2: create many wifi stations, wait until we see IPs appear
##       on them and then disassociate all of them. This activity could
##       also be modified to test for wifi association instead of address
##       aquisition. The present example uses static address assignment.
##
##    add: create and delete WiFi Virtual Radios. Also has option to
##       create station on specified virtual radio.
##
## (C) 2020, Candela Technologies Inc. support@candelatech.com
## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
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

no warnings 'portable';  # Support for 64-bit ints required
use Socket;
#use Data::Dumper;
our $binsleep = 0;
if ( -x "/bin/sleep" || -x "/usr/bin/sleep") {
   $::binsleep = 1;
}

sub altsleep {
   my ($time) = @_;
   if ($::binsleep) {
      `sleep $time`;
   }
   elsif ( $time < 1) {
      sleep(1);
   }
   elsif (int($time) != $time) {
      $time += 1.0;
      $time = int($time);
      sleep($time);
   }
   else {
      sleep($time);
   }
}

# Un-buffer output
$| = 1;
use Cwd qw(getcwd);
my $cwd = getcwd();

# use lib prepends to @INC, so put lower priority first
# This is before run-time, so cannot condition this with normal 'if' logic.
use lib '/home/lanforge/scripts';
use lib "./";

use List::Util qw(first);
use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
#use Net::Telnet ();

our $num_stations       = 1;
our $netmask            = "255.255.0.0";
our $default_ip_addr    = "DHCP"; # or IP
my  $log_cli            = "unset"; # use ENV{'LOG_CLI'}

# the upstream port should have an IP in same subnet range
# and we're assuming the port is on the same resource (1).
our $upstream_port      = "eth1";      # Step 1 upstream port
our $sta_wiphy          = "wiphy0";    # physical parent (radio) of virtual stations
our $phy_channel        = ""; # channel number
our $phy_antenna        = ""; # number of antennas, 0 means all
our %wiphy_bssids       = ();
our $admin_down_on_add  = 0;
our $ssid;
our $first_sta          = "sta100";
our $passphrase         = '';
our $change_mac         = 0;
our $min_tx             = "10000000";
our $max_tx             = "SAME";
our $security           = "open";
our $xsec               = "";    # extra 802.1* options: use-11u,use-11u-internet,use-dot1x
our %sec_options        = (
   "open"                  =>    0x0,
   "wpa"                   =>    0x10,
   "wep"                   =>    0x200,
   "wpa2"                  =>    0x400,
   "no-ht40"               =>    0x800,      # Disable ht-40
   "use-scan-ssid"         =>    0x1000,     # Enable SCAN-SSID flag in wpa_supplicant.
   "use-pasv-scan"         =>    0x2000,     # Use passive scanning (don't send probe requests).
   "no-sgi"                =>    0x4000,     # Disable SGI (Short Guard Interval).
   "use-radio-migration"   =>    0x8000,     # OK-To-Migrate (Allow migration between LANforge radios)
   "use-more-debug"        =>    0x10000,    # Verbose-Debug: more info in wpa-supplicant and hostapd logs.
   "use-11u"               =>    0x20000,    # Enable 802.11u (Interworking) feature.
   "use-11u-auto"          =>    0x40000,    # Enable 802.11u (I...) Auto-internetworking. Always enabled currently.
   "use-11u-internet"      =>    0x80000,    # AP Provides access to internet (802.11u I...)
   "use-11u-x-steps"       =>    0x100000,   # AP requires additional step for access (802.11u I...)
   "use-11u-emrg-advert"   =>    0x200000,   # AP claims emergency services reachable (802.11u I...)
   "use-11u-emrg-unauth"   =>    0x400000,   # AP provides Unauthenticated emergency services (802.11u I...)
   "use-hs20"              =>    0x800000,   # Enable Hotspot 2.0 (HS20) feature.  Req WPA-2.
   "no-dgaf"               =>    0x1000000,  # AP:  Disable DGAF (used by HotSpot 2.0).
   "use-dot1x"             =>    0x2000000,  # Use 802.1x (RADIUS for AP).
   "use-11r-pmska"         =>    0x4000000,  # Enable PMSKA caching for WPA2 (Rel to 802.11r).
   "no-ht80"               =>    0x8000000,  # Disable HT80 (for AC chipset NICs only)
   "use-ibss"              =>    0x20000000, # Station should be in IBSS mode.
   "use-osen"              =>    0x40000000, # Enable OSEN protocol (OSU Server-only Auth)
   "disable_roam"          =>    0x80000000,    # Disable automatic station roaming based on scan results.
   "ht160_enable"          =>    0x100000000,   # Enable HT160 mode.
   "disable_fast_reauth"   =>    0x200000000,   # Disable fast_reauth option for virtual stations.
   "mesh_mode"             =>    0x400000000,   # Station should be in MESH mode.
   "power_save_enable"     =>    0x800000000,   # Station should enable power-save.  May not work in all drivers/configurations.
   "create_admin_down"     =>    0x1000000000,  # Station should be created admin-down.
   "wds-mode"              =>    0x2000000000,  # WDS station (sort of like a lame mesh), not supported on ath10k
   "no-supp-op-class-ie"   =>    0x4000000000,  # Do not include supported-oper-class-IE in assoc requests.  May work around AP bugs.
   "txo-enable"            =>    0x8000000000,  # Enable/disable tx-offloads, typically managed by set_wifi_txo command
   "wpa3"                  =>    0x10000000000, # Enable WPA-3 (SAE Personal) mode.
   "use-bss-transition"    =>    0x80000000000, # Enable BSS transition.
   "disable-twt"           =>    0x100000000000, # Disable TWT mode 
);
our %ieee80211w_options = (
   "disabled"  => 0,
   "optional"  => 1,
   "required"  => 2,
   "0"         => 0,
   "1"         => 1,
   "2"         => 2
);
our $ieee80211w = "NA";

our $cx_type            = "tcp";
our %cx_types           = (
   "tcp"    =>    "lf_tcp",
   "udp"    =>    "lf_udp",
   "tcp6"   =>    "lf_tcp6",
   "udp6"   =>    "lf_udp6",
);
our %antenna_table = (
    0       => 0,
    "0"     => 0,
    -1      => 0,
    '0'     => 0,
    '-1'    => 0,
    'ALL'   => 0,

    '1'     => 1,
    '1x1'   => 1,
    'A'     => 1,

    '2'     => 4,
    '2x2'   => 4,
    'AB'    => 4,

    '3'     => 7,
    '3x3'   => 7,
    'ABC'   => 7,

    '4'     => 8,
    '4x4'   => 8,
    'ABCD'  => 8,
  );

our $duration           = 30; # seconds to transmit in step 1
our $db_preload         = ""; # use for loading before station creation
our $db_save            = ""; # use for saving a scenario that we just ran
our $db_postload        = ""; # use for cleanup after running/saving a scenario
our $poll_time          = 5;  # seconds
our $traffic_type       = "separate"; # separate: download then upload, concurrent: at same time
our $default_mac_pat    = "xx:xx:xx:*:*:xx";
our $mac_pattern        = $::default_mac_pat;
our $gateway            = "NA";
our %wifi_modes = (
   "a"      => "1",
   "b"      => "2",
   "g"      => "3",
   "abg"    => "4",
   "abgn"   => "5",
   "bgn"    => "6",
   "bg"     => "7",
   "abgnAC" => "8",
   "anAC"   => "9",
   "an"     => "10",
   "bgnAC"  => "11",
   "abgnAX" => "12",
   "bgnAX"  => "13",
   "anAX"   => "14"
);
our $wifi_mode ="";
our $bssid = "";
my $mode_list = join("|", sort keys %wifi_modes);

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
##                   Usage                                     #
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
my $usage = qq($0   [--mgr {host-name | IP}]
      [--mgr_port {ip port}]     # use if on non-default management port
      [--resource {resource}]    # use if multiple lanforge systems; defaults to 1
      [--quiet { yes | no }]     # debug output; -q
      [--log_cli]                # enables CLI command printing to STDOUT
                                 # same effect when setting env var LOG_CLI=STDOUT
      ##       AP selection
      [--radio {name}]           # e.g. wiphy2
      [--channel {channel}]      # e.g. 52, 161, 153
                                 # please check the LANforge GUI to verify resulting selection
                                 # center channels might be selected differently than you intended
      [--antenna {1,2,3,4}]      # select number of antennas
      [--ssid {ssid}]            # e.g. jedtest
      [--bssid {aa:bb:cc:00:11:22, or DEFAULT} # AP BSSID to connect to
      [--security {open|wep|wpa|wpa2|wpa3}] # station authentication type, Default is open
      [--xsec {comma,separated,list} ] # dot1x, 11u, other features, read script {to set flags same as in add_sta}
      [--passphrase {...}]       # Set security too if you want to enable security
      [--wifi_mode {$mode_list}]
      [--ieee80211w {disabled,optional,required}] # protected management frames (wpa2-ent/wpa3) also { NA, 0, 1, 2 }

      ##       station configuration
      [--num_stations {$num_stations}] # Defaults to 1
      [--first_sta {$first_sta}]
      [--first_ip {DHCP | DHCP6 | DHCP,DHCP6 |<ip address>}]
          # use DHCP,DHCP6 to enable both DHCP and DHCP6
      [--netmask {$netmask}]
      [--gateway {$gateway}]
      [--change_mac {0|1}]
         # If this is set to 0, then we will not change MAC if the station already exists.
         # This is now the default behaviour.
      [--mac-pattern {$default_mac_pat}]
         # xx        : uses parent radio octet
         # [0-9a-f]  : use this value for octet
         # *         : generates random octet
         # Use quotes around this argument! EG:
         # --mac_pattern '00:xx:*:*:xx:xx'

      ##       connection configuration
      [--cxtype {tcp/tcp6/udp/udp6}]   # use a tcp/udp connection, default tcp
      [--upstream {name|$upstream_port}]
         # could be AP or could be port on LANforge
         # connected to WAN side of AP
      [--bps-min {$min_tx}]         # minimum tx bps
      [--bps-max {SAME|bps-value}]  # maximum tx bps, use SAME or omit for SAME
      [--duration {$duration}]      # connection duration, seconds, default 60
      [--poll-time {$poll_time}]    # nap time between connection displays
      [--action {step1,step2,add,del,del_all_phy}]
         # step1: creates <num_stations> stations and L3 connections
         # step2: does bringup test
         # add: creates station on specified radio, or radio if no stations are requested
         # del: Delete the specified port.
         # del_all_phy: Delete all interfaces with the specified parent device.

      [--traffic_type {separate|concurrent}]
         # for step1: separate does download then upload
         # concurrent does upload and download at same time

      [--admin_down_on_add]
         # when creating stations, create them admin-down

      [--db_preload {scenario name}]
         # load this database before creating stations
         # option intended as a cleanup step

      [--db_save {name}]
         # save the state of this test scenario after running the
         # connections, before --db_postload

      [--db_postload {scenario name}]
         # load this database after running connections,
         # option intended as a cleanup step

      ##       virtual radio configuration
      [--vrad_chan {channel}]
      [--port_del {name}] # deletes port given

Examples:
## connecting to an open AP, at 2Mbps, for 20 minutes
 $0 --action step1   --radio wiphy0  --ssid ap-test-01  \\
   --bps-min 2000000 --duration 1200 --upstream eth1

 $0 --action step2 --radio wiphy2 --ssid jedtest \\
   --first_sta sta100 --first_ip DHCP --num_stations 3 \\
   --security wpa2 --passphrase jedtest1 --mac_pattern 'xx:xx:xx:*:*:*'
   Note: mac_pattern is NOT a regex, it is octet based tokens:
   * = rand(256)
   xx = parent mac octet
   You can specify a numeric mac address (d0:01:00:00:af:ff) and it can get incremented

## using a second lanforge system to connect to wpa2 AP:
 $0 --mgr 192.168.100.1 --resource 2 --radio wiphy2 \\
   --ssid jedtest       --passphrase 'asdf1234' \\
   --num_stations 10    --first_sta sta400 \\
   --first_ip DHCP      --upstream eth1 --action step1

## (Windows) using a beginning database and saving the resulting database:
 C:\\Users\\bob> cd "c:\\Program Files (x86)\\LANforge-Server\\scripts"
 C:\\Program Files (x86)\\LANforge-Server\\scripts>perl lf_associate_ap.pl --mgr jedtest \\
 --resource 2  --radio wiphy2 --first_ip DHCP \\
 --duration 10 --bps-min 10k  --bps-max 20M --cxtype tcp \\
 --ssid jedtest --passphrase jedtest1 --security wpa2 \\
 --first_sta 300 --db_preload Radio2 --db_save run_results --num_stations 3

## connecting to wpa AP:
$0 --mgr 192.168.100.1 --radio wiphy0 \\
   --ssid jedtest    --passphrase 'asdf1234' --security wep \\
   --num_stations 10 --first_sta sta400 \\
   --first_ip DHCP   --upstream eth1        --action step1

## creating and deleting a virtual radio:
 $0 --mgr 192.168.100.1 --resource 2 \\
   --radio vphy1    --vrad_chan 36    --action add

 $0 --mgr 192.168.100.1 --resource 2 \\
   --port_del vrad1 --action del

## Adding a station to a new or existing virtual radio:
 $0 --mgr 192.168.100.1 --resource 2 \\
   --radio vphy1 --first_sta sta0 --first_ip DHCP --ssid my_ssid  --action add

## Add lots of stations to a radio

 $0 --mgr ben-ota-1 --resource 2 --action add --radio wiphy0 --ssid Lede-ventana \\
    --first_sta sta100 --first_ip DHCP --num_stations 63

## Delete all virtual devices on wiphy0

 $0 --mgr ben-ota-1 --resource 2 --action del_all_phy --port_del wiphy0

## Create a station and set Flags

 $0 --mgr localhost --radio wiphy1 --ssid sushant-AP --action add --num_stations 1 \\
    --xsec use-bss-transition --first_ip DHCP
);

my $shelf_num = 1;

# Default values for cmd-line args.
our $report_timer       = 1000;           # milliseconds
our $test_mgr           = "default_tm";   # name of test manager
our $resource           = 1;              # might be referred to as card_id
our $resource2          = 1;              # might be referred to as card_id
our $begin_ip           = $default_ip_addr;

# sta_names is a set of names and static IP addresses to assign them.
# As many stations as are in the set will be created. If you want to use
# DHCP, replace the ip with "DHCP".
# example
# %sta_names = (
#     "sta1" => "192.168.0.1",
#     "sta2" => "NEXT"
#     "sta2" => "DHCP"
#);
our %sta_names          = ();
our %cx_names           = ();
our $quiet              = "yes";             # debugging
our $action             = "step1";           # default action
our $lfmgr_host         = "localhost";       # LANforge manager IP

# Virtual radio defaults.
our $vrad_chan          = -1;                # default channel (AUTO)

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# Nothing to configure below here, most likely.
# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
my $lfmgr_port          = 4001;              # LANforge manager port
our $quiesce_sec        = 3;                 # pretty standard

=pod
this fmt_cmd subroutine is now disabled, please use utils->fmt_cmd
=cut

sub db_exists {
   my $db_name = shift;
   die ("::db_exists: called with blank database name. Did you mean EMPTY?") if ($db_name eq "");
   print "Looking for database $db_name ...";
   my @db_names = split("\n", $::utils->doAsyncCmd("show_dbs"));
   my @match = grep { /^$db_name\/$/ } @db_names;
   return 1 if (@match > 0);

   print "Warning! Scenario $db_name not found among: ".join(", ", @db_names)."\n";
   return 0;
}

sub load_db {
   my $db_name = shift;
   die ("::load_db: called with blank database name. Did you mean EMPTY?") if ($db_name eq "");
   print "Loading database $db_name ...";
   $::utils->doCmd(fmt_cmd("load", $db_name, "overwrite"));

   for (my $i = 20 ; $i>0; $i--) {
      sleep(1);
      my $up            = 0;
      my $has_tx_bytes  = 0;
      my $sta_cnt       = 0;
      my $prev_cnt      = 0;
      my $status        = $::utils->doAsyncCmd($::utils->fmt_cmd("nc_show_ports", 1, $::resource, "ALL"));
      my @status        = split("\n", $status);

      foreach (@status){
         if (/^Shelf: 1, Card: \d+\s+Port: \d+\s+Type: STA\s+/) {
            $sta_cnt++;
            print "sta_cnt $sta_cnt up $up has_tx %has_tx_bytes\n";
         }
         if ($sta_cnt > $prev_cnt) {
            if ( /IP: \d+\.\d+\.\d+\.\d+ / && !/IP: 0\.0\.0\.0 /) {
               $up++;
            }
            if ( /Txb: \d+ / && !/Txb: 0 / ) {
               $has_tx_bytes ++;
            }
            $prev_cnt = $sta_cnt if ( /^\s*$/ );
         }
      } # ~foreach
   }
   print " done\n";
}

sub save_db {
   my $db_name = shift;
   die ("::save_db: called with blank database name. Please debug.") if ($db_name eq "");
   print "Saving database $db_name ...";
   if (db_exists($db_name)==1) {
      print "Warning: will over-write database $db_name! ";
   }
   $::utils->doCmd($::utils->fmt_cmd("save", $db_name));
   print " done\n";
}

sub get_radio_bssid {
   my $radio_name = shift;
   die ("::get_radio_bssid: blank radio name. Please debug.")  if ($radio_name eq "");

   return $::wiphy_bssids{ $radio_name }
      if (exists($::wiphy_bssids{ $radio_name }));

   #print "* looking up $radio_name for bssid...";
   my @status_lines  = split("\n", $::utils->doAsyncCmd($::utils->fmt_cmd("show_port", 1, $::resource, $radio_name)));
   my @mac_lines     = grep { /\s+MAC:\s+[^ ]+/ } @status_lines;
   die ("::get_radio_bssid: failed to find radio bssid, no MAC lines")
      if (@mac_lines < 1);

   my ($parent_bssid) = $mac_lines[0] =~ /\s+MAC:\s+([^ ]+)/;
   die ("::get_radio_bssid: failed to find radio bssid, MAC was empty")
      if ($parent_bssid eq "");

   $::wiphy_bssids{ $radio_name } = $parent_bssid;
   #print $parent_bssid."\n";

   return $parent_bssid;
}

sub new_mac_from_pattern {
   my $parent_mac = shift;
   my $pattern    = shift;
   die ("::new_mac_pattern: blank parent_mac. Please debug.")  if ($parent_mac eq "");
   die ("::new_mac_pattern: blank pattern. Please debug.")     if ($pattern eq "");

   if (($pattern !~ /x+/i) && ($pattern !~ /[*]+/)) {
      return $pattern; # this lacks pattern tokens
   }

   my @parent_hunks  = split(":", $parent_mac);
   my @pattern_hunks = split(":", $pattern);

   die ("::new_mac_pattern: parent_mac needs to be colon-separated. Please debug.") if (@parent_hunks != 6);
   die ("::new_mac_pattern: pattern needs to be colon-separated. Please debug.")    if (@pattern_hunks != 6);

   my @new_hunks = ();
   for (my $i=0; $i < 6; $i++) {
      if ($pattern_hunks[$i] =~ /xx/i) {
         $new_hunks[ $i ] = $parent_hunks[ $i ];
      }
      elsif ($pattern_hunks[$i] =~ /[*]+/) {
         my $r=int(rand(255));
         if ($i == 0) {
            $r |= 0x002; # sets the 'locally administered bit'
            $r &= 0x0FE;
            # use if this upstream routers squash local admin bit macs
            # $r &= 0x0DF;
         }
         $new_hunks[ $i ] = sprintf("%02X", $r);
      }
      else {
         $new_hunks[ $i ] = $pattern_hunks[ $i ];
      }
   }
   #print "####### new_mac_from_pattern: [$parent_mac][$pattern] -> ".lc(join(":", @new_hunks))."\n";
   return lc(join(":", @new_hunks));
} # ~new_mac_pattern

sub new_random_mac {
   my $rv = "00:";
   for (my $i=0; $i<5; $i++) {
      $rv.=sprintf("%02X",int(rand(255))).(($i<4)?':':'');
   }
   #print "new_random_mac $rv\n";
   return $rv;
}

sub fmt_vsta_cmd {
   my ($resource, $sta_wiphy, $sta_name, $flags, $ssid, $passphrase, $mac, $flags_mask, $wifi_m, $bssid ) = @_;
   die("fmt_vsta_cmd wants sta_wiphy name, bye.") unless($sta_wiphy);
   my $key              = "[BLANK]";
   my $ap               = "DEFAULT";
   if ((defined $bssid) && ($bssid ne "")) {
      $ap = $bssid;
   }
   my $cfg_file         = "NA";
   my $mode             = 8; # default to a/b/g/n/AC
   my $rate             = "NA";
   my $amsdu            = "NA";
   my $ampdu_factor     = "NA";
   my $ampdu_density    = "NA";
   my $sta_br_id        = "NA";
   $key = $passphrase if ($passphrase ne "");

   if ($wifi_m ne "") {
      if (exists $::wifi_modes{$wifi_m}) {
         $mode = $::wifi_modes{$wifi_m};
      }
      else {
         print "Wifi Mode [$wifi_m] not recognised. Please use:\n";
         print join(", ", sort keys %::wifi_modes);
         exit 1;
      }
   }

   $flags      = "+0" if ($flags       == 0); # perl goes funny on zeros
   $flags_mask = "+0" if ($flags_mask  == 0);
   $flags      = "NA" if ($flags eq "");

   $::ieee80211w = "NA"
      if (!(defined $::ieee80211w) || ($::ieee80211w eq ""));
   if ($::ieee80211w ne "NA") {
      if ( exists $::ieee80211w_options{ $::ieee80211w }) {
         $::ieee80211w = $::ieee80211w_options{ $::ieee80211w };
      }
      elsif ((int($::ieee80211w) < 0) || (int($::ieee80211w) > 2)) {
         print("\n* ieee80211w value outside of values {0, 1, 2} or {disabled, optional, required} -- being set to NA\n");
         $::ieee80211w = "NA";
      }
      # print("\n* ieee80211w value set to $::ieee80211w \n");
   }

   return $::utils->fmt_cmd("add_sta", 1, $resource, $sta_wiphy, $sta_name, "$flags",
                  "$ssid", "NA", "$key", $ap, $cfg_file, $mac,
                  $mode, $rate, $amsdu, $ampdu_factor, $ampdu_density,
                  $sta_br_id, "$flags_mask", $::ieee80211w );
}

sub fmt_vrad_cmd {
   my ($resource, $sta_wiphy, $vrad_chan ) = @_;
   die("fmt_vrad_cmd requires sta_wiphy.") unless($sta_wiphy);
   my $mode             = "NA";
   my $country          = "NA";
   my $frequency        = "NA";
   my $frag_thresh      = "NA";
   my $rate             = "NA";
   my $rts              = "NA";
   my $txpower          = "NA";
   my $mac              = "NA";
   my $antenna          = "NA";
   my $flags            = "0x1";
   my $flags_mask       = "NA";
   return $::utils->fmt_cmd("set_wifi_radio", 1, $resource, $sta_wiphy, $mode, $vrad_chan,
                  $country, $frequency, $frag_thresh, $rate, $rts, $txpower,
                  $mac, "$antenna", "$flags", "$flags_mask" );
}

sub createEpPair {
   my $sta_name      = shift;
   die("createEpPair: please pass station name, bye")    unless(defined $sta_name         && $sta_name ne '');
   die("createEpPair: please define upstream_port, bye") unless(defined $::upstream_port  && $::upstream_port ne '');
   my $port_a        = $sta_name;
   my $port_b        = $::upstream_port;
   my $cx_name       = $::cx_names{$sta_name}->{"cx"};
   my $ep1           = $::cx_names{$sta_name}->{"ep1"};
   my $ep2           = $::cx_names{$sta_name}->{"ep2"};
   my %min_pkt_szs   = (
      'tcp'    => [ 1460, 1460 ],
      'tcp6'   => [ 1460, 1460 ],
      'udp'    => [ 1472, 1472 ],
      'udp6'   => [ 1472, 1472 ]
      );
   my %max_pkt_szs   = (
      'tcp'    => [ 1460, 1460 ],
      'tcp6'   => [ 1460, 1460 ],
      'udp'    => [ 1472, 1472 ],
      'udp6'   => [ 1472, 1472 ]
      );
   $::cx_type = "tcp" if ($::cx_type eq "");
   print "\n cxtype [$::cx_type]\n" unless($::utils->isQuiet());
   if ( ! exists $::cx_types{$::cx_type} ) {
      die( "Please choose connection type: ".join(", ", keys(%::cx_types)));
   }
   my $cxtype        = $::cx_types{$::cx_type};
   my $rate_min      = "+0";     # we will set these later
   my $rate_max      = "+0";     # using set_endp_tx_bounds

   die("createEpPair: wants cx_name, bye.")           unless(defined $cx_name && $cx_name ne '');
   die("createEpPair: wants ep1 name, bye.")          unless(defined $ep1     && $ep1     ne '');
   die("createEpPair: wants ep2 name, bye.")          unless(defined $ep2     && $ep2     ne '');

   my $cmd = $::utils->fmt_cmd("add_endp", $ep1, 1, $::resource, $port_a, $cxtype,
                     -1, "NA", "$rate_min", "$rate_max", "NA",
                     $min_pkt_szs{$::cx_type}[0],  @{$max_pkt_szs{$::cx_type}}[0],
                     "increasing", "NO", "NA", "NA", "NA");
   print "EP1: $cmd\n" unless($::utils->isQuiet());
   $::utils->doCmd($cmd);

   $cmd = $::utils->fmt_cmd("add_endp", $ep2, 1, $::resource2, $port_b, $cxtype,
                     -1, "NA", "$rate_min", "$rate_max", "NA",
                     $min_pkt_szs{$::cx_type}[1],  @{$max_pkt_szs{$::cx_type}}[1],
                     "increasing", "NO", "NA", "NA", "NA");
   print "EP2: $cmd\n"  unless($::utils->isQuiet());
   $::utils->doCmd($cmd);

   # Now, add the cross-connect
   $::utils->doCmd($::utils->fmt_cmd("add_cx", $cx_name, $::test_mgr, $ep1, $ep2));
   $::utils->doCmd($::utils->fmt_cmd("set_cx_report_timer", $::test_mgr, $cx_name, $::report_timer));
}

sub fmt_port_cmd {
   my($resource, $port_id, $ip_addr, $mac_addr) = @_;
   my $use_dhcp         = ($ip_addr =~ /\bDHCP\b/) ? 1 : 0;
   my $use_dhcp6        = ($ip_addr =~ /\bDHCP6\b/) ? 1 : 0;
   my $ip               = ($use_dhcp||$use_dhcp6) ? "0.0.0.0" : $ip_addr ;
   $mac_addr            = die("fmt_port_cmd requires mac_addr") if(!$mac_addr); # || $mac_addr eq "NA");
   #print "fmt_port_cmd: RES $resource PORT $port_id IP_A $ip_addr MAC $mac_addr -> $ip\n" unless($::quiet eq "yes");
   my $cmd_flags        = 'NA'; #0;
   my $cur_flags        = 0;
   $cur_flags           |= 0x80000000    if ($use_dhcp);
   $cur_flags           |= 0x20000000000 if ($use_dhcp6);
   #print "fmt_port_cmd: DHCP($use_dhcp) $cur_flags\n" unless($::quiet eq "yes");
   my $ist_flags        = 0;
   $ist_flags           |= 0x2;       # check current flags
   $ist_flags           |= 0x4        if ($ip ne "NA");
   $ist_flags           |= 0x8        if ($::netmask ne "NA");
   $ist_flags           |= 0x10       if (($::gateway ne "NA") || ($::gateway ne "") || ($::gateway ne "0.0.0.0"));
   $ist_flags           |= 0x20       if ($mac_addr ne "NA");
   $ist_flags           |= 0x4000;    # Always interested in DHCP, we either set it to DHCP or IP
   $ist_flags           |= 0x800000;  # port up
   $ist_flags           |= 0x1000000; # Always interested in DHCP, we either set it to DHCP or IP


   my $gw               = "0.0.0.0";
   if (($::gateway ne "") || ($::gateway ne "") || ($::gateway ne "0.0.0.0")) {
      $gw = $::gateway;
   }

   my $dns_servers      = "NA";
   my $dhcp_client_id   = "NONE";
   my $flags2           = "NA";

   # Ben suggests using $sta_name before using $port_id
   $cur_flags = "+0" if(!$cur_flags);
   $cmd_flags = "+0" if(!$cmd_flags);
   $ist_flags = "+0" if(!$ist_flags);
   my $cmd = $::utils->fmt_cmd("set_port", 1, $::resource, $port_id, $ip, $::netmask,
                     $gw, "$cmd_flags", "$cur_flags",
                     "$mac_addr", "NA", "NA", "NA", "$ist_flags", $::report_timer, "$flags2",
                     "NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA",
                     $dns_servers, "NA", $dhcp_client_id);
   print("fmt_port_cmd: ".$cmd) unless($::utils->isQuiet());
   return $cmd;
}

sub fmt_port_down {
   my($resource, $port_id, $ip_addr, $ip_mask) = @_;
   die("fmt_port_down wants resource id, bye.") unless($resource);
   die("fmt_port_down wants port_id id, bye.") unless($port_id);
   die("fmt_port_down wants ip_addr id, bye.") unless($ip_addr);
   die("fmt_port_down wants ip_mask id, bye.") unless($ip_mask);

   my $use_dhcp         = ($ip_addr =~ /\bDHCP\b/) ? 1 : 0;
   my $use_dhcp6        = ($ip_addr =~ /\bDHCP6\b/) ? 1 : 0;
   my $ip               = ($use_dhcp||$use_dhcp6) ? "0.0.0.0" : $ip_addr ;
   my $cmd_flags        = "NA";
   my $cur_flags        = 0;
   $cur_flags           |= 0x1;       # port down
   my $ist_flags        = 0;
   $ist_flags           |= 0x2;       # check current flags
   $ist_flags           |= 0x800000;  # port down
   my $dhcp_id          = "NONE";
   my $netmask          = "$ip_mask";
   my $gw               = (($::gateway eq "NA") || ($::gateway eq "") || ($::gateway eq "0.0.0.0")) ? "0.0.0.0" : $::gateway;
   my $dns_servers      = "NA";
   my $dhcp_client_id   = "NONE";
   my $flags2           = "NA";

   $cmd_flags  = "+0" if(!$cmd_flags); # zeros are falsy in perl
   $cur_flags  = "+0" if(!$cur_flags);
   $ist_flags  = "+0" if(!$ist_flags);
   my $cmd = $::utils->fmt_cmd("set_port", 1, $resource, $port_id, $ip_addr,
                     $netmask, $gw, "$cmd_flags", "$cur_flags",
                     "NA", "NA", "NA", "NA", "$ist_flags", $::report_timer, "$flags2",
                     "NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA",
                     $dns_servers, "NA", $dhcp_client_id);
   return $cmd;
}

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----#
#                             WiFi FLAGS                                                  #
#        and please see the CLI users guide (flags can get updated)                       #
#           http://www.candelatech.com/lfcli_ug.php                                       #
#                                                                                         #
#    0x10         Enable WPA                                                              #
#    0x20         Use Custom wpa_supplicant config file.                                  #
#    0x100        Use wpa_supplicant configured for WEP encryption.                       #
#    0x200        Use wpa_supplicant configured for WPA2 encryption.                      #
#    0x400        Disable HT-40 even if hardware and AP support it.                       #
#    0x800        Enable SCAN-SSID flag in wpa_supplicant.                                #
#    0x1000       Enable PCSC (used by WPA-SIM)                                           #
#    0x2000       Disable SGI (Short Guard Interval).                                     #
#    0x4000       OK-To-Migrate (Allow migration between LANforge radios)                 #
#    0x8000       Verbose-Debug:  Increase debug info in wpa-supplicant and hostapd logs. #
#    0x10000      Enable 802.11u (Interworking) feature.                                  #
#    0x20000      Enable 802.11u (Interworking) Auto-internetworking feature.             #
#    0x40000      AP Provides access to internet (802.11u Interworking)                   #
#    0x80000      AP requires additional step for access (802.11u Interworking)           #
#    0x100000     AP claims emergency services reachable (802.11u Interworking)           #
#    0x200000     AP provides Unauthenticated emergency services (802.11u Interworking)   #
#    0x400000     Enable Hotspot 2.0 (HS20) feature.  Requires WPA-2.                     #
#    0x800000     AP:  Disable DGAF (used by HotSpot 2.0).                                #
#    0x1000000    Use 802.1x (RADIUS for AP).                                             #
#    0x2000000    Enable oportunistic PMSKA caching for WPA2 (Related to 802.11r).        #
#                                                                                         #
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----#
sub new_wifi_station {
   my $sta_name   = shift;
   die("new_wifi_station wants station name, bye")                unless(defined $sta_name && $sta_name ne '');
   my $ip_addr    = shift;
   die("new_wifi_station wants ip_address, bye")                  unless(defined $ip_addr && $ip_addr ne '');
   my $rh_results = shift;
   die("new_wifi_station wants hash ref to place results, bye.")  unless(defined $rh_results);
   my $wifi_m     = shift;
   my $num_in_series = shift; # use this to add to non-patterned mac-address
   my $mac_addr = "";

   #print "## new-wifi-station, sta-name: $sta_name  change-mac: $change_mac" unless($::utils->isQuiet());

   if (! $::change_mac) {
     my $status = $::utils->doAsyncCmd($::utils->fmt_cmd("show_port", 1, $::resource, $sta_name));
     if ($status =~ /MAC:\s+(\S+)\s+/) {
       $mac_addr = $1;
     }
   }
   #print "new_wifi_station->mac_addr: $mac_addr\n";
   if ($mac_addr eq "") {
     # Couldn't find it, or we want to change the mac
     #print "## calculating new mac-addr.." unless($::utils->isQuiet());
     my $parent_mac = get_radio_bssid($::sta_wiphy);
     die("new_wifi_station: unable to find bssid of parent radio") if ($parent_mac eq "");
     $mac_addr   = new_mac_from_pattern($parent_mac, $::mac_pattern);
     #print "OLD MAC $::mac_pattern NEW MAC $mac_addr\n";
     if (($mac_addr eq $::mac_pattern) && ($num_in_series > 0)) {
        $mac_addr = $::utils->mac_add($::mac_pattern, $num_in_series);
     }
     #print "OLD MAC $::mac_pattern NEWER MAC $mac_addr\n";
     #print "new_wifi_station->new_mac_from_pattern: $mac_addr\n";
   }

   #print "## $sta_name $mac_addr; " unless($::utils->isQuiet());
   my $flags      = +0; # set this to string later
   my $flagsmask  = +0; # set this to string later

   # To set zero value set the bit in flags to zero.
   # Set the flagsmask value to 1 if you want the value to be set to 1 or 0.
   # NOTE:  This script is used to change things, not just create them, so it is not
   # always wrong to not set passphrase since it could be set already.
   if ($::passphrase eq "") {
      $::passphrase = "NA";
      #if($::security ne "open") {
      #   die("Passphrase not set when --security [$::security] chosen. Please set passphrase.");
      #}
   }
   if ( ! exists($::sec_options{$::security})) {
      die( "Unknown security option [{$::security}]");
   }
   $flags         |= $::sec_options{$::security};
   # This doesn't work since 'open' maps to 0x0 and we need to also disable
   # flags that might be set previously.
   # $flagsmask     |= $::sec_options{$::security};
   # We are always configuring security to one thing or another, so we need to
   # mask all of the bits properly.
   $flagsmask |= (0x10 | 0x200 | 0x400 | 0x10000000000);
   $flagsmask |= 0x1000000000 if ($::admin_down_on_add);

   if (defined $::xsec && "$::xsec" ne "") {
      for my $sec_op (split(',', $::xsec)) {
         next if (!defined $::sec_options{$sec_op});

         $flags      |= $::sec_options{$sec_op};
         $flagsmask  |= $::sec_options{$sec_op};
      }
   }
   $flags      = "+0" if ( $flags      == 0);
   $flagsmask  = "+0" if ( $flagsmask  == 0);
   # perform the station create first, then assign IP as necessary
   my $sta1_cmd   = fmt_vsta_cmd($::resource, $::sta_wiphy, $sta_name,
                                 "$flags", "$::ssid", "$::passphrase",
                                 $mac_addr, "$flagsmask", $wifi_m, $::bssid);
   $::utils->doCmd($sta1_cmd);
   #$::utils->sleep_ms(20);
   $sta1_cmd = fmt_port_cmd($resource, $sta_name, $ip_addr, $mac_addr);
   $::utils->doCmd($sta1_cmd);
   #$::utils->sleep_ms(20);
   #$::utils->doAsyncCmd($::utils->fmt_cmd("nc_show_port", 1, $::resource, $sta_name));
   if ($::admin_down_on_add) {
     my $cur_flags = 0x1; # port down
     my $ist_flags = 0x800000; # port down
     $sta1_cmd = $::utils->fmt_cmd("set_port", 1, $resource, $sta_name, "NA",
                         "NA", "NA", "NA", "$cur_flags",
                         "NA", "NA", "NA", "NA", "$ist_flags");
     $::utils->doCmd($sta1_cmd);
     #$::utils->sleep_ms(20);
   }

   #if ($sleep_amt > 0) {
   #  sleep $sleep_amt;
   #}
   my $data = [ $mac_addr, $sta_name, $sta1_cmd ];
   $rh_results->{$sta_name} = $data;
}

sub new_wifi_radio {
   my $cmd = fmt_vrad_cmd($::resource, $::sta_wiphy, $::vrad_chan );
   $::utils->doCmd($cmd);
}

sub delete_port {
   if (defined $::port_del) {
      print "deleting port $::port_del\n" unless($::utils->isQuiet());
      $::utils->doCmd($::utils->fmt_cmd("rm_vlan", 1, $::resource, $::port_del));
      $::utils->sleep_ms(20);
   }
}

sub get_sta_state {
   my($rs_status) = @_;
   die("is_assoc_state: wants ref to status string")     unless($rs_status);
   my @lines      = split(/\r?\n/, $$rs_status);
   my $careful    = 0;
   my $name       = "unknown";
   my $ip         = "0.0.0.0";
   my $assoc      = "unknown";
   my $first;
   my $freq;
   my @hunks;
   my $mac;
   my $gw;
   my $mask;
   my $channel;
   my $mode;
   my $probed_seen = 0;
   for my $line (@lines) {
      $first = "_";
      my($key) = $line =~ m/^\s*([^:]+:)\s+/;
      #print "{{{$key}}} $line\n";
      next if ($line =~ /^\s*$/);
      next if ($line =~ /RSLT:/);
      last if ($line =~ /default@/);

      $probed_seen++ if ($line =~ /Probed/);
      if ($key && $key eq "MAC:" ) {
         @hunks   = split(/: /, $line);
         $mac     = (split(/ /, $hunks[1]))[0];
         $name    = (split(/ /, $hunks[2]))[0];
         next;
      }
      if ($key && $key eq "IP:") {
         @hunks   = split(/: /, $line);
         $ip      = (split(/ /, $hunks[1]))[0];
         $mask    = (split(/ /, $hunks[2]))[0];
         $gw      = (split(/ /, $hunks[3]))[0];
         next;
      }
      if ($probed_seen && ($line =~ /Mode:/)) {
         @hunks   = split(/: /, $line);
         $careful = 1;
         $mode    = (split(/ /, $hunks[2]))[0];
         next;
      }
      if( $probed_seen && $careful && ($key eq "Channel:")) {
         @hunks   = split(/: /, $line);
         #print Dumper(\@hunks);
         $channel = (split(/ /, $hunks[1]))[0];
         $freq    = (split(/ /, $hunks[3]))[0];
         if ((@hunks > 3) && (defined $hunks[4])) {
           $assoc   = (split(/ /, $hunks[4]))[0];
         }

      }
   }
   my %rv = (
      "assoc"  => $assoc,
      "freq"   => $freq,
      "ip"     => $ip,
      "mask"   => $mask,
      "gw"     => $gw,
      "mac"    => $mac,
      "mode"   => $mode,
      "name"   => $name );
   #print Dumper(\%rv);
   return %rv;
}

sub awaitStationRemoval {
   my $old_sta_count = (keys %::sta_names);
   print "Waiting for $old_sta_count stations to be removed...";
   while( $old_sta_count > 0 ) {
      $old_sta_count = (keys %::sta_names);
      for my $sta_name (sort(keys %::sta_names)) {
         print " $sta_name,";
         my $status = $::utils->doAsyncCmd($::utils->fmt_cmd("show_port", 1, $::resource, $sta_name));
         $old_sta_count-- if( $status =~ m/Could not find/);
      }
      if ($old_sta_count > 0) {
        #print "$old_sta_count...";
        sleep 1;
      }
   }
   print " Old stations removed\n";
}

#~expand to multiple cross-connects
sub removeOldCrossConnects {
   print "Removing old cross-connects, and endpoints ...\n";
   for my $sta_name (sort(keys(%::sta_names))) {
      my $cx_name = $::cx_names{$sta_name}->{"cx"};
      my $ep1     = $::cx_names{$sta_name}->{"ep1"};
      my $ep2     = $::cx_names{$sta_name}->{"ep2"};
      $::utils->doCmd("rm_cx $::test_mgr $cx_name");
      $::utils->doCmd("rm_endp $ep1");
      $::utils->doCmd("rm_endp $ep2");
      print " $cx_name ($ep1 - $ep2)...";
   }
   print " done.\n";
}

sub removeOldStations {
   print "Deleting ports:";
   foreach my $sta_name (reverse sort(keys %::sta_names)) {
      my $status = $::utils->doAsyncCmd($::utils->fmt_cmd("show_port", 1, $::resource, $sta_name));
      if ($status =~ /Type:/) {
        # It exists, remove it
        #
        print "...$sta_name ";
        $::utils->doCmd($::utils->fmt_cmd("rm_vlan", 1, $::resource, $sta_name));
      }
   }
   sleep(1);
   # force a refresh on them so phantom doesn't show
   foreach my $sta_name (reverse sort(keys %::sta_names)) {
      my $status = $::utils->doAsyncCmd($::utils->fmt_cmd("nc_show_port", 1, $::resource, $sta_name));
   }
   print " done.\n";
}

sub awaitNewStations {
   print "Waiting for stations to associate...";
   my $new_sta_count    = keys(%::sta_names);
   my $found_stations   = 0;
   while( $new_sta_count > $found_stations ) {
      $found_stations = 0;
      my @are_assoc        = ();
      my @not_assoc        = ();
      for my $sta_name (sort(keys(%::sta_names))) {
         my $status     = $::utils->doAsyncCmd($::utils->fmt_cmd("show_port", 1, $::resource, $sta_name));
         #print "STATUS: $status\n\n";
         my %sta_status = get_sta_state(\$status);
         #print " $sta_name ".$sta_status{"assoc"};
         if( $sta_status{"assoc"} !~ /NA|Not-Associated|unknown/) {
            push(@are_assoc, $sta_name);
         }
         else {
            push(@not_assoc, $sta_name);
         }
      } #~foreach sta
      $found_stations = @are_assoc;
      print " $found_stations/$new_sta_count seen to associate\n";
      if ( $found_stations != $new_sta_count ){
         print "  Associated:".join(", ", @are_assoc)."\n";
         print "  Pending   :".join(", ", @not_assoc)."\n";
      }
      sleep 1;
   } # ~while
}

sub endpointReport {
   my $ep = shift;
   my ($ep_name, $tx_rate, $rx_rate,$rx_bps);
   die("endpointReport: should be passed name of endpoint, bye.") unless ( $ep ne '' );
   my $blob = $::utils->doAsyncCmd($::utils->fmt_cmd("nc_show_endpoints", "$ep"), "\n");
   #print "BLOB: $blob\n\n\n";
   ( $ep_name ) = ($blob =~ m/^Endpoint \[(.*?)\] /mg);
   ( $tx_rate ) = ($blob =~ m/(Tx Bytes: .*$)/mg);
   ( $rx_rate ) = ($blob =~ m/(Rx Bytes: .*$)/mg);
   print "$ep_name:\t$tx_rate\n\t\t$rx_rate\n";
}

sub showEndpoints {
   for my $sta_name (sort(keys(%::sta_names))) {
      my $ep1 = $::cx_names{$sta_name}->{ep1};
      my $ep2 = $::cx_names{$sta_name}->{ep2};
      endpointReport($ep1);
      endpointReport($ep2);
   }
}

sub createEndpointPairs {
   print "\nCreating connections: ";
   for my $sta_name (sort(keys(%::sta_names))) {
      my $cx   = $::cx_names{$sta_name}->{"cx"};
      print " $cx ($sta_name - $::upstream_port), ";
      createEpPair($sta_name);
   }
   print "done.\n";
}

sub evalUnits {
   my $val = shift;

   if ($val =~ /^\d+$/) {
      return +0+$val;
   }
   my $pow = 1;
   if ($val =~ /(\d+)(\w+)/) {
      my $pref = $1;
      my $suff = $2;
      if ($suff =~ /[Kk][Bbps]*$/) {
         $pow = 1000;
      }
      elsif ($suff =~ /[Mm][Bbps]*$/) {
         $pow = 1000000;
      }
      elsif ($suff =~ /[Gg][Bbps]*$/) {
         $pow = 1000000000;
      }
      if ($pref == 0 || $pow == 0) {
         print "Warning: speed coeficients [$pref,$pow] appear suspicious\n";
      }
      my $speed =0 + ($pref * $pow);
      #print ">>>> setting speed to $speed <<<<\n";
      return $speed;
   }
   print "Warning: speed[$val] appears suspicious\n";
   return $val;
}

sub adjustForSimultaneous {
   my $no_rate    = "+0";
   if (lc($::min_tx) eq "same" ) {
      die "--min_tx may not be 'same', please provide a number or formatted unit in K, M or G";
   }
   my $rate_min   = evalUnits($::min_tx);
   #print "rate_min now: $rate_min\n";
   $::max_tx      = $::min_tx if (lc($::max_tx) eq "same" ) ;
   my $rate_max   =  evalUnits($::max_tx);
   #print "rate_max now: $rate_max\n";
   print "Adjusting cx min/max tx for concurrent test: ";

   for my $sta_name (sort(keys(%::sta_names))) {
      my $cx   = $::cx_names{$sta_name}->{"cx"};
      my $ep1  = $::cx_names{$sta_name}->{"ep1"};
      my $ep2  = $::cx_names{$sta_name}->{"ep2"};

      #print "UPLOAD: ".$::utils->fmt_cmd("set_endp_tx_bounds", $ep1, "$rate_min", "$rate_max")."\n";
      #print "UPLOAD: ".$::utils->fmt_cmd("set_endp_tx_bounds", $ep2, "$no_rate", "$no_rate")."\n";

      $::utils->doCmd($::utils->fmt_cmd("set_endp_tx_bounds", $ep1, "$rate_min", "$rate_max"));
      $::utils->doCmd($::utils->fmt_cmd("set_endp_tx_bounds", $ep2, "$rate_min",  "$rate_max"));
      $::utils->doCmd($::utils->fmt_cmd("set_endp_quiesce",   $ep1, "$::quiesce_sec"));
      $::utils->doCmd($::utils->fmt_cmd("set_endp_quiesce",   $ep2, "$::quiesce_sec"));
   }
   for my $sta_name (sort(keys(%::sta_names))) {
      my $cx   = $::cx_names{$sta_name}->{"cx"};
      $::utils->doCmd($::utils->fmt_cmd("set_cx_state",       $::test_mgr, $cx, "RUNNING"));
      print " $cx...";
   }
   print "done.\n";
} # ~adjustForDuplex


# adjust the transmit rate up for endpoint 1, and down for endpoint 2
sub adjustForUpload {
   my $no_rate    = "+0";
   if (lc($::min_tx) eq "same" ) {
      die "--min_tx may not be 'same', please provide a number or formatted unit in K, M or G";
   }
   my $rate_min   = evalUnits($::min_tx);
   $::max_tx      = $::min_tx if (lc($::max_tx) eq "same" ) ;

   my $rate_max   =  evalUnits($::max_tx);

   print "Adjusting cx min/max tx for upload test: ";

   for my $sta_name (sort(keys(%::sta_names))) {
      my $cx   = $::cx_names{$sta_name}->{"cx"};
      my $ep1  = $::cx_names{$sta_name}->{"ep1"};
      my $ep2  = $::cx_names{$sta_name}->{"ep2"};

      #print "UPLOAD: ".fmt_cmd("set_endp_tx_bounds", $ep1, "$rate_min", "$rate_max")."\n";
      #print "UPLOAD: ".fmt_cmd("set_endp_tx_bounds", $ep2, "$no_rate", "$no_rate")."\n";

      $::utils->doCmd($::utils->fmt_cmd("set_endp_tx_bounds", $ep1, "$rate_min", "$rate_max"));
      $::utils->doCmd($::utils->fmt_cmd("set_endp_tx_bounds", $ep2, "$no_rate",  "$no_rate"));
      $::utils->doCmd($::utils->fmt_cmd("set_endp_quiesce",   $ep1, "$::quiesce_sec"));
      $::utils->doCmd($::utils->fmt_cmd("set_endp_quiesce",   $ep2, "$::quiesce_sec"));
   }
   for my $sta_name (sort(keys(%::sta_names))) {
      my $cx   = $::cx_names{$sta_name}->{"cx"};
      $::utils->doCmd($::utils->fmt_cmd("set_cx_state",       $::test_mgr, $cx, "RUNNING"));
      print " $cx...";
   }
   print "done.\n";
} # ~adjustForUpload


sub printShowEndpointStats {
   my $lines = shift;
   for my $line (split(/\n/, $lines)) {
      if ($line =~ m/RealRxRate:/) {
            my ($bps_rx) = ($line =~ m/RealRxRate: (\d+)bps /);

            if ($bps_rx >=1000000) {
               $bps_rx = ceil($bps_rx / 1000000)."M";
            }
            elsif ($bps_rx >= 1000) {
               $bps_rx = ceil($bps_rx / 1000)."K";
            }
            print "  ${bps_rx}bps";
      }
      if ($line =~ m/Tx Bytes:/) {
            my ($tx) = ($line =~ m/Total:\s+(\d+)/);
            if($tx >=(1024*1024)) {
               $tx = ceil($tx / (1024*1024))."M";
            }
            elsif ($tx >= 1024) {
               $tx = ceil($tx / 1024)."K";
            }
            print " / ${tx}B\t";
      }
   }
}

sub awaitTransfers {
   my $begin_time = time;
   my $end_time   = $begin_time + $::duration;
   my $lines;
   #my $print_nap = 3;
   my $passes = 0;

   for my $sta_name (sort(keys(%::sta_names))) {
      my $ep1  = $::cx_names{$sta_name}->{"ep1"};
      my $ep2  = $::cx_names{$sta_name}->{"ep2"};
      print "  $ep1  Rx-bps/Tx-B \t$ep2  Rx-bps/Tx-B |"
   }
   print "\n";
   while( time < $end_time ) {
      sleep $::poll_time;
      #if($passes == 0) {
         for my $sta_name (sort(keys(%::sta_names))) {
            my $cx   = $::cx_names{$sta_name}->{"cx"};
            my $ep1  = $::cx_names{$sta_name}->{"ep1"};
            my $ep2  = $::cx_names{$sta_name}->{"ep2"};

            $lines = $::utils->doAsyncCmd($::utils->fmt_cmd("nc_show_endpoints", "$ep1"), "\n");
            printShowEndpointStats($lines);
            $lines = $::utils->doAsyncCmd($::utils->fmt_cmd("nc_show_endpoints", "$ep2"), "\n");
            printShowEndpointStats($lines);
            print " |";
         }
         #$passes = $print_nap + 1;
         print "\n";
      #}
      #$passes--;
   }
} # ~awaitUploads

sub adjustForDownload {
   my $no_rate    = "+0";

   if (lc($::min_tx) eq "same" ) {
      die "--min_tx may not be 'same', please provide a number or formatted unit in K, M or G";
   }
   my $rate_min   = evalUnits($::min_tx);
   $::max_tx      = $::min_tx if (lc($::max_tx) eq "same" ) ;
   my $rate_max   = evalUnits($::max_tx);

   print "Adjusting tx_rate for download...";
   for my $sta_name (sort(keys(%::sta_names))) {
      my $ep1  = $::cx_names{$sta_name}->{"ep1"};
      my $ep2  = $::cx_names{$sta_name}->{"ep2"};

      #print "Download: ".fmt_cmd("set_endp_tx_bounds", $ep1, "$no_rate", "$no_rate")."\n";
      #print "Download: ".fmt_cmd("set_endp_tx_bounds", $ep2, "$rate_min", "$rate_max")."\n";

      $::utils->doCmd($::utils->fmt_cmd("set_endp_tx_bounds", $ep1, "$no_rate", "$no_rate"));
      $::utils->doCmd($::utils->fmt_cmd("set_endp_tx_bounds", $ep2, "$rate_min", "$rate_max"));
      $::utils->doCmd($::utils->fmt_cmd("set_endp_quiesce",   $ep1, "$::quiesce_sec"));
      $::utils->doCmd($::utils->fmt_cmd("set_endp_quiesce",   $ep2, "$::quiesce_sec"));
   }
   for my $sta_name (sort(keys(%::sta_names))) {
      my $cx   = $::cx_names{$sta_name}->{"cx"};
      $::utils->doCmd($::utils->fmt_cmd("set_cx_state",       $::test_mgr, $cx, "RUNNING"));
      print " $cx..."
   }
   print " done\n";
} # ~adjustForUpload

sub quiesceConnections {
  for my $sta_name (sort(keys(%::sta_names))) {
      my $cx   = $::cx_names{$sta_name}->{"cx"};
      $::utils->doCmd($::utils->fmt_cmd("set_cx_state", $::test_mgr, $cx, "QUIESCE"));
  }
}

sub resetCounters {
   for my $sta_name (sort(keys(%::sta_names))) {
      my $cx   = $::cx_names{$sta_name}->{"cx"};
      $::utils->doCmd("clear_cx_counters $cx");
   }
   $::utils->doCmd("clear_endp_counters all");
}

## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##
##    Create a virtual station and associate it with and SSID,
##    then pass traffic to and from it.
##
## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub doStep_1 {
   my $sta_name   = (sort(keys %::sta_names))[0];


   removeOldCrossConnects();
   sleep(2);
   removeOldStations();
   sleep(1);
   awaitStationRemoval();

   sleep 1;
   my $cmd;
   my %results1    = ();

   # make sure that ::num_station and ::sta_names is consistent

   if ($::num_stations != (keys %::sta_names)) {
      die "Unexpected difference between number of station names and num_stations, did num_stations not get set?";
   }

   # create stations
   print " Creating new stations: ";
   my $i = 0;
   for $sta_name (sort(keys %::sta_names)) {
      # sta, ip, rh, $ip_addr
      print " $sta_name ";
      new_wifi_station( $sta_name, $::sta_names{$sta_name}, \%results1, $::wifi_mode, $i);
      altsleep(0.12);
      altsleep(0.6) if (($i % 5) == 0);
      $i++;
   }
   sleep(1);
   #print "**************************************************\n";
   foreach my $sta_name (sort(keys %::sta_names)) {
      my $status = $::utils->doAsyncCmd($::utils->fmt_cmd("nc_show_port", 1, $::resource, $sta_name));
   }
   sleep(1);
   #print "**************************************************\n";

   print " Created $::num_stations stations\n";
   sleep(1);

   my $new_sta_count    = keys %results1;
   my $found_stations   = 0;
   awaitNewStations();
   sleep 1;

   # we create a pair of connection endpoints and
   # a cross-connect between them for every station
   createEndpointPairs();
   sleep 5;

   if ($::traffic_type eq "separate") {
      adjustForUpload();
      print " started uploads.\n";
      awaitTransfers();
      quiesceConnections();
      sleep 1+$::quiesce_sec; # the STOPPED signal might report short on packets because
               # there might be queued packets in the backlog. If you need
               # more precise readings, use the QUIESCE command which waits
               # a specified number of seconds for all connections to close

      showEndpoints();
      resetCounters();
      # adjust the transmit rate down for endpoint 1, and up for endpoint 2
      adjustForDownload();
      print "\nStarted download...\n";
      awaitTransfers();
   }
   elsif ($::traffic_type eq "concurrent") {
      adjustForSimultaneous();
      print "\nStarted concurrent traffic...\n";
      awaitTransfers();
   }
   else {
      print "Unkown traffic_type $::traffic_type, exiting.\n";
      exit(1);
   }
   quiesceConnections();
   sleep 1+$::quiesce_sec;
   showEndpoints();
} # ~step1


## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##
##    Create a series of stations and associate them to
##    the SSID. Then disassociate them.
##
## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub doStep_2 {
   my %results2      = ();
   # delete previous stations
   print "Removing old stations...";
   for my $sta_name (sort(keys %::sta_names)) {
      # if we have a port eid for this station, let's delete the port so we can start fresh
      my $del_cmd = $::utils->fmt_cmd("rm_vlan", 1, $::resource, $sta_name);
      print "$sta_name " unless($::utils->isQuiet());
      $::utils->doCmd($del_cmd);
   }
   # poll until they are gone
   my $old_sta_count = (keys(%::sta_names));
   while( $old_sta_count > 0 ) {
      $old_sta_count = (keys(%::sta_names));
      sleep 1;
      for my $sta_name (sort(keys %::sta_names)) {
         my $status = $::utils->doAsyncCmd($::utils->fmt_cmd("show_port", 1, $::resource, $sta_name));
         #print ">>status>>$status\n";
         $old_sta_count-- if( $status =~ /Could not find/); # ??
      }
   }
   print "Old stations removed.\n";
   print "Creating new stations...";

   # create new stations
   my $i = 0;
   for my $sta_name (sort(keys %::sta_names)) {
      die("misconfiguration! ") if( ref($sta_name) eq "HASH");
      my $ip = $::sta_names{$sta_name};
      print "$sta_name " unless($::utils->isQuiet());
      new_wifi_station( $sta_name, $ip, \%results2, $::wifi_mode, $i);
      $i++;

      # Uncomment to diagnose connection results. The IPs assigned
      # are unlikely to appear instantly, but the mac and entity id
      # used internally by LANforge will be set.
      #my $ra_data   = $results{$sta_name}};
      #my $mac       = $results{$sta_name}[0];
      #my $eid       = $results{$sta_name}[1];
      #print "created $sta_name, mac $mac, EID: $eid\n";
      #print "CMD: ".$results{$sta_name}[2]."\n\n";
   }
   sleep 1;
   my $num_stations = (keys %::sta_names);
   print "Created $num_stations stations.\nPolling for association: ";
   # we can view IP assignment as well as station association
   my $num_assoc     = 0;
   my $num_ip        = 0;
   my $begin_time    = time;
   my %assoc_state   = ();
   for my $sta_name (sort(keys %::sta_names)) {
      $assoc_state{$sta_name} = {};
   }
   my $port;

   #while($num_ip < $num_stations) { # if we just cared about IPs

   while($num_assoc < $num_stations) {
      sleep 1;
      $num_assoc     = 0;
      $num_ip        = 0;
      for my $sta_name (sort(keys %::sta_names)) {
         my $status  =  $::utils->doAsyncCmd($::utils->fmt_cmd("show_port", 1, $::resource, $sta_name));
         my %state   = get_sta_state(\$status);
         #print $state{"name"}.": ".$state{"assoc"}." ";
         $num_assoc++ if( $state{"assoc"} !~ /NA|Not-Associated|unknown/);
         #print $state{"ip"}."/".$state{"mask"}." gw:".$state{"gw"}."\n";
         $num_ip++ if($state{"ip"} ne "0.0.0.0" );
      }

      print "$num_assoc stations associated, $num_ip stations with IPs\n";
   }
   my $end_time      = time;
   my $delta         = $end_time - $begin_time;

   print "Association took about $delta seconds\n";
   print "Bringing those stations down now: ";
   for my $sta_name (keys %::sta_names) {
      my $cmd = fmt_port_down($::resource, $sta_name, "0.0.0.0", "0.0.0.0"); #$::netmask
      $::utils->doCmd($cmd);
      print "$sta_name " unless ($::utils->isQuiet());
   }
   print "...stations down. Done.\n"
}
## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##
##    Create a station
##
## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub doAdd {
   # create virtual station
   #print "## doAdd: sta_wiphy[$::sta_wiphy]\n";
   if ($::num_stations > 0 && defined $::sta_wiphy) {
      my %results2 = ();
      print "creating stations:";
      my $i = 0;
      for my $sta_name (sort(keys %::sta_names)) {
         die("misconfiguration! ") if( ref($sta_name) eq "HASH");
         my $ip = $::sta_names{$sta_name};
         print " $sta_name";
         new_wifi_station( $sta_name, $ip, \%results2, $::wifi_mode, $i);
         if (($i % 10) == 9) {
            $::utils->sleep_ms(120);
         }
         else {
            $::utils->sleep_ms(30);
         }
         $i++;
      }
      print " done\n";
   }
   elsif (defined $::sta_wiphy) {
      print "Creating virtual radio: $::sta_wiphy.\n";
      new_wifi_radio();
   }
   else {
      print "Please define a radio with --radio\n";
      exit(1);
   }
}# doAdd

sub doDelWiphyVdevs {
   if (defined $::port_del) {
      # List ports on the resource in question, delete anything that has port_del for
      # a parent.
      my $q;
      for ($q = 0; $q < 5; $q++) {
        my @ports = $::utils->getPortListing(1, $::resource);
        my $found = 0;
        my $i;
        for ($i = 0; $i<@ports; $i++) {
          my $dev = $ports[$i]->dev();
          my $parent = $ports[$i]->parent();
          if ($parent eq $::port_del) {
            print "deleting port $dev\n" unless($::utils->isQuiet());
            $::utils->doCmd($::utils->fmt_cmd("rm_vlan", 1, $::resource, $dev));
            $found++;
          }
        }

        if ($found == 0) {
          last;
        }
        sleep(10);
      }
   }
}

sub doDel {
   if (defined $::port_del) {
      #delete any port listed
      delete_port();
   }
}# doDel

sub ip2ipn {
     return unpack 'N', inet_aton(shift);
}
sub ipn2ip {
    return inet_ntoa( pack 'N', shift );
}

sub initStationAddr {
   die("Zero stations cannot be very useful, bye.") if ($::num_stations < 1);
   if ($::num_stations > 200 ) {
      println("Over 200 stations is unlikely to work on one machine, expect over-subscription behavior.");
      sleep 2;
   }

   my $ip;
   my $ip_obj;
   if ($::first_ip =~ /^DHCP/){
      $ip   = $::first_ip;
   }
   else {
      $ip   = $::first_ip;
   }

   # often people create own stations at sta0 or sta1 and
   # those are really hard to sort in the Ports Tab. We shall
   # start with sta100 by default. Separate the numeric suffix
   # use that as offset
   my $offset = 100;
   if ($::first_sta =~ /^.*?(\d+)\s*$/) {
      $offset = $1;
   }
   for( my $i=0; $i < $::num_stations ; $i++ ) {
      my $suffix     = 0 + $i + $offset;
      my $name;
      if ($i == 0) {
        $name = $::first_sta;
      }
      else {
        $name       = sprintf("sta%03d",    $suffix);
      }
      my $ep_name1   = sprintf("ep-A%03d",   $suffix);
      my $ep_name2   = sprintf("ep-B%03d",   $suffix);
      my $cx_name    = sprintf("cx-%03d",    $suffix);

      if ($ip ne 'DHCP' && $i > 0) {
         my $val = ip2ipn($ip);
         #print "ip[$ip] to int[$val]\n";
         $ip = ipn2ip( 1 + $val);
         #print "ip[$ip] from int[".(1+$val)."]\n";
      }

      $::sta_names{$name}  = $ip;
      $::cx_names{$name}   = {
         ep1   => $ep_name1,
         ep2   => $ep_name2,
         cx    => $cx_name
      };
   }
} # ~initStationAddr

## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##
##    Set phy channel, antennas
##
## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub set_channel {
    my $res = shift;
    my $phy = shift;
    my $chan = shift;

    die("set_channel: unset resource") unless ((defined $res) && ("" ne $res));
    die("set_channel: unset radio") unless ((defined $phy) && ("" ne $phy));
    die("set_channel: unset channel") unless ((defined $chan) && ("" ne $chan));

    my $mode = 'NA';
    my $cmd = $::utils->fmt_cmd("set_wifi_radio", 1, $res,
                                 $phy,
                                 $mode,
                                 $chan);
    $::utils->doAsyncCmd($cmd);
    sleep 1;
}

sub set_antenna {
  my $res = shift;
  my $phy = shift;
  my $ant = shift;
  die("set_channel: unset resource") unless ((defined $res) && ("" ne $res));
  die("set_channel: unset radio") unless ((defined $phy) && ("" ne $phy));
  die("Antenna mode [$ant] does not exist.")
    if (! exists $::antenna_table{$ant});
  my $mode = 'NA';
  my $chan = $::phy_channel;
  if ($chan eq "") {
     $chan = "NA";
  }
  my $country = 'NA';
  my $freq = 'NA'; #'0xFFFF' will override channel
  my $frag = 'NA';
  my $rate = 'NA';
  my $rts = 'NA';
  my $txpower = 'NA';
  my $mac = 'NA';

  my $antenna = $::antenna_table{$ant};
  #print "ANTENNA: $ant -> $antenna\n";
  my $cmd = $::utils->fmt_cmd("set_wifi_radio", 1, $::resource,
                               $phy,
                               $mode,
                               $chan,
                               $country,
                               $freq,
                               $frag,
                               $rate,
                               $rts,
                               $txpower,
                               $mac,
                               $antenna);
  $::utils->doAsyncCmd($cmd);
  sleep 1;
}



## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##
##                         M A I N
##
## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

my $help;

if (@ARGV < 2) {
   print $usage;
   exit 0;
}
GetOptions
(
  'mgr|m=s'                   => \$::lfmgr_host,
  'lf_mgr_port|lf_port|mgr_port|p=i' => \$lfmgr_port,
  'resource|r=i'              => \$::resource,
  'resource2|r2=i'            => \$::resource2,
  'quiet|q=s'                 => \$::quiet,
  'radio|o=s'                 => \$::sta_wiphy,
  'channel|chan=i'            => \$::phy_channel,
  'antenna|ant=s'             => \$::phy_antenna,
  'ssid|s=s'                  => \$::ssid,
  'security=s'                => \$::security,
  'xsec=s'                    => \$::xsec,
  'passphrase|password|pass|h=s' => \$::passphrase,
  'first_ip|b=s'              => \$::first_ip,
  'first_sta|c=s'             => \$::first_sta,
  'num_stations|num_sta|n=i'  => \$::num_stations,
  'netmask|k=s'               => \$::netmask,
  'gateway|g=s'               => \$::gateway,
  'change_mac=i'              => \$::change_mac,
  'mac-pattern|mac_pattern=s' => \$::mac_pattern,
  'cxtype|x=s'                => \$::cx_type,
  'bps_min|bps-min|y=s'       => \$::min_tx,
  'bps_max|bps-max|z=s'       => \$::max_tx,
  'duration|e=i'              => \$::duration,
  'upstream|t=s'              => \$::upstream_port,
  'action|a=s'                => \$action,
  'db_preload=s'              => \$::db_preload,
  'db_save=s'                 => \$::db_save,
  'db_postload=s'             => \$::db_postload,
  'poll_time|poll-time=i'     => \$::poll_time,
  'wifi_mode|mode=s'          => \$::wifi_mode,
  'bssid=s'                   => \$::bssid,
  'traffic_type=s'            => \$::traffic_type,
  'vrad_chan=i'               => \$::vrad_chan,
  'port_del=s'                => \$::port_del,
  'admin_down_on_add'         => \$::admin_down_on_add,
  'ieee80211w=s'              => \$::ieee80211w,
  'log_cli=s{0,1}'            => \$log_cli, # use ENV{LOG_CLI} elsewhere
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

# Configure our utils.
our $utils = new LANforge::Utils();
print "Connecting to $lfmgr_host, $lfmgr_port\n";
$::utils->connect($lfmgr_host, $lfmgr_port);

if ($db_postload ne "" && db_exists($::db_postload)==0) {
   print("Scenario [$::db_postload] does not exist. Please create it first.");
   exit(1);
}

if ($::db_preload ne "") {
   if(db_exists($::db_preload)==1) {
      print "Loading scenario $::db_preload...";
      load_db($::db_preload);
      print " done\n";
   }
   else {
      print("Scenario [$::db_postload] does not exist. Please create it first.");
      exit(1);
   }
}

if (!($action =~ /del/)) { # Below steps are unrelated to deleting objects
   if(!defined $::first_ip || $::first_ip eq '') {
      print("Please specify the first IP for stations. You may choose DHCP, DHCP6, or DHCP,DHCP6 or an IP that will be incremented.\n");
      exit(1);
   }

   if(! $::ssid ) {
      print("Please configure SSID for stations to associate with.\n");
      exit(1);
   }
   if(! $::sta_wiphy ) {
      print("Please specify the base radio port for the wifi stations. ".$usage );
      exit(1);
   }
}

if(! $action ) {
   print("Please specify which test action we want:
   step1: connect one station and pass upload and download traffic
   step2: connect 10 wifi stations and disconnect.
   add: create virtual radio.\n
   del: Delete virtual radio.\n");
   exit(1);
}

if (!($action =~ /del/)) { # Below steps are unrelated to deleting objects
   if(0 == keys(%::sta_names)) {
      initStationAddr();
   }
   if(! %sta_names ) {
      print("Please configure station list to test with.\n");
      exit(1);
   }
}

if ($action =~ /step|add/) {
  if ($::phy_channel ne "") {
    set_channel($::resource, $::sta_wiphy, $::phy_channel);
  }
  if ($::phy_antenna ne "") {
    set_antenna($::resource, $::sta_wiphy, $::phy_antenna);
  }
}

# take first station and associate it or fail
if ($action eq "step1" ) {
   if ($traffic_type !~ /^(concurrent|separate)$/ ) {
      print("Please specify concurrent or separate as traffic_type.\n");
      exit(1);
   }
   doStep_1(%sta_names, $::ssid, $sta_wiphy);
   if ($db_save ne "") {
      save_db($::db_save);
   }
   if ($::db_postload ne "") {
      load_db($::db_postload);
   }

}
elsif( $action eq "step2" ) {
   doStep_2(%sta_names, $::ssid, $sta_wiphy);
   if ($::db_postload ne "") {
      load_db($::db_preload);
   }
}
elsif ($action eq "add" ) {
   doAdd();
   if ($::db_postload ne "") {
      load_db($::db_preload);
   }
}
elsif ($action eq "del" ) {
   doDel();
   if ($::db_postload ne "") {
      load_db($::db_preload);
   }
}
elsif ($action eq "del_all_phy" ) {
   doDelWiphyVdevs();
   if ($::db_postload ne "") {
      load_db($::db_preload);
   }
}
elsif ($action eq "show_port") {
   print $::utils->doAsyncCmd($::utils->fmt_cmd("nc_show_port", 1, $resource, (sort(keys %sta_names))[0])) . "\n";
}

exit(0);
