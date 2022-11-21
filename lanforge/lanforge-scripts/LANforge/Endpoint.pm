#!/usr/bin/perl

package LANforge::Endpoint;
use strict;

##################################################
## the object constructor                       ##
## To use:  $ep = LANforge::Endpoint->new();    ##
##     or:  $ep2 = $ep->new();                  ##
##################################################

sub new {
   my $proto = shift;
   my $class = ref($proto) || $proto;
   my $self  = {};

   $self->{name} = undef;

   bless( $self, $class );

   initDataMembers();

   return $self;
}

sub initDataMembers {
   my $self = shift;

   $self->{payload}                = undef;
   $self->{shelf_id}               = undef;
   $self->{card_id}                = undef;
   $self->{port_id}                = undef;
   $self->{endp_id}                = undef;
   $self->{endp_type}              = undef;
   $self->{pattern}                = undef;
   $self->{ip_port}                = undef;
   $self->{ip_tos}                 = undef;
   $self->{ip_addr}                = undef;
   $self->{dst_ip_port}            = undef;
   $self->{dst_ip_addr}            = undef;
   $self->{dst_mac}                = undef;
   $self->{src_addr}               = undef;
   $self->{role}                   = undef;
   $self->{ep_flags}               = undef;
   $self->{min_pkt_size}           = undef;
   $self->{max_pkt_size}           = undef;
   $self->{min_tx_rate}            = undef;
   $self->{max_tx_rate}            = undef;
   $self->{report_timer}           = undef;
   $self->{start_time}             = undef;
   $self->{stop_time}              = undef;
   $self->{cx_detected_dropped_rx} = undef;
   $self->{last_rpt}               = undef;
   $self->{rx_pkts}                = undef;
   $self->{tx_pkts}                = undef;
   $self->{tx_failed_pkts}         = undef;
   $self->{tx_failed_bytes}        = undef;
   $self->{rx_bytes}               = undef;
   $self->{tx_bytes}               = undef;
   $self->{rx_dropped_pkts} = undef;  # figure out by looking at gaps in pkt ids
   $self->{rx_dup_pkts}     = undef;
   $self->{rx_ooo_pkts}     = undef;
   $self->{rx_wrong_dev}    = undef;
   $self->{rx_crc_failed}   = undef;
   $self->{connection_dropped} = undef;
   $self->{real_tx_rate}       = undef;
   $self->{real_rx_rate}       = undef;
   $self->{counters}           = undef;
   $self->{avg_latency}        = undef;
   $self->{ttl}                = undef;
   $self->{filename}           = undef;
   $self->{send_bad_crc}       = undef;
   $self->{rx_drop_cx}         = undef;
   $self->{rx_drop_seq}        = undef;
   $self->{rx_bit_errors}      = undef;
   $self->{conn_estab}         = undef;
   $self->{tcp_retrans}        = undef;

   # WanLink (LANforge ICE) fields.
   $self->{cfg_latency}  = undef;
   $self->{max_jitter}   = undef;
   $self->{drop_freq}    = undef;
   $self->{dup_freq}     = undef;
   $self->{jitter_freq}  = undef;
   $self->{reord_freq}   = undef;
   $self->{max_buf}      = undef;
   $self->{extra_buf}    = undef;
   $self->{wan_paths}    = undef;
   $self->{record_q}     = undef;
   $self->{dump_file}    = undef;
   $self->{min_drop_amt} = undef;
   $self->{max_drop_amt} = undef;

   # VOIP fields.
   $self->{proxy_ip}               = undef;
   $self->{phone_num}              = undef;
   $self->{peer_phone_num}         = undef;
   $self->{min_rtp_port}           = undef;
   $self->{max_rtp_port}           = undef;
   $self->{reg_expire_timer}       = undef;
   $self->{sound_dev}              = undef;
   $self->{tx_sound_file}          = undef;
   $self->{rx_sound_file}          = undef;
   $self->{fc_delay}               = undef;
   $self->{min_ic_gap}             = undef;
   $self->{max_ic_gap}             = undef;
   $self->{loop_calls}             = undef;
   $self->{loop_wav_files}         = undef;
   $self->{call_setup_dist}        = undef;
   $self->{last_call_setup_time}   = undef;
   $self->{state_change_in}        = undef;
   $self->{min_call_duration}      = undef;
   $self->{max_call_duration}      = undef;
   $self->{register_state}         = undef;
   $self->{call_state}             = undef;
   $self->{msg_proto}              = undef;
   $self->{rtp_encoding}           = undef;
   $self->{latency}                = undef;
   $self->{rt_latency}             = undef;
   $self->{jitter}                 = undef;
   $self->{calls_attempted}        = undef;
   $self->{calls_completed}        = undef;
   $self->{calls_answered}         = undef;
   $self->{calls_connected}        = undef;
   $self->{calls_RHUP}             = undef;
   $self->{calls_failed}           = undef;
   $self->{calls_failed_404}       = undef;
   $self->{calls_failed_no_answer} = undef;
   $self->{calls_failed_busy}      = undef;
   $self->{ringing_timer}          = undef;
   $self->{rcvd_487_cancel}        = undef;

   # Armageddon fields - Added by Adam
   $self->{udp_src_min}  = undef;
   $self->{udp_src_max}  = undef;
   $self->{udp_dst_min}  = undef;
   $self->{udp_dst_max}  = undef;
   $self->{pps}          = undef;
   $self->{pkts_to_send} = undef;
   $self->{arm_flags}    = undef;
   $self->{src_mac_cnt}  = undef;
   $self->{dst_mac_cnt}  = undef;
   $self->{multi_pkt}    = undef;
   $self->{min_src_ip}   = undef;
   $self->{max_src_ip}   = undef;
   $self->{min_dst_ip}   = undef;
   $self->{max_dst_ip}   = undef;

}    #initDataMembers

# VOIP endpoints look like this:
#VoipEndp [voip1-B] (RUNNING, UDP_TRANSPORT, SAVE_RX_PCM, PLAY_AUDIO, RCV_CALL_ONLY)
#     Shelf: 1, Card: 2  Port: 0  Endpoint: 27  Type: VOIP
#     ProxyIP: 192.168.1.24  PhoneNum: 2102  PeerPhone: 2103
#     MinRtpPort: 10000  MaxRtpPort: 10002  RegExpireTimer: 300
#     SoundDev: /dev/dsp  TxSoundFile: /tmp/fvoice.wav  RxSoundFile: /tmp/pcm_rx.wav
#     FC-Delay: 5  MinInterCallGap: 5  MaxInterCallGap: 5
#     LoopCalls: FOREVER  LoopWaveFiles: 1  MinCallDuration: 30  Max: 30
#     RegisterState: REGISTERED  CallState: CALL_IN_PROGRESS  Protocol: SIP/G711U
#     RingingTimer: 10000ms  LastCallSetup: 12ms  StateChangeIn: 4s
#     RptTimer: 5000ms  RunningFor: 150446s  StopIn: 206276387s
#     LastRpt: 0.000 secs ago     RealWriteRate: 62044bps   RealReadRate: 62044bps
#     Latency:    -32 -:-24:- -10  [ 9 1 2 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ] (5)
#     RT-Latency: 0 -:73:- 1760  [ 5 0 1 0 0 0 0 2 2 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ] (5)
#     Jitter:     -20 -:-1:- 2010  [ 891 1 1968 95 0 0 1 0 5 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ] (5)
#     CallSetup:  0 -:13:- 37  [ 0 0 49 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ] (5)
#       CallsAttempted:  Total: 0           Time: 300000ms    Current: 0
#       CallsCompleted:  Total: 501         Time: 300000ms    Current: 1
#       CallsAnswered    Total: 502         Time: 300000ms    Current: 1
#       CallsConnected   Total: 0           Time: 300000ms    Current: 0
#       CallsRemoteHUP   Total: 501         Time: 300000ms    Current: 1
#       CallsFailed:     Total: 0           Time: 300000ms    Current: 0
#       RTP Pkts Tx:     Total: 7292502     Time: 300000ms    Current: 14361
#       RTP Pkts Rx:     Total: 7292442     Time: 300000ms    Current: 14361
#       RTP Bytes Tx:    Total: 1166800320  Time: 300000ms    Current: 2297760
#       RTP Bytes Rx:    Total: 1166790720  Time: 300000ms    Current: 2297760
#       RTP Pkts Dropped:   Total: 0           Time: 300000ms    Current: 0
#       RTP Pkts Dup:       Total: 0           Time: 300000ms    Current: 0
#       RTP Pkts OOO:       Total: 0           Time: 300000ms    Current: 0
#       CallsFailed-404  Total: 0           Time: 300000ms    Current: 0
#       CF 408 (No-Answer)  Total: 3           Time: 300000ms    Current: 3
#       CallsFailed-busy    Total: 0           Time: 300000ms    Current: 0
#       Rcvd 487 (Cancel)   Total: 4           Time: 300000ms    Current: 4

