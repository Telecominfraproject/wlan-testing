#!/usr/bin/perl

use strict;

$| = 1; # Don't buffer things...

my $last_seq = -1;
my $last_pkt = -1;
my $last_ts = -1;

my $last_seq_ooo = -1;
my $last_pkt_ooo = -1;
my $last_ts_ooo = -1;

# Reads in input like:
#23930  18.005150 192.168.1.102 -> 192.168.1.101 LANforge Seq: 66653
#23931  18.005265 192.168.1.102 -> 192.168.1.101 LANforge Seq: 66654
#23932  18.005391 192.168.1.102 -> 192.168.1.101 LANforge Seq: 66655

while(<>) {
  my $ln = $_;
  chomp($ln);
  if ($ln =~ /^\s*(\d+)\s+(\S+)\s+(.*)\s+LANforge Seq:\s+(\d+)/) {
    my $pkt = $1;
    my $ts = $2;
    my $stream = $3;
    my $seq = $4;

    #print "pkt is LANforge protocol: $ln\n";

    my $gap = $seq - $last_seq;
    my $skip_update = 0;
    # TODO:  Deal with different streams, have to take IP ports into account too probably.
    if ($gap != 1) {
      if ($gap > 1) {
	print "DROP: pkt-gap, seq: $last_seq\/$seq  pkt-cnt: $last_pkt\/$pkt  timestamp: $last_ts\/$ts  gap: $gap\n";
	$last_seq_ooo = -1;
      }
      elsif ($gap == 0) {
	print "DUP: pkt-gap, seq: $last_seq\/$seq  pkt-cnt: $last_pkt\/$pkt  timestamp: $last_ts\/$ts  gap: $gap\n";
	$last_seq_ooo = -1;
      }
      else {
	# New seq is smaller than old.  Either an OOO pkt, or perhaps a seq-number wrap?
	if ($seq <= 10) {
	  # Assume wrap
	  print "WRAP: pkt-gap, seq: $last_seq\/$seq  pkt-cnt: $last_pkt\/$pkt  timestamp: $last_ts\/$ts  gap: $gap\n";
	  $last_seq_ooo = -1;
	}
	else {
	  my $ooo_gap = $seq - $last_seq_ooo;
	  my $skip_update_ooo = 0;
	  if ($last_seq_ooo == -1) {
	    print "OOO: pkt-gap, seq: $last_seq\/$seq  pkt-cnt: $last_pkt\/$pkt  timestamp: $last_ts\/$ts  gap: $gap\n";
	  }
	  elsif ($ooo_gap > 1) {
	    print "OOO-DROP: pkt-gap, seq: $last_seq_ooo\/$seq  pkt-cnt: $last_pkt_ooo\/$pkt  timestamp: $last_ts_ooo\/$ts  gap: $ooo_gap\n";
	  }
	  elsif ($ooo_gap == 0) {
	    print "OOO-DUP: pkt-gap, seq: $last_seq_ooo\/$seq  pkt-cnt: $last_pkt_ooo\/$pkt  timestamp: $last_ts_ooo\/$ts  gap: $ooo_gap\n";
	  }
	  elsif ($ooo_gap < 0) {
	    # Fun, out of order flow in already out of order flow!
	    print "OOO-OOO: pkt-gap, seq: $last_seq_ooo\/$seq  pkt-cnt: $last_pkt_ooo\/$pkt  timestamp: $last_ts_ooo\/$ts  gap: $ooo_gap\n";
	    $skip_update_ooo = 1;
	  }

	  if (! $skip_update_ooo) {
	    # Start of OOO pkt sequence
	    $last_seq_ooo = $seq;
	    $last_pkt_ooo = $pkt;
	    $last_ts_ooo = $ts;
	  }

	  # Don't update main pkt counters for OOO pkts.
	  $skip_update = 1;
	}
      }
    }
	
    if (! $skip_update) {
      $last_seq = $seq;
      $last_pkt = $pkt;
      $last_ts = $ts;
    }
  }
}
