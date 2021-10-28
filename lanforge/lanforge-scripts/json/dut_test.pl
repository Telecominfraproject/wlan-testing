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

my $usage = qq("$0 --action {add|list|show|annotate|del}
   # list: lists all device names
   # show: shows everything about device
   # annotate: updates the note for the device
   --note {"double quoted stuff"}
   # del:
   --name {Device Under Test name}
   # when adding, use:
   --name {Device Under Test name}
   --img {picture name: c:\\stuff.png}
   --sw_version {text}
   --hw_version {text}
   --mgt_ip {1.1.1.1}
   --model_num {blanktronix345}
   --serial_num {asdf1234}
   --serial_port {1.2.ttyS0}
   --api_id {0-127}
   --lan_port {1.1.eth1}
   --wan_port {1.1.eth2}
   --ssid1 --passwd1 --ssid2 --passwd2 --ssid3 --passwd3 {stuff}
);


my $action;
my $name = "";
my $notes = "";
my $img_file = "";
my $sw_version  = "";
my $hw_version = "";
my $mgt_ip  = "";
my $model_num  = "";
my $serial_num  = "";
my $serial_port  = "";
my $api_id = "";
my $lan_port = "";
my $wan_port = "";
my $ssid1 = "";
my $ssid2 = "";
my $ssid3 = "";
my $passwd1 = "";
my $passwd2 = "";
my $passwd3 = "";

my $help;
##
##    M A I N
##

GetOptions(   'host=s'          => \$::Host,
   'action=s'        => \$action,
   'name=s'          => \$name,
   'notes=s'         => \$notes,
   'img_file=s'      => \$img_file,
   'sw_version=s'    => \$sw_version,
   'hw_version=s'    => \$hw_version,
   'mgt_ip=s'        => \$mgt_ip,
   'model_num=s'     => \$model_num,
   'serial_num=s'    => \$serial_num,
   'serial_port=s'   => \$serial_port,
   'api_id=s'        => \$api_id,
   'lan_port=s'      => \$lan_port,
   'wan_port=s'      => \$wan_port,
   'ssid1=s'         => \$ssid1,
   'ssid2=s'         => \$ssid2,
   'ssid3=s'         => \$ssid3,
   'passwd1=s'       => \$passwd1,
   'passwd2=s'       => \$passwd2,
   'passwd3=s'       => \$passwd3,
   'h|help'          => \$help)
|| (print($usage) && exit(1));

if ($help) {
   print $usage;
   exit 0;
}
if (!defined $action) {
   print $usage;
   exit 1;
}
$::HostUri = "http://$Host:$Port";
my $DEBUGURI = "?__debug=1";
my $uri_args = ""; # ="$DEBUG_URI";

our $URI = "$::HostUri/dut";
our $Post_URI = "$::HostUri/cli-json";

if ($action eq "list") {
   my $uri = "$::URI/list";
   my $rh = json_request($uri);
   flatten_list($rh, 'duts');
   for my $rh_dut (sort keys %{$rh->{'flat_list'}}) {
      print "$rh_dut\n";
   }
   exit 0;
}

if ($action eq "show") {
   die ("show what DUT? use --name:\n$usage")
      unless (defined $name && $name ne "");
   my $uri = "$::URI/$name";
   my $rh = json_request($uri);
   print Dumper($rh->{'dut'});
   die("unable to find DUT $name")
      unless(defined $rh->{'dut'});
   print Dumper($rh->{'dut'});
   exit 0;
}

my $varnames = q(name img_file sw_version hw_version mgt_ip model_num serial_num serial_port api_id lan_port wan_port ssid1 ssid2 ssid3 passwd1 passwd2 passwd3);

if ($action eq "add") {
   die ("show what DUT? use --name:\n$usage")
      unless (defined $name && $name ne "");
   my $rh_post = {};
   for my $k (sort split(' ', $varnames)) {
      my $v = eval("return \$$k;");
      if ((defined $v) && ($v ne "")) {
         $rh_post->{$k} = $v ;
      }
      else {
         $rh_post->{$k} = "NA";
      }
   }
   print Dumper($rh_post);
   my $post_uri = "$::Post_URI/add_dut$DEBUGURI";
   json_post($post_uri, $rh_post);
}


if ($action eq "annotate") {
   die ("show what DUT? use --name:\n$usage")
      unless (defined $name && $name ne "");
   die ("what notes? use --notes:\n$usage")
      unless (defined $notes);

   my $rh_post = {};
   my @note_lines=();
   if ($notes eq "") {
      $notes = '[BLANK]';
   }
    @note_lines = split(/\r?\n/, $notes);

    if ($note_lines[0] ne "[BLANK]") {
       unshift(@note_lines, "[BLANK]");
    }
    print Dumper(\@note_lines);
    my $post_uri = "$::Post_URI/add_dut_notes${DEBUGURI}";
    for my $note_line (@note_lines) {
       print Dumper(\$note_line);
       my $rh = {
          'dut' => $name,
          'text' => $note_line
       };
       json_post($post_uri, $rh);
    }
}
#
