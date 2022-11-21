#!/usr/bin/perl -w
use strict;
use warnings;
use diagnostics;
use Carp;
use Time::HiRes qw(usleep);
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
our $use_ssid  = "kedtest-wpa2";
our $use_pass  = "kedtest-wpa2";

my $usage = qq("$0 --host {ip or hostname} # connect to this
   --port {port number} # defaults to 8080
   --ssid {ssid}
   --pass {passwd}
);


my $num_sta = 3;
my $des_resource = 1;
##
##    M A I N
##

GetOptions
(
  'host=s'  => \$::Host,
  'port=i'  => \$::Port,
  'ssid=s'  => \$::use_ssid,
  'pass=s'  => \$::use_pass,
) || (print($usage) && exit(1));

$::HostUri = "http://$Host:$Port";

my $uri = "/shelf/1";
my $rh = json_request($uri);
my $ra_links = get_links_from($rh, 'resources');
my @links2= ();
my $ra_alias_links = [];

# TODO: make this a JsonUtils::list_ports()
for $uri (@$ra_links) {
   $uri =~ s{/resource}{/port}g;
   $uri .= "/list?fields=_links,device,alias,port";
   print "$uri\n";
   $rh = json_request($uri);
   if (defined $rh->{'interfaces'}) {
      flatten_list($rh, 'interfaces');
      #push(@$ra_alias_links, keys(%{$rh->{'flat_list'}}));
      push( @$ra_alias_links, get_port_names($rh, 'interfaces'));
      #push(@links2, keys(%{$rh->{'flat_list'}}));
      push(@links2, @{get_links_from($rh, 'interfaces')});
   }
}

# destroy stations
my @radios = ();
my @destroy_me = ();
for my $rh_alias_link (@$ra_alias_links) {
   for my $rh_link (@$rh_alias_link) {
      if (  ($rh_link->{'uri'} =~m{^/port/1/$des_resource/})
         && ($rh_link->{'device'} =~m{^sta})) {
         push(@destroy_me, $rh_link);
      }

      push(@radios, $rh_link)
         if (($rh_link->{'uri'} =~m{^/port/1/$des_resource/})
            && ($rh_link->{'device'} =~m{^wiphy}));
   }
}
logg("\nDestroying these: ");

for my $rh_target (@destroy_me) {
   my $alias = $rh_target->{'device'};
   my @hunks = split(/[\/]/, $rh_target->{'uri'});

   # TODO: create JsonUtils::rm_vlan($eid, $alias)
   # suppress_postexec used to reduce the update traffic concurrent with large set of deletions
   my $rh_data = {
      'shelf'=>1,
      'resource'=>$hunks[3],
      'port'=>$alias
   };
   logg(" $alias");
   my $rh_response =  json_post("/cli-json/rm_vlan", $rh_data);
   usleep (15000);
}
my $rh_update = {
   'shelf'=>1, 'resource'=>$des_resource, 'port'=>'all', 'probe_flags'=>'0x1'
};
logg("\nRefreshing: ");
my $rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);
my $remaining = 1;
while ($remaining > 0) {
   $rh = json_request("/port/1/$des_resource/list");
   flatten_list($rh, 'interfaces');
   $remaining = 0;
   for my $name (keys %{$rh->{'flat_list'}}) {
      $remaining ++
         if ($name =~ /^v*sta/);
   }
   print "Remaining stations: $remaining, ";
   sleep 1;
}



# this really should poll for ports to wait for them to disappear
sleep 3;

my @new_stations = ();
logg("\nCreating new stations on these: ");
#print Dumper(\@radios);
my $rh_radio;
my $radio_name;
my $resource;
my $range;
my $radio_num;
my $radio_counter = 0;
$rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);

# add_sta + ht20 -ht40 -ht80 -create_admin_down
# flags=142609408&mode=8

