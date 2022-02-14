#!/usr/bin/perl -w
use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{ __DIE__  } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };

# Un-buffer output
$| = 1;
use Getopt::Long;
use JSON::XS;
use HTTP::Request;
use LWP;
use LWP::UserAgent;
use Data::Dumper;
use Time::HiRes qw(usleep);
use JSON;
use lib '/home/lanforge/scripts';
use lib "../";
use lib "./";
use LANforge::JsonUtils qw(logg err json_request get_links_from get_thru json_post get_port_names flatten_list);

package main;
# Default values for ye ole cmd-line args.
our $Resource  = 1;
our $quiet     = "yes";
our $Host      = "localhost";
our $Port      = 8080;
our $HostUri   = "http://$Host:$Port";
our $Web       = LWP::UserAgent->new;
our $Decoder   = JSON->new->utf8;
our $ssid;
our $security;
our $passphrase;

my $usage = qq("$0 --host {ip or hostname} # connect to this
   --port {port number} # defaults to 8080
);

my $des_resource = 6;
#my $pat_port_type = '^eth\d[#]\d+';
my $pat_port_type = '^v*sta\d+';
##
##    M A I N
##

GetOptions
(
  'host=s'        => \$::Host,
  'port=i'        => \$::Port
) || (print($usage) && exit(1));

$::HostUri = "http://$Host:$Port";

my $DEBUGURI = "?__debug=1";
my $uri_args = ""; # ="$DEBUG_URI";

my $uri = "/shelf/1";
my $rh = json_request($uri);
my $ra_links = get_links_from($rh, 'resources');
my @ports_up= ();

# TODO: make this a JsonUtils::list_ports()
$uri = "/port/1/${des_resource}/list?fields=alias,device,down,phantom,port";
#logg("requesting $uri");
$rh = json_request($uri);
flatten_list($rh, 'interfaces');
for my $rh_p (keys %{$rh->{'flat_list'}}) {
   # truthy value evaluates better
   my $onoff = $rh->{'flat_list'}->{$rh_p}->{'down'};
   print "$rh_p down? $onoff ";
   if ($onoff) {
      push(@ports_up, $rh_p);
   }
}
# find first station
my $rh_sta;
for my $rh_up (@ports_up) {
   my $eid = $rh->{'flat_list'}->{$rh_up}->{'port'};
   my @hunks = split(/[.]/, $eid);
   if ($hunks[1]) {
      $rh_sta = $rh_up;
   }
}
if (!defined $rh_sta) {
   die("Unable to find a virtual station. Is one up?");
}

# delete old CXes and old endpoints
# TODO: collect_l4cx_names

my $rh_endplist = json_request("/layer4/list");
print "\nRemoving L4: ";
my @endp_names = ();
#sleep 2;
#print "-------------------------------------------------------------------------\n";
#print Dumper($rh_endplist);
#print "-------------------------------------------------------------------------\n";
#sleep 2;

if (defined $rh_endplist->{"endpoint"}
   && (ref $rh_endplist->{"endpoint"} eq "HASH")) {
   # indicates we only have one
   push(@endp_names, $rh_endplist->{"endpoint"}->{"name"});
}
elsif (defined $rh_endplist->{"endpoint"}) {
   flatten_list($rh_endplist, 'endpoint');
   #print "FLAT LIST:\n";
   #print Dumper($rh_endplist->{'flat_list'});
   for my $ep_name (keys %{$rh_endplist->{'flat_list'}}) {
      print "?$ep_name? ";
      next if (!defined $ep_name);
      next if ($ep_name eq "");
      next if ((ref $ep_name) eq "ARRAY");
      next if (!defined $rh_endplist->{'flat_list'}->{$ep_name}->{"name"});
      next if ($rh_endplist->{'flat_list'}->{$ep_name}->{"name"} eq "");
      #print "\nepn:".Dumper($rh_endplist->{'flat_list'}->{$ep_name}->{"name"});
      push(@endp_names, $ep_name);
   }
}
if ((@endp_names < 1) && (defined $rh_endplist->{"endpoint"})) {
   # check for mutated L4endp entries that only exist in EID form
   #die "Unknown L4 endpoint state"
   #   if (!(defined $rh_endplist->{"endpoint"}));
   die "No endpoint entries"
      if (scalar @{$rh_endplist->{"endpoint"}} < 1);
   for $rh (@{$rh_endplist->{"endpoint"}}) {
      #print Dumper($rh);
      my @k = keys(%$rh);
      #print "$k[0] ";
      push(@endp_names, $k[0]);
   }
}
#print Dumper(\@endp_names);