# A WanLink (LANforge ICE) endpoint's output from the CLI looks something like this
#WanLink [wl1-B] (NOT_RUNNING)
#     Shelf: 1, Card: 1  Port: 2  Endpoint: 10  Type: WAN_LINK
#     MaxTxRate: 56000bps  Latency: 0ms  MaxJitter: 0ms
#     DropFreq: 0  DupFreq: 0  ReorderFreq: 0  ExtraBuf: 64KB
#     RptTimer: 5000ms  RunningFor: 0s  StopIn: 0s  MaxBuf: 67050B
#     Cur Backlog: 0  Real Tx Rate: 0bps  WanPaths: 1
#       Rx Pkts:           Total: 0           Time: 300000ms    Current: 0
#       Rx Bytes:          Total: 0           Time: 300000ms    Current: 0
#       Tx OOO Pkts:       Total: 0           Time: 300000ms    Current: 0
#       Rx Dropped Pkts:   Total: 0           Time: 300000ms    Current: 0
#       Rx Dropped Bytes:  Total: 0           Time: 300000ms    Current: 0
#       Tx Duplicate Pkts: Total: 0           Time: 300000ms    Current: 0
#       Tx Pkts:           Total: 0           Time: 300000ms    Current: 0
#       Tx Bytes:          Total: 0           Time: 300000ms    Current: 0
#       Tx Failed Pkts:    Total: 0           Time: 300000ms    Current: 0
#       Tx Failed Bytes:   Total: 0           Time: 300000ms    Current: 0
#
#   Name    RxPkts  RxBytes Dropped MaxRate(bps) Latency Backlog TxPkts TxBytes
#   wp1      0       0       0       56000       6       0       0       0

# A Data-Generating (LANforge FIRE) endpoint's output from the CLI looks something like this
#Endpoint [endp-399-RX] (NOT_RUNNING, FIXED_PLD_SIZE, PHANTOM, RATE_CONSTANT, IP_PORT_AUTO)
#     Shelf: 1, Card: 1  Port: 409  Endpoint: 400 Type: LANFORGE_TCP  Pattern: INCREASING
#     MinTxRate: 9600bps  MaxTxRate: 9600bps  MinPktSize: 1472B  MaxPktSize: 1472B
#     DestMAC: 00 00 00 00 00 00   DestIpAddr: 0.0.0.0  DestIpPort: 0  Quiesce: 3
#     SrcMAC:  00 00 00 00 00 00   SrcIp:  0.0.0.0  IpPort:  0  IpTOS: DONT-SET  Priority: 0
#     Role: ACCEPT  RptTimer: 1000ms  RunningFor: 0s  StopIn: 0s
#     Latency: 0 -:0:- 0  [ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ] (1)
#     Last Rpt: 0.000 secs ago  RealTxRate: 0bps  RealRxRate: 0bps  TTL: 0
#     FileName:   SendBadCrc: 0  RcvBuf: 0  SndBuf: 0  CWND: 0
#     RxDrop%-SEQ:  0.0000  RxDrop%-CX: 0.0000  Conn-Timer: -1ms
#       Rx Pkts:           Total: 0           Time: 60s   Cur: 0         0/s
#       Rx Bytes:          Total: 0           Time: 60s   Cur: 0         0/s
#       Rx OOO Pkts:       Total: 0           Time: 60s   Cur: 0         0/s
#       RX Wrong Dev:      Total: 0           Time: 60s   Cur: 0         0/s
#       RX CRC Failed:     Total: 0           Time: 60s   Cur: 0         0/s
#       RX Bit Errors:     Total: 0           Time: 3s    Cur: 0         0/s
#       Rx Dropped Pkts:   Total: 0           Time: 3s    Cur: 0         0/s
#          Cx Detected:    0
#       Rx Duplicate Pkts: Total: 0           Time: 60s   Cur: 0         0/s
#       Tx Pkts:           Total: 0           Time: 60s   Cur: 0         0/s
#       Tx Bytes:          Total: 0           Time: 60s   Cur: 0         0/s
#       Tx Failed Pkts:    Total: 0           Time: 60s   Cur: 0         0/s
#       Tx Failed Bytes:   Total: 0           Time: 60s   Cur: 0         0/s
#       Conn Established:  Total: 0           Time: 30s   Cur: 0         0/s
#       TCP Retransmits:   Total: 0           Time: 3s    Cur: 0         0/s