print "\nAdding stations...\n";
for $rh_radio (@radios) {
   $radio_name = $rh_radio->{'alias'};
   my @hunks = split(/[\/]/, $rh_radio->{'uri'});
   ($radio_num) = $radio_name =~ /wiphy(\d+)/;
   $resource = $hunks[3];
   $range = ($resource * 1000) + ($radio_num * 100);
   logg("\n/cli-json/add_sta on 1.$resource.$radio_name\n");
   for (my $i = $range; $i < ($range+$num_sta); $i++) {
      # TODO: create JsonUtils::add_sta($eid, $alias...)
      my $rh_data = {
         'shelf'=>1,
         'resource'=>$resource,
         #'radio'=>'x'.$radio_name, # use to prompt radio not found error
         'radio'=>$radio_name,
         'sta_name'=>'sta'.$radio_counter,
         #'alias'=>'vsta'.$i, # deprecated, use set_port + interest.set_alias
         #'flags'=>68862086144, # has port-down set
         'flags'=>142609408,
         'ssid'=> $::use_ssid,
         'key'=> $::use_pass,
         'mac'=>'xx:xx:xx:xx:*:xx',
         'mode'=>0,
         'rate'=>'DEFAULT'
      };
      logg(" sta$radio_counter");
      my $rh_response = json_post("/cli-json/add_sta", $rh_data);
      usleep(300000);
      $radio_counter +=1;
   }
   $rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);
   sleep 1;
} # for
logg("\nUpdating aliases ");
$rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);
sleep 5;
$radio_counter = 0;
for $rh_radio (@radios) {
   $radio_name = $rh_radio->{'alias'};
   my @hunks = split(/[\/]/, $rh_radio->{'uri'});
   ($radio_num) = $radio_name =~ /wiphy(\d+)/;
   $resource = $hunks[3];
   $range = ($resource * 10000) + ($radio_num * 1000);

   for (my $i = $range; $i < ($range+$num_sta); $i++) {
      print "sta$radio_counter:vsta$i  ";
      #my $eidname = "1.$resource.sta$radio_counter";

      # set port up + dhcp + alias
      my $rh_data = {
         'shelf'=>1,
         'resource'=>$resource,
         'port'=>'sta'.$radio_counter,
         'current_flags'=>2147483648,
         'interest'=>20480,
         'alias'=>'vsta'.$i
      };
      my $rh_response = json_post("/cli-json/set_port", $rh_data);
      $radio_counter+=1;
      usleep(300000);
   }
}
$rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);
sleep 5;
$radio_counter = 0;
for $rh_radio (@radios) {
   $radio_name = $rh_radio->{'alias'};
   my @hunks = split(/[\/]/, $rh_radio->{'uri'});
   ($radio_num) = $radio_name =~ /wiphy(\d+)/;
   $resource = $hunks[3];
   $range = ($resource * 10000) + ($radio_num * 1000);
   for (my $i = $range; $i < ($range+$num_sta); $i++) {
      print "sta$radio_counter:vsta$i  ";
      #my $eidname = "1.$resource.sta$radio_counter";

      # set port up + dhcp + alias
      my $rh_data = {
         'shelf'=>1,
         'resource'=>$resource,
         'port'=>'sta'.$radio_counter,
         'current_flags'=>0,
         'interest'=>8388608,
      };
      my $rh_response = json_post("/cli-json/set_port", $rh_data);
      $radio_counter+=1;
      sleep 1;
   }
}
logg("\nRefreshing after setting up... ");
$rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);
sleep 4;
# wait on ports up
my $ports_still_down = 1;
while ($ports_still_down > 0) {
   # this logic has to see if port is phantom and if port is over-subscribed
   $rh = json_request("/port/1/$des_resource/list?fields=_links,port,device,down,phantom,channel");
   flatten_list($rh, 'interfaces');
   $ports_still_down=0;
   for my $rh_p (values %{$rh->{'flat_list'}}) {
      next unless $rh_p->{'device'} =~ /^sta/;
      #print "$rh_p->{'device'} Down: $rh_p->{'down'} Ph $rh_p->{'phantom'} Channel: $rh_p->{'channel'} \n";
      next if ($rh_p->{'phantom'}); # does not count as down
      next if (!$rh_p->{'channel'}); # probably oversubscribed or misconfigured
      $ports_still_down++
         if ($rh_p->{'down'});
   }
   print "ports down: $ports_still_down ";
   $rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);
   sleep 4;
}
sleep 4;
my $port_uri = "/port/1/$des_resource?fields=_links,device,alias,port";
# ports down
my $set_port = "/cli-json/set_port";
logg("\nsetting ports down: ");
$rh = json_request($port_uri);
flatten_list($rh, 'interfaces');
@links2 = ();
for my $k (keys %{$rh->{"flat_list"}}) {
   print "\n -- 200 ---------------------------------------------------------------\n";
   print Dumper($rh->{"flat_list"}->{$k});
   print "\n -- 200 ---------------------------------------------------------------\n";
   my $Link =  $rh->{"flat_list"}->{$k}->{"_links"};
   print "LINK $Link\n";
   push(@links2, $Link);
}

for my $port_uri (@links2) {
   print "URI: $port_uri\n";
   $rh = json_request($port_uri);
   my $device = get_thru('interface', 'device', $rh);
   next if ($device !~ /^sta/);
   logg($device." ");
   my $port = get_thru('interface', 'port', $rh);
   my @hunks = split(/\./, $port);
   my $resource = $hunks[1];
   my %post = (
      #'suppress_preexec_cli'=>'false',
      #'suppress_preexec_method'=>'false',
      #'suppress_postexec_cli'=>'false',
      #'suppress_postexec_method'=>'false',
      "shelf" => 1,
      "resource" => 0+$resource,
      "port" => $device,
      'suppress_postexec_cli'=>'true',
      "current_flags" => 1,
      "interest" => 8388610
   );
   my $rh_response = json_post($set_port, \%post);
   usleep(10000);
}
logg(" updating ");
$rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);
sleep 1;
logg("\nsetting ports up ");
for my $port_uri (@links2) {
   $rh = json_request($port_uri);
   my $device = get_thru('interface', 'device', $rh);
   next if ($device !~ /^sta/);
   logg($device." ");
   my $port = get_thru('interface', 'port', $rh);
   my @hunks = split(/\./, $port);
   my $resource = $hunks[1];
   # 'shelf=1&resource=2&port=vap2000&cmd_flags=0&current_flags=0&interest=8388610'
   my %post = (
      #'suppress_preexec_cli'=>'false',
      #'suppress_preexec_method'=>'false',
      #'suppress_postexec_cli'=>'false',
      #'suppress_postexec_method'=>'false',
      "shelf" => 1,
      "resource" => 0+$resource,
      "port" => $device,
      'suppress_postexec_cli'=>'true',
      "current_flags" => 0,
      "interest" => 8388610
   );
   my $rh_response = json_post($set_port, \%post);
   usleep(10000);
}
logg(" updating ");
$rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);
#
