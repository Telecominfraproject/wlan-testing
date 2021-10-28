package Tid;

use strict;
use warnings;
use diagnostics;
use bigint;
use bignum;
use Carp;
$SIG{ __DIE__  } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };

my $warn_dup_ba_once = 1;
my $max_pkt_store = 250;

sub new {
  my $class = shift;
  my %options = @_;

  my $self = {
              pkts => [],
              rx_no_ack_found_all => 0,
              rx_no_ack_found_big => 0,
              tx_no_ack_found_all => 0,
              tx_no_ack_found_big => 0,
              tx_retrans_pkts => 0,
              rx_retrans_pkts => 0,
              tx_amsdu_retrans_pkts => 0,
              rx_amsdu_retrans_pkts => 0,
              rx_pkts => 0,
              tx_pkts => 0,
              rx_amsdu_pkts => 0,
              tx_amsdu_pkts => 0,
              dummy_rx_pkts => 0,
              dummy_tx_pkts => 0,
              tot_pkts => 0,
              last_tot_pkts => 0,
              last_rx_pkts => 0,
              last_tx_pkts => 0,
              last_rx_retrans_pkts => 0,
              last_tx_retrans_pkts => 0,
              last_dummy_rx_pkts => 0,
              last_dummy_tx_pkts => 0,
              last_ps_timestamp => 0,
              last_rx_amsdu_pkts => 0,
              last_tx_amsdu_pkts => 0,
              last_tx_amsdu_retrans_pkts => 0,
              last_rx_amsdu_retrans_pkts => 0,
              %options,
             };

  bless($self, $class);

  if (0) { # Skip per-tid reporting files for now.
    # I am seeing failure due to > 1024 files being opened, and we don't
    # use these anyway...
    my $rpt_fname = $self->{report_prefix} .
      "tid-" . $self->tidno() . "-" .
        $self->{addr_a} . "." .
          $self->{addr_b} . "-rpt.txt";
    open(my $MCS, ">", $rpt_fname) or die("Can't open $rpt_fname for writing: $!\n");
    $self->{mcs_fh} = $MCS;

    $rpt_fname = $self->{report_prefix} . "tid-" . $self->tidno() . "-" . $self->{addr_a} . "." . $self->{addr_b} . "-ps-rpt.txt";
    open(my $MCS_PS, ">", $rpt_fname) or die("Can't open $rpt_fname for writing: $!\n");
    $self->{mcs_fh_ps} = $MCS_PS;

    $rpt_fname = $self->{report_prefix} . "tid-" . $self->tidno() . "-" . $self->{addr_a} . "." . $self->{addr_b} . "-ba-rpt.txt";
    open(my $BA, ">", $rpt_fname) or die("Can't open $rpt_fname for writing: $!\n");
    $self->{fh_ba} = $BA;
  }

  return $self;
}

sub tidno {
  my $self = shift;
  return $self->{tidno};
}

