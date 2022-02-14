package Packet;

use warnings;
use strict;

use bignum;
use bigint;
our $d_counter = 0;

sub new {
  my $class = shift;
  my %options = @_;

  my $self = {
	      ba_valid => 0,
	      dbg => "NA",
	      priority => "",
	      wmm_info => "",
	      raw_pkt => "",
	      seqno => -1, # block-ack will not have a seqno
	      bytes_on_wire => 0,
	      acked_by => -1,
	      block_acked_by => -1,
	      retrans => 0,
	      seen_ip => 0,
	      timestamp => 0,
	      datarate => 0,
              ppdu_format => "UNKNOWN",
	      dummy_tx_pkts => 0,
	      dummy_rx_pkts => 0,
	      is_last_ampdu => 0,
	      is_ampdu => 0,
	      is_msdu => 0,
	      is_malformed => 0,
	      type_subtype => "UNKNOWN",
	      receiver => "UNKNOWN",
	      transmitter => "UNKNOWN",
	      tid => 17, # anything that does not specify a tid gets this.
	      %options,
	      amsdu_frame_count => 0,
	      ssi_sig_found => 0,
              ba_bitmap => "0000000000000000", # empty bitmap
              ba_starting_seq => 0, # needs to be initialized
              bss_color => 0,
              bss_color_known => 0,
              trigger_type_basic => 0, # basic trigger type relates to OFDMA
              trigger_type_num => -1,
              trigger_user_aid => "",
              trigger_user_ru_alloc => "",
              ps_awake => -1,
	     };

  bless($self, $class);

  if ($self->frame_num() == -1) {
    $self->{dummy_counter} = $d_counter;
    $d_counter++;
    print "Creating dummy pkt: " . $self->{dummy_counter} . "\n";
  }
  else {
    $self->{dummy_counter} = -1;
  }

  return($self);
}

sub desc {
  my $self = shift;
  my $rv = $self->frame_num() . " len: " . $self->{bytes_on_wire};
  if ($self->frame_num() == -1) {
    $rv = $rv . " dummy-counter: " . $self->{dummy_counter} . " dbg: " . $self->{dbg}
  }
  return $rv;
}

sub raw_pkt {
  my $self = shift;
  return $self->{raw_pkt};
}