sub decode {
   my $self = shift;
   my $txt  = shift;
   my @ta   = split( /\n/, $txt );
   my $i        = -1;
   my $got_endp = 0;
   my $got_wl   = 0;
   my $got_voip = 0;
   my $got_arm  = 0;

   print "Endpoint::decode, txt -:$txt:-\n";

   foreach my $ln (@ta) {
      $i++;

      next if ($ln =~ /^\s*$/);
      next if ($ln =~ /^\s*>>RSLT:/);
      next if ($ln =~ /(admin|default)\@btbits>>/i);
      #print "Line: -:$ln:-\n";

      #Endpoint [endp-34-TX] (NOT_RUNNING, RND_PLD_SIZE, RATE_BURSTY)
      #print STDERR "NAME:".$self->{name}."\n";
      if ( !defined( $self->{name} ) ) {
         if ( $ln =~ /Endpoint\s+\[(.*)\]\s+\((.*)\)/ ) {
            print "line has Endpoint\n";
            $self->name($1);    # set our name
            $self->ep_flags($2);
            $got_endp = 1;
            next;
         }
         elsif ( $ln =~ /WanLink\s+\[(.*)\]\s+\((.*)\)/ ) {
            print "line has Wanlink\n";
            $self->name($1);    # set our name
            $self->ep_flags($2);
            $got_wl = 1;
            next;
         }
         elsif ( $ln =~ /VoipEndp\s+\[(.*)\]\s+\((.*)\)/ ) {
            print "line has Voip\n";
            $self->name($1);    # set our name
            $self->ep_flags($2);
            $got_voip = 1;
            next;
         }
         elsif ( $ln =~ /ArmEndp\s+\[(.*)\]\s+\((.*)\)/ ) {
            # added by Adam 8-17-04
            print "line has Armg\n";
            $self->name($1);    # set our name
            $self->ep_flags($2);
            $got_arm = 1;
            next;
         }
         else {
            warn "$0:  Don't know about this endpoint: $ln\n";
         }
      }
      elsif (($got_endp + $got_wl + $got_arm) == 0) {
         my $nm = $self->{name};
         if ( $ln =~ /Endpoint\s+\[$nm\]\s+\((.*)\)/ ) {
            $self->ep_flags($1);
            #print "Set flags -:" . $self->ep_flags() . ":-  orig -:$1:-\n";
            $got_endp = 1;
            next;
         }
         elsif ( $ln =~ /WanLink\s+\[$nm\]\s+\((.*)\)/ ) {
            $self->ep_flags($1);
            #print "Set flags -:" . $self->ep_flags() . ":-  orig -:$1:-\n";
            $got_wl = 1;
            next;
         }
         elsif ( $ln =~ /ArmEndp\s+\[(.*)\]\s+\((.*)\)/ ) {
            $self->ep_flags($2);
            #print "Set flags -:" . $self->ep_flags() . ":-  orig -:$2:-\n";
            $got_arm = 1;
            next;
         }
         else {
            warn "$0:  Don't know about this endpoint, nm: $nm, ln: $ln\n";
         }
         next;
      }

#     Shelf: 1, Card: 1  Port: 3  Endpoint: 15  Type: CUSTOM_TCP  Pattern: CUSTOM
      if ($got_endp) {

         if ( $ln =~
/Shelf:\s+(\d+)\,*\s+Card:\s+(\d+)\s+Port:\s+(\d+)\s+Endpoint:\s+(\d+)\s+Type:\s+(\S+)\s+Pattern:\s+(\S+)/
           )
         {
            $self->shelf_id($1);
            $self->card_id($2);
            $self->port_id($3);
            $self->ep_id($4);
            $self->ep_type($5);
            $self->pattern($6);
            next;
         }

#     MinTxRate: 512000bps  MaxTxRate:  1024000bps  MinPktSize: 128B  MaxPktSize: 128B
         if ( $ln =~
/MinTxRate:\s+(\d+)bps\s+MaxTxRate:\s+(\d+)bps\s+MinPktSize:\s+(\d+)B\s+MaxPktSize:\s+(\d+)B/
           )
         {
            $self->min_tx_rate($1);
            $self->max_tx_rate($2);
            $self->min_pkt_size($3);
            $self->max_pkt_size($4);
            next;
         }

  #     DestMAC: 00 90 27 a2 9e 54   DestIpAddr: 172.1.2.201  DestIpPort:  33011
         if ( $ln =~
/DestMAC:\s+(([0-9a-fA-F]{2}[: ]){5}([0-9a-fA-F]{2}))\s+DestIpAddr:\s+(\S+)\s+DestIpPort:\s+(\d+)/
           )
         {
            $self->dest_mac($1);
            $self->dest_ip_addr($2);
            $self->dest_ip_port($3);
            next;
         }

#     SrcMAC: 00 c0 95 e2 4c 0c   SrcIp: 172.1.2.200  IpPort:  33011  IpTOS: 0x8
         if ( $ln =~
/SrcMAC:\s+(([0-9a-fA-F]{2}[: ]){5}([0-9a-fA-F]{2}))\s+SrcIp:\s+(\S+)\s+IpPort:\s+(\d+(-\d+)?)\s+IpTOS:\s+(\S+)/
           )
         {
            $self->src_mac($1);
            $self->ip_addr($2);
            $self->ip_port($3);
            $self->ip_tos($4);
            next;
         }

#     Role: CONNECT RptTimer: 3000ms  RunningFor: 1271256573s  StopIn: 0s
         if ( $ln =~
/Role:\s+(\S+)\s+RptTimer:\s+(\d+)ms\s+RunningFor:\s+(\d+)s\s+StopIn:\s+(\d+)s/
           )
         {
            $self->role($1);
            $self->report_timer($2);
            $self->running_for($3);
            $self->stop_in($4);
            next;
         }

         if ( $ln =~ /PktsToSend:\s+(\d+)/) {
             $self->pkts_to_send($4);
             next;
         }

# Latency: 0 -:0:- 0  [ 0 0 0 0 0 0 0 0 ] (0)
         if ( $ln =~ /Latency:\s+(\S+) -:(\S+):- (\S+)\s+\[ (.*) \]\s+\((\S+)\)/ ) {
            $self->min_lat($1);
            $self->avg_latency($2);
            $self->max_lat($3);
            $self->lat_buckets($4);
            $self->lat_bucket_size($5);
            next;
         }

#     Last Rpt: 0.000 secs ago     RealTxRate: 0bps  RealRxRate: 5bps TTL: 0
         if ( $ln =~
/Last[- ]Rpt:\s+(\S+) secs ago\s+RealTxRate:\s+(\d+)bps\s+RealRxRate:\s+(\d+)bps\s+TTL:\s+(\S+)/
           )
         {
            $self->last_rpt($1);
            $self->real_tx_rate($2);
            $self->real_rx_rate($3);
            $self->ttl($4);
            next;
         }

#     FileName:
         if ( $ln =~ /FileName:\s+(\S+)\s+SendBadCrc:\s+(\S+)/ ) {
            $self->filename($1);
            $self->send_bad_crc($2);
            next;
         }
         elsif ( $ln =~ /FileName:\s+SendBadCrc:\s+(\S+)/ ) {
            $self->filename("");
            $self->send_bad_crc($1);
            next;
         }

#     RxDrop%-SEQ:  0.0000  RxDrop%-CX: 12.1819
         if ($ln =~ /RxDrop\%-SEQ:\s+(\S+)\s+RxDrop\%-CX:\s+(\S+)/ ) {
            $self->rx_drop_seq($1);
            $self->rx_drop_cx($2);
            next;
         }

#     Multi-Conn: 0  Active-Connections: 0
#       Rx Pkts:           Total: 0             Time: 300000ms      Current: 0
         if ($ln =~ /Rx Pkts:\s+Total:\s+(\d+)/ ) {
            $self->rx_pkts($1);
            next;
         }

#       Rx Bytes:          Total: 2455112960    Time: 300000ms      Current: 0
         if ($ln =~ /Rx Bytes:\s+Total:\s+(\d+)/ ) {
            $self->rx_bytes($1);
            next;
         }

#       Rx OOO Pkts:       Total: 0             Time: 300000ms      Current: 0
         if ($ln =~ /Rx OOO Pkts:\s+Total:\s+(\d+)/ ) {
            $self->rx_ooo_pkts($1);
            next;
         }

#       RX Wrong Dev:      Total: 0             Time: 300000ms      Current: 0
#       RX CRC Failed:     Total: 0             Time: 300000ms      Current: 0
#       RX Bit Errors:     Total: 0           Time: 3s    Cur: 0         0/s
         if ( $ln =~ /RX Bit Errors:\s+Total:\s+(\d+)/ ) {
            $self->rx_bit_errors($1);
            next;
         }

#       Rx Dropped Pkts:   Total: 0             Time: 300000ms      Current: 0
         if ( $ln =~ /Rx Dropped Pkts:\s+Total:\s+(\d+)/ ) {
            $self->rx_dropped_pkts($1);
            next;
         }

#       Tx Pkts:           Total: 30288945      Time: 300000ms      Current: 0

         if ( $ln =~ /Tx Pkts:\s+Total:\s+(\d+)/ ) {
            $self->tx_pkts($1);
            next;
         }

#       Tx Bytes:          Total: 3876984960    Time: 300000ms      Current: 0
         if ( $ln =~ /Tx Bytes:\s+Total:\s+(\d+)/ ) {
            $self->tx_bytes($1);
            next;
         }

#       Conn Established:  Total: 0           Time: 30s   Cur: 0         0/s
         if ( $ln =~ /Conn Established:\s+Total:\s+(\d+)/ ) {
            $self->conn_estab($1);
            next; 
         }

#       TCP Retransmits:   Total: 0           Time: 3s    Cur: 0         0/s
         if ( $ln =~ /TCP Retransmits:\s+Total:\s+(\d+)/ ) {
            $self->tcp_retrans($1);
            next;
         }

         next if ($ln =~ /RX Wrong Dev:/ );
         next if ($ln =~ /RX CRC Failed:/);
         next if ($ln =~ /Multi-Conn:/ );
         next if ($ln =~ /Cx Detected:/);
         next if ($ln =~ /Rx Duplicate Pkts:/);
         next if ($ln =~ /Tx Failed Pkts:/);
         next if ($ln =~ /Tx Failed Bytes:/);
         next if ( $ln =~ /Pkt-Gaps:/ );
         next if ( $ln =~ /First-Rx:/);
         next if ( $ln =~ /RunningInGroup:/);
         next if ( $ln =~ /[RT]x Pkts .On Wire./);
         next if ( $ln =~ /[RT]x Bytes .On Wire./);
         next if ( $ln =~ /Conn Timeouts:/);


         warn( "Could not parse line -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n" );
         return;
      }

      # If we were a LANforge-FIRE endpoint.
      elsif ($got_wl) {
         print "PARSING WANLINK: $ln\n";
         if ( $ln =~
/Shelf:\s+(\d+)\,\s+Card:\s+(\d+)\s+Port:\s+(\d+)\s+Endpoint:\s+(\d+)\s+Type:\s+(\S+)/
           )
         {
            #     Shelf: 1, Card: 1  Port: 3  Endpoint: 4  Type: WAN_LINK
            $self->shelf_id($1);
            $self->card_id($2);
            $self->port_id($3);
            $self->ep_id($4);
            $self->ep_type($5);
            next;
         }

         #     Description:
         $i++;
         $ln = $ta[$i];
         if ( $ln =~ /Description:/ ) { # ignore
            next;
         }

         #     MaxTxRate: 4000000bps  Latency: 10ms  MaxJitter: 0ms
         if ( $ln =~
            /MaxTxRate:\s+(\d+)bps\s+Latency:\s+(\d+)ms\s+MaxJitter:\s+(\d+)ms/
           )
         {
            $self->max_tx_rate($1);
            $self->cfg_latency($2);
            $self->max_jitter($3);
            next;
         }

         # Case where MaxTxRate < 0. It shouldn't happen, but i added it
         # so the regression script wouldn't die - Adam.
         elsif ( $ln =~
            /MaxTxRate:\s+-(\d+)bps\s+Latency:\s+(\d+)ms\s+MaxJitter:\s+(\d+)ms/
           )
         {
            my $tmp = "-" . $1;
            $self->max_tx_rate($tmp);
            $self->cfg_latency($2);
            $self->max_jitter($3);
            next;
         }

         #     DropFreq: 0  DupFreq: 0  ReorderFreq: 0  ExtraBuf: 100KB
         if ( $ln =~
/DropFreq:\s+(\d+)\s+DupFreq:\s+(\d+)\s+ReorderFreq:\s+(\d+)\s+ExtraBuf:\s+(\d+)KB/
           )
         {
            $self->drop_freq($1);
            $self->dup_freq($2);
            $self->reord_freq($3);
            $self->extra_buf($4);
            next;
         }

     #     RptTimer: 5000ms  RunningFor: 277602940s  StopIn: 0s  MaxBuf: 103914B
         if ( $ln =~
/RptTimer:\s+(\d+)ms\s+RunningFor:\s+(\d+)s\s+StopIn:\s+(\d+)s\s+MaxBuf:\s+(\d+)B/
           )
         {
            $self->report_timer($1);
            $self->running_for($2);
            $self->stop_in($3);
            $self->max_buf($4);
            next;
         }

         #     Cur Backlog: 0  Real Tx Rate: 0bps  WanPaths: 1
         $i++;
         $ln = $ta[$i];
         if ( $ln =~
/Cur Backlog:\s+(\d+)\s+Real Tx Rate:\s+(\d+)bps\s+WanPaths:\s+(\d+)/
           )
         {
            $self->cur_backlog($1);
            $self->real_tx_rate($2);
            $self->wan_paths($3);
            next;
         }

         # JitterFreq: 1000  RecordQ: 0 Dump File:
         if ( $ln =~
            /JitterFreq:\s+(\d+)\s+RecordQ:\s+(\d+)\s+Dump File:\s+(\S*)/ )
         {
            $self->jitter_freq($1);
            $self->record_q($2);
            $self->dump_file($3);
            next;
         }

         # MinDropAmt: 0  MaxDropAmt: 0
         $ln = $ta[ ++$i ];
         if ( $ln =~ /MinDropAmt:\s+(\d+)\s+MaxDropAmt:\s+(\d+)/ ) {
            $self->min_drop_amt($1);
            $self->max_drop_amt($2);
            next;
         }

         if ( $ln =~ /\s+QueueDiscipline:/ ) { # ignore
            next;
         }

       #  Rx Pkts:           Total: 0             Time: 300000ms      Current: 0
         if ( $ln =~ /\s+Rx Pkts:\s+Total:\s+(\d+)/ ) {
            $self->rx_pkts($1);
            next;
         }

   # Adam - I am just matching the fields in these sections for now because I am
   # not using this data.  Will complete when the data is needed

       #  Rx Bytes:          Total: 2455112960    Time: 300000ms      Current: 0
         if ( $ln =~ /Rx Bytes:\s+Total:\s+(\d+)/ ) {
            $self->rx_bytes($1);
            next;
         }

      #       Tx OOO Pkts:       Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /Tx OOO Pkts:\s+Total:\s+(\d+)/ ) { 
            #$self->tx_ooo_pkts($1);
            next;
         }

      #       Rx Dropped Pkts:   Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /Rx Dropped Pkts:\s+Total:\s+(\d+)/ ) {
            $self->rx_dropped_pkts($1);
            next;
         }

     #       Rx Dropped Bytes:   Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /Rx Dropped Bytes:\s+Total:\s+(\d+)/ ) {
            # $self->rx_dropped_bytes($1);
            next;
         }

      #       Tx Duplicate Pkts: Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /Tx Duplicate Pkts:\s+Total:\s+(\d+)/ ) {
            #$self->tx_duplicate_pkts($1);
            next;
         }

      #       Tx Pkts:           Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /Tx Pkts:\s+Total:\s+(\d+)/ ) {
            #$self->tx_pkts_pkts($1);
            next;
         }

      #       Tx Bytes:          Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /Tx Bytes:\s+Total:\s+(\d+)/ ) {
            $self->tx_bytes($1);
            next;
         }

      #       Tx Failed Pkts:    Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /Tx Failed Pkts:\s+Total:\s+(\d+)/ ) {
            #$self->tx_failed_pkts($1);
            next;
         }

 #       Tx Failed Late Pkts:  Total: 5           Time: 60s   Cur: 5         0/s
         if ( $ln =~ /Tx Failed Late Pkts:\s+Total:\s+(\d+)/ ) { # ignore
            next;
         }

      #       Tx Failed Bytes:   Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /Tx Failed Bytes:\s+Total:\s+(\d+)/ ) {
            next;
            #$self->tx_bytes($1);
         }

 #       Tx Failed Late Pkts:  Total: 5           Time: 60s   Cur: 5         0/s
         if ( $ln =~ /Tx Failed Late Bytes:\s+Total:\s+(\d+)/ ) { # ignore
            next;
         }

         # Recorded Pkts:      Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /Recorded Pkts:/ ) {
            next;
         }

         #  Recorded Bytes:     Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /Recorded Bytes:/ ) {
            next;
         }

         # Rcrd Dropped Pkts:  Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /Rcrd Dropped Pkts:/ ) {
            next;
         }

         #  Rcrd Dropped Bytes: Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /Rcrd Dropped Bytes:/ ) {
            next;
         }
         else {
            warn( "LAST LINE? Could not parse line -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n" );
         }
         return;
         # return for now, the rest of wanlink stuff not completely implemented - Adam

         # TODO: Adam - redo the rest of this wanpath stuff

         # WanPaths
