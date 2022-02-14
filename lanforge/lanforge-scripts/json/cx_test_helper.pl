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
use JSON;
use Linux::Inotify2;
use lib '/home/lanforge/scripts';
use lib "../";
use lib "./";
use LANforge::JsonUtils qw(logg err json_request get_links_from get_thru json_post get_port_names);

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
   --port {port number}                # defaults to 8080
   --cxname {name of connection to toggle}
);


##
##    M A I N
##

our $cxname;
GetOptions
(
  'host=s'        => \$::Host,
  'port=i'        => \$::Port,
  'cxname=s'      => \$::cxname
) || (print($usage) && exit(1));

$::HostUri = "http://$Host:$Port";


# using this is going to want high inotify instances, like mentioned here:
# sysctl fs.inotify.max_user_instances=256
# https://forum.proxmox.com/threads/unable-to-create-new-inotify-object-too-many-open-files-at-usr-share-perl5.23700/



# wait until /tmp/startcx appears
our $toggle="startcx";
 
# create a new object
my $inotify_c = new Linux::Inotify2
   or die "Unable to create new inotify object: $!" ;
my $inotify_d = new Linux::Inotify2
   or die "Unable to create new inotify object: $!" ;
     
# create watch
$inotify_c->watch ("/tmp", IN_CREATE, sub {
   my $event = shift;
   print("I see $event->{name}\n");
   return if ($event->{name} =~ /$toggle$/);
}) or die "watch creation failed" ;

while() {
   my @events = $inotify_c->read;
   last;
   #unless (@events > 0) { print "read error: $!"; last; }
}

print "run $cxname ";
my $set_state = {
      'test_mgr'  => 'default_tm',
      'cx_name'   => $cxname,
      'cx_state'  => 'RUNNING'
   };
json_post("/cli-json/set_cx_state", $set_state);


$inotify_d->watch ("/tmp", IN_DELETE, sub {
   my $event = shift;
   print("Delete seen for $event->{name}\n");
   return if ($event->{name} =~ /$toggle$/);
}) or die "watch creation failed" ;
while() {
   my @events = $inotify_d->read;
   last;
   #unless (@events > 0) { print "read error: $!"; last; }
}

print "quiesce $cxname ";
$set_state = {
      'test_mgr'  => 'default_tm',
      'cx_name'   => $cxname,
      'cx_state'  => 'QUIESCE'
   };
json_post("/cli-json/set_cx_state", $set_state);
print "...done\n";