sub add_pkt {
  my $self = shift;
  my $pkt = shift;

  $self->{tot_pkts}++;
  if ($pkt->receiver() eq $self->{addr_a}) {
    $pkt->{is_rx} = 1;
    $self->{rx_pkts}++;
    $self->{rx_amsdu_pkts} += $pkt->{amsdu_frame_count};
    if ($pkt->retrans()) {
      $self->{rx_retrans_pkts}++;
      $self->{rx_amsdu_retrans_pkts} += $pkt->{amsdu_frame_count}
    }
  }
  else {
    $pkt->{is_rx} = 0;
    $self->{tx_pkts}++;
    $self->{tx_amsdu_pkts} += $pkt->{amsdu_frame_count};
    if ($pkt->retrans()) {
      $self->{tx_retrans_pkts}++;
      $self->{tx_amsdu_retrans_pkts} += $pkt->{amsdu_frame_count};
    }
  }

  if ($self->{last_ps_timestamp} == 0) {
    $self->{last_ps_timestamp} = $pkt->timestamp();
  }

  my $pkt_count = @{$self->{pkts}};

  # If this is a block-ack, then check for previous frames that would match.
  if ($pkt->type_subtype() eq "802.11 Block Ack (0x0019)") {
    my $ba_dup = 0;
    my $ba_tot = 0;
    my $transmitter = $pkt->transmitter();
    my $starting_seqno = $pkt->{ba_starting_seq};
    my $i;
    my $bitmap = $pkt->{ba_bitmap}; # 0100000000000000 for instance
    my $bi_as_long = 0;
    my $bi_mask = 0;
    my $q;
    my $last_timestamp = 0;
    my $glb;

    if ($pkt->transmitter() eq $self->{addr_a}) {
      $glb = $self->{glb_fh_ba_tx};
    }
    else {
      $glb = $self->{glb_fh_ba_rx};
    }
    for ($q = 0; $q < 8; $q++) {
      my $bmap_octet = substr($bitmap, $q * 2, 2);
      my $bmi = hex($bmap_octet);
      #print STDERR "bmap-octet: $bmap_octet bmi: " . hex($bmi) . "\n";
      $bi_as_long |= ($bmi << ($q * 8));
    }

    for ($i = 0; $i<$pkt_count; $i++) {
      my $tmp = $self->{pkts}[$i];
      #print "checking tmp-pkt frame: " . $tmp->{frame_num} . " seqno: " . $tmp->seqno();
      #print " transmitter: " . $tmp->transmitter();
      #print " pkt-rcvr: " . $pkt->receiver() . "\n";
      #print "Starting_seqno:$starting_seqno\n";
      if ($tmp->transmitter() eq $pkt->receiver()) {
        if (($tmp->seqno() >= $starting_seqno) && ($tmp->seqno() < ($starting_seqno + 64))) {
          # tmp pkt might match this BA bitmap..check closer.
          my $diff = $tmp->seqno() - $starting_seqno;
          if ($bi_as_long & (1 << $diff)) {
            # Found a matching frame.
            $bi_mask |= (1 << $diff);

            if ($tmp->block_acked_by() != -1) {
              # This seems to be a common thing, warn once and not again.
              if ($warn_dup_ba_once) {
                print "WARNING:  block-ack frame: " . $pkt->frame_num() . " acking frame: " .
                  $tmp->frame_num() . " already block-acked by frame: " . $tmp->block_acked_by() . ".  This warning will not be shown again.\n";
                $warn_dup_ba_once = 0;
              }
              $ba_dup++;
            }
            elsif ($tmp->acked_by() != -1) {
              print "WARNING:  block-ack frame: " . $pkt->frame_num() . " acking frame: " .
                $tmp->frame_num() . " already acked by frame: " . $tmp->acked_by() . "\n";
            }
            $tmp->set_block_acked_by($pkt->frame_num());
            $ba_tot++;

            # Only calculate timestamp if previous packet was last one ACKd and it is not a dummy
            # otherwise we probably failed to capture some frames.
            if ($i == ($pkt_count - 1)) {
              if ($tmp->{raw_pkt} ne "") {
                $last_timestamp = $tmp->timestamp();
              }
            }
          }
        }
      }
    }# for all pkts

    # See if we block-acked anything we could not find?
    if ($bi_mask != $bi_as_long) {
      my $missing = $bi_mask ^ $bi_as_long;
      my $missing_str = "";
      for ($i = 0; $i<64; $i++) {
        if ($missing & (1<<$i)) {
          my $missing_seqno = $starting_seqno + $i;
          $missing_str .= $missing_seqno . " ";

          # Add a dummy pkt
          my $dummy = Packet->new(dbg => "tid-add-pkt",
                                  frame_num => -1,
                                  receiver => $pkt->transmitter(),
                                  transmitter => $pkt->receiver(),
                                  data_subtype => "DUMMY_BA_ACKED",
                                  timestamp => $pkt->timestamp(),
                                  seqno => $missing_seqno,
                                  tid => $self->tidno());
          $dummy->set_block_acked_by($pkt->frame_num());
          push(@{$self->{pkts}}, $dummy);
          # A transmitting block-ack indicates we dropped pkts sent to us.
          if ($pkt->transmitter() eq $self->{addr_a}) {
            $self->{dummy_rx_pkts}++;
            $pkt->{dummy_rx_pkts}++;
          }
          else {
            $self->{dummy_tx_pkts}++;
            $pkt->{dummy_tx_pkts}++;
          }
          #print "pushing dummy pkt, seqno: $missing_seqno\n";
          $ba_tot++;
        }
      }
      print "WARNING:  block-ack frame: " . $pkt->frame_num() . " acked frames we did not capture, found-these: " . $bi_mask->as_hex .
        " acked these: " . $bi_as_long->as_hex . " missing: " . $missing->as_hex . "($missing_str), starting-seq-no: $starting_seqno\n";
    }

    my $new_ba = $ba_tot - $ba_dup;
    #my $fh_ba = $self->{fh_ba};
    my $ts_diff;
    if ($last_timestamp == 0) {
      $ts_diff = "0.0";
    }
    else {
      $ts_diff = sprintf("%.10f", $pkt->timestamp() - $last_timestamp);
    }
    my $ln = "" . $pkt->timestamp() . "\t" . $self->tidno() . "\t$ba_tot\t$ba_dup\t$new_ba\t$ts_diff\n";

    #print $fh_ba $ln; # Tid specific data file
    print $glb $ln; # Global data file
  }# if block-ack frame

  # Shift off old frames.
  while ($pkt_count > 0) {
    my $tmp = shift(@{$self->{pkts}});
    if (($tmp->timestamp() + 60 < $pkt->timestamp()) ||
        ($pkt_count > $max_pkt_store)) {
      if (! $tmp->was_acked()) {
        if ($tmp->wants_ack()) {
          if ($tmp->transmitter() eq $self->{addr_a}) {
            $self->{tx_no_ack_found_all}++;
            if ($tmp->{bytes_on_wire} > 1000) {
              print "WARNING:  did not find ack for BIG TX frame: " . $tmp->desc() . ", removing after processing frame: " . $pkt->frame_num() . "\n";
              $self->{tx_no_ack_found_big}++;
            }
            else {
              print "WARNING:  did not find ack for small TX frame: " . $tmp->desc() . ", removing after processing frame: " . $pkt->frame_num() . "\n";
            }
          }
          else {
            $self->{rx_no_ack_found_all}++;
            if ($tmp->{bytes_on_wire} > 1000) {
              print "WARNING:  did not find ack for BIG RX frame: " . $tmp->desc() . ", removing after processing frame: " . $pkt->frame_num() . "\n";
              $self->{rx_no_ack_found_big}++;
            }
            else {
              print "WARNING:  did not find ack for small RX frame: " . $tmp->desc() . ", removing after processing frame: " . $pkt->frame_num() . "\n";
            }
          }
        }
      }
      $pkt_count--;
      next; # Drop frames when we have more than $max_pkt_store or they are older than 1 minute ago
    }
    # Put this one back on
    unshift(@{$self->{pkts}}, $tmp);
    last;
  }

  if (0) { # Skip per-tid reporting files for now...global info seems enough
    my $tsp1 = $self->{last_ps_timestamp} + 1.0;
    my $gen_ps = $tsp1 < $pkt->{timestamp};
    #print STDERR "last-ps-timestamp: " . $self->{last_ps_timestamp} . " tsp1: $tsp1 gen-ps: $gen_ps "
    #  . $self->{last_ps_timestamp} . " pkt-ts: " . $pkt->{timestamp} . "\n";
    if ($gen_ps) {
      my $diff =  $pkt->{timestamp} - $self->{last_ps_timestamp};
      my $period_tot_pkts = $self->{tot_pkts} - $self->{last_tot_pkts};
      my $period_rx_pkts = $self->{rx_pkts} - $self->{last_rx_pkts};
      my $period_rx_amsdu_pkts = $self->{rx_amsdu_pkts} - $self->{last_rx_amsdu_pkts};
      my $period_rx_retrans_pkts = $self->{rx_retrans_pkts} - $self->{last_rx_retrans_pkts};
      my $period_rx_retrans_amsdu_pkts = $self->{rx_amsdu_retrans_pkts} - $self->{last_rx_amsdu_retrans_pkts};
      my $period_tx_pkts = $self->{tx_pkts} - $self->{last_tx_pkts};
      my $period_tx_amsdu_pkts = $self->{tx_amsdu_pkts} - $self->{last_tx_amsdu_pkts};
      my $period_tx_retrans_pkts = $self->{tx_retrans_pkts} - $self->{last_tx_retrans_pkts};
      my $period_tx_retrans_amsdu_pkts = $self->{tx_amsdu_retrans_pkts} - $self->{last_tx_amsdu_retrans_pkts};
      my $period_dummy_rx_pkts = $self->{dummy_rx_pkts} - $self->{last_dummy_rx_pkts};
      my $period_dummy_tx_pkts = $self->{dummy_tx_pkts} - $self->{last_dummy_tx_pkts};

      my $period_tot_pkts_ps = $period_tot_pkts / $diff;
      my $period_rx_pkts_ps = $period_rx_pkts / $diff;
      my $period_rx_amsdu_pkts_ps = $period_rx_amsdu_pkts / $diff;
      my $period_rx_retrans_pkts_ps = $period_rx_retrans_pkts / $diff;
      my $period_rx_retrans_amsdu_pkts_ps = $period_rx_retrans_amsdu_pkts / $diff;
      my $period_tx_pkts_ps = $period_tx_pkts / $diff;
      my $period_tx_amsdu_pkts_ps = $period_tx_amsdu_pkts / $diff;
      my $period_tx_retrans_pkts_ps = $period_tx_retrans_pkts / $diff;
      my $period_tx_retrans_amsdu_pkts_ps = $period_tx_retrans_amsdu_pkts / $diff;
      my $period_dummy_rx_pkts_ps = $period_dummy_rx_pkts / $diff;
      my $period_dummy_tx_pkts_ps = $period_dummy_tx_pkts / $diff;

      $self->{last_ps_timestamp} = $pkt->timestamp();
      $self->{last_tot_pkts} = $self->{tot_pkts};
      $self->{last_rx_pkts} = $self->{rx_pkts};
      $self->{last_rx_amsdu_pkts} = $self->{rx_amsdu_pkts};
      $self->{last_rx_retrans_pkts} = $self->{rx_retrans_pkts};
      $self->{last_rx_amsdu_retrans_pkts} = $self->{rx_amsdu_retrans_pkts};
      $self->{last_tx_pkts} = $self->{tx_pkts};
      $self->{last_tx_amsdu_pkts} = $self->{tx_amsdu_pkts};
      $self->{last_tx_retrans_pkts} = $self->{tx_retrans_pkts};
      $self->{last_tx_amsdu_retrans_pkts} = $self->{tx_amsdu_retrans_pkts};
      $self->{last_dummy_rx_pkts} = $self->{dummy_rx_pkts};
      $self->{last_dummy_tx_pkts} = $self->{dummy_tx_pkts};

      my $fh_ps = $self->{mcs_fh_ps};

      my $ln =  "" . $pkt->timestamp() . "\t" . $self->tidno() . "\t$diff\t$period_tot_pkts_ps\t" .
        "$period_rx_pkts_ps\t$period_rx_retrans_pkts_ps\t$period_rx_amsdu_pkts_ps\t$period_rx_retrans_amsdu_pkts_ps\t$period_dummy_rx_pkts_ps\t" .
          "$period_tx_pkts_ps\t$period_tx_retrans_pkts_ps\t$period_tx_amsdu_pkts_ps\t$period_tx_retrans_amsdu_pkts_ps\t$period_dummy_tx_pkts_ps\n";
      print $fh_ps $ln;
    }

    # Generate reporting data for this pkt
    my $fh = $self->{mcs_fh};
    my $ln = "" . $pkt->timestamp() . "\t" . $self->tidno() . "\t" . $pkt->datarate() . "\t" . $pkt->retrans() . "\n";

    print $fh $ln;
  }

  push(@{$self->{pkts}}, $pkt);
}

