package LANforge::Port;
use strict;

##################################################
## the object constructor                       ##
## To use:  $ep = LANforge::Port->new();        ##
##     or:  $ep2 = $ep->new();                  ##
##################################################

# Must be kept in sync with Port.h, the GUI, gnuforge (gui_msgs.h), etc...
# Hopefully it won't change too much!

my $IF_down                 = 0;
my $IF_10bt_HD              = 1;
my $IF_10bt_FD              = 2;
my $IF_100bt_HD             = 3;
my $IF_100bt_FD             = 4;
my $IF_1000_HD              = 5;
my $IF_1000_FD              = 6;
my $IF_100bt4               = 7;
my $IF_auto_negotiate       = 8;
my $IF_link_OK              = 9;
my $IF_flow_control         = 10;
my $IF_negotiation_complete = 11;
my $IF_remote_fault         = 12;
my $IF_link_jabber          = 13;
my $IF_802_3X_flow_control  = 14;
my $IF_10bt_link            = 15;
my $IF_100bt_link           = 16;
my $IF_PHANTOM              = 17;
my $IF_ADMIN_DOWN           = 18;
my $IF_MII_PROBE_ERROR      = 19;
my $IF_ADV_10bt_HD      = 20;  #  What to advertise when in auto-negotiate mode.
my $IF_ADV_10bt_FD      = 21;
my $IF_ADV_100bt_HD     = 22;
my $IF_ADV_100bt_FD     = 23;
my $IF_ADV_1000_HD      = 24;
my $IF_ADV_1000_FD      = 25;
my $IF_ADV_100bt4       = 26;
my $IF_ADV_flow_control = 27;
my $IF_PROMISC          = 28;

sub new {
   my $proto = shift;
   my $class = ref($proto) || $proto;
   my $self  = {};

   $self->{shelf_id} = undef;
   $self->{card_id}  = undef;
   $self->{port_id}  = undef;

   bless( $self, $class );

   $self->initDataMembers();

   return $self;
}    #new

sub initDataMembers {
   my $self = shift;

   $self->{pps_tx}          = undef;
   $self->{pps_rx}          = undef;
   $self->{bps_tx}          = undef;
   $self->{bps_rx}          = undef;
   $self->{port_type}       = undef;
   $self->{cur_flags}       = undef;
   $self->{parent}          = undef;
   $self->{supported_flags} = undef;
   $self->{partner_flags}   = undef;
   $self->{advert_flags}    = undef;
   $self->{ip_addr}         = undef;
   $self->{ip_mask}         = undef;
   $self->{ip_gw}           = undef;
   $self->{ipv6_global}     = undef;
   $self->{ipv6_link}       = undef;
   $self->{ipv6_gw}         = undef;
   $self->{dns_servers}     = undef;
   $self->{mac_addr}        = undef;
   $self->{dev}             = undef;
   $self->{mtu}             = undef;
   $self->{tx_q_len}        = undef;
   $self->{rx_pkts}         = undef;
   $self->{tx_pkts}         = undef;
   $self->{rx_bytes}        = undef;
   $self->{tx_bytes}        = undef;
   $self->{rx_errors}       = undef;
   $self->{tx_errors}       = undef;
   $self->{rx_drop}         = undef;
   $self->{tx_drop}         = undef;
   $self->{multicasts}      = undef;
   $self->{collisions}      = undef;
   $self->{rx_len_err}      = undef;
   $self->{rx_overflow}     = undef;
   $self->{rx_crc}          = undef;
   $self->{rx_frame}        = undef;
   $self->{rx_fifo}         = undef;
   $self->{rx_missed}       = undef;
   $self->{tx_abort}        = undef;
   $self->{tx_carrier}      = undef;
   $self->{tx_fifo}         = undef;
   $self->{tx_heartbeat}    = undef;
   $self->{tx_window}       = undef;
   $self->{tx_bytes_ll}     = undef;
   $self->{tx_bytes_ll}     = undef;
   $self->{alias}           = undef;
   $self->{dhcp_client_id}  = undef;
   $self->{dhcp_vendor_id}  = undef;
}    #initDataMembers

sub isPhantom {
   my $self = shift;
   my $cf   = $self->{cur_flags};
   if ( $cf =~ /PHANTOM/ ) {
      return 1;
   }
   return 0;
}

