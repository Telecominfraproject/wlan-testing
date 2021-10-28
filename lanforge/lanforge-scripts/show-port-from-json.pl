#!/usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
#use JSON;
use Data::Dumper;
use LANforge::GuiJson;
#GuiResponseToHash GetHeaderMap GetRecordsMatching GetFields
package main;


my $gjson = new LANforge::GuiJson();
$gjson->Request("http://localhost:8080/PortTab");

my @port_names = ("eth0", "wlan0");
my $ra_matches = $gjson->GetRecordsMatching('Alias', \@port_names);
#print "Records matching Alias (eth0, wlan0):\n";
#print Dumper($ra_matches);

$ra_matches = $gjson->GetRecordsMatching('Device', \@port_names);
#print "Records matching Port:\n";
#print Dumper($ra_matches);

my @field_names = ("Device", "bps TX", "bps RX");
my $ra_fields = $gjson->GetFields('Device', \@port_names, \@field_names);
print "Fields (".join(", ", @field_names).") from records matching Device (".join(", ", @port_names)."):\n";
print Dumper($ra_fields);

@field_names = ("Alias", "RX-.*", "No CX.*");
$ra_fields = $gjson->GetFields('Device', \@port_names, \@field_names);
print "Fields (".join(", ", @field_names).") from records matching Device (".join(", ", @port_names)."):\n";
print Dumper($ra_fields);


=pod
10:57 < greearb> lets just do regex since we may have funny spaces or other characters in column headers
10:59 < greearb> GetFields wants arg1: json data structure
10:59 < greearb> Fields (bps TX, bps RX, TX-Rate, RX-Rate, AP, Channel, CX Time.*) from records matching Device (sta010, sta011, sta012, sta013, sta014,
                 eth5):
10:59 < greearb> $VAR1 = {};
10:59 < greearb> my $port_tab = `curl -sq http://localhost:8080/PortTab`;
10:59 < greearb> my $ports_data = decode_json($port_tab);
10:59 < greearb> #print Dumper($ports_data);
10:59 < greearb> my @field_names = ("bps TX", "bps RX", "TX-Rate", "RX-Rate", "AP", "Channel", "CX Time.*");
10:59 < greearb> my @port_names = (@stations, $upstream);
10:59 < greearb> my $ra_fields = GetFields($ports_data, 'Device', \@port_names, \@field_names);
10:59 < greearb> print "Fields (".join(", ", @field_names).") from records matching Device (".join(", ", @port_names)."):\n";
10:59 < greearb> print Dumper($ra_fields);
=cut