#         my $j      = 0;
#         my $wpaths = "";
#         for ( $j = 0 ; $j < $self->wan_paths() ; $j++ ) {
#
# #   Name    RxPkts  RxBytes Dropped MaxRate(bps) Latency Backlog TxPkts TxBytes
# #   wp1      0       0       0       56000       6       0       0       0
#            $i++;
#            $ln = $ta[$i];
#            if ( $ln =~
#/\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d)\s+(\d+)\s+(\d+)/
#              )
#            {
#               $wpaths .= $ln;
#            }
#            else {
#               warn( "Could not parse line -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n" );
#            }
#            $self->wan_path_rpts($wpaths);
#         }
#         return;
      }    # If we were a LANforge-ICE endpoint.

      elsif ($got_voip) {
         # Skip first line, we ignore VOIP flags for now.
         if ( $ln =~
/Shelf:\s+(\d+)\,\s+Card:\s+(\d+)\s+Port:\s+(\d+)\s+Endpoint:\s+(\d+)\s+Type:\s+(\S+)/
           )
         {

            #     Shelf: 1, Card: 1  Port: 3  Endpoint: 4  Type: VOIP
            $self->shelf_id($1);
            $self->card_id($2);
            $self->port_id($3);
            $self->ep_id($4);
            $self->ep_type($5);
            next;
         }

         #     ProxyIP: 192.168.1.24  PhoneNum: 2102  PeerPhone: 2103
         if ( $ln =~
/ProxyIP:\s+(\S+)\s+SipPort:\s+\S+\s+PhoneNum:\s+(\S+)\s+PeerPhone:\s+(\S+)/
           )
         {
            $self->proxy_ip($1);
            $self->phone_num($2);
            $self->peer_phone_num($3);
            next;
         }

#     MinRtpPort: 10000  MaxRtpPort: 10002  RegExpireTimer: 300
         if ( $ln =~
/MinRtpPort:\s+(\S+)\s+MaxRtpPort:\s+(\S+)\s+RegExpireTimer:\s+(\S+)/
           )
         {
            $self->min_rtp_port($1);
            $self->max_rtp_port($2);
            $self->reg_expire_timer($3);
            next;
         }

#     SoundDev: /dev/dsp  TxSoundFile: /tmp/graceland.wav  RxSoundFile: /tmp/pcm_rx.wav
         if ( $ln =~ /SoundDev:\s+(\S+)\s+TxSoundFile:\s+(.*\S)\s+JB-Bufs/ ) {
            $self->sound_dev($1);
            $self->tx_sound_file($2);
            next;
         }

         if ( $ln =~ /RxSoundFile:\s+(.*)  PESQ-Server/ ) {
            $self->rx_sound_file($3);
            next;
         }

         #     FC-Delay: 5  MinInterCallGap: 5  MaxInterCallGap: 5
         if ( $ln =~
/FC-Delay:\s+(\S+)\s+MinInterCallGap:\s+(\S+)\s+MaxInterCallGap:\s+(\S+)/
           )
         {
            $self->fc_delay($1);
            $self->min_ic_gap($2);
            $self->max_ic_gap($3);
            next;
         }

         #     LoopCalls: FOREVER  LoopWaveFiles: 1  MinCallDuration: 0
         if ( $ln =~
/LoopCalls:\s+(\S+)\s+LoopWaveFiles:\s+(\S+)\s+MinCallDuration:\s+(\S+)\s+Max:\s+(\S+)/
           )
         {
            $self->loop_calls($1);
            $self->loop_wav_files($2);
            $self->min_call_duration($3);
            $self->max_call_duration($4);
            next;
         }

#     RegisterState: REGISTERED  CallState: CALL_IN_PROGRESS  Protocol: SIP/G711U
         if ( $ln =~
/RegisterState:\s+(\S+)\s+CallState:\s+(\S+)\s+Protocol:\s+(\S+)\/(\S+)/
           )
         {
            $self->register_state($1);
            $self->call_state($2);
            $self->msg_proto($3);
            $self->rtp_encoding($4);
            next;
         }

         #     RingingTimer: 10000ms  LastCallSetup: 12ms  StateChangeIn: 4s
         if ( $ln =~
/RingingTimer:\s+(\S+)\s+LastCallSetup:\s+(\S+)ms\s+StateChangeIn:\s+(\S+)s/
           )
         {
            $self->ringing_timer($1);
            $self->last_call_setup_time($2);
            $self->state_change_in($3);
            next;
         }

         #     RptTimer: 5000ms  RunningFor: 150446s  StopIn: 206276387s
         if ( $ln =~
            /RptTimer:\s+(\d+)ms\s+RunningFor:\s+(\d+)s\s+StopIn:\s+(\d+)s/ )
         {
            $self->report_timer($1);
            $self->running_for($2);
            $self->stop_in($3);
            next;
         }

#     LastRpt: 0.000 secs ago     RealWriteRate: 62044bps   RealReadRate: 62044bps
         if ( $ln =~
/LastRpt:\s+(\S+) secs ago\s+RealWriteRate:\s+(\d+)bps\s+RealReadRate:\s+(\d+)bps/
           )
         {
            $self->last_rpt($1);
            $self->real_tx_rate($2);
            $self->real_rx_rate($3);
            next;
         }

         # Skip VAD settings

#     Latency:    -32 -:-24:- -10  [ 9 1 2 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ] (5)
         if ($ln =~ /\s+Latency:/) {
            $self->latency($ln);
            next;
         }

#     RT-Latency: 0 -:73:- 1760  [ 5 0 1 0 0 0 0 2 2 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ] (5)
         if ($ln =~ /RT-Latency:/) {
            $self->rt_latency($ln);
            next; 
         }

#     Jitter:     -20 -:-1:- 2010  [ 891 1 1968 95 0 0 1 0 5 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ] (5)
         if ($ln =~ /Jitter:/) {
            $self->jitter($ln);
            next;
         }

#     CallSetup:  0 -:13:- 37  [ 0 0 49 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ] (5)
         if ($ln =~ /CallSetup:/) {
            $self->call_setup_dist($ln);
            next;
         }

         #       CallsAttempted:  Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /CallsAttempted:\s+Total:\s+(\d+)/ ) {
            $self->calls_attempted($1);
            next;
         }

         #       CallsCompleted:  Total: 501         Time: 300000ms    Current: 1
         if ( $ln =~ /CallsCompleted:\s+Total:\s+(\d+)/ ) {
            $self->calls_completed($1);
            next;
         }

         #       CallsAnswered    Total: 502         Time: 300000ms    Current: 1
         if ( $ln =~ /CallsAnswered.*\s+Total:\s+(\d+)/ ) {
            $self->calls_answered($1);
            next;
         }

         #       CallsConnected   Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /CallsConnected.*\s+Total:\s+(\d+)/ ) {
            $self->calls_connected($1);
            next;
         }

         #       CallsRemoteHUP   Total: 501         Time: 300000ms    Current: 1
         if ( $ln =~ /CallsRemoteHUP.*\s+Total:\s+(\d+)/ ) {
            $self->calls_RHUP($1);
            next;
         }

         #       CallsFailed:     Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /CallsFailed:\s+Total:\s+(\d+)/ ) {
            $self->calls_failed($1);
            next;
         }

         #       RTP Pkts Tx:     Total: 7292502     Time: 300000ms    Current: 14361
         if ( $ln =~ /RTP Pkts Tx:\s+Total:\s+(\d+)/ ) {
            $self->tx_pkts($1);
            next;
         }

         if ($ln =~ /VAD:/) {
            next;
         }

         #       RTP Pkts Rx:     Total: 7292442     Time: 300000ms    Current: 14361
         if ( $ln =~ /RTP Pkts Rx:\s+Total:\s+(\d+)/ ) {
            $self->rx_pkts($1);
            next;
         }

  #       RTP Bytes Tx:    Total: 1166800320  Time: 300000ms    Current: 2297760
         if ( $ln =~ /RTP Bytes Tx:\s+Total:\s+(\d+)/ ) {
            $self->tx_bytes($1);
            next;
         }

  #       RTP Bytes Rx:    Total: 1166790720  Time: 300000ms    Current: 2297760
         if ( $ln =~ /RTP Bytes Rx:\s+Total:\s+(\d+)/ ) {
            $self->rx_bytes($1);
            next;
         }

     #       RTP Pkts Dropped:   Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /RTP Pkts Dropped:\s+Total:\s+(\d+)/ ) {
            $self->rx_dropped_pkts($1);
            next;
         }

         #       RTP Pkts Dup:   Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /RTP Pkts Dup:\s+Total:\s+(\d+)/ ) {
            $self->rx_dup_pkts($1);
            next;
         }

     #       RTP Pkts Dropped:   Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /RTP Pkts OOO:\s+Total:\s+(\d+)/ ) {
            $self->rx_ooo_pkts($1);
            next;
         }

         # Skip JB silence played, overruns, underruns
         #$i += 3;

        #       CallsFailed-404  Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /CallsFailed-404\s+Total:\s+(\d+)/ ) {
            $self->calls_failed_404($1);
            next;
         }

     #       CF 408 (No-Answer)  Total: 3           Time: 300000ms    Current: 3
         if ( $ln =~ /CF 408 \(No-Answer\)\s+Total:\s+(\d+)/ ) {
            $self->calls_failed_no_answer($1);
            next;
         }
         else {
            warn( "Could not parse line -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n" );
         }

        #       CallsFailed-busy Total: 0           Time: 300000ms    Current: 0
         if ( $ln =~ /CallsFailed-busy\s+Total:\s+(\d+)/ ) {
            $self->calls_failed_busy($1);
            next;
         }

     #       Rcvd 487 (Cancel)   Total: 4           Time: 300000ms    Current: 4
         if ( $ln =~ /Rcvd 487 \(Cancel\)\s+Total:\s+(\d+)/ ) {
            $self->rcvd_487_cancel($1);
            next;
         }
         warn( "Could not parse line -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n" );
         return;
      }
      elsif ($got_arm) {

         if ( $ln =~
/Shelf:\s+(\d+)\,\s+Card:\s+(\d+)\s+Port:\s+(\d+)\s+Endpoint:\s+(\d+)\s+Type:\s+(\S+)/
           )
         {    #Shelf: 1, Card: 1  Port: 1  Endpoint: 125  Type: ARM_UDP
            $self->shelf_id($1);
            $self->card_id($2);
            $self->port_id($3);
            $self->ep_id($4);
            $self->ep_type($5);
            next;
         }
         if ( $ln =~
/MinPktSz:\s+(\d+)B\s+MaxPktSz:\s+(\d+)B\s+Pps:\s+(\d+)/
           )
         {    #MinPktSz: 128B  MaxPktSz: 128B  Pps: 1  PktsToSend: 0
            $self->min_pkt_size($1);
            $self->max_pkt_size($2);
            $self->pps($3);
         }
         if ( $ln =~ /PktsToSend:\s+(\d+)/) {
             $self->pkts_to_send($4);
             next;
         }

         if ( $ln =~
/UdpSrcMin:\s+(\d+)\s+UdpSrcMax:\s+(\d+)\s+UdpDstMin:\s+(\d+)\s+UdpDstMax:\s+(\d+)/
           )
         {    #UdpSrcMin: 9  UdpSrcMax: 9  UdpDstMin: 9  UdpDstMax: 9
            $self->udp_src_min($1);
            $self->udp_src_max($2);
            $self->udp_dst_min($3);
            $self->udp_dst_max($4);
             next;
         }
         if ( $ln =~
/TcpSrcMin:\s+(\d+.\d+.\d+.\d+)\s+TcpSrcMax:\s+(\d+.\d+.\d+.\d+)\s+TcpDstMin:\s+(\d+.\d+.\d+.\d+)\s+TcpDstMax:\s+(\d+.\d+.\d+.\d+)/
           )
         { #TcpSrcMin: 192.168.99.2  TcpSrcMax: 192.168.99.2  TcpDstMin: 192.168.99.3  TcpDstMax: 192.168.99.3
            $self->min_src_ip($1);
            $self->max_src_ip($2);
            $self->min_dst_ip($3);
            $self->max_dst_ip($4);
             next;
         }
         if ( $ln =~
/SrcMac:\s+(\S\S \S\S \S\S \S\S \S\S \S\S)\s+SrcMacCount:\s+(\d+)\s+RepeatedPkts:\s+(\d+)/
           )
         {    #SrcMac: 00 e4 14 d5 e7 14   SrcMacCount: 0  RepeatedPkts: 0
            $self->src_mac($1);
            $self->src_mac_cnt($2);
            $self->multi_pkt($3);
             next;
         }
         if ( $ln =~
/DstMac:\s+(\S\S \S\S \S\S \S\S \S\S \S\S)\s+DstMacCount:\s+(\d+)\s+PeerRepeatedPkts:\s+(\d+)/
           )
         {    #DstMac: 00 30 f7 03 c5 4a   DstMacCount: 0  PeerRepeatedPkts: 0
            $self->dest_mac($1);
            $self->dst_mac_cnt($2);
            next;

            #$self->peer_multi_pkt($3);

         }
         if ( $ln =~
/RptTimer:\s+(\d+)ms\s+RunningFor:\s+(\d+)s\s+StopIn:\s+(\d+)s\s+ArmFlags:\s+\S+/
           )
         {    #RptTimer: 156746ms  RunningFor: 0s  StopIn: 0s  ArmFlags: 0x0
            $self->report_timer($1);
            $self->running_for($2);
            $self->stop_in($3);
            $self->arm_flags($4);
            next;
         }
         if ( $ln =~
            /LastRpt:\s+(\d+)\s+RealTxRate:\s+(\d+)bps\s+RealRxRate:\s+(\d+)bps/
           )
         {    #LastRpt:  137608640    RealTxRate: 0bps   RealRxRate: 0bps
                #	print "FOUND LINE 8\n";
                next;
         }

         warn( "Could not parse line -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n" );
      }
      else {
         warn( "Could not parse line -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n" );
      }
   }    #for all the lines in our buffer
}    #decode