# A Port's output from the CLI looks something like this
#Shelf: 1, Card: 1, Port: 5  Type: Ethernet  Alias: dut1
#   Current:     LINK-UP 100bt FULL-DUPLEX AUTO-NEGOTIATE NEG-COMPLETE
#   Supported:   10bt 100bt FULL-DUPLEX AUTO-NEGOTIATE
#   Partner:     10bt 100bt FULL-DUPLEX
#   Advertising: 10bt-HD 10bt-FD 100bt-HD 100bt-FD FLOW-CONTROL
#   IP: 0.0.0.0  MASK: 0.0.0.0  GW: 0.0.0.0
#   IPv6-Global: DELETED
#   IPv6-Link: DELETED
#   IPv6-Gateway: DELETED
#   MAC: 00:c0:95:e2:4c:0e  DEV: eth5  MTU: 1500  TX Queue Len: 400
#     Rxp: 88210  Txp: 0  Rxb: 5292600  Txb: 0  RxERR: 18338  TxERR: 0
#     RxDrop: 0  TxDrop: 0  Multi: 0  Coll: 0  RxLenERR: 0  RxOverFlow: 0
#     RxCRC: 0  RxFrame: 0  RxFifo: 0  RxMissed: 0  TxAbort: 0  TxCarrier: 0
#     TxFifo: 0  TxHeartBeat: 0  TxWindow: 0  RxBytesLL: 0  TxBytesLL: 0