my @cx_names = ();
if (@endp_names > 0) {
   for my $endp_name (@endp_names) {
      next if ($endp_name =~ /^CX_D_/);
      print " endp_name[$endp_name]";
      push(@cx_names, "CX_".$endp_name);
   }
}
my $rh_req = {
   "test_mgr" => "default_tm",
   "suppress_preexec_method" => 1,
   "suppress_preexec_cli" => 1,
};
for my $cx_name (@cx_names) {
   print "rm_cx $cx_name ";
   $rh_req->{"cx_name"} = $cx_name;
   print "rm_cx $cx_name ";
   json_post("/cli-json/rm_cx", $rh_req);
}
print "\nRemoved ".scalar @cx_names." cx\n";
my $rh_show_cxe = { "test_mgr"=>"all", "cross_connect"=>"all"};
json_post("/cli-json/show_cxe${DEBUGURI}", $rh_show_cxe);
sleep 2;
print "\nRemoving ".scalar @endp_names;
$uri = "/cli-json/rm_endp${uri_args}";
for my $ep_name (@endp_names) {
   if (!defined $ep_name || $ep_name =~/^\s*$/ || (ref $ep_name) eq "ARRAY") {
      #print " rm_endp [$ep_name]"; #skipping
      #print Dumper(\$ep_name);
      next;
   }
   print " -$ep_name ";
   $rh = { "endp_name" => $ep_name };
   json_post($uri, $rh);
}
print "\nRefreshing...";
my $h = {"endpoint"=>"all"};
json_request("/cli-json/nc_show_endpoints${uri_args}", $h);
sleep 1;
$h = {"test_mgr"=>"all", "cross_connect"=>"all"};
json_request("/cli-json/show_cxe${uri_args}", $h);




# assume resource 1, eth1 is present, and create an endpoint to it
# -A and -B are expected convention for endpoint names

##
## Create New Endpoints
##
my $rh_ports = json_request("/port/1/${des_resource}/list");
flatten_list($rh_ports, 'interfaces');

my $rh_endp_A = { # actual endpoint
      #'alias'           => "untitled",
      'shelf'           => 1,
      'resource'        => $des_resource,
      'type'            => 'l4_generic',
      'timeout'         => '2000',
      'url_rate'        => '600',
      'url'             => 'dl http://idtest.candelatech.com/ /dev/null',
      'max_speed'       => '1000000',
      'http_auth_type'  => 0,
      'proxy_auth_type' => 512,
   };
my $rh_endp_B = { # dummy endpoints, # we don't actually need
      #'alias'           => "D_untitled",
      'shelf'           => 1,
      'resource'        => $des_resource,
      # port
      'type'            => 'l4_generic',
      'proxy_port'      => 'NA',
      'timeout'         => 0,
      'url_rate'        => 0,
      'url'             => ' ',
      'max_speed'       => 'NA',
   };
my $rh_set_flags_a = {
   # 'name' =>
   'flag' => 'GetUrlsFromFile',
   'val' => 0,
   };
my $rh_set_flags_b = {
   # 'name' =>
   'flag' => 'unmanaged',
   'val' => 1,
   };