sub decodePayload {
   my $self = shift;

   my $txt = shift;

   my @ta = split( /\n/, $txt );
   my $i;
   my $got_one = 0;

   #print "Endpoint::decodePayload, txt -:$txt:-\n";
   my $pld = "";

   for ( $i = 0 ; $i < @ta ; $i++ ) {
      my $ln = $ta[$i];

      #print "Line: -:$ln:-\n";

      #Endpoint [endp-34-TX] (NOT_RUNNING, RND_PLD_SIZE, RATE_BURSTY)
      my $nm = $self->{name};
      if ( $ln =~ /$nm payload\,/ ) {
         $got_one = 1;
         $i++;
         $ln = $ta[$i];
      }

#     Shelf: 1, Card: 1  Port: 3  Endpoint: 15  Type: CUSTOM_TCP  Pattern: CUSTOM
      if ($got_one) {

         if ( $ln =~ /(\S.*\S\s)\s\s.*/ ) {
            $pld .= "$1";
         }
         else {
            last;    #done
         }
      }
   }    #for

   # Trim off remaining white-space
   if ( $pld =~ /\s*(\S.*\S)\s*/ ) {
      $self->payload($1);
   }
   else {
      $self->payload("");
   }

}    #decodePayload

sub toStringBrief {
   my $self = shift;

   return "Endpoint: " . $self->name() . " (" . $self->ep_id() . ")";
   my $rv = "";
}    #toStringBrief