sub decode {
   my $self = shift;
   my $txt  = shift;

   my $dvname = "";

   #print "Port::decode, txt -:$txt:-\n";
   if ( $txt =~ /DEV:\s+(\S+)\s+/g ) {
      $dvname = $1;
   }

   my @ta = split( /\n/, $txt );
   my $i;
   my $got_one = 0;
   for ( $i = 0 ; $i < @ta ; $i++ ) {
      my $ln = $ta[$i];

      #print "Got line -:$ln:-\n";

      #Shelf: 1, Card: 1, Port: 5  Type: Ethernet  Alias: dut1
      if (
         !(
               defined( $self->{shelf_id} )
            && defined( $self->{card_id} )
            && defined( $self->{port_id} )
         )
        )
      {
         if ( $ln =~
/Shelf:\s+(\d+)\,\s+Card:\s+(\d+)\,\s+Port:\s+(\S+)\s+Type:\s+(\S+)\s+Alias:\s+(\S+)/
           )
         {
            $self->shelf_id($1);
            $self->card_id($2);
            $self->port_id($3);
            $self->port_type($4);
            $self->alias($5);
            $got_one = 1;
         }
         elsif ( $ln =~
            /Shelf:\s+(\d+)\,\s+Card:\s+(\d+)\,\s+Port:\s+(\S+)\s+Type:\s+(\S+)/
           )
         {
            $self->shelf_id($1);
            $self->card_id($2);
            $self->port_id($3);
            $self->port_type($4);
            $self->alias("");
            $got_one = 1;
         }
      }
      else {
         my $sid = $self->shelf_id();
         my $cid = $self->card_id();
         my $pid = $self->port_id();
         if ( $dvname eq $pid ) {

            #print "Looking for match, ln -:$ln:-\n";
            if ( $ln =~
               /Shelf:\s+$sid\,\s+Card:\s+$cid\,\s+Port:\s+\S+\s+Type:\s+(\S+)/
              )
            {
               $self->port_type($1);
               $got_one = 1;
            }
         }
         else {

            #print "Looking for match, ln -:$ln:-\n";
            if ( $ln =~
               /Shelf:\s+$sid\,\s+Card:\s+$cid\,\s+Port:\s+$pid\s+Type:\s+(\S+)/
              )
            {
               $self->port_type($1);
               $got_one = 1;
            }
         }
      }

      #print "Got_one: $got_one\n";

      if ($got_one) {

         #   Current:     LINK-UP 100bt FULL-DUPLEX AUTO-NEGOTIATE NEG-COMPLETE
         $i++;
         $ln = $ta[$i];

         if ( $ln =~ /.*Parent\/Peer:\s+(\S+)\s+Rpt-Timer.*/ ) {
            $self->parent($1);
            $i++;
            $ln = $ta[$i];
         }
         elsif ( $ln =~ /.*Parent\/Peer:\s+Rpt-Timer.*/ ) {
            $self->parent("");
            $i++;
            $ln = $ta[$i];
         }

         if ( $ln =~ /\s+Current:\s+(.*)/ ) {
            $self->cur_flags($1);
         }
         else { die("Could not parse line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n"); }

         #   Supported:   10bt 100bt FULL-DUPLEX AUTO-NEGOTIATE
         $i++;
         $ln = $ta[$i];
         if ( $ln =~ /\sSupported:\s+(.*)/ ) {
            $self->supported_flags($1);
         }
         else { die("Could not parse line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n"); }

         #   Partner:     10bt 100bt FULL-DUPLEX
         $i++;
         $ln = $ta[$i];
         if ( $ln =~ /\s+Partner:\s+(.*)/ ) {
            $self->partner_flags($1);
         }
         else { die("Could not parse line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n"); }

         #   Advertising: 10bt-HD 10bt-FD 100bt-HD 100bt-FD FLOW-CONTROL
         $i++;
         $ln = $ta[$i];
         if ( $ln =~ /\s+Advertising:\s+(.*)/ ) {
            $self->advert_flags($1);
         }
         else { die("Could not parse line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n"); }

         #   IP: 0.0.0.0  MASK: 0.0.0.0  GW: 0.0.0.0
         $i++;
         $ln = $ta[$i];
         if ( $ln =~ /\s+IP:\s+(\S+)\s+MASK:\s+(\S+)\s+GW:\s+(\S+)/ ) {

            #print "Found ip_addr: $1\n";
            $self->ip_addr($1);

            #print "After setting ip_addr: $1, " . $self->ip_addr() . "\n";
            $self->ip_mask($2);
            $self->ip_gw($3);
         }
         else { die("Could not parse line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n"); }

         $i++;
         $ln = $ta[$i];
         if ( $ln =~ /\s+DNS[ -]Servers:\s+(.*)/ ) {
            $self->dns_servers($i);
            $i++;
            $ln = $ta[$i];
         }

         #   IPv6-Global: DELETED
         if ( $ln =~ /\s+IPv6-Global:\s+(\S+)/ ) {

            #print "Found ipv6_global: $1\n";
            $self->ipv6_global($1);

         #print "After setting ipv6_global: $1, " . $self->ipv6_global() . "\n";

            #   IPv6-Link: DELETED
            $i++;
            $ln = $ta[$i];
            if ( $ln =~ /\s+IPv6-Link:\s+(\S+)/ ) {

               #print "Found ipv6_link: $1\n";
               $self->ipv6_link($1);

             #print "After setting ipv6_link: $1, " . $self->ipv6_link() . "\n";
            }
            else { die("Could not parse line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n"); }

            #   IPv6-Gateway: DELETED
            $i++;
            $ln = $ta[$i];
            if ( $ln =~ /\s+IPv6-Gateway:\s+(\S+)/ ) {

               #print "Found ipv6_gw: $1\n";
               $self->ipv6_gw($1);

               #print "After setting ipv6_gw: $1, " . $self->ipv6_gw() . "\n";
            }
            else { die("Could not parse line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n"); }
            $i++;
            $ln = $ta[$i];
         }
         # stuff to skip
         if ( $ln =~ /\s+(Cfg|Rpt)-Secondary-IPs:/) {
            $i++;
            $ln = $ta[$i];
         }
         if ($ln =~ /\s+IPv6-Global:/) {
            $i++;
            $ln = $ta[$i];
         } # IPv6-Link:
         if ($ln =~ /\s+IPv6-Link:/) {
            $i++;
            $ln = $ta[$i];
         } # IPv6-Link:
         if ($ln =~ /\s+IPv6-Global:/) {
            $i++;
            $ln = $ta[$i];
         } #IPv6-Gateway:
         if ($ln =~ /\s+IPv6-Gateway:/) {
            $i++;
            $ln = $ta[$i];
         } #IPv6-Gateway:

         #   MAC: 00:c0:95:e2:4c:0e  DEV: eth5  MTU: 1500  TX Queue Len: 400
         if ( $ln =~
/\s+MAC:\s+(\S+)\s+DEV:\s+(\S+)\s+MTU:\s+(\d+)\s+TX[ -]Queue[ -]Len:\s+(\d+)/
           )
         {
            $self->mac_addr($1);
            $self->dev($2);
            $self->mtu($3);
            $self->tx_q_len($4);
         }
         else {
            die("MAC test could not parse line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n");
         }
         #print "MAC line $i\n";

         $i++;
         $ln = $ta[$i];
         if (( $ln =~ /\s+Bridge[ -]Port-Cost:.*/ ) ||
            ( $ln =~ /\s+Bus-Speed:.*/ ) ||
            ( $ln =~ /\s+LastDHCP:.*/ )) {
            # Ignore this line, skip on to the next
            #print "Bridge DHCP or Bus line $i\n";
            $i++;
            $ln = $ta[$i];
         }
         if (( $ln =~ /\s+Bridge[ -]Port-Cost:.*/ ) ||
            ( $ln =~ /\s+Bus-Speed:.*/ ) ||
            ( $ln =~ /\s+LastDHCP:.*/ )) {
            # Ignore this line, skip on to the next
            #print "DHCP, Bus or Bridge line $i\n";
            $i++;
            $ln = $ta[$i];
         }
         if (( $ln =~ /\s+Bridge[ -]Port-Cost:.*/ ) ||
            ( $ln =~ /\s+Bus-Speed:.*/ ) ||
            ( $ln =~ /\s+LastDHCP:.*/ )) {
            # Ignore this line, skip on to the next
            #print "Bus DHCP or Bridge line $i\n";
            $i++;
            $ln = $ta[$i];
         }

         if ($ln =~ /DHCP-Client-ID: (.*?)\s+DHCP-Vendor-ID: (.*)\s*$/) {
            $self->dhcp_client_id($1);
            $self->dhcp_vendor_id($2);
            $i++;
            $ln = $ta[$i];
         }
         # IPSec-Concentartor: 0.0.0.0  IPSec-Password: NONE  IPSec-Local-ID: NONE  IPSec-Remote-ID: NONE
         # careful, Concentrator is mis-spelled and will get corrected
         if ($ln =~
/IPSec-Con[a-z]+r:\s+([0-9.]+)\s+IPSec-Password:\s+([^ ]+)\s+IPSec-Local-ID:\s+([^ ])+\s+IPSec-Remote-ID:\s+([^ ]+)/
            )
         {
            $self->{'IPSec-Concentrator'} = $1 if (defined $1);
            $self->{'IPSec-Password'} = $1 if (defined $2);
            $self->{'IPSec-Local-ID'} = $1 if (defined $3);
            $self->{'IPSec-Remote-ID'} = $1 if (defined $4);
            $i++;
            $ln = $ta[$i];
         }

        #     pps_tx: 0  pps_rx: 0  bps_tx: 0  bps_rx: 0
         if ( $ln =~
/\s+pps_tx:\s+(\d+)\s+pps_rx:\s+(\d+)\s+bps_tx:\s+(\d+)\s+bps_rx:\s+(\d+)/
           )
         {
            $self->pps_tx($1);
            $self->pps_rx($2);
            $self->bps_tx($3);
            $self->bps_rx($4);
         }
         else { die("Could not parse pps line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n"); }

         #     Rxp: 88210  Txp: 0  Rxb: 5292600  Txb: 0  RxERR: 18338  TxERR: 0
         $i++;
         $ln = $ta[$i];
         if ( $ln =~
/\s+Rxp:\s+(\d+)\s+Txp:\s+(\d+)\s+Rxb:\s+(\d+)\s+Txb:\s+(\d+)\s+RxERR:\s+(\d+)\s+TxERR:\s+(\d+)/
           )
         {
            $self->rx_pkts($1);
            $self->tx_pkts($2);
            $self->rx_bytes($3);
            $self->tx_bytes($4);
            $self->rx_errors($5);
            $self->tx_errors($6);
         }
         else { die("Could not parse line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n"); }

       #     RxDrop: 0  TxDrop: 0  Multi: 0  Coll: 0  RxLenERR: 0  RxOverFlow: 0
         $i++;
         $ln = $ta[$i];
         if ( $ln =~
/\s+RxDrop:\s+(\d+)\s+TxDrop:\s+(\d+)\s+Multi:\s+(\d+)\s+Coll:\s+(\d+)\s+RxLenERR:\s+(\d+)\s+RxOverFlow:\s+(\d+)/
           )
         {
            $self->rx_drop($1);
            $self->tx_drop($2);
            $self->multicasts($3);
            $self->collisions($4);
            $self->rx_len_err($5);
            $self->rx_overflow($6);
         }
         else { die("Could not parse line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n"); }

    #     RxCRC: 0  RxFrame: 0  RxFifo: 0  RxMissed: 0  TxAbort: 0  TxCarrier: 0
         $i++;
         $ln = $ta[$i];
         if ( $ln =~
/\s+RxCRC:\s+(\d+)\s+RxFrame:\s+(\d+)\s+RxFifo:\s+(\d+)\s+RxMissed:\s+(\d+)\s+TxAbort:\s+(\d+)\s+TxCarrier:\s+(\d+)/
           )
         {
            $self->rx_crc($1);
            $self->rx_frame($2);
            $self->rx_fifo($3);
            $self->rx_missed($4);
            $self->tx_abort($5);
            $self->tx_carrier($6);
         }
         else { die("Could not parse line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n"); }

#     TxFifo: 0  TxHeartBeat: 0  TxWindow: 0  TxCompressed: 0  RxCompr: 0  (This is pre 5.2.3 API)
         $i++;
         $ln = $ta[$i];
         if ( $ln =~
/\s+TxFifo:\s+(\d+)\s+TxHeartBeat:\s+(\d+)\s+TxWindow:\s+(\d+)\s+TxCompressed:\s+(\d+)\s+RxCompr:\s+(\d+)/
           )
         {
            $self->tx_fifo($1);
            $self->tx_heartbeat($2);
            $self->tx_window($3);
         }
         elsif ( $ln =~
/\s+TxFifo:\s+(\d+)\s+TxHeartBeat:\s+(\d+)\s+TxWindow:\s+(\d+)\s+RxBytesLL:\s+(\d+)\s+TxBytesLL:\s+(\d+)/
           )
         {
            $self->tx_fifo($1);
            $self->tx_heartbeat($2);
            $self->tx_window($3);
            $self->rx_bytes_ll($4);
            $self->tx_bytes_ll($5);
         }
         else { die("Could not parse line[$i] -:$ln:-\n ".__PACKAGE__.".".__FILE__.".".__LINE__."\n($txt)\n"); }

         return;
      }    #if found the beginning for the/a endpoint
   }    #for all the lines in our buffer
}    #decode

