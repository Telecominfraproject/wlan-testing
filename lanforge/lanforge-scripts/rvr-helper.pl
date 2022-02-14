#!/usr/bin/perl

# Example (fake) rvr-helper script.  The Rate-vs-Range test can be made to call out
# to scripts/programs, with goal that this script can return some additional info in csv format.
# The output will then be incorporated into the RvR report.

use strict;
use warnings;
use diagnostics;
use Getopt::Long;

our $usage = qq($0:  Rate vs Range DUT callout example
  --headers       Output headers.
);

my $headers = undef;

GetOptions(
   'headers'		=> \$headers,
) || die("$usage");

if ($headers) {
   # A real script might query AP for its view of MCS, RSSI, etc.
   print "date,user\n";
   exit(0);
}

my $dt = `date`;
chomp($dt);
my $me = `whoami`;
chomp($me);
print($dt . "," . $me . "\n");
exit(0);
