#!/bin/perl
# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# use this script after bringing up stations with a DHCP lease
# then admin-down the stations. Go into /home/lanforge/vr_conf
# and change the settings with this script on all the files
# in a manner like this:
#
# root# cd /home/lanforge/vr_conf
# root# ~lanforge/scripts/add-dhcp-hostname.pl dhclient_sta*conf
#
# At this point you can bring up your stations. If you need to 
# check a lanforge dhcpd lease file, please look at the dhcp database
# found in /home/lanforge/vr_conf/vrcx_br1_dhcp_lease.db
# entries should have a "client-hostname: " entry.
# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
use strict;
use warnings;
use diagnostics;
$| = 1;

if (@ARGV < 1) {
   print "No files requested.\n";
   exit 1;
}
my @chars = ("A".."Z", "a".."z", "0".."9");

my $rand_name = "";
for my $fname (@ARGV) {
   print "File: $fname  ";

   my @lines = `cat $fname`;
   chomp @lines;
   die("Unable to open $fname for writing: $!")
      unless open(my $fh, ">", $fname);

   my $ifname='';
   for my $line (@lines) {
      next if ($line =~ /^\s*$/);
      next if ($line =~ /^. LANforge-generated/);
      next if ($line =~ /^. Remove first/);
      next if ($line =~ /^. automatically over-write/);
      next if ($line =~ /^send host-name/);
      if ($line =~ /^# sta\d+/) {
         ($ifname) = $line =~ /^# (sta\d+)\s*$/;
      }
      print $fh "$line\n";
   }
   $rand_name = "";
   $rand_name .= $chars[ rand @chars] for 1..8;
   #print "* ";
   #print "$rand_name\n";
   print $fh "interface \"$ifname\" {\n";
   print $fh "    send host-name \"$rand_name\";\n";
   print $fh "}\n";
   close $fh;
}
print "done\n";