sub toStringBrief {
   my $self = shift;

   return ( "Port: "
        . $self->{shelf_id} . "."
        . $self->{card_id} . "."
        . $self->{port_id} . " ("
        . $self->{dev}
        . ")" );
}

sub toString {
   my $self = shift;

   my $rv = "";
   $rv = <<__END_TS;
Shelf: $self->{shelf_id}, Card: $self->{card_id}, Port: $self->{port_id} Type: $self->{port_type}  Alias: $self->{alias}
   Parent:      $self->{parent}
   Current:     $self->{cur_flags}
   Supported:   $self->{supported_flags}
   Partner:     $self->{partner_flags}
   Advertising: $self->{advert_flags}
   IP: $self->{ip_addr}  MASK: $self->{ip_mask}  GW: $self->{ip_gw}
   DNS Servers: $self->{dns_servers}
   IPv6-Global: $self->{ipv6_global}
   IPv6-Link: $self->{ipv6_link}
   IPv6-Gateway: $self->{ipv6_gw}
   MAC: $self->{mac_addr}  DEV: $self->{dev}  MTU: $self->{mtu}  TX Queue Len: $self->{tx_q_len}
     Rxp: $self->{rx_pkts}  Txp: $self->{tx_pkts}  Rxb: $self->{rx_bytes}  Txb: $self->{tx_bytes}  RxERR: $self->{rx_errors}  TxERR: $self->{tx_errors}
     RxDrop: $self->{rx_drop}  TxDrop: $self->{tx_drop}  Multi: $self->{multicasts}  Coll: $self->{collisions}  RxLenERR: $self->{rx_len_err}  RxOverFlow: $self->{rx_overflow}
     RxCRC: $self->{rx_crc}  RxFrame: $self->{rx_frame}  RxFifo: $self->{rx_fifo}  RxMissed: $self->{rx_missed}  TxAbort: $self->{tx_abort}  TxCarrier: $self->{tx_carrier}
     TxFifo: $self->{tx_fifo}  TxHeartBeat: $self->{tx_heartbeat}  TxWindow: $self->{tx_window}  RxBytesLL: $self->{rx_bytes_ll}  TxBytesLL: $self->{tx_bytes_ll}

__END_TS

   return $rv;
}

