#!/usr/bin/perl

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# Load different databases, turn on/off packet capturing.

use strict;

# Un-buffer output
$| = 1;

my $i = 0;
my $nm = "VRWL-1.1.000";
my $im = "./lf_icemod.pl --quiet=2";
my $cap_for = 10;

while (1) {
  print "Doing round: $i\n";
  printAndExec("$im --load db1");
  printAndExec("$im --cx $nm --state running");
  save_captures();
  printAndExec("$im --load db2");
  printAndExec("$im --cx $nm --state running");
  save_captures();
  $i++;
}


sub save_captures {
  my $i;
  for ($i = 0; $i<5; $i++) {
    printAndExec("$im --endp $nm-A --pcap /tmp/endp-a");
    printAndExec("$im --endp $nm-B --pcap /tmp/endp-b");
    sleep($cap_for);
    printAndExec("$im --endp $nm-A --pcap off");
    printAndExec("$im --endp $nm-B --pcap off");
    printAndExec("rm -fr /tmp/endp-a/");
    printAndExec("rm -fr /tmp/endp-b/");
  }
}


sub printAndExec {
  my $cmd = $_[0];

  print "$cmd\n";
  # NOTE:  If you use the single back-ticks here, it will hang, probably some
  #   signal problem...never figured out why really (ERESTARTSYS) was the error
  #   that perl hung on... --Ben
  system("$cmd");
}
