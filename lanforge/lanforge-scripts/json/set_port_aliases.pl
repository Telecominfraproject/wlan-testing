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

my $usage = qq("$0 --host {ip or hostname} # connect to this
   --port {port number} # defaults to 8080
);


##
##    M A I N
##

GetOptions
(
  'host=s'                   => \$::Host,
  'port=i'                   => \$::Port,
) || (print($usage) && exit(1));

$::HostUri = "http://$Host:$Port";

my $uri = "/shelf/1";
my $rh = json_request($uri);
my $ra_links = get_links_from($rh, 'resources');
my @links2= ();
my $ra_alias_links = [];


#print Dumper($rh_stations);

#sub flatten_list {
#   my $rh_list = shift;
#   my $list_name = shift;
#   my $rh_irefs = {};
#   for (my $i=0; $i < @{$rh_stations->{"interfaces"}}; $i++) {
#      my @k = keys(%{$rh_stations->{"interfaces"}[$i]});
#      my $id = $k[0];
#      #print "ID[$id]\n";
#      $rh_irefs->{$id} = $rh_stations->{"interfaces"}[$i]->{$id};
#   }
#   $rh_list->{"flat_list"} = $rh_irefs;
#}

# TODO: make this a JsonUtils::list_ports()
for $uri (@$ra_links) {
   $uri =~ s{/resource}{/port}g;
   $uri .= "/list";
   #logg("requesting $uri");
   $rh = json_request($uri);
   #print Dumper($rh);
   push( @$ra_alias_links, @{get_port_names($rh, 'interfaces')});
   push(@links2, @{get_links_from($rh, 'interfaces')});
   #logg("\nfound: ");
   #logg(@links2);
}
#print Dumper($ra_alias_links);

# destroy stations on resource 3
my @radios = ();
for my $rh_alias_link (@$ra_alias_links) {
   push(@radios, $rh_alias_link)
      if (($rh_alias_link->{'uri'} =~m{^/port/1/[3]/})
         && ($rh_alias_link->{'alias'} =~m{^wiphy}));
}
logg(" updating ");
my $rh_update = {
   'shelf'=>1, 'resource'=>'all', 'port'=>'all', 'probe_flags'=>'0x1'
};
my $rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);

# this really should poll for ports to wait for them to disappear
sleep 2;

my @new_stations = ();
logg("\nCreating new stations on these: ");
#print Dumper(\@radios);
my $rh_radio;
my $radio_name;
my $resource;
my $range;
my $num_sta = 160;
my $radio_num;
my $radio_counter = 0;


logg(" updating ");
$rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);
sleep 2;
$radio_counter = 0;
for $rh_radio (@radios) {
   $radio_name = $rh_radio->{'alias'};
   my @hunks = split(/[\/]/, $rh_radio->{'uri'});
   ($radio_num) = $radio_name =~ /wiphy(\d+)/;
   $resource = $hunks[3];
   $range = ($resource * 10000) + ($radio_num * 1000);

   my $rh_stations = json_request("/port/1/$resource/all?fields=port,device,mac");
   flatten_list($rh_stations, "interfaces");

   for (my $i = $range; $i < ($range+$num_sta); $i++) {
      print "sta$radio_counter = vsta$i [ $range .. ".($range+$num_sta)."] 1/$resource/$radio_num $radio_name \n";
      my $portname = "sta$radio_counter";
      my $eidport = "1.$resource.$portname";
      if (defined $rh_stations->{"flat_list"}->{$eidport}) {
         #my $macaddr = $rh_stations->{"flat_list"}->{$eidport}->{"mac"};
         my $eid = $rh_stations->{"flat_list"}->{$eidport}->{"port"};
         my @hunks = split(/[.]/, $eid);
         die("port eid is bad: $eid")
            if (!defined $hunks[2]);
         my $portid = 0 + $hunks[2];
         my $rh_data = {
            'shelf'=>1,
            'resource'=>$resource,
            'port'=>$portname,
            'interest'=>4096,
            #'suppress_preexec_cli'=>'true',
            #'suppress_preexec_method'=>'true',
            #'suppress_postexec_cli'=>'false',
            #'suppress_postexec_method'=>'false',
            'alias'=>'vsta'.$i
         }; # todo: set_alias
         $rh_response = json_post("/cli-json/set_port", $rh_data);
         #usleep(10000);

         # set port up + dhcp
         $rh_data = {
            #'suppress_preexec_cli'=>'true',
            #'suppress_preexec_method'=>'true',
            #'suppress_postexec_cli'=>'false',
            #'suppress_postexec_method'=>'false',
            'shelf'=>1,
            'resource'=>$resource,
            'port'=>'sta'.$radio_counter,
            'cmd_flags'=>0,
            'current_flags'=>2147483648,
            'interest'=>16386
         };
      # TODO: create JsonUtils::set_dhcp($eid, $alias, $on_off)
      # set_port - port up, enable dhcp
      # current_flags=2147483648&interest=16386
         my $rh_response = json_post("/cli-json/set_port", $rh_data);
         $radio_counter+=1;
         usleep(10000);
      }
      else {
         print " 1.$resource.sta$radio_counter not found ";
      }
   }
}
logg(" updating ");
$rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);
sleep 2;

#