# Sets IP & MAC information
sub getSetCmd {
   my $self = shift;
   my $rv =
     (    "set_port "
        . $self->shelf_id() . " "
        . $self->card_id() . " "
        . $self->port_id . " "
        . $self->ip_addr() . " "
        . $self->ip_mask() . " "
        . $self->ip_gw()
        . " NA NA "
        . $self->mac_addr()
        . " NA NA" );
   return $rv;
}

sub getDeleteCmd {
   my $self = shift;
   my $rv;
   if ( $self->dev() ) {
      $rv =
        (    "rm_vlan "
           . $self->shelf_id() . " "
           . $self->card_id() . " "
           . $self->dev() );
   }
   else {
      $rv =
        (    "rm_vlan "
           . $self->shelf_id() . " "
           . $self->card_id() . " "
           . $self->port_id() );
   }
   return $rv;
}

sub isMacVlan {
   my $self = shift;
   if ( $self->{port_type} eq "MacVLAN" ) {
      return 1;
   }
   return 0;
}

sub is8021qVlan {
   my $self = shift;
   if ( $self->{port_type} eq "Vlan" ) {
      return 1;
   }
   return 0;
}

# Set MTU only
sub getSetMtuCmd {
   my $self = shift;
   my $rv =
     (    "set_port "
        . $self->shelf_id() . " "
        . $self->card_id() . " "
        . $self->port_id()
        . " NA NA NA NA NA NA "
        . $self->mtu()
        . " NA" );
   return $rv;
}

