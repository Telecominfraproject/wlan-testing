#!/usr/bin/perl -w
#
# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# This script sets up connections of types:
# lf, lf_udp, lf_tcp, custom_ether, custom_udp, custom_tcp, l4 (http, https, ftp and fileIO)
# across real ports and MACVLAN ports on one or more machines.
# It then continously starts and stops the connections.
package main;
$| = 1; # Un-buffer output

use strict;
use warnings;
use Carp;
use Net::Telnet ();
$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
use Scalar::Util; #::looks_like_number;
use lib '/home/lanforge/scripts'; # this is pedantic necessity for the following use statements
use LANforge::Port;
use LANforge::Utils;
use LANforge::Endpoint;
use Net::Telnet ();
use Net::Ping;
use Getopt::Long;
use Time::HiRes ('sleep');
use Socket;

use POSIX;
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##       package variables below
use constant   NL    => "\n";
use constant   NA    => "NA";
use constant   AUTO  => "AUTO";
use constant   READ  => "read";
use constant   WRITE => "write";

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
our $report_timer    = 8000;       # Set report timer for all tests created in ms, i.e. 8 seconds
our $lfmgr_host      = undef;
our $lfmgr_port      = 4001;
our $resource        = 1;
our $quiet           = 1;
our $group           = undef;
our $tmp_group       = undef;
our $tmp_group_min   = 0;
our $tmp_group_max   = 0;
our $action          = undef;
our $nfs_mnt         = undef;
our $nfs_list        = undef;
our $local_mnt       = AUTO;
our $first_mvlan_ip  = undef; #"10.26.1.10";
our $netmask         = "255.255.255.0";
our $parent_port     = undef;
our $utils           = undef;
our $shelf_num       = 1;
our $DEBUG           = 0;
our $sleep_after_wo  = 15; # Second to sleep after starting writers (before starting readers)
our $D_PAUSE         = 3;

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# File-IO configuration constants
our $quiesce_after_files = 0;
our $min_rw_size     = "512";
our $max_rw_size     = "65536";
our $use_crc         = "yes";
our $min_read_bps    = "1000000"; # 1Mbps
our $max_read_bps    = "2000000"; # 2Mbps
our $num_files       = 2;
our $min_file_size   = 1024 * 1024;
our $max_file_size   = 1024 * 1024 * 2;
our $min_write_bps   = "3000000"; # 3Mbps
our $max_write_bps   = "4000000"; # 4Mbps
our $mount_options   = "NONE";
our $skip_writers    = 0;
our $skip_readers    = 0;

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# below are sorted names and associated endpoints
# the third argument can be used as the default parent
# port for the mac-vlans for that group
our %group_names     = (
   #"group1"  => [   1,    20, 'eth1'],
   #"group2"  => [  21,    40, 'eth1'],
   #"group3"  => [  41,    60, 'eth1'],
   #"group4"  => [  1,    1, 'eth1'],
   #"group5"  => [  2,    2, 'eth1']
);
our $fast_forward_ep = 0;  # set this to 1 to leave exiting file endpoints alone
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
our %mnt_map         = ();
our %file_endpoints  = ();
our %cross_connects  = ();
our %test_groups     = ();
our %all_file_ep     = ();
our %mac_vlans       = ();
our %vlan_ips        = ();

# These are set based on group chosen.
our $qty_mac_vlans   = 0;
our $start           = 0; # First idx, inclusive
our $stop            = 0; # Last idx

sub ipSummary {
   my $first;
   if((!defined $::first_mvlan_ip ) || ("$::first_mvlan_ip" eq "")) {
      $first      = "0.0.0.0";
   }
   else {
      $first      = $::first_mvlan_ip;
   }
   my $linestart  = "                                             # ";
   my $summary    = NL;
   for my $name (sort keys %::group_names) {
      $summary .= $linestart.$name.": ";
      my $a = addrtoint( $first ) + $::group_names{ $name }->[0] -1;
      my $b = addrtoint( $first ) + $::group_names{ $name }->[1] -1;
      $summary .= inttoaddr( $a )." - ".inttoaddr( $b ).NL;
   }
   return $summary;
}

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##                   Usage                                        ==
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
my $first = ($::first_mvlan_ip) ? $::first_mvlan_ip : "0.0.0.0";