sub isCustom {
   my $self = shift;
   my $tp   = $self->ep_type();
   if (!defined $tp || ($tp eq "")) {
      return 0;
   }
   if ( ( $tp =~ /custom/ ) || ( $tp =~ /CUSTOM/ ) ) {
      return 1;
   }
   return 0;
}

sub usesIP() {
   my $self = shift;
   my $tp   = $self->ep_type();
   if ( ( $tp =~ /tcp/ ) || ( $tp =~ /udp/ ) ) {
      return 1;
   }
   return 0;
}    #usesIP

sub isOfType {
   my $self = shift;
   my $tp   = shift;

   my $_tp = $self->ep_type();
   if ( $_tp eq $tp ) {
      return 1;
   }

   # Deal with special (**puke**) cases
   if ( $_tp eq "LANFORGE" ) {
      return ( ( $tp eq "lf" ) || ( $tp eq "LF" ) );
   }

   if ( $_tp eq "LANFORGE_UDP" ) {
      return ( ( $tp eq "lf_udp" ) || ( $tp eq "LF_UDP" ) );
   }

   if ( $_tp eq "LANFORGE_TCP" ) {
      return ( ( $tp eq "lf_tcp" ) || ( $tp eq "LF_TCP" ) );
   }

   if ( $_tp eq "CUSTOM_ETHER" ) {
      return ( $tp eq "custom_ether" );
   }

   if ( $_tp eq "CUSTOM_TCP" ) {
      return ( $tp eq "custom_tcp" );
   }

   if ( $_tp eq "CUSTOM_UDP" ) {
      return ( $tp eq "custom_udp" );
   }

   if ( $_tp eq "WAN_LINK" ) {
      return ( $tp eq "wan_link" );
   }

   return 0;
}    #isOfType

# Not sure this works, and I know it does not deal well with WAN_LINK endpoints.
# TODO: Support WAN_LINK
sub toString {
   my $self = shift;

   my $rv = "";
   $rv = <<__END_TS;
Endpoint [$self->{name}] ($self->{ep_flags})
     Shelf: $self->{shelf_id}, Card: $self->{card_id}  Port: $self->{port_id}  Endpoint: self->{endp_id}  Type: self->{endp_type}  Pattern: $self->{pattern} 
     MinTxRate: self->{min_tx_rate}bps  MaxTxRate:  self->{max_tx_rate}bps  MinPktSize: self->min_pkt_sizeB  MaxPktSize: self->{max_pkt_size}B
     DestMAC: self->{dst_mac}   DestIpAddr: self->{dest_ip_addr}  DestIpPort:  self->{dst_ip_port}   
     SrcMAC: self->{src_mac}   SrcIP: self->{src_ip_addr}  IpPort:  self->{src_ip_port}  IpTOS:  self->{ip_tos}
     Role: self->{role} ReportTimer: self->{report_timer}ms  RunningFor: self->{running_for}s  StopIn: self->{stop_in}s
     Last Rpt: self->{last_rpt} secs ago     Real Tx Rate: self->{real_tx_rate}bps
self->{counters}

__END_TS

   return $rv;
}

sub getSetCmds {
   my $self = shift;

   my @rslt = ();
   my $i    = 0;

   if ( $self->ep_type() eq "WAN_LINK" ) {
      $rslt[$i] =
        (    "add_wl_endp "
           . $self->name() . " "
           . $self->shelf_id() . " "
           . $self->card_id() . " "
           . $self->port_id() . " "
           . $self->cfg_latency() . " "
           . $self->max_tx_rate() );
      $i++;

      $rslt[$i] =
        (    "set_wanlink_info "
           . $self->name() . " "
           . $self->max_tx_rate() . " "
           . $self->cfg_latency() . " " . " "
           . $self->max_jitter() . " "
           . $self->reord_freq() . " "
           . $self->extra_buffer() . " "
           . $self->drop_freq . " "
           . $self->dup_freq() );
      $i++;
   }

   # TODO:  Support other types of endpoints.
   #elsif ($self->ep_type() eq "WAN_LINK") {
   else {
      $rslt[$i] =
        (    "add_endp "
           . $self->name() . " "
           . $self->shelf_id() . " "
           . $self->card_id() . " "
           . $self->port_id() . " "
           . $self->getSetType() . " "
           . $self->getSetIpPort() . " "
           . $self->getBursty() . " "
           . $self->min_tx_rate() . " "
           . $self->max_tx_rate() . " "
           . $self->size_random() . " "
           . $self->min_pkt_size() . " "
           . $self->max_pkt_size() . " "
           . $self->pattern() . " "
           . $self->checksum() );
      $i++;

      $rslt[$i] = ( "set_endp_tos " . $self->name() . " " . $self->ip_tos() );
      $i++;
   }

   return @rslt;

}    #getSetCmds

sub getSetPayloadCmd {
   my $self = shift;

   return "set_endp_pay " . $self->name() . " custom " . $self->payload();
}    #getPayloadSetCmd

sub getSetType {
   my $self = shift;

   my $tp = $self->ep_type();
   if (!defined $tp || ($tp eq "")) {
      print STDERR "Endpoint type not defined\n";
      return "";
   }
   if ( $tp eq "LANFORGE" ) {
      return "lf";
   }
   if ( $tp eq "LANFORGE_UDP" ) {
      return "lf_udp";
   }
   if ( $tp eq "LANFORGE_TCP" ) {
      return "lf_tcp";
   }
   return $tp;
}    #getSetType

sub getSetIpPort {
   my $self = shift;

   if ( $self->isFlagSet("IP_PORT_AUTO") ) {
      return "-1";
   }
   return $self->ip_port();
}

##############################################
## methods to access per-object data        ##
##                                          ##
## With args, they set the value.  Without  ##
## any, they only retrieve it/them.         ##
##############################################

sub name {
   my $self = shift;
   if (@_) { $self->{name} = shift }
   return $self->{name};
}

sub setRandom {
   my $self = shift;
   my $val  = shift;
   if ( $val eq "YES" ) {
      $self->ensureFlagSet("RND_PLD_SIZE");
      $self->ensureFlagNotSet("FIXED_PLD_SIZE");
   }
   else {
      $self->ensureFlagNotSet("RND_PLD_SIZE");
      $self->ensureFlagSet("FIXED_PLD_SIZE");
   }

   #print "Endpoint::setBursty -:$val:-  flags: " . $self->ep_flags() . "\n";
}    #setBursty

sub size_random {
   my $self = shift;

   if ( $self->isFlagSet("RND_PLD_SIZE") ) {
      return "YES";
   }
   return "NO";
}

sub checksum {
   my $self = shift;

   if ( $self->isFlagSet("CHECKSUM") ) {
      return "YES";
   }
   return "NO";
}

sub setBursty {
   my $self = shift;
   my $val  = shift;
   if ( $val eq "YES" ) {
      $self->ensureFlagSet("RATE_BURSTY");
   }
   else {
      $self->ensureFlagNotSet("RATE_BURSTY");
   }

   #print "Endpoint::setBursty -:$val:-  flags: " . $self->ep_flags() . "\n";
}    #setBursty

sub getBursty {
   my $self = shift;

   #print "Endpoint::getBursty  flags: " . $self->ep_flags() . "\n";

   if ( $self->isFlagSet("RATE_BURSTY") ) {
      return "YES";
   }
   return "NO";
}

sub isRunning {
   my $self = shift;

   #print "Endpoint::getBursty  flags: " . $self->ep_flags() . "\n";

   if ( $self->isFlagSet("NOT_RUNNING") ) {
      return "NO";
   }
   return "YES";
}

