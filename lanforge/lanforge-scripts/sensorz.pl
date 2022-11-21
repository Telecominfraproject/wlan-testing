#!/usr/bin/perl -w
use strict;
use warnings;
use diagnostics;

my @sensor_lines = `sensors`;

my @sensor_devices = [];
my %sensor_readings = ();

my $temp = 0;
my $device = "Unknown";
for my $line (@sensor_lines) {
   next if ($line =~ /^\s*$/);
   chomp $line;
   if ($line =~ /^[^: ]+$/) {
      ($::device) = $line =~ /^(.*?-[\da-f]+)$/;
      if (!(defined $::device)) {
         print STDOUT "not a device? [$line]\n";
      }
      next if ($line !~ /^(k10temp-pci|mt7915_|ath10k_hwmon-pci|physical|coretemp|Core )/);
      if ( !defined $::sensor_readings{$::device}) {
         $::sensor_readings{$::device} = 0;
         push(@::sensor_devices, $::device);
      }
      next;
   }

   next if ($line !~ /^(temp|physical|coretemp|Core )/i);
   my $t = 0;
   if ($line =~ m{.*?:\s+N/A}) {
      $t = 0;
   }
   else {
      ($t) = $line =~ /.*?:\s+[+](\d+(\.\d+)?)°C/;
   }
   $::temp = $t if (!defined $::temp || $t > $::temp);
  
   $::sensor_readings{ $::device } = $::temp;
   #print "Device[$::device] temp[$::temp]\n";
   #$::device = "Unknown";
   $::temp = 0;
}

for my $dev (@::sensor_devices) {
   print "$dev, ";
}
print "\n";
for my $dev (@::sensor_devices) {
   print "$::sensor_readings{$dev}, ";
}
print "\n";