# Set tx-queue-length only
sub getSetTxQueueLenCmd {
   my $self = shift;
   my $rv =
     (    "set_port "
        . $self->shelf_id() . " "
        . $self->card_id() . " "
        . $self->port_id()
        . " NA NA NA NA NA NA NA "
        . $self->tx_q_len() );
   return $rv;
}

#set rate (current flags) only
sub getSetRateCmd {
   my $self = shift;
   my $rv =
     (    "set_port "
        . $self->shelf_id() . " "
        . $self->card_id() . " "
        . $self->port_id()
        . " NA NA NA NA " );
   my $i = 0;
   if ( $self->isAutoNegotiate() ) {
      $i |= ( 1 << $IF_auto_negotiate );
   }
   else {
      if ( $self->isCurrent("10bt-HD") ) {
         $i |= ( 1 << $IF_10bt_HD );
      }
      elsif ( $self->isCurrent("10bt-FD") ) {
         $i |= ( 1 << $IF_10bt_FD );
      }
      elsif ( $self->isCurrent("100bt-HD") ) {
         $i |= ( 1 << $IF_100bt_HD );
      }
      elsif ( $self->isCurrent("100bt-FD") ) {
         $i |= ( 1 << $IF_100bt_FD );
      }
   }

   if ( $self->isAdvertising("10bt-HD") ) {
      $i |= ( 1 << $IF_ADV_10bt_HD );
   }
   if ( $self->isAdvertising("10bt-FD") ) {
      $i |= ( 1 << $IF_ADV_10bt_FD );
   }
   if ( $self->isAdvertising("100bt-HD") ) {
      $i |= ( 1 << $IF_ADV_100bt_HD );
   }
   if ( $self->isAdvertising("100bt-FD") ) {
      $i |= ( 1 << $IF_ADV_100bt_FD );
   }
   if ( $self->isAdvertising("FLOW-CONTROL") ) {
      $i |= ( 1 << $IF_ADV_flow_control );
   }

   $rv .= "$i NA NA NA";

   return $rv;
}    #getSetRateCmd

sub setRate {
   my $self = shift;
   my $val  = shift;

   if ( $val eq "auto" ) {
      $self->ensureCurSet("AUTO-NEGOTIATE");
   }
   else {
      $self->cur_flags($val);
   }
}    #setRate