my $usage = "$0   [--mgr               {host-name | IP}]
                  [--mgr_port          {ip port ($lfmgr_port)}]
                  [--resource          {resource ($resource)}]
                  [--nfs_mnt           {[IP|host-name]:/path}]
                     # 192.168.1.1:/foo
                     # filehost:/home/fileio
                  [--nfs_list          {local file}]\t# list of nfs mountpoints
                     # Will be modulo distributed among groups mac vlans
                     # Obviates --nfs_mnt; examples:
                     #     --nfs_list ./my-list-of-mounts
                     #     --nfs_list /tmp/mnt-list
                     # File format:
                     #     10.20.30.40:/a/b/c
                     #     filehost:/z/y
                  [--parent_port       {parent eth port}]\t# parent of mac vlans
                  [--first-mvlan-ip    {ip ($first)}]\t# mvlan ips: ".ipSummary()."
                  [--netmask {mask ($netmask)}]\t#mac-vlan netmask
                  [--action      {list_groups|run_group|stop_group|del_group}]
                     # list_groups: list test groups
                     # run_group:   assemble and start writer then reader group
                     # stop_group:  quiece writer then reader group
                     # del_group:   delete reader then writer file endpoints
                  [--group          {name}] # test group base name, creates:
                     # <group>_wo for writers and
                     # <group>_ro for readers
                  [--min_rw_size    ($min_rw_size)]\t# in bytes
                  [--max_rw_size    ($max_rw_size)]\t# in bytes
                  [--use_crc        {yes|no}]
                  [--min_read_bps   ($min_read_bps)]\t# in bps, 2000000 = 1Mbps
                  [--max_read_bps   ($max_read_bps)]\t# in bps, 2000000 = 2Mbps
                  [--num_files      ($num_files)]\t# files per writer
                  [--quiesce_after_files ($quiesce_after_files)]\t# files to read/write before stopping test.
                          O == infinite (default)

                  [--skip_readers   ($skip_readers)]\t# Should we not create reader connections: 0 | 1
                  [--skip_writers   ($skip_readers)]\t# Should we not create writer connections: 0 | 1
                  [--min_file_size  ($min_file_size)]\t# in bytes
                  [--max_file_size  ($max_file_size)]\t# in bytes
                  [--min_write_bps  ($min_write_bps)]\t# in bps, 3000000 = 3Mbps
                  [--max_write_bps  ($max_write_bps)]\t# in bps, 4000000 = 4Mbps
                  [--mount_options  ($mount_options)]\t# as per nfs(1)
                  [--tmp_group      {name}]\t# for specifying ad-hoc group, you will see group <name>
                  [--min            1-n]\t first macvlan in tmp group
                  [--max            1-n]\t last macvlan in tmp group

Examples:
 $0 --mgr 10.0.0.1 --resource 1 --action list_groups

 $0 --mgr 10.0.0.1 --resource 1 --action run_group --group group1 \\
         --parent_port eth2 --netmask 255.255.0.0 \\
         --nfs_mnt 192.168.99.99:/fire

 $0 --mgr 10.0.0.1 --resource 1 \\
         --action stop_group --group group1

 $0 --mgr 10.0.0.1 --resource 1 \\
         --action del_group --group group1

 $0 --mgr 10.0.0.1 --resource 1 \\
         --action run_group --group group2 --parent_port eth9 \\
         --first_mvlan_ip 172.168.90.1 --netmask 255.255.0.0 \\
         --nfs_list ./nfsexports.txt  \\
         --num_files 20 --min_file_size 4096 --max_file_size 524288 \\ 
         --min_write_bps 1000000 --max_write 900000000

$0 --mgr 10.0.0.1 --resource 1 \\
         --action run_group --group group1 \\
         --nfs_mnt 192.168.99.99:/fire \\
         --mount_options sync,hard,timeo=120,retrans=4

$0 --mgr 10.0.0.1 --resource 1 --action run_group \\
         --tmp_group lag1 --min 1 --max 2 --parent_port eth1 \\
         --first_mvlan_ip 10.30.0.10 \\
         --nfs_mnt 10.30.0.1:/tmp

$0 --mgr 10.0.0.1 --resource 1 \\
         --action stop_group --tmp_group lag1 --min 1 --max 2 --parent_port eth1
";

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    ip_to_a/a_to_ip
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub addrtoint {
   return( unpack( "N", pack( "C4", split( /[.]/,$_[0]) ) ) );
};
sub inttoaddr {
   return( join( ".", unpack( "C4", pack( "N", $_[0] ) ) ) );
};


## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    Open connection to the LANforge server, configure our utils.
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub init {
   my $conn = new Net::Telnet(Timeout => 20,
                              Prompt => '/default\@btbits\>\>/');
   $conn->open(Host    => $::lfmgr_host,
               Port    => $::lfmgr_port,
               Timeout => 10);

   $conn->waitfor("/btbits\>\>/");
   $conn->max_buffer_length(1024 * 1024 * 10);  # 10M buffer

   $::utils = new LANforge::Utils();
   $::utils->connect($lfmgr_host, $lfmgr_port);

   if ($::group && $::group ne "") {
      my $ra_bounds  = $::group_names{ $::group };
      $::start       = @$ra_bounds[0];
      $::stop        = @$ra_bounds[1];

      $::qty_mac_vlans = ($::stop - $::start) + 1;
      print "group [$group] vlans: $::stop - $::start = $::qty_mac_vlans\n" if($::DEBUG);
   }
}

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
## set a port or mvlan up or down
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub fmt_port_up_down {
   my ($resource, $port_id, $state) = @_;

   my $cur_flags        = 0;
   if ($state eq "down") {
      $cur_flags        |= 0x1;       # port down
   }

   # Specify the interest flags so LANforge knows which flag bits to pay attention to.
   my $ist_flags        = 0;
   $ist_flags           |= 0x2;       # check current flags
   $ist_flags           |= 0x800000;  # port down

   my $cmd = $::utils->fmt_cmd("set_port", 1, $resource, $port_id, NA,
                    NA, NA, NA, "$cur_flags",
                    NA, NA, NA, NA, "$ist_flags");
   return $cmd;
} # ~port up/down


## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    Create mac_vlans if they do not exist.
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub preparePorts {
   do_err_exit("First mac vlan IP is not set. Please set --first_mvlan_ip.")
      unless ((defined $::first_mvlan_ip) && ("$::first_mvlan_ip" ne ""));

   do_err_exit( "preparePorts: Unnamed parent port. Please set \$parent_port")
      unless((defined $::parent_port) && ("$::parent_port" ne ""));

   my $sleep_after                  = 0;
   my %all_ports                    = ();
   # build list of MAC VLANS
   print "shelf_num $::shelf_num, resource $::resource\n" if ($::DEBUG);
   my @ports                        = $::utils->getPortListing( 1, $::resource +0);

   for my $rh_port (@ports) {
      print "added port $rh_port->{'dev'}".NL if($::DEBUG);
      $all_ports{ $rh_port->{'dev'} } = $rh_port;
      next unless ( $rh_port->{'dev'} eq $::parent_port );
   }
   do_err_exit("preparePorts: Failed to populate ports list, please debug.")
      unless (keys %all_ports > 0);

   my $i;
   my %new_items                    = ();
   my $ra_bounds                    = $::group_names{ $group };
   my $start_str                    = $::first_mvlan_ip;
   my $start_int                    = addrtoint($start_str);
   my $next_ip;

   if (($::qty_mac_vlans + $::start) < 1) {
      do_err_exit("preparePorts: expects a positive, non-zero number of mvlans to create. Cannot continue.");
   }

   for ($i = 0 + $::start; $i < $::qty_mac_vlans + $::start; $i++) {
      my $devname                   = $::parent_port."#".$i;
      print "start_str[$start_str] start_int[$start_int] i[$i]\n" if ($::DEBUG);
      my $next_ip                   = inttoaddr( $start_int + $i -1);
      print "next_ip[$next_ip]\n" if ($::DEBUG);
      $::vlan_ips{ $devname }       = $next_ip;
      $::mac_vlans{ $devname }      = 0;
      if ( defined $all_ports{ $devname }) {
         $::mac_vlans{ $devname }   = 1;
      }
      else { # create mac_vlan
         my $mac_addr               = mac();
         my $cmd = $::utils->fmt_cmd( "add_mvlan", $::shelf_num,
                                    $::resource, $::parent_port, $mac_addr, $i);
         print " + ".$cmd.NL if ($::DEBUG);
         $::utils->doCmd($cmd);
         sleep(0.1);
      }
      $new_items{ $devname }        = 1;
      $sleep_after++;
   } #~for

   if ( keys %new_items > 0 ) {
      print "Creating ".(keys %new_items)." new ports:...";

      # set the port IP
      for my $new_item (keys(%new_items)) {
         my $ip            = $::vlan_ips{ $new_item };
         my $cmd_flags     = 0x0;
         my $current       = 0x0;
         my $interesting   = 0x0 | 0x4 | 0x8;

         my $cmd = $::utils->fmt_cmd("set_port",
            $::shelf_num, $::resource, $new_item, $ip,
            $::netmask, NA, $cmd_flags, $current, NA,
            NA, NA, NA, $interesting,
            NA, NA, NA, NA, NA, NA, NA, NA, NA, NA,
            NA, NA, NA, NA, NA, NA, NA);

         if ($::DEBUG) {
            print NL." $new_item $ip: $cmd ";
         }
         else {
            print ".";
         }
         $::utils->doCmd($cmd);
         sleep(0.1);
         $sleep_after++;

         my @ports = $::utils->getPortListing($::shelf_num, $::resource);
         for my $rh_port (@ports) {
            $::all_ports{ $rh_port->{'dev'} } = $rh_port; #reset ports
         }
      }
      print NL."Created ".(keys %new_items)." new mac vlans".NL;
   }
   if ($sleep_after > 10) {
     $sleep_after = $sleep_after / 2;
   }   
   
   if ($sleep_after) {
     print "\nSleeping: $sleep_after seconds to allow ports to be created and configured.\n";
     for $i (1..$sleep_after) { sleep(1); print "."; }
     print NL;
   }
   # check that the port is up by trying to run a ping from it
   if ( defined $::nfs_mnt && "$::nfs_mnt" ne "") {
      my ($nfs_name) = split(/:/, $::nfs_mnt );
      print "Emitting one ping from each mvlan reduces failed mounts:";

      foreach my $name (reverse sort keys %new_items) {
         my $rh_p    = $::all_ports{ $name };
         my $ip      = $rh_p->{'ip_addr'};
         #my $ping    = "ping -n -c1 -w1 -W1 -I $ip $nfs_name";
         print "ping $ip".NL if ($::DEBUG);
         my $ping = Net::Ping->new('tcp', 1);
         $ping->bind($ip);
         $ping->port_number(scalar(getservbyname("nfs", "tcp")));
         my $counter = 5;
         while( $counter > 0 ) {
            if ($ping->ping($nfs_name)) {
               print ".";
               $counter = 0;
            }
            else {
               print "$nfs_name did not ack nfs packet from $ip".NL;
               $counter --;
               sleep(0.2);
            }
         }
         $ping->close();
         undef($ping);
         #$ping->close();
      }
   }
   print NL;

} # ~preparePorts