sub append {
  my $self = shift;
  my $ln = shift;

  $self->{raw_pkt} .= $ln;

  #print "ln: $ln\n";

  if ($ln =~ /^\s*Internet Protocol Version/) {
    $self->{seen_ip} = 1;
    return;
  }

  if ($self->{seen_ip}) {
    if ($ln =~ /^\s*A-MSDU Subframe/) {
      $self->{seen_ip} = 0;
    }
    else {
      # Ignore
      return;
    }
  }

  if ($ln =~ /^\s*Transmitter address: .*\((\S+)\)/) {
    $self->{transmitter} = $1;
  }
  elsif ($ln =~ /^\s*Epoch Time:\s+(\S+)/) {
    #print "timestamp: $1\n";
    $self->{timestamp} = $1;
  }
  elsif ($ln =~ /^.* = This is the last subframe of this A-MPDU: True/) {
    $self->{is_last_ampdu} = 1;
  }
  elsif ($ln =~ /^.* = BSS Color known: Known/) {
    $self->{bss_color_known} = 1;
  }
  elsif ($ln =~ /^.* = BSS Color: (\S+)/) {
    $self->{bss_color} = hex($1);
  }
  elsif ($ln =~ /^.* = Priority: (.*) \(.*/) {
    $self->{priority} = " $1";
  }
  elsif ($ln =~ /^.* = Payload Type: A-MSDU/) {
    $self->{is_ampdu} = 1;
  }
  elsif ($ln =~ /^.* = Payload Type: MSDU/) {
    $self->{is_msdu} = 1;
  }
  elsif ($ln =~ /^.* = PPDU Format: (.*)/) {
    $self->{ppdu_format} = $1;
  }
  elsif ($ln =~ /^\s+PHY type: \S+\s+\((\S+)\)/) {
     # The PPDU Format matches first, so don't over-ride that if we found something already.
     if ($self->{ppdu_format} eq "UNKNOWN") {
        $self->{ppdu_format} = $1; # OFDM etc
     }
  }
  elsif ($ln =~ /^\s*\[Time delta from previous captured frame:\s+(\S+)/) {
    $self->{timedelta} = $1;
  }
  elsif ($ln =~ /^\s*Receiver address: .*\((\S+)\)/) {
    $self->{receiver} = $1;
  }
  elsif (($ln =~ /^\s*Fragment number: (\d+)/) ||
	 ($ln =~ /^.*\s+=\s+Fragment number: (\d+)/)) {
    $self->{fragno} = $1;
  }
  elsif (($ln =~ /^\s*Sequence number: (\d+)/) ||
	 ($ln =~ /^.*\s+=\s+Sequence number: (\d+)/)) {
    $self->{seqno} = $1;
  }
  elsif ($ln =~ /^\s*Type\/Subtype: (.*)/) {
    $self->{type_subtype} = $1;
  }
  elsif ($ln =~ /.* = (Trigger Type: .*)/) {
     # Differentiate some special subtypes.
     my $ttstr = $1;
     $self->{type_subtype} = $ttstr;
     if ($ttstr =~ /Trigger Type: .*\s\((\d+)\)/) {
        if ($1 eq "0") {
           $self->{trigger_type_basic} = 1;
        }
        $self->{trigger_type_num} = $1;
     }
  }
  elsif ($ln =~ /.* = AID12: (\S+)/) {
     if ($self->{trigger_type_basic}) {
        if ($self->{trigger_user_aid} ne "") {
           $self->{trigger_user_aid} .= ",";
        }
        $self->{trigger_user_aid} .= $1;
     }
  }
  elsif ($ln =~ /.* = RU Allocation: (.*)/) {
     if ($self->{trigger_type_basic}) {
        if ($self->{trigger_user_ru_alloc} ne "") {
           $self->{trigger_user_ru_alloc} .= ",";
        }
        $self->{trigger_user_ru_alloc} .= $1;
        #print("ru-alloc: " . $self->{trigger_user_ru_alloc} . "\n");
     }
  }
  elsif ($ln =~ /.*(\d) \.\.\.\. = PWR MGT:.*/) {
     if ($1 eq "0") {
        $self->{ps_awake} = 1;
     }
     else {
        $self->{ps_awake} = 0;
     }
  }
  elsif ($ln =~ /.* = Starting Sequence Number: (\d+)/) {
    $self->{ba_starting_seq} = $1;
  }
  elsif ($ln =~ /.*Malformed Packet.*/) {
    $self->{is_malformed} = 1;
  }
  elsif ($ln =~ /.* = TID for which a Basic BlockAck frame is requested: (\S+)/) {
    #print STDERR "tid: $1\n";
    $self->{ba_tid} = hex($1);
  }
  elsif ($ln =~ /^\s*Block Ack Bitmap: (\S+)/) {
    #print "ba-bitmap: $1\n"; # this bitmap needs to be at least 16 bytes
     if (length($1) != 16) {
        print("WARNING:  input-line: $.:  ba_bitmap is " . length($1) . " bytes instead of expected 16: " . $1);
        $self->{ba_bitmap} = "0000000000000000";  # default to something somewhat sane.
     }
     else {
        $self->{ba_bitmap} = $1;
     }
  }
  elsif ($ln =~ /.* = Retry: Frame is being retransmitted/) {
    $self->{retrans} = 1;
  }
  elsif ($ln =~ /^\s*VHT information/) {
    $self->{is_vht} = 1;
  }
  elsif ($ln =~ /^\s*Bandwidth: (.*)/) {
    $self->{bandwidth} = $1;
  }
  elsif ($ln =~ /^\s*User 0: MCS (.*)/) {
    $self->{mcs} = $1;
  }
  elsif ($ln =~ /.* = Spatial streams 0: (.*)/) {
    $self->{nss} = $1;
  }
  elsif ($ln =~ /.* = TID: (.*)/) {
    $self->{tid} = $1;
  }
  elsif ($ln =~ /.* = Payload Type: (.*)/) {
    $self->{payload_type} = $1;
  }
  elsif (($ln =~ /^\s+\[Data Rate: (.*)\]/) ||
	 ($ln =~ /^\s*Data [rR]ate: (.*)/)) {
    my $dr = $1;
    if ($dr =~ /(\S+) Mb/) {
      $self->{datarate} = $1;
    }
    else {
      print "ERROR:  Unknown datarate: $dr for frame: " . $self->frame_num() . "\n";
      $self->{datarate} = 0;
    }
  }
  elsif (($ln =~ /^\s*SSI Signal: (.*)/) ||
	 ($ln =~ /^\s*Antenna signal: (.*)/)) {
    if ($self->{ssi_sig_found} == 0) {
      $self->{ssi_combined} = $1;
      $self->{ssi_sig_found}++;
    }
    elsif ($self->{ssi_sig_found} == 1) {
      $self->{ssi_ant_0} = $1;
      $self->{ssi_sig_found}++;
    }
    elsif ($self->{ssi_sig_found} == 2) {
      $self->{ssi_ant_1} = $1;
      $self->{ssi_sig_found}++;
    }
    elsif ($self->{ssi_sig_found} == 3) {
      $self->{ssi_ant_2} = $1;
      $self->{ssi_sig_found}++;
    }
    elsif ($self->{ssi_sig_found} == 4) {
      $self->{ssi_ant_3} = $1;
      $self->{ssi_sig_found}++;
    }
  }
  # AMPDU and such...
  elsif ($ln =~ /^\s*A-MSDU Subframe #(\d+)/) {
    if ($1 > $self->{amsdu_frame_count}) {
      $self->{amsdu_frame_count} = $1;
    }
  }
  else {
    if ($self->type_subtype() eq "Beacon frame (0x0008)") {
      if ($ln =~ /^\s+(Ac Parameters ACI.*)/) {
	$self->{wmm_info} .= $ln;
      }
    }
  }
}

sub frame_num {
  my $self = shift;
  return $self->{frame_num};
}

sub type_subtype {
  my $self = shift;
  return $self->{type_subtype};
}

sub transmitter {
  my $self = shift;
  return $self->{transmitter};
}

sub datarate {
  my $self = shift;
  return $self->{datarate};
}

sub retrans {
  my $self = shift;
  return $self->{retrans};
}

sub seqno {
  my $self = shift;
  return $self->{seqno};
}

sub block_acked_by {
  my $self = shift;
  return $self->{block_acked_by};
}

sub acked_by {
  my $self = shift;
  return $self->{acked_by};
}

sub set_block_acked_by {
  my $self = shift;
  $self->{block_acked_by} = shift;
}

sub set_acked_by {
  my $self = shift;
  $self->{acked_by} = shift;
}

sub was_acked {
  my $self = shift;

  if ($self->block_acked_by() != -1) {
    return 1;
  }
  if ($self->acked_by() != -1) {
    return 1;
  }
  return 0;
}

sub wants_ack {
  my $self = shift;
  my $rcvr_b0 = substr($self->receiver(), 0, 1);
  if ($rcvr_b0 eq "U") {
    #print STDERR "wants-ack, receiver: " . $self->receiver() . "\n";
    #print STDERR $self->raw_pkt() . "\n";
    #exit(1);
    return 0;
  }
  my $rb0 = hex("$rcvr_b0");
  if ($rb0 & 0x1) {
    return 0;  # Don't ack bcast/bcast frames
  }

  if ($self->type_subtype() eq "802.11 Block Ack (0x0019)") {
    return 0;
  }

  if ($self->type_subtype() eq "802.11 Block Ack Req (0x0018)") {
    return 0;
  }

  if ($self->type_subtype() eq "VHT NDP Announcement (0x0015)") {
    return 0;
  }

  if ($self->type_subtype() eq "Clear-to-send (0x001c)") {
    return 0;
  }

  if ($self->type_subtype() eq "Request-to-send (0x001b)") {
    return 0;
  }

  if ($self->type_subtype() eq "Acknowledgement (0x001d)") {
    return 0;
  }

  if ($self->type_subtype() eq "Action No Ack (0x000e)") {
    return 0;
  }

  # TODO:  Need to parse QoS no-ack frames too, this will return false positives currently
  return 1;
}

sub timestamp {
  my $self = shift;
  return $self->{timestamp};
}

sub receiver {
  my $self = shift;
  return $self->{receiver};
}

sub tid {
  my $self = shift;
  if (exists $self->{ba_tid}) {
    return $self->{ba_tid};
  }
  return $self->{tid};
}

sub set_transmitter {
  my $self = shift;
  my $tx = shift;
  $self->{transmitter} = $tx;
}

sub set_receiver {
  my $self = shift;
  my $rx = shift;
  $self->{receiver} = $rx;
}

1;