sub ensureCurSet {
   my $self = shift;
   my $flg  = shift;
   my $flgs = $self->cur_flags();
   if ( $flgs =~ /$flg/ ) {
      return;
   }
   else {
      $flgs .= "$flg ";
      $self->cur_flags($flgs);
   }
}

sub ensureCurNotSet {
   my $self = shift;
   my $flg  = shift;
   my $flgs = $self->cur_flags();
   if ( $flgs =~ /$flg/ ) {
      $flgs =~ s/$flg //;
      $self->cur_flags($flgs);
   }
   else {
      return;
   }
}

sub isAutoNegotiate {
   my $self = shift;
   return $self->isCurrent("AUTO-NEGOTIATE");
}

sub isAdvertising {
   my $self = shift;
   my $flg  = shift;
   my $flgs = $self->advert_flags();
   if ( $flgs =~ /$flg/ ) {
      return 1;
   }
   return 0;
}    #isAdvertisting (flag set)

sub isCurrent {
   my $self     = shift;
   my $flg      = shift;
   my $cur_flgs = $self->cur_flags();
   if ( $cur_flgs =~ /$flg/ ) {
      return 1;
   }
   return 0;
}    #isCurrent (flag set)

##############################################
## methods to access per-object data        ##
##                                          ##
## With args, they set the value.  Without  ##
## any, they only retrieve it/them.         ##
##############################################

sub pps_tx {
   my $self = shift;
   if (@_) { $self->{pps_tx} = shift }
   return $self->{pps_tx};
}

sub pps_rx {
   my $self = shift;
   if (@_) { $self->{pps_rx} = shift }
   return $self->{pps_rx};
}

sub bps_tx {
   my $self = shift;
   if (@_) { $self->{bps_tx} = shift }
   return $self->{bps_tx};
}