my $rh_add_cx = {
   # "alias" =>,
   'test_mgr' => 'default_tm',
   #'tx_endp' =>,
   #'rx_endp' =>
};
print "\nConstructing new Endpoints B: ";
my $num_ports = scalar keys(%{$rh_ports->{'flat_list'}});
my $num_cx = 0;
my $disp_num = $des_resource * 1000;
# create dummy port and set it unmanaged
my $create_b_side = 0;
if ($create_b_side) {
   for my $rh_p (values %{$rh_ports->{'flat_list'}}) {
      last if ($num_cx >= ($num_ports-1));
      next if ($rh_p->{'alias'} !~ /$pat_port_type/);

      # create dummy port and set it unmanaged
      my $end_b_alias = "D_l4json${disp_num}";
      $rh_endp_B->{'port'} = $rh_p->{'alias'};
      $rh_endp_B->{'alias'} = $end_b_alias;
      $num_cx++;
      $disp_num++;
      print " +$end_b_alias ";
      json_post("/cli-json/add_l4_endp${uri_args}", $rh_endp_B);
   }
   sleep 1;
   $num_cx = 0;
   $disp_num = $des_resource * 1000;
   print "\nSetting Endpoint flags: ";
   for my $rh_p (values %{$rh_ports->{'flat_list'}}) {
      last if ($num_cx >= ($num_ports-1));
      next if ($rh_p->{'alias'} !~ /$pat_port_type/);
      my $end_b_alias = "D_l4json${disp_num}";
      $rh_set_flags_b->{'name'} = $end_b_alias;
      $num_cx++;
      $disp_num++;
      print " ~$end_b_alias ";
      json_post("/cli-json/set_endp_flag${uri_args}", $rh_set_flags_b);
   }
   sleep 1;
}
$num_cx = 0;
$disp_num = $des_resource * 1000;
print "\nAdding Endpoint A: ";
for my $rh_p (values %{$rh_ports->{'flat_list'}}) {
   last if ($num_cx >= ($num_ports-1));
   next if ($rh_p->{'alias'} !~ /$pat_port_type/);
   my $end_a_alias = "l4json${disp_num}";
   $rh_endp_A->{'port'} = $rh_p->{'alias'};
   $rh_endp_A->{'alias'} = $end_a_alias;
   $num_cx++;
   $disp_num++;
   print " +$end_a_alias; ";
   json_post("/cli-json/add_l4_endp${uri_args}", $rh_endp_A);
}
$num_cx = 0;
$disp_num = $des_resource * 1000;
print "\nSet_endp_flag: ";
for my $rh_p (values %{$rh_ports->{'flat_list'}}) {
   last if ($num_cx >= ($num_ports-1));
   next if ($rh_p->{'alias'} !~ /$pat_port_type/);
   my $end_a_alias = "l4json${disp_num}";
   $rh_set_flags_a->{'name'} = $end_a_alias;
   $num_cx++;
   $disp_num++;
   print " ~$end_a_alias ";
   json_post("/cli-json/set_endp_flag${uri_args}", $rh_set_flags_a);
}
print "\nRefreshing...";
$h = {"endpoint"=>"all"};
json_request("/cli-json/nc_show_endpoints${uri_args}", $h);
sleep 4;
print "\nConstructing new CX: ";
$num_cx = 0;
$disp_num = $des_resource * 1000;
print Dumper($rh_ports->{'flat_list'});
for my $rh_p (values %{$rh_ports->{'flat_list'}}) {
   last if ($num_cx >= ($num_ports-1));
   next if ($rh_p->{'alias'} !~ /$pat_port_type/);
   my $end_a_alias = "l4json${disp_num}";
   my $end_b_alias = ($create_b_side) ? "D_l4json${disp_num}" : "NA";
   my $cx_alias = "CX_l4json${disp_num}";
   $rh_add_cx->{'alias'} = $cx_alias;
   $rh_add_cx->{'tx_endp'} = $end_a_alias;
   $rh_add_cx->{'rx_endp'} = $end_b_alias;
   $num_cx++;
   $disp_num++;
   print " $cx_alias ";
   json_post("/cli-json/add_cx${uri_args}", $rh_add_cx);
}
$h = {"endpoint"=>"all"};
json_request("/cli-json/nc_show_endpoints", $h);
sleep 4;
$h = {"test_mgr"=>"all", "cross_connect"=>"all"};
json_request("/cli-json/show_cxe", $h);
sleep 4;