sub notBlank {
   my ($name, $value) = @_;
   if((!defined $name) || ("$name" eq "")) {
      print "Name itself is blank, value[$value]".NL;
   }
   if((!defined $value) || ("$value" eq "")) {
      print "Value of $name is blank".NL;
   }
   #die if($::DEBUG);
}

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    prepareFileEndp - creates requested file endpoints if they do not exist,
##    creates implied FIO endpoints if they dont exist and adds endpoints
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub prepareFileEndpoints {
   do_err_exit("prepareFileEndpoints: Unnamed parent port. Please set \$parent_port")
      unless((defined $::parent_port) && ("$::parent_port" ne ""));

   do_err_exit("prepareFileEndpoints: Blank all_ports array. Please run preparePorts() first.")
      unless( keys %::all_ports > 1 );

   do_err_exit("prepareFileEndpoints: Blank mac_vlans array. Please run preparePorts() first.")
      unless( keys %::mac_vlans > 0 );

   if((defined $::nfs_list) && ("$::nfs_list" ne "")) {
      if((keys %::mnt_map) < 1) {
         do_err_exit("prepareFileEndpoints: empty --nfs_list. Provide mountpoints in [$::nfs_list]");
      }
   }
   elsif((! defined $::nfs_mnt) || ("$::nfs_mnt" eq "")) {
      do_err_exit("prepareFileEndpoints: undefined --nfs_mnt. Please specify --nfs_mnt first");
   }

   my %all_file_endpoints  = ();
   my %all_cross_connects  = ();
   my %endpoints_mvlans    = ();
   my @new_file_endpoints  = ();
   my @new_cross_connects  = ();

   my $ep_name             = undef;
   for my $grp (sort(keys %::group_names)) {
      my $ra_bounds = $::group_names{ $grp };
      print "skip_writers[$::skip_writers] skip_readers[$::skip_readers]" if ($::DEBUG);
      sleep(3) if($::DEBUG);

      for my $i (@$ra_bounds[0]..@$ra_bounds[1]) {
         if (! $::skip_writers) {
            $ep_name                         = $grp ."_wo_".sprintf( "%03d", $i);
            $all_file_endpoints{ $ep_name }  = 0;
            $endpoints_mvlans{   $ep_name }  = $::parent_port."#".$i;
            $all_cross_connects{ $ep_name }  = 0;
         }

         if (! $::skip_readers) {
            $ep_name                         = $grp ."_ro_".sprintf( "%03d", $i);
            $all_file_endpoints{ $ep_name }  = 0;
            $endpoints_mvlans{   $ep_name }  = $::parent_port."#".$i;
            $all_cross_connects{ $ep_name }  = 0;
         }
      }
   }

   print NL."Reading endpoints...";
   my $endpoint_str = $::utils->doCmd("nc_show_endpoints all all");
   my @endpoint_lines = split(/\n/, $endpoint_str);

   if ($::fast_forward_ep) {
      for my $line (@endpoint_lines) {
         $line =~ m/Endpoint \[(.*?)\]/; # proves this ep exists
         next if(! $1);
         $all_file_endpoints{ $1 } = 1;
      }
   }
   for my $ep_name (sort(keys %all_file_endpoints)) {
      print " $ep_name [".$all_file_endpoints{$ep_name}."] " if ($::DEBUG);
      if ($all_file_endpoints{$ep_name} == 0 ){
         my $begins = $::group."_";
         if( $ep_name =~ /^$begins/ ){
            push( @new_file_endpoints, $ep_name );
         }
      }
   }
   # assert we have sufficient remote_mnt entries
   for my $ep_name (@new_file_endpoints) {
      my $mvlan         = $endpoints_mvlans{ $ep_name };
      my $remote_mnt    = $::mnt_map{ $mvlan };
      notBlank( $mvlan, $remote_mnt );
   }

   if (@new_file_endpoints > 0) {
      print "Creating ".@new_file_endpoints." new file endpoints...";
      my $endpoint_type = "lf";
      my $ip_port       = "-1";
      my $bursty        = "no";
      my $rand_pkt_sz   = "no";
      my $remote_mnt    = undef;

      for my $ep_name (@new_file_endpoints) {
         my $mvlan            = $endpoints_mvlans{ $ep_name };
         $remote_mnt          = $::mnt_map{ $mvlan };

         my $read_write       = ($ep_name =~ /_ro_/)? READ : WRITE;
         my $rw_prefix        = $ep_name;
         $rw_prefix           =~ s/_ro_/_wo_/;
         my $prefix           = ($read_write eq WRITE) ? AUTO  : $rw_prefix;
         my $directory        = ($read_write eq WRITE) ? AUTO  : '/mnt/lf/'.$rw_prefix;
         my $min_write_rt     = ($read_write eq READ ) ? "0"   : $::min_write_bps;
         my $max_write_rt     = ($read_write eq READ ) ? "0"   : $::max_write_bps;
         my $min_read_rt      = ($read_write eq WRITE ) ? "0"   : $::min_read_bps;
         my $max_read_rt      = ($read_write eq WRITE ) ? "0"   : $::max_read_bps;
         my $pattern          = "increasing"; #($read_write eq "read" ) ? NA              : "increasing";
         my $mount_retry_nap  = 3500;
         my $mount_dir        = "NA";

         # we do not want anything 'blank' in this
         my @names=qw(ep_name ::shelf_num ::resource mvlan min_read_rt max_read_rt  min_write_rt max_write_rt pattern directory prefix remote_mnt mount_options mount_dir mount_retry_nap);

         my @values=($ep_name, $::shelf_num, $::resource, $mvlan, $min_read_rt, $max_read_rt,  $min_write_rt, $max_write_rt, $pattern, $directory, $prefix, $remote_mnt, $mount_options, $mount_dir, $mount_retry_nap);
         for (my $i=0; $i<@names; $i++) {
            notBlank($names[$i], $values[$i]);
         }

         my $cmd = $::utils->fmt_cmd(
                     "add_file_endp",  $ep_name,      $::shelf_num,  $::resource,   $mvlan,
                     'fe_nfs',         $min_read_rt , $max_read_rt,  $min_write_rt, $max_write_rt,
                     $pattern,         $directory,    $prefix,       $remote_mnt,   $mount_options,
                     "7",              $mount_dir,    NA,            $mount_retry_nap);
         print " + " . $cmd.NL if ($::DEBUG);
         $::utils->doCmd($cmd);
         sleep(0.1); # if ($::DEBUG);
         print ".";
         $cmd = $::utils->fmt_cmd( "set_fe_info", $ep_name,
                     $min_rw_size,     $max_rw_size,  $num_files,    $min_file_size, $max_file_size,
                     $directory,       $prefix,       $read_write,   $quiesce_after_files);
         print " + " . $cmd.NL if ($::DEBUG);

         $::utils->doCmd($cmd);
         sleep(0.1); # if ($::DEBUG);

         print "\bo";
         $::utils->doCmd($::utils->fmt_cmd( "set_endp_quiesce",      $ep_name, 5));
         sleep(0.1);
         print "\bO";
         $::utils->doCmd($::utils->fmt_cmd( "set_endp_report_timer", $ep_name, 1000));
         sleep(0.1);
         print "\b*";
         $::utils->doCmd($::utils->fmt_cmd( "set_endp_flag",         $ep_name, "ClearPortOnStart", 0));
         sleep(0.1);
         print "\b|";
         my $cx_name       = "CX_".$ep_name;
         my $tg_name       = $::group.(($read_write eq READ) ? "_ro" : "_wo");
         my $tm_name       = "default_tm"; #= $::group.(($read_write eq READ) ? "_ro" : "_wo");
         my $tx_endp       = $ep_name;
         my $rx_endp       = NA;

         my $add_cx        = $::utils->fmt_cmd( "add_cx",                $cx_name, $tm_name, $tx_endp, $rx_endp );
         my $set_cx        = $::utils->fmt_cmd( "set_cx_report_timer",   $tm_name, $cx_name, "1000", "cxonly");
         my $add_tgcx      = $::utils->fmt_cmd( "add_tgcx",              $tg_name, $cx_name );
         print $add_tgcx.NL   if ($::DEBUG);
         print $add_cx.NL     if ($::DEBUG);
         print $set_cx.NL     if ($::DEBUG);

         $::utils->doCmd($add_cx);
         sleep(0.1);
         print "\bi";
         $::utils->doCmd($set_cx);
         sleep(0.1);
         print "\b:";
         $::utils->doCmd($add_tgcx);
         sleep(0.1);
         print "\b.";
      } #~for
      print "\nAdded ".@new_file_endpoints." endpoints to group $::group\n";
      sleep(3);
   } #~if need to create file endpoints

} #~prepareFileEndpoints

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    prepareExportList - assemble the list of nfs exports from either
##    the nfs_list resource or the nfs_mnt option
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub prepareExportList {

   if ((defined $::nfs_list) && ("$::nfs_list" ne "")) {
      open(my $fh, "<", $::nfs_list) or do_err_exit("Unable to open [$::nfs_list]. Cannot continue.");
      my @lines = ();
      while(<$fh>) {
         chomp;
         next if (/^\s*[#;]/);
         next if (/^\s*$/);
         s/^\s+//;
         s/\s+$//;
         if (/[0-9a-zA-Z.-]+:\/.*$/) {
            push( @lines, $_ );
         }
      }
      close($fh);
      if (@lines < 1) {
         do_err_exit("Unable to find lines that look like nfs mount points in [$::nfs_list]. Cannot continue.");
      }
      my $i = 0;
      for my $mvlan (sort keys %::mac_vlans) {
         $::mnt_map{ $mvlan } = $lines[ $i ];
         print " mapping $mvlan => ".$lines[ $i ].NL if($::DEBUG);
         $i = ++$i % @lines;
      }
   }
   elsif ((defined $::nfs_mnt) && ("$::nfs_mnt" ne "")) {
      for my $mvlan (sort keys %::mac_vlans) {
         $::mnt_map{ $mvlan } = $::nfs_mnt;
      }
   }
   else {
      do_err_exit("Niether --nfs_list or --nfs_mnt are specified. Cannot continue.");
   }

   if ((keys %::mnt_map) < 1) {
      do_err_exit("prepareExportList: unable to build map of mount entries. Cannot continue.");
   }
}
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    prepareGroups - creates requested test group if it does not exist,
##    file-endpoints will be created expecting these refs
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub prepareTestGroups {
   my @new_items        = ();
   my $test_group_str   = $::utils->doCmd("show_group all");
   my @test_group_lines = split(/\n/, $test_group_str );
   my %test_groups      = ();

   for my $group_name (sort(keys %::group_names)) {
      $test_groups{ $group_name } = 0;
   }
   for my $line ( @test_group_lines) {
      if ($line =~ /TestGroup name: ([^\[]+)\s*\[.*$/) {
         $test_groups{ $1 } = 1;
      }
   }
   for my $group_name (keys %test_groups) {
      if ($test_groups{$group_name} == 0 ) {
         push(@new_items, $group_name);
      }
   }
   if (@new_items > 0 ) {
      sleep(5);
      for my $group_name (@new_items) {

         $::utils->doCmd($::utils->fmt_cmd("add_group",  $group_name."_wo", NA, NA)) if (!$::skip_writers);
         $::utils->doCmd($::utils->fmt_cmd("add_group",  $group_name."_ro", NA, NA)) if (!$::skip_readers);

         #print " + tg $group_name ";
      }
   }
} # ~prepareTestGroups

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    generates random mac address
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub mac {
   my $rv = "00:";
   for (my $i=0; $i<5; $i++) {
      $rv.=sprintf("%02X",int(rand(255))).(($i<4)?':':'');
   }
   return $rv;
}



## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    list ports
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub showGroups {
   my @ports = $::utils->getPortListing($::shelf_num, $::resource);
   print "in show groups, found $#ports ports\n" if ($::DEBUG);
   for my $group_name ( sort(keys(%::group_names))) {
      print "show groups, $group_name _ro\n" if ($::DEBUG);
      my $cmd = $::utils->fmt_cmd("show_group", $group_name."_ro");
      print $::utils->doCmd($cmd);

      print "show groups, $group_name _wo\n" if ($::DEBUG);
      $cmd = $::utils->fmt_cmd("show_group", $group_name."_wo");
      print $::utils->doCmd($cmd);
   }
   print "\n";
}

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    start the writers then start the readers
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub runGroup {
   my $cmd;
   if (!$::skip_writers) {
      $cmd = "start_group ".$::group."_wo";
      $::utils->doCmd($cmd);
      print "Starting ".$::group."_wo...";
      for my $i ( 1..$sleep_after_wo ) { sleep(1); print "."; }
      print "...started".NL;
   }
   if (!$::skip_readers) {
      $cmd = "start_group ".$::group."_ro";
      $::utils->doCmd($cmd);
      print "Starting ".$::group."_ro ...";
      for my $i ( 1..3 ) { sleep(1); print "."; }
      print "...started".NL;
   }
}

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    stop writers then stop readers
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub stopGroup {
   my $cmd;
   if (!($::skip_writers || $skip_readers)) {
      print NL."Quiesceing all connections...";
      $cmd = "quiesce_group all";
      $::utils->doCmd($cmd);
   }
   if (!$::skip_writers) {
      print NL."Quiesceing writers...";
      $cmd = "quiesce_group ".$::group."_wo";
      $::utils->doCmd($cmd);
   }
   if (!$::skip_readers) {
      print NL."Quiesceing readers...";
      $cmd = "quiesce_group ".$::group."_ro";
      $::utils->doCmd($cmd);
   }
}

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
## poll the set of connections to see if they are 'stopped'
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub pollCxForStop {
   my $cmd;
   my $lines;
   my $num_lines     = 0;
   my $num_counted   = 0;
   my $num_stopped   = 0;
   my $upper_limit   = 60;
   my $attempts      = 0;
   while( $num_counted == 0 || ($num_counted != $num_stopped)) {
      return 0 if ($attempts > $upper_limit);
      sleep(2);
      $attempts++;
      $cmd           = $::utils->fmt_cmd("show_cx", "all", "all");
      $lines         = $::utils->doCmd($cmd);
      $num_counted   = 0;
      $num_stopped   = 0;
      for my $line (split(NL, $lines)) {
         next unless ($line =~ /CX_.*?_[wr]o_\d+/);
         $num_counted ++;
         my @h = split(/ +/, $line);

         $num_stopped += ($h[10] eq "STOPPED") ? 1 : 0;
         print "${h[2]} target:${h[8]} reported:${h[10]} counted:$num_counted stopped:$num_stopped attempts: $attempts".NL if ($::DEBUG);
      }
      print "                                  counted:$num_counted stopped:$num_stopped attempts: $attempts".NL if ($::DEBUG);
   }
   return 1;
}


## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    stop the group,
##    delete the file endpoints from the group,
##    then delete the group
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

sub deleteGroup {
   if ((!defined $::group) || ("$::group" eq "")) {
      do_err_exit("Cannot delete group if --group unspecified.");
   }
   my $group_name = undef;
   if( @_ < 1 ) {
      if ( $::skip_readers || $::skip_writers) {
         if (!$::skip_readers) {
            print "send Delete Group $group_name to $::group _ro \n" if ($::DEBUG);
            deleteGroup( $::group."_ro") ;
         }
         if (!$::skip_writers) {
            print "send Delete Group $group_name to $::group _wo \n" if ($::DEBUG);
            deleteGroup( $::group."_wo");
         }
         return;
      }
      $group_name = $::group;
   }
   else {
      ($group_name) = @_;
   }
   print "Delete Group $group_name\n" if ($::DEBUG);

   my %cx_names            = ();
   my %endp_names          = ();
   my %portlist            = ();
   my $cx_prefix           = "CX_".$group_name."_";
   my $should_stop_group   = 0;
   my $cmd;
   my $resp;
   my $endp_name;
   my $cx_name;

   if ("$group_name" eq "$::group") {
      $cmd = $::utils->fmt_cmd("show_group", $group_name."_wo");
      $resp = $::utils->doCmd($cmd);
      $cmd = $::utils->fmt_cmd("show_group", $group_name."_ro");
      $resp .= $resp.NL.$::utils->doCmd($cmd);
   }
   else {
      $cmd = $::utils->fmt_cmd("show_group", $group_name);
      $resp = $::utils->doCmd($cmd);
   }

   # collect cross connect names
   for my $line (split(NL, $resp)) {
      chomp $line;
      $should_stop_group = 1 if ($line =~ /TestGroup name:.*?\[RUNNING/);
      if( $line =~ / $cx_prefix/ ) {
         for my $tg_name_hunk (sort split(/\s+/, $line )) {
            next if ( $tg_name_hunk =~ /^ *$/);
            print "$tg_name_hunk " if ($::DEBUG);
            $cx_names{$tg_name_hunk}++ if ($tg_name_hunk =~ /^CX_/);
         }
      }
   }

   if ($should_stop_group) {
      stopGroup();
      if (! pollCxForStop()) {
         stopGroup();
         print "Not all connections have stopped. Continuing.".NL;
      }
   }

   # I'm not getting output here for many seconds after polling for stop
   foreach my $x (1..10) { sleep(1); print "."; } 
   print NL;

   # build endpoint names and find ports
   for $cx_name (reverse sort keys %cx_names) {
      next if( $cx_name !~ /^CX_/);
      my $endp_name  = $cx_name;
      $endp_name     =~ s/CX_//;
      print "."; sleep(0.2);
      my $lines      = $::utils->doCmd("nc_show_endp $endp_name");
      for my $line (split(NL, $lines)) {
         if ($line =~ /Shelf: /) {
            $line =~ s/,//g;
            my @hunks   = split(/\s+/, $line);
            my $port    = $hunks[2]." ".$hunks[4]." ".$hunks[6];
            #print "PORT: $port\n";
            $portlist{$port}++;
         }
      }
   }
   print NL;
   die "Error making portlist"   if (length(keys %portlist) < 1);

   # remove cross connects and endpoints immediately after each
   print "Removing Cross Connects and endpoints: ";
   for $cx_name (reverse sort keys %cx_names) {
      next if( $cx_name !~ /^CX_/);
      $cmd = $::utils->fmt_cmd("rm_cx", "all", $cx_name);
      print "** $cmd **".NL if ($::DEBUG);
      
      $::utils->doCmd($cmd);
      print "0"; #$cx_name ";
      sleep(0.5);
      my $endp_name = $cx_name;
      $endp_name =~ s/CX_//;
      $cmd = $::utils->fmt_cmd("rm_endp", $endp_name);
      $::utils->doCmd($cmd);
      print "o"; #$endp_name ";
      sleep(0.1);
   }
   print NL;
   sleep(1);

   # remove group
   if ( "$group_name" eq "$::group" ) {
      $cmd = $::utils->fmt_cmd("rm_group", $group_name."_wo");
      print " + $cmd".NL if ($::DEBUG);
      $::utils->doCmd($cmd);
      print "Removed ".$group_name."_wo".NL;
      sleep(0.2);
      $cmd = $::utils->fmt_cmd("rm_group", $group_name."_ro");
      print " + $cmd".NL if ($::DEBUG);
      $::utils->doCmd($cmd);
      print "Removed ".$group_name."_ro".NL;
      sleep(0.2);
   }
   else {
      $cmd = $::utils->fmt_cmd("rm_group", $group_name);
      print " + $cmd".NL if ($::DEBUG);
      $::utils->doCmd($cmd);
      print "Removed ".$group_name.NL;
   }
   sleep(2);

   # set those vlans admin down
   print "Setting mvlans down: ";
   for my $port (reverse sort keys %portlist) {
      my @h    = split(/\s+/, $port);
      $cmd     = fmt_port_up_down($h[1], $h[2], "down");
      print "$cmd".NL if ($::DEBUG);
      $::utils->doCmd($cmd);
      print "o"; # $port ";
      sleep(0.4);
   }
   print NL;
   sleep(0.2 * length(keys %portlist));
   # remove macvlans
   print "Removing mvlans ports: ";
   for my $port (reverse sort keys %portlist) {
      $cmd = "rm_vlan $port";
      print "Remove VLAN: $cmd".NL if ($::DEBUG);
      $::utils->doCmd($cmd);
      print "*"; #$port ";
      sleep(0.2);
   }
   print "...done.".NL;
}

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##    use this method to find the user prefix for each ip last octet
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
sub get_prefix_for_octet {
   my($octet) = @_;
   die "get_prefix_for_octet called without octet as argument" if ((!defined $octet) || ("$octet" eq ""));
   for my $name (sort( keys %::group_names)) {
      my $ra_bounds = $::group_names{ $name };
      if (($octet >= @$ra_bounds[0]) && ($octet <= @$ra_bounds[1])) {
         return $name;
      }
   }
   die "get_prefix_for_octet: no prefix found for octet [$octet]";
}

sub do_err_exit {
  my $msg = shift;
  print $msg.NL;
  exit(1);
}

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ==
##                                                                   ==
##    M A I N                                                        ==
##                                                                   ==
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ==

GetOptions
(
   'mgr|m=s'               => \$lfmgr_host,
   'mgr_port|mp=i'         => \$lfmgr_port,
   'resource|r=i'          => \$resource,
   'quiet|q=s'             => \$quiet,
   'action|a=s'            => \$action,
   'nfs_mnt|h=s'           => \$nfs_mnt,
   'nfs_list|e=s'          => \$nfs_list,
   'first_mvlan_ip|n=s'    => \$first_mvlan_ip,
   'group|g=s'             => \$group,
   'debug'                 => \$DEBUG,
   'dbg_nap|dp=i'          => \$D_PAUSE,
   'parent_port|pp=s'      => \$parent_port,
   'min_rw_size|nws=i'     => \$min_rw_size,
   'max_rw_size|xws=i'     => \$max_rw_size,
   'use_crc|crc=s'         => \$use_crc,
   'min_read_bps|nrbps=i'  => \$min_read_bps,
   'max_read_bps|xrbps=i'  => \$max_read_bps,
   'num_files|nf=i'        => \$num_files,
   'quiesce_after_files|qaf=i' => \$quiesce_after_files,
   'skip_readers|sr=i'     => \$skip_readers,
   'skip_writers|sw=i'     => \$skip_writers,
   'min_file_size|nsz=i'   => \$min_file_size,
   'max_file_size|xsz=i'   => \$max_file_size,
   'min_write_bps|nwbps=i' => \$min_write_bps,
   'max_write_bps|xwbps=i' => \$max_write_bps,
   'mount_options|mo=s'    => \$mount_options,
   'netmask|nm=s'          => \$netmask,
   'tmp_group|tmp=s'       => \$tmp_group,
   'min|ga=i'              => \$tmp_group_min,
   'max|gb=i'              => \$tmp_group_max,
) || do_err_exit("$usage");


if ((!defined $action) || ($action eq "")) {
  do_err_exit("Please specify an action to perform.\n$usage");
}

if ( ! ( $action eq "list_groups"
    || $action eq "run_group"
    || $action eq "stop_group"
    || $action eq "del_group" )) {
  do_err_exit("Unknown action $action:\n$usage");
}

if ((defined $tmp_group) && ($tmp_group ne "")) {
   print "Using temporary group [$tmp_group]\n";
   do_err_exit("Please set --min when using tmp_group") if ($tmp_group_min <= 0);
   do_err_exit("Please set --max when using tmp_group") if ($tmp_group_max <= 0);
   $group = $tmp_group;
}
elsif ( !(defined $group) || ("$group" eq "")) {
   do_err_exit("Blank or unknown group. Cannot continue.");
}

if ( $group eq $tmp_group ) {
   if ( !defined $parent_port || "$parent_port" eq "" ) {
      do_err_exit("Undefined --parent_port value. Cannot continue.");
   }
   $group_names{ $tmp_group } = [ $tmp_group_min, $tmp_group_max, $parent_port ];
   print "assigned values to group name [$group]\n" if ($::DEBUG);
   my $ra = $group_names{ $tmp_group };
   print "values: [".join(':', @$ra)."]\n" if ($::DEBUG);
}

if ( !defined $parent_port || "$parent_port" eq "" ) {
   $parent_port = $group_names{ $group }[2];
   if ( !defined $parent_port || "$parent_port" eq "" ) {
      do_err_exit("Undefined --parent_port value. Cannot continue.");
   }
}

init();

if ( $action eq "list_groups" ) {
   showGroups();
   exit(0);
}

print "checking group name [$group]\n" if ($::DEBUG);
if ( !defined $group || $group eq "" || ! $group_names{ $group }) {
   $group = "" if ( !defined $group );
   do_err_exit("Blank or unknown group [$group]"
      .NL."Known groups: ".join(', ', sort(keys(%group_names))));
}
print "Using group [$group]\n";


if ( $action eq "stop_group" ) {
   stopGroup();
}
elsif ( $action eq "run_group" ) {
   prepareTestGroups();
   preparePorts();
   prepareExportList();
   prepareFileEndpoints();
   runGroup();
}
elsif ( $action eq "del_group" ) {
   if ( $::skip_readers || $::skip_writers ) {
      deleteGroup();
   }
   else {
      deleteGroup( $::group );
   }
}
else {
   die "Unknown action $action:\n$usage";
}

#eof