sub ensureFlagSet {
   my $self = shift;
   my $flg  = shift;
   my $flgs = $self->ep_flags();
   if ( $flgs =~ /$flg/ ) {
      return;
   }
   else {
      $flgs .= "$flg ";
      $self->ep_flags($flgs);
   }
}    #ensureFlagSet

sub ensureFlagNotSet {
   my $self = shift;
   my $flg  = shift;
   my $flgs = $self->ep_flags();
   if ( $flgs =~ /$flg/ ) {
      $flgs =~ s/$flg//;
      $self->ep_flags($flgs);
   }
   else {
      return;
   }
}    #ensureFlagNotSet

sub isFlagSet {
   my $self     = shift;
   my $flg      = shift;
   my $cur_flgs = $self->ep_flags();

   #print "Endpoint::isFlagSet, flags -:$cur_flgs:-  flg -:$flg:-\n";
   if ( $cur_flgs =~ /$flg/ ) {
      return 1;
   }
   return 0;
}    #isFlagSet

sub ep_flags {
   my $self = shift;
   if (@_) { $self->{ep_flags} = shift }
   return $self->{ep_flags};
}

sub tx_bytes {
   my $self = shift;
   if (@_) { $self->{tx_bytes} = shift }
   return $self->{tx_bytes};
}

sub rx_bytes {
   my $self = shift;
   if (@_) { $self->{rx_bytes} = shift }
   return $self->{rx_bytes};
}

sub rx_pkts {
   my $self = shift;
   if (@_) { $self->{rx_pkts} = shift }
   return $self->{rx_pkts};
}

sub tx_pkts {
   my $self = shift;
   if (@_) { $self->{tx_pkts} = shift }
   return $self->{tx_pkts};
}

sub rx_dropped_pkts {
   my $self = shift;
   if (@_) { $self->{rx_dropped_pkts} = shift }
   return $self->{rx_dropped_pkts};
}

sub ttl {
   my $self = shift;
   if (@_) { $self->{ttl} = shift }
   return $self->{ttl};
}

sub rx_ooo_pkts {
   my $self = shift;
   if (@_) { $self->{rx_ooo_pkts} = shift }
   return $self->{rx_ooo_pkts};
}

sub rx_dup_pkts {
   my $self = shift;
   if (@_) { $self->{rx_dup_pkts} = shift }
   return $self->{rx_dup_pkts};
}

sub shelf_id {
   my $self = shift;
   if (@_) { $self->{shelf_id} = shift }
   return $self->{shelf_id};
}

sub card_id {
   my $self = shift;
   if (@_) { $self->{card_id} = shift }
   return $self->{card_id};
}

sub port_id {
   my $self = shift;
   if (@_) { $self->{port_id} = shift }
   return $self->{port_id};
}

sub ep_id {
   my $self = shift;
   if (@_) { $self->{endp_id} = shift }
   return $self->{endp_id};
}

sub ep_type {
   my $self = shift;
   if (@_) { $self->{endp_type} = shift }
   return $self->{endp_type};
}

sub payload {
   my $self = shift;
   if (@_) { $self->{payload} = shift }
   return $self->{payload};
}

sub pattern {
   my $self = shift;
   if (@_) { $self->{pattern} = shift }
   return $self->{pattern};
}

sub min_tx_rate {
   my $self = shift;
   if (@_) { $self->{min_tx_rate} = shift }
   return $self->{min_tx_rate};
}

sub max_tx_rate {
   my $self = shift;
   if (@_) { $self->{max_tx_rate} = shift }
   return $self->{max_tx_rate};
}

sub min_pkt_size {
   my $self = shift;
   if (@_) { $self->{min_pkt_size} = shift }
   return $self->{min_pkt_size};
}

sub max_pkt_size {
   my $self = shift;
   if (@_) { $self->{max_pkt_size} = shift }
   return $self->{max_pkt_size};
}

sub dest_mac {
   my $self = shift;
   if (@_) { $self->{dst_mac} = shift }
   return $self->{dst_mac};
}

sub dest_ip_addr {
   my $self = shift;
   if (@_) { $self->{dst_ip_addr} = shift }
   return $self->{dst_ip_addr};
}

sub dest_ip_port {
   my $self = shift;
   if (@_) { $self->{dst_ip_port} = shift }
   return $self->{dst_ip_port};
}

sub src_mac {
   my $self = shift;
   if (@_) { $self->{src_mac} = shift }
   return $self->{src_mac};
}

sub ip_addr {
   my $self = shift;
   if (@_) { $self->{ip_addr} = shift }
   return $self->{ip_addr};
}

sub ip_port {
   my $self = shift;
   if (@_) { $self->{ip_port} = shift }
   return $self->{ip_port};
}

sub ip_tos {
   my $self = shift;
   if (@_) { $self->{ip_tos} = shift }
   return $self->{ip_tos};
}

sub role {
   my $self = shift;
   if (@_) { $self->{role} = shift }
   return $self->{role};
}

sub report_timer {
   my $self = shift;
   if (@_) { $self->{report_timer} = shift }
   return $self->{report_timer};
}

sub running_for {
   my $self = shift;
   if (@_) { $self->{running_for} = shift }
   return $self->{running_for};
}

sub stop_in {
   my $self = shift;
   if (@_) { $self->{stop_in} = shift }
   return $self->{stop_in};
}

sub last_rpt {
   my $self = shift;
   if (@_) { $self->{last_rpt} = shift }
   return $self->{last_rpt};
}

sub real_tx_rate {
   my $self = shift;
   if (@_) { $self->{real_tx_rate} = shift }
   return $self->{real_tx_rate};
}

sub real_rx_rate {
   my $self = shift;
   if (@_) { $self->{real_rx_rate} = shift }
   return $self->{real_rx_rate};
}

sub cur_backlog {
   my $self = shift;
   if (@_) { $self->{cur_backlog} = shift }
   return $self->{cur_backlog};
}

sub avg_latency {
   my $self = shift;
   if (@_) { $self->{avg_latency} = shift }
   return $self->{avg_latency};
}

sub filename {
   my $self = shift;
   if (@_) { $self->{filename} = shift }
   return $self->{filename};
}

sub send_bad_crc {
   my $self = shift;
   if (@_) { $self->{send_bad_crc} = shift }
   return $self->{send_bad_crc};
}

sub rx_drop_seq {
   my $self = shift;
   if (@_) { $self->{rx_drop_seq} = shift }
   return $self->{rx_drop_seq};
}

sub rx_drop_cx {
   my $self = shift;
   if (@_) { $self->{rx_drop_cx} = shift }
   return $self->{rx_drop_cx};
}

sub rx_bit_errors {
   my $self = shift;
   if (@_) { $self->{rx_bit_errors} = shift }
   return $self->{rx_bit_errors};
}

sub conn_estab {
   my $self = shift;
   if (@_) { $self->{conn_estab} = shift }
   return $self->{conn_estab};
}

sub tcp_retrans {
   my $self = shift;
   if (@_) { $self->{tcp_retrans} = shift }
   return $self->{tcp_retrans};
}

sub min_lat {
   my $self = shift;
   if (@_) { $self->{min_lat} = shift }
   return $self->{min_lat};
}

sub max_lat {
   my $self = shift;
   if (@_) { $self->{max_lat} = shift }
   return $self->{max_lat};
}

sub lat_buckets {
   my $self = shift;
   if (@_) { $self->{lat_buckets} = shift }
   return $self->{lat_buckets};
}

sub lat_bucket_size {
   my $self = shift;
   if (@_) { $self->{lat_bucket_size} = shift }
   return $self->{lat_bucket_size};
}

sub cfg_latency {
   my $self = shift;
   if (@_) { $self->{cfg_latency} = shift }
   return $self->{cfg_latency};
}

sub max_jitter {
   my $self = shift;
   if (@_) { $self->{max_jitter} = shift }
   return $self->{max_jitter};
}

sub wan_paths {
   my $self = shift;
   if (@_) { $self->{wan_paths} = shift }
   return $self->{wan_paths};
}

sub drop_freq {
   my $self = shift;
   if (@_) { $self->{drop_freq} = shift }
   return $self->{drop_freq};
}

sub dup_freq {
   my $self = shift;
   if (@_) { $self->{dup_freq} = shift }
   return $self->{dup_freq};
}

sub jitter_freq {
   my $self = shift;
   if (@_) { $self->{jitter_freq} = shift }
   return $self->{jitter_freq};
}

sub record_q {
   my $self = shift;
   if (@_) { $self->{record_q} = shift }
   return $self->{record_q};
}

sub dump_file {
   my $self = shift;
   if (@_) { $self->{dump_file} = shift }
   return $self->{dump_file};
}

sub min_drop_amt {
   my $self = shift;
   if (@_) { $self->{min_drop_amt} = shift }
   return $self->{min_drop_amt};
}

sub max_drop_amt {
   my $self = shift;
   if (@_) { $self->{max_drop_amt} = shift }
   return $self->{max_drop_amt};
}