sub check_remaining_pkts {
  my $self = shift;

  my $pkt_count = @{$self->{pkts}};

  # Shift off old frames.
  while ($pkt_count > 0) {
    my $tmp = shift(@{$self->{pkts}});
    if (! $tmp->was_acked()) {
      if ($tmp->wants_ack()) {
        if ($tmp->transmitter() eq $self->{addr_a}) {
          $self->{tx_no_ack_found_all}++;
          if ($tmp->{bytes_on_wire} > 1000) {
            print "WARNING:  did not find ack for BIG TX frame: " . $tmp->desc() . ", removing at end of file.\n";
            $self->{tx_no_ack_found_big}++;
          }
          else {
            print "WARNING:  did not find ack for small TX frame: " . $tmp->desc() . ", removing at end of file.\n";
          }
        }
        else {
          $self->{rx_no_ack_found_all}++;
          if ($tmp->{bytes_on_wire} > 1000) {
            print "WARNING:  did not find ack for BIG RX frame: " . $tmp->desc() . ", removing at end of file.\n";
            $self->{rx_no_ack_found_big}++;
          }
          else {
            print "WARNING:  did not find ack for small RX frame: " . $tmp->desc() . ", removing at end of file.\n";
          }
        }
      }
    }
    $pkt_count--;
  }
}

sub get_pkts {
  my $self = shift;
  return @{$self->{pkts}};
}

sub tx_no_ack_found_all {
  my $self = shift;
  return $self->{tx_no_ack_found_all};
}

sub tx_no_ack_found_big {
  my $self = shift;
  return $self->{tx_no_ack_found_big};
}

sub rx_no_ack_found_all {
  my $self = shift;
  return $self->{rx_no_ack_found_all};
}

sub rx_no_ack_found_big {
  my $self = shift;
  return $self->{rx_no_ack_found_big};
}

sub printme {
  my $self = shift;
  print "   tidno: " . $self->tidno() . " pkt-count: " . $self->get_pkts()
    . " tx-pkts: " . $self->{tx_pkts} . " tx-retrans: " . $self->{tx_retrans_pkts}
    . " rx-pkts: " . $self->{rx_pkts} . " rx-retrans: " . $self->{rx_retrans_pkts}
    . " tx-no-acks-all: " . $self->{tx_no_ack_found_all} . " tx-no-acks-big: " . $self->{tx_no_ack_found_big}
    . " rx-no-acks-all: " . $self->{rx_no_ack_found_all} . " rx-no-acks-big: " . $self->{rx_no_ack_found_big}
    . "\n";
}

1;