print "\nRefreshing...";
$h = {"endpoint"=>"all"};
json_request("/cli-json/nc_show_endpoints", $h);
sleep 4;
$h = {"test_mgr"=>"all", "cross_connect"=>"all"};
json_request("/cli-json/show_cxe", $h);
sleep 4;

# wait for data to distribute

my $num_unfinished = 1;
while ($num_unfinished > 0) {
   $num_unfinished = 0;
   my $rh_cx = json_request("/layer4/list");
   print "\n- 337 --------------------------------------------------------\n";
   print Dumper($rh_cx);
   print "\n- 337 --------------------------------------------------------\n";
   flatten_list($rh_cx, "endpoint");
   @cx_names = sort keys %{$rh_cx->{'flat_list'}};
   for my $cx_alias (sort @cx_names) {
      if ($cx_alias =~ /^1\./) {
         print " -$cx_alias ";
         $num_unfinished++ ;
      }
   }
   print " Unfinished: $num_unfinished\n";
   sleep 1 if ($num_unfinished);
}
@endp_names = ();
my $rh_endp = json_request("/layer4/list");
flatten_list($rh_endp, "endpoint");
   print "\n- 354 --------------------------------------------------------\n";
   print Dumper($rh_endp);
   print "\n- 354 --------------------------------------------------------\n";
@endp_names = sort keys %{$rh_endp->{'flat_list'}};
@cx_names = ();
for my $endp_name (@endp_names) {
   next if ($endp_name =~ m/^D_/);
   if ($endp_name =~ m/^1\./) {
      print " what? $endp_name ";
      next;
   }
   push(@cx_names, "CX_${endp_name}");
}

my $rh_cx_t = {
      'test_mgr'  => 'default_tm',
      #'cx_name'   => $cx_alias,
      'milliseconds'=> 1000,
   };
print "\nSetting timers: ";
for my $cx_alias (sort @cx_names) {
   if ($cx_alias =~ /^\s*$/ || ref $cx_alias eq "ARRAY") {
      print "BLANK CX_NAME: ".Dumper(\@cx_names);
      next;
   }
   $rh_cx_t->{'cx_name'} = $cx_alias;
   print " ~$cx_alias ";
   json_post("/cli-json/set_cx_report_timer", $rh_cx_t);
}

print "\nRefreshing...";
$h = {"endpoint"=>"all"};
json_request("/cli-json/nc_show_endpoints", $h);
sleep 1;
$h = {"test_mgr"=>"all", "cross_connect"=>"all"};
json_request("/cli-json/show_cxe", $h);
sleep 1;

$rh_cx_t = {
      'test_mgr'  => 'default_tm',
      #'cx_name'   => $cx_alias,
      'cx_state'=> "RUNNING",
   };
print "\nStarting cx...";
for my $cx_alias (sort @cx_names) {
   $rh_cx_t->{'cx_name'} = $cx_alias;
   print " +$cx_alias ";
   json_post("/cli-json/set_cx_state", $rh_cx_t);
}
sleep 5;

print "\nStopping cx...";
$rh_cx_t = {
      'test_mgr'  => 'default_tm',
      #'cx_name'   => $cx_alias,
      'cx_state'=> "STOPPED",
   };
for my $cx_alias (sort @cx_names) {
   $rh_cx_t->{'cx_name'} = $cx_alias;
   print " -$cx_alias ";
   json_post("/cli-json/set_cx_state", $rh_cx_t);
}

#