sub reord_freq {
   my $self = shift;
   if (@_) { $self->{reord_freq} = shift }
   return $self->{reord_freq};
}

sub max_buf {
   my $self = shift;
   if (@_) { $self->{max_buf} = shift }
   return $self->{max_buf};
}

sub extra_buf {
   my $self = shift;
   if (@_) { $self->{extra_buf} = shift }
   return $self->{extra_buf};
}

sub counters {
   my $self = shift;
   if (@_) { $self->{counters} = shift }
   return $self->{counters};
}

sub proxy_ip {
   my $self = shift;
   if (@_) { $self->{proxy_ip} = shift }
   return $self->{proxy_ip};
}

sub phone_num {
   my $self = shift;
   if (@_) { $self->{phone_num} = shift }
   return $self->{phone_num};
}

sub peer_phone_num {
   my $self = shift;
   if (@_) { $self->{peer_phone_num} = shift }
   return $self->{peer_phone_num};
}

sub min_rtp_port {
   my $self = shift;
   if (@_) { $self->{min_rtp_port} = shift }
   return $self->{min_rtp_port};
}

sub max_rtp_port {
   my $self = shift;
   if (@_) { $self->{max_rtp_port} = shift }
   return $self->{max_rtp_port};
}

sub reg_expire_timer {
   my $self = shift;
   if (@_) { $self->{reg_expire_timer} = shift }
   return $self->{reg_expire_timer};
}

sub sound_dev {
   my $self = shift;
   if (@_) { $self->{sound_dev} = shift }
   return $self->{sound_dev};
}

sub tx_sound_file {
   my $self = shift;
   if (@_) { $self->{tx_sound_file} = shift }
   return $self->{tx_sound_file};
}

sub rx_sound_file {
   my $self = shift;
   if (@_) { $self->{rx_sound_file} = shift }
   return $self->{rx_sound_file};
}

sub fc_delay {
   my $self = shift;
   if (@_) { $self->{fc_delay} = shift }
   return $self->{fc_delay};
}

sub min_ic_gap {
   my $self = shift;
   if (@_) { $self->{min_ic_gap} = shift }
   return $self->{min_ic_gap};
}

sub max_ic_gap {
   my $self = shift;
   if (@_) { $self->{max_ic_gap} = shift }
   return $self->{max_ic_gap};
}

sub loop_calls {
   my $self = shift;
   if (@_) { $self->{loop_calls} = shift }
   return $self->{loop_calls};
}

sub loop_wav_files {
   my $self = shift;
   if (@_) { $self->{loop_wav_files} = shift }
   return $self->{loop_wav_files};
}

sub min_call_duration {
   my $self = shift;
   if (@_) { $self->{min_call_duration} = shift }
   return $self->{min_call_duration};
}

sub state_change_in {
   my $self = shift;
   if (@_) { $self->{state_change_in} = shift }
   return $self->{state_change_in};
}

sub call_setup_dist {
   my $self = shift;
   if (@_) { $self->{call_setup_dist} = shift }
   return $self->{call_setup_dist};
}

sub last_call_setup_time {
   my $self = shift;
   if (@_) { $self->{last_call_setup_time} = shift }
   return $self->{last_call_setup_time};
}

sub max_call_duration {
   my $self = shift;
   if (@_) { $self->{max_call_duration} = shift }
   return $self->{max_call_duration};
}

sub register_state {
   my $self = shift;
   if (@_) { $self->{register_state} = shift }
   return $self->{register_state};
}

sub call_state {
   my $self = shift;
   if (@_) { $self->{call_state} = shift }
   return $self->{call_state};
}

sub msg_proto {
   my $self = shift;
   if (@_) { $self->{msg_proto} = shift }
   return $self->{msg_proto};
}

sub rtp_encoding {
   my $self = shift;
   if (@_) { $self->{rtp_encoding} = shift }
   return $self->{rtp_encoding};
}

sub latency {
   my $self = shift;
   if (@_) { $self->{latency} = shift }
   return $self->{latency};
}

sub rt_latency {
   my $self = shift;
   if (@_) { $self->{rt_latency} = shift }
   return $self->{rt_latency};
}

sub jitter {
   my $self = shift;
   if (@_) { $self->{jitter} = shift }
   return $self->{jitter};
}

sub calls_attempted {
   my $self = shift;
   if (@_) { $self->{calls_attempted} = shift }
   return $self->{calls_attempted};
}

sub calls_completed {
   my $self = shift;
   if (@_) { $self->{calls_completed} = shift }
   return $self->{calls_completed};
}

sub calls_answered {
   my $self = shift;
   if (@_) { $self->{calls_answered} = shift }
   return $self->{calls_answered};
}

sub calls_connected {
   my $self = shift;
   if (@_) { $self->{calls_connected} = shift }
   return $self->{calls_connected};
}

sub calls_RHUP {
   my $self = shift;
   if (@_) { $self->{calls_RHUP} = shift }
   return $self->{calls_RHUP};
}

sub calls_failed {
   my $self = shift;
   if (@_) { $self->{calls_failed} = shift }
   return $self->{calls_failed};
}

sub calls_failed_404 {
   my $self = shift;
   if (@_) { $self->{calls_failed_404} = shift }
   return $self->{calls_failed_404};
}

sub calls_failed_busy {
   my $self = shift;
   if (@_) { $self->{calls_failed_busy} = shift }
   return $self->{calls_failed_busy};
}

sub calls_failed_no_answer {
   my $self = shift;
   if (@_) { $self->{calls_failed_no_answer} = shift }
   return $self->{calls_failed_no_answer};
}

sub rcvd_487_cancel {
   my $self = shift;
   if (@_) { $self->{rcvd_487_cancel} = shift }
   return $self->{rcvd_487_cancel};
}

sub ringing_timer {
   my $self = shift;
   if (@_) { $self->{ringing_timer} = shift }
   return $self->{ringing_timer};
}

#
# Armageddon get/set functions - Added by Adam
#

sub udp_src_min {
   my $self = shift;
   if (@_) { $self->{udp_src_min} = shift }
   return $self->{udp_src_min};
}

sub udp_src_max {
   my $self = shift;
   if (@_) { $self->{udp_src_max} = shift }
   return $self->{udp_src_max};
}

sub udp_dst_min {
   my $self = shift;
   if (@_) { $self->{udp_dst_min} = shift }
   return $self->{udp_dst_min};
}

sub udp_dst_max {
   my $self = shift;
   if (@_) { $self->{udp_dst_max} = shift }
   return $self->{udp_dst_max};
}

sub pps {
   my $self = shift;
   if (@_) { $self->{pps} = shift }
   return $self->{pps};
}

sub pkts_to_send {
   my $self = shift;
   if (@_) { $self->{pkts_to_send} = shift }
   return $self->{pkts_to_send};
}

sub arm_flags {
   my $self = shift;
   if (@_) { $self->{arm_flags} = shift }
   return $self->{arm_flags};
}

sub src_mac_cnt {
   my $self = shift;
   if (@_) { $self->{src_mac_cnt} = shift }
   return $self->{src_mac_cnt};
}

sub dst_mac_cnt {
   my $self = shift;
   if (@_) { $self->{dst_mac_cnt} = shift }
   return $self->{dst_mac_cnt};
}

sub multi_pkt {
   my $self = shift;
   if (@_) { $self->{multi_pkt} = shift }
   return $self->{multi_pkt};
}

sub min_src_ip {
   my $self = shift;
   if (@_) { $self->{min_src_ip} = shift }
   return $self->{min_src_ip};
}

sub max_src_ip {
   my $self = shift;
   if (@_) { $self->{max_src_ip} = shift }
   return $self->{max_src_ip};
}

sub min_dst_ip {
   my $self = shift;
   if (@_) { $self->{min_dst_ip} = shift }
   return $self->{min_dst_ip};
}

sub max_dst_ip {
   my $self = shift;
   if (@_) { $self->{max_dst_ip} = shift }
   return $self->{max_dst_ip};
}

1;    # So the require or use succeeds (perl stuff)
__END__


# Plain Old Documentation (POD)

=head1 NAME
  Endpoint - class to implement LANforge Endpoints

=head1 SYNOPSIS

  use LANforge::Endpoint

  #################
  # class methods #
  #################
  $ob    = LANforge::Endpoint->new;

  #######################
  # object data methods #
  #######################

  ### get versions ###
  $name   = $ob->name;

  ### set versions ###
  $ob->name("endp-2-TX");

  ########################
  # other object methods #
  ########################

  $ob->decode("CLI output that contains this Endpoint's output");

=head1 DESCRIPTION

  The Endpoint class gives you some clever access into the Endpoint
  objects as sent by the LANforge CLI.

=head1 AUTHOR
  Ben Greear (greearb@candelatech.com)

  Copyright (c) 2001  Candela Technologies.  All rights reserved.
  This program is free software; you can redistribute it and/or
  modify it under the same terms as Perl itself.


=head1 VERSION
  Version 0.0.1  May 26, 2001

=end
