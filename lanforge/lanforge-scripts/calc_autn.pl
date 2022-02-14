#!/usr/bin/perl
##
## Calculated EAP-AKA AUTN based on:
## AUTN = (SQN xor AK) || AMF || MAC = 48 + 16 + 64 = 128 bits
##
use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{__DIE__} = sub{Carp::confess(@_)};
use Getopt::Long;
$| = 1;

our $usage = qq($0: calculate AUTN
   All input is in ascii hex.
   --sqn           SQN
   --ak            AK, output of f5
   --amf           AMF for test-set configuration
   --mac           MAC, output of f1

Example for test-set 19 (4.3.19) from 3GPP TS 35.208, v6.0.0 Release 6
   $0 --sqn 16f3b3f70fc2 --ak ada15aeb7bb8 --amf c3ab --mac 2a5c23d15ee351d5
);


our $sqn = "";
our $ak = "";
our $amf = "";
our $mac = "";

GetOptions (
   'sqn=s'    => \$::sqn,
   'ak=s'    => \$::ak,
   'amf=s'    => \$::amf,
   'mac=s'    => \$::mac,
) || die("$::usage");

#AUTN = (SQN xor AK) || AMF || MAC = 48 + 16 + 64 = 128 bits
print "AUTN for SQN: $sqn AK: $ak AMF: $amf MAC: $mac\n";
my $i;
my @sqnc = split("", $sqn);
my @akc = split("", $ak);
if (@sqnc != 12) {
  die("sqn must have 12 ascii bytes.");
}
if (@akc != 12) {
  die("akc must have 12 ascii bytes.");
}

for ($i = 0; $i<12; $i++) {
  my  $v = hex($sqnc[$i]);
  $v ^= hex($akc[$i]);
  printf "%1x", $v;
}
print $amf;
print $mac;
print "\n";

## eof
