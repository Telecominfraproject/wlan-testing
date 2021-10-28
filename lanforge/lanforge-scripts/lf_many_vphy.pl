#!/usr/bin/perl -w
# Create lots of virtual radios with stations.
# Note that lf_associate_ap.pl has many more options that
# are not currently used here.

use strict;
use Getopt::Long;

my $usage = "$0
  [--num_radios { number } ]
  [--ssid {ssid}]
";

my $num_radios = 1;
my $ssid = "ssid";




GetOptions (
	    'num_radios|r=i'     => \$num_radios,
	    'ssid|s=s'           => \$ssid,
	   ) || (print($usage) && exit(1));

my $i;
for ($i = 0; $i < $num_radios; $i++) {
  my $idx = $i + 1;
  my $sta = 600 + $idx;
  my $cmd = "./lf_associate_ap.pl --resource 1 --radio vphy$idx --vrad_chan 1 --num_stations 1 --first_sta sta$sta --action add --first_ip DHCP --ssid $ssid";
  print "$cmd\n";
  system($cmd);
}