sub bps_rx {
   my $self = shift;
   if (@_) { $self->{bps_rx} = shift }
   return $self->{bps_rx};
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

sub port_type {
   my $self = shift;
   if (@_) { $self->{port_type} = shift }
   return $self->{port_type};
}

sub cur_flags {
   my $self = shift;
   if (@_) { $self->{cur_flags} = shift }
   return $self->{cur_flags};
}

sub parent {
   my $self = shift;
   if (@_) { $self->{parent} = shift }
   return $self->{parent};
}

sub supported_flags {
   my $self = shift;
   if (@_) { $self->{supported_flags} = shift }
   return $self->{supported_flags};
}

sub partner_flags {
   my $self = shift;
   if (@_) { $self->{partner_flags} = shift }
   return $self->{partner_flags};
}

sub advert_flags {
   my $self = shift;
   if (@_) { $self->{advert_flags} = shift }
   return $self->{advert_flags};
}

sub ip_addr {
   my $self = shift;
   if (@_) { $self->{ip_addr} = shift }
   return $self->{ip_addr};
}

sub ip_mask {
   my $self = shift;
   if (@_) { $self->{ip_mask} = shift }
   return $self->{ip_mask};
}

sub ip_gw {
   my $self = shift;
   if (@_) { $self->{ip_gw} = shift }
   return $self->{ip_gw};
}

sub ipv6_global {
   my $self = shift;
   if (@_) { $self->{ipv6_global} = shift }
   return $self->{ipv6_global};
}

sub ipv6_link {
   my $self = shift;
   if (@_) { $self->{ipv6_link} = shift }
   return $self->{ipv6_link};
}

sub ipv6_gw {
   my $self = shift;
   if (@_) { $self->{ipv6_gw} = shift }
   return $self->{ipv6_gw};
}

sub dns_servers {
   my $self = shift;
   if (@_) { $self->{dns_servers} = shift }
   return $self->{dns_servers};
}

sub mac_addr {
   my $self = shift;
   if (@_) { $self->{mac_addr} = shift }
   return $self->{mac_addr};
}

sub dev {
   my $self = shift;
   if (@_) { $self->{dev} = shift }
   return $self->{dev};
}

sub mtu {
   my $self = shift;
   if (@_) { $self->{mtu} = shift }
   return $self->{mtu};
}

sub tx_q_len {
   my $self = shift;
   if (@_) { $self->{tx_q_len} = shift }
   return $self->{tx_q_len};
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

sub rx_bytes {
   my $self = shift;
   if (@_) { $self->{rx_bytes} = shift }
   return $self->{rx_bytes};
}

sub tx_bytes {
   my $self = shift;
   if (@_) { $self->{tx_bytes} = shift }
   return $self->{tx_bytes};
}

sub rx_errors {
   my $self = shift;
   if (@_) { $self->{rx_errors} = shift }
   return $self->{rx_errors};
}

sub tx_errors {
   my $self = shift;
   if (@_) { $self->{tx_errors} = shift }
   return $self->{tx_errors};
}

sub rx_drop {
   my $self = shift;
   if (@_) { $self->{rx_drop} = shift }
   return $self->{rx_drop};
}

sub tx_drop {
   my $self = shift;
   if (@_) { $self->{tx_drop} = shift }
   return $self->{tx_drop};
}

sub multicasts {
   my $self = shift;
   if (@_) { $self->{multicasts} = shift }
   return $self->{multicasts};
}

sub collisions {
   my $self = shift;
   if (@_) { $self->{collisions} = shift }
   return $self->{collisions};
}

sub rx_len_err {
   my $self = shift;
   if (@_) { $self->{rx_len_err} = shift }
   return $self->{rx_len_err};
}

sub rx_overflow {
   my $self = shift;
   if (@_) { $self->{rx_overflow} = shift }
   return $self->{rx_overflow};
}

sub rx_crc {
   my $self = shift;
   if (@_) { $self->{rx_crc} = shift }
   return $self->{rx_crc};
}

sub rx_frame {
   my $self = shift;
   if (@_) { $self->{rx_frame} = shift }
   return $self->{rx_frame};
}

sub rx_fifo {
   my $self = shift;
   if (@_) { $self->{rx_fifo} = shift }
   return $self->{rx_fifo};
}

sub rx_missed {
   my $self = shift;
   if (@_) { $self->{rx_missed} = shift }
   return $self->{rx_missed};
}

sub tx_abort {
   my $self = shift;
   if (@_) { $self->{tx_abort} = shift }
   return $self->{tx_abort};
}

sub tx_carrier {
   my $self = shift;
   if (@_) { $self->{tx_carrier} = shift }
   return $self->{tx_carrier};
}

sub tx_fifo {
   my $self = shift;
   if (@_) { $self->{tx_fifo} = shift }
   return $self->{tx_fifo};
}

sub tx_heartbeat {
   my $self = shift;
   if (@_) { $self->{tx_heartbeat} = shift }
   return $self->{tx_heartbeat};
}

sub tx_window {
   my $self = shift;
   if (@_) { $self->{tx_window} = shift }
   return $self->{tx_window};
}

sub rx_bytes_ll {
   my $self = shift;
   if (@_) { $self->{rx_bytes_ll} = shift }
   return $self->{rx_bytes_ll};
}

sub tx_bytes_ll {
   my $self = shift;
   if (@_) { $self->{tx_bytes_ll} = shift }
   return $self->{tx_bytes_ll};
}

sub alias {
   my $self = shift;
   if (@_) { $self->{alias} = shift }
   return $self->{alias};
}

sub dhcp_client_id {
   my $self = shift;
   if (@_) { $self->{dhcp_client_id} = shift }
   return $self->{dhcp_client_id};
}

sub dhcp_vendor_id {
   my $self = shift;
   if (@_) { $self->{dhcp_vendor_id} = shift }
   return $self->{dhcp_vendor_id};
}


1;    # So the require or use succeeds (perl stuff)
__END__


# Plain Old Documentation (POD)

=head1 NAME
  Port - class to implement LANforge Ports

=head1 SYNOPSIS

  use LANforge::Port

  #################
  # class methods #
  #################
  $ob    = LANforge::Port->new;

  #######################
  # object data methods #
  #######################

  ### get versions ###
  $port_id = $ob->port_id();

  ### set versions ###
  $ob->port_id(2);

  ########################
  # other object methods #
  ########################

  $ob->decode("CLI output that contains this Port's output");

=head1 DESCRIPTION

  The Port class gives you some clever access into the Port
  objects as sent by the LANforge CLI.

=head1 AUTHOR
  Ben Greear (greearb@candelatech.com)

  Copyright (c) 2001  Candela Technologies.  All rights reserved.
  This program is free software; you can redistribute it and/or
  modify it under the same terms as Perl itself.


=head1 VERSION
  Version 0.0.1  May 26, 2001

=end
