package LANforge::Utils;
use strict;
use warnings;
use Carp;
use Net::Telnet;
#use bigint;
use Math::BigInt;
$| = 1;
#$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
#$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };
if ($ENV{DEBUG}) {
  use Data::Dumper;
}

##################################################
## the object constructor                       ##
## To use:  $ep = LANforge::Utils->new();       ##
##     or:  $ep2 = $ep->new();                  ##
##################################################

sub new {
   my $proto = shift;
   my $class = ref($proto) || $proto;
   my $self  = {};

   $self->{telnet}          = undef;
   $self->{cli_send_silent} = 0;
   $self->{cli_rcv_silent}  = 0;
   $self->{error}           = "";
   $self->{async_waitfor}   = '/btbits>> $/';
   $self->{prompt}          = '/btbits>> $/';

   bless( $self, $class );
   return $self;
}

sub connect {
   my ($self, $host, $port) = @_;
   my $t = new Net::Telnet(Prompt   => '/btbits>> $/',
                           Timeout  => 30);
   $self->{telnet} = \$t;
   $t->open(Host     => $host,
            Port     => $port,
            Timeout  => 20);
   $t->max_buffer_length(16 * 1024 * 1000); # 16 MB buffer
   $t->waitfor($self->{prompt});
   $t->print("set_flag brief 0"); # If we leave it brief, RSLT prompt is not shown.
   $t->waitfor($self->{prompt});
   if ($self->isQuiet()) {
      if (defined $ENV{'LOG_CLI'} && $ENV{'LOG_CLI'} ne "") {
         $self->cli_send_silent(0);
         $self->log_cli("# $0 ".`date "+%Y-%m-%d %H:%M:%S"`);
      }
      else {
         $self->cli_send_silent(1); # Do not show input to telnet
      }
      $self->cli_rcv_silent(1);  # Repress output from telnet
   }
   else {
      $self->cli_send_silent(0); # Show input to telnet
      $self->cli_rcv_silent(0);  # Show output from telnet
   }
   return ${$self->{telnet}};
}

sub telnet {
  my $self = shift;

  die("Utils::telnet -- telnet object undefined")
    if (!(defined $self->{telnet}));
  my $t = ${$self->{telnet}};
  $t->max_buffer_length(50 * 1024 * 1024);
  $t->print("\n");
  $t->waitfor($self->{prompt});

  return $t;
}

# This submits the command and returns the success/failure
# of the command.  If the results from the command are not
# immediately available (say, if LANforge needs to query a remote
# resource for endpoint stats, then that results may NOT be
# in the returned string.  In that case, you must wait for the
# prompt to be seen, so use the doAsyncCmd below instead.
# doCmd is good for rapidly doing lots of configuration without
# waiting for each step (port creation, for example) to fully
# complete.
sub doCmd {
   my $self = shift;
   my $cmd  = shift;
   my $nowait = shift;
   my $waitfor = shift;

   if (!defined($waitfor)) {
      $waitfor = '/ >>RSLT:(.*)/';
   }

   #print "CMD[[$cmd]]\n";
   my $t = ${$self->{telnet}};
   if ( !$self->cli_send_silent() || (defined $ENV{'LOG_CLI'} && $ENV{'LOG_CLI'} ne "")) {
      $self->log_cli($cmd);
   }
   $t->print($cmd);

   if (defined($nowait) && ($nowait == 1)) {
      return "";
   }

   my @rslt = $t->waitfor($waitfor);
   if ( !$self->cli_rcv_silent() ) {
      print "**************\n@rslt\n................\n\n";
   }
   return join( "\n", @rslt );
}

#  This will wait for the prompt, not just for the results.
# Use this instead of doCmd if you are unsure.
sub doAsyncCmd {
   my $self = shift;
   my $cmd  = shift;
   my $t    = ${$self->{telnet}};
   my @rv   = ();

   if ( !$self->cli_send_silent() || (defined $ENV{'LOG_CLI'} && $ENV{'LOG_CLI'} ne "")) {
      $self->log_cli($cmd);
   }
   $t->print($cmd);
   my @rslt = $t->waitfor('/ \>\>RSLT:(.*)/');
   my @rslt2 = $t->waitfor( $self->async_waitfor() );
   @rv = (@rslt, @rslt2);

   if ( !$self->cli_rcv_silent() ) {
      print "**************\n @rv \n................\n\n";
   }
   return join( "\n", @rv );
} # ~doAsyncCmd

sub normalize_bucket_hdr {
  my $self  = shift;
  my $amt = shift;
  my $rv = "Min Max Avg ";
  my $i;
  for ($i = 0; $i<$amt; $i++) {
    if ($i == 0) {
      $rv .= "0 ";
    }
    elsif ($i == 1) {
      $rv .= "1 ";
    }
    else {
      $rv .= 2**($i-1) . "-" . (2**($i) - 1) . " ";
    }
  }
  return $rv;
}

# Normalize lat1, taking peer latency (lat2) into account for negative latency and such.
sub normalize_latency {
  my $self = shift;
  my $lat1 = shift;
  my $lat2 = shift;

  #print "lat1 -:$lat1:-\n";
  #print "lat2 -:$lat2:-\n";

  my $min1 = 0;
  my $min2 = 0;

  # Looks like this: 5 -:5:- 6  [ 17 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ] (1)
  if ($lat1 =~ /(\S+)\s+-:(\S+):-\s+(\S+)\s+\[\s+(.*)\s+\]\s+\((\S+)\)/) {
    $min1 = $1;
  }
  if ($lat2 =~ /(\S+)\s+-:(\S+):-\s+(\S+)\s+\[\s+(.*)\s+\]\s+\((\S+)\)/) {
    $min2 = $1;
  }

  # For instance, min1 is -5, min2 is 25, rt-latency is 20.
  # Adjust lat1 by (25 - -5) / 2
  # For instance, min1 is 25, min2 is -5, rt-latency is 20.
  # Adjust lat1 by (-5 -25) / 2
  #print "min1: $min1  min2: $min2  half: " . int(($min2 - $min1) / 2) . "\n";
  # So, the above seems nice, but often we have a small negative value due to
  # clock drift in one direction, and large latency in the other (due to real one-way latency)
  # So, we will just adjust enough to make the smallest value positive.
  my $adjust = 0;
  if ($min1 < 0) {
    $adjust = -$min1;
  }
  elsif ($min2 < 0) {
    $adjust = $min2;
  }
  return $self->normalize_bucket($lat1, $adjust);
}

sub normalize_bucket {
   my $self = shift;
   my $line = shift;
   my $adjust = shift;

   #print "line -:$line:-\n";

   # Looks like this: 5 -:5:- 6  [ 17 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ] (1)
   if ($line =~ /(\S+)\s+-:(\S+):-\s+(\S+)\s+\[\s+(.*)\s+\]\s+\((\S+)\)/) {
      my $min = $1;
      my $avg = $2;
      my $max = $3;
      my $bks = $4;
      my $width = $5; # Assumes one currently
      if (!($width eq "1")) {
         return $line;
      }
      else {
         my @bkts = split(/\s+/, $bks);
         @bkts = (@bkts, "0");
         my $i;
         my $rv = ($min + $adjust) . " " . ($max + $adjust) . " " . ($avg + $adjust) . " ";
         #print "bkts len: " . @bkts . "\n";
         my @nbkts = (0) x (@bkts);
         for ($i = 0; $i<@bkts; $i++) {
            # Figure out the bkt range
            my $minv = 0;
            my $maxv = 2 ** $i - 1;
            if ($i > 0) {
               $minv = 2 ** ($i - 1);
            }
            # Adjust by the min value, which is treated as an offset
            $minv += $min;
            $maxv += $min;

            # And adjust based on round-trip time to deal with clock lag
            $minv += $adjust;
            $maxv += $adjust;

            # And now find the normalized bucket this fits in
            #print "maxv: $maxv\n";
            my $z;
            my $idx = 0;
            for ($z = 0; $z < 32; $z++) {
               if ($maxv < (2 ** $z)) {
                  #print "maxv: $maxv  z: $z  2^$z: " . 2 ** $z . + "\n";
                  $idx = $z;
                  # Everything else falls in the last bucket
                  if ($idx >= @bkts) {
                     $idx = (@bkts - 1);
                  }
                  last;
               }
            }

            #print "idx: $idx i: $i  minv: $minv  maxv: $maxv  min: $min  adjust: $adjust\n";
            #print "nbkts: " . $nbkts[$idx];
            #print " bkts: " . $bkts[$i] . "\n";
            my $nv = $nbkts[$idx] + $bkts[$i];
            @nbkts[$idx] = $nv;
         }

         for ($i = 0; $i < @nbkts; $i++) {
            $rv .= ($nbkts[$i] . " ");
         }
         return $rv;
      }
   }
   else {
      return $line;
   }
}

#  Uses cached values (so it will show Phantom ones too)
sub getPortListing {
   my $self  = shift;
   my $shelf = shift;
   my $card  = shift;

   my @rv   = ();
   my $prts = $self->doAsyncCmd( "show_port " . $shelf . " " . $card );

   if ( $prts =~ /Timed out waiting for/g ) {
      $self->error("Partial Failure: Timed out");
   }

   my @ta = split( /\n/, $prts );

   my $i;
   for ( $i = 0 ; $i < @ta ; $i++ ) {
      my $ln = $ta[$i];
      if ( $ln =~ /Shelf:\s+\d+,\s+Card:\s+\d+,\s+Port:\s+\d+\s+Type/ ) {
         my $ptxt;
         while ( $ln =~ /\S+/ ) {
            $ptxt .= "$ln\n";
            $i++;
            $ln = $ta[$i];
         }

         my $p1 = new LANforge::Port();
         $p1->decode($ptxt);
         @rv = ( @rv, $p1 );
      }
   }
   return @rv;
} #~getPortListing

sub updatePortRetry {
   my $self = shift;
   return $self->updatePort( shift, shift, shift, shift, shift, 10000 );
}

# Call with args: Port, (these next ones are optional): Shelf-id, Card-id, Port-Id
sub updatePort {
   my $self        = shift;
   my $port        = shift;
   my $sid         = shift;    #shelf-id
   my $max_retries = undef;
   if ( defined($sid) ) {
      $port->shelf_id($sid);
      $port->card_id(shift);
      $port->port_id(shift);

      $max_retries = shift;
   }

   if ( !defined($max_retries) ) {
      $max_retries = 10;
   }

 # Since I use this for testing, I'm going to obliterate the port's data so that
 # there will be no question as to whether or not the update worked.
   $port->initDataMembers();   #Shouldn't mess with the shelf, card, or port id.

   my $cmd =
       "nc_show_port "
     . $port->shelf_id() . " "
     . $port->card_id() . " "
     . $port->port_id;

   #print "cmd -:$cmd:-\n";

   # Use the non-caching port show.
   my $prt = $self->doAsyncCmd($cmd);

# There is a small race condition, where one report may be on the way back to the
# main server when the first request is still being sent.  So, we'll ask again.  This
# one will definately be up to date.
   $prt = "";
   my $i = 0;
   while (1) {
      $prt = $self->doAsyncCmd($cmd);
      if ( !$self->cli_rcv_silent() ) {    # added by Adam - 8/9/2004
         print "prt: $prt\n";
      }

      if ( $i++ > $max_retries ) {
         last;
      }

      if (  ( $prt =~ /Could not find that Port/g )
         || ( $prt =~ /Timed out waiting/g )
         || ( !( $prt =~ /, Port:/g ) ) )
      {
         sleep(5);
      }
      else {
         last;
      }
   }

   if ( !$self->cli_rcv_silent() ) {    # added by Adam - 8/9/2004
      print "decoding port -:$prt:-\n";
   }
   $port->decode($prt);
}    #updatePort

sub updateEndpoint {
   my $self = shift;
   my $endp = shift;
   my $name = shift;
   my $fast = shift;

   if ( defined($name) ) {
      $endp->name($name);
   }

# Since I use this for testing, I'm going to obliterate the Endpoint's data so that
# there will be no question as to whether or not the update worked.
   $endp->initDataMembers();   #Shouldn't mess with the shelf, card, or port id.

   my $ep;
   if ($fast) {
      $ep = $self->doAsyncCmd( "show_endpoint " . $endp->name() );
   }
   else {
      # Use the non-caching endpoint show.
      $ep = $self->doAsyncCmd( "nc_show_endpoint " . $endp->name() );

# There is a small race condition, where one report may be on the way back to the
# main server when the first request is still being sent.  So, we'll ask again.  This
# one will definately be up to date.
      $ep = $self->doAsyncCmd( "nc_show_endpoint " . $endp->name() );
   }

   #print "EP show_endp results for cmd: " . $endp->name() . "\n-:$ep:-\n";

   $endp->decode($ep);

   if ( $endp->isCustom() ) {
      $ep = $self->doCmd( "show_endp_pay " . $endp->name() . " 5000" );
      $endp->decodePayload($ep);
   }
}    #updateEndpoint

sub log_cli {
  my $self = shift;
  my $cmd = shift;
  my $using_stdout = 0;
  #print "utils::log_cli: $ENV{'LOG_CLI'}\n";
  if (defined $ENV{'LOG_CLI'} && $ENV{'LOG_CLI'} ne "") {
    if ($ENV{'LOG_CLI'} =~ /^--/) {
      die("Incorrect format for LOG_CLI, it should be '1' or  filename like '/tmp/cmdlog.txt'");
    }
    if ($ENV{'LOG_CLI'} eq "1" || $ENV{'LOG_CLI'} =~ /STDOUT/i) {
      $using_stdout = 1;
      #print "STDOUT utils::log_cli: $ENV{'LOG_CLI'}\n";
    }
    else { # write to a file
      if ( ! -f $ENV{'LOG_CLI'}) {
        print "Creating new file $ENV{'LOG_CLI'}\n";
        `touch $ENV{'LOG_CLI'}`;
        chmod(0666, $ENV{'LOG_CLI'});
      }
      if ( -w $ENV{'LOG_CLI'}) {
        open(my $fh, ">>", $ENV{'LOG_CLI'});
        if (defined $fh) {
          #print "FILE utils::log_cli: \n";
          print $fh "$cmd\n";
          close $fh;
        }
        else {
          warn ("$ENV{'LOG_CLI'} not writable");
          $using_stdout=1;
          #print "ELSE STDOUT utils::log_cli: $ENV{'LOG_CLI'}\n";
        }
      }
    }
  }
  if ($using_stdout == 1 || !isQuiet() ) {
    print qq(\nCMD: \"$cmd\"\n);
  }
}

# returns 1 if we're quiet, 0 if we're verbose
# if $::quiet is undefined, we assume verbose
sub isQuiet {
  my $self = shift;
  return 0
    if (! defined $::quiet);

  if (length( do { no warnings "numeric"; $::quiet & "" } )) {
    # we're numeric
    if ($::quiet != 0) {
      #print "numeric and quiet [$::quiet]\n";
      return 1;
    }
    #print "numeric and verbose [$::quiet]\n";
    return 0;
  }

  # else we're textual
  if ($::quiet =~ /(1|yes|on)/i) {
    #print "textual and quiet [$::quiet]\n";
    return 1;
  }
  #print "textual and verbose [$::quiet]\n";
  return 0;
}

sub async_waitfor {
   my $self = shift;
   if (@_) { $self->{async_waitfor} = shift }
   return $self->{async_waitfor};
}

sub error {
   my $self = shift;
   if (@_) { $self->{error} = shift }
   return $self->{error};
}

sub cli_rcv_silent {
   my $self = shift;
   if (@_) { $self->{cli_rcv_silent} = shift }
   return $self->{cli_rcv_silent};
}

sub cli_send_silent {
   my $self = shift;
   if (@_) { $self->{cli_send_silent} = shift }
   return $self->{cli_send_silent};
}

sub fmt_cmd {
   #print Dumper(@_);
   my $self = shift;
   my $rv;
   my $mod_hunk;
   my $show_err = 0;
   my $item = 1;
   my $prev_item;
   for my $hunk (@_) {
      if (defined $hunk && $hunk eq '') {
         print STDERR "\nfmt_cmd() arg $item blank, converting to NA\n";
         print STDERR "            prev argument was [$prev_item]\n" if (defined $prev_item);
         $show_err = 1;
      }
      die("rv[${rv}]\n --> fmt_cmd passed an array, bye.")  if (ref($hunk) eq 'ARRAY');
      die("rv[${rv}]\n --> fmt_cmd passed a hash, bye.")    if (ref($hunk) eq 'HASH');
      $mod_hunk = $hunk;
      $mod_hunk = "0" if ($hunk eq "0" || $hunk eq "+0");

      if( $hunk eq "" ) {
         #print "hunk[".$hunk."] --> ";
         $mod_hunk = 'NA';
         #print "hunk[".$hunk."]\n";
         #print "fmt_cmd: warning: hunk was blank, now NA. Prev hunks: $rv\n"
      }
      $prev_item = $hunk;
      $item++;
      $rv .= ( $mod_hunk =~m/ +/) ? "'$mod_hunk' " : "$mod_hunk ";
   }
   if (rindex($rv, ' ', length($rv)-2) > 1) {
      #print STDERR "[$rv]\n";
      $rv =~ s/\s+$//g;
      #print STDERR "[$rv]\n";
   }
   print STDERR qq(\nFormatted cmd: "$rv"\n) if ($show_err or $::quiet ne "yes");
   return $rv;
}

##
## Check if usleep() exists
##
our $has_usleep = 0;
if (defined &usleep) {
   print("I see usleep\n");
   $LANforge::Utils::has_usleep=1;
}


sub sleep_ms {
  my $self;
  my $millis = 0;
  if (@_ > 1) {
    ($self, $millis) = @_;
  }
  else {
    $millis = pop(@_);
  }
  return if (!(defined $millis) || ($millis == 0));

  my $secs = $millis / 1000;

  if ($LANforge::Utils::has_usleep) {
    usleep($millis);
  }
  else {
    select(undef, undef, undef, $secs);
  }
}

sub sleep_sec {
  my $self;
  my $secs = 0;
  if (@_ > 1) {
    ($self, $secs) = @_;
  }
  else {
    ($secs) = @_;
  }
  return if (!(defined $secs) || ($secs == 0));

  if ($LANforge::Utils::has_usleep) {
    usleep($secs);
  }
  else {
    select(undef, undef, undef, $secs);
  }
}

##
##  Returns ref to map of all stations maching a parent device
##  EG: $rh_eid_map = $u->get_eid_map($::resource)
##

sub get_eid_map {
  my ($self, $resource) = @_;
  my $rh_eid_map = {};
  my @ports_lines = split(/\r?\n/, $self->doAsyncCmd("nc_show_ports 1 $resource all"));
  chomp(@ports_lines);

  my ($eid, $card, $port, $type, $mac, $dev, $parent, $ip);
  foreach my $line (@ports_lines) {
    # collect all stations on that radio add them to @interfaces
    if ($line =~ /^Shelf: /) {
      $card = undef; $port = undef;
      $type = undef; $parent = undef;
      $eid = undef; $mac = undef;
      $dev = undef;
      $ip = undef;
    }

    # careful about that comma after card!
    # NO EID for Shelf: 1, Card: 1, Port: 2  Type: WIFI-Radio  Alias:
    ($card, $port, $type) = $line =~ m/^Shelf: 1, Card: (\d+),\s+Port: (\d+)\s+Type: (\w+)/;
    if ((defined $card) && ($card ne "") && (defined $port) && ($port ne "") && ($type ne "VRF")) {
      $eid = "1.".$card.".".$port;
      my $rh_eid = {
        eid => $eid,
        type => $type,
        parent => undef,
        dev => undef,
      };
      $rh_eid_map->{$eid} = $rh_eid;
    }
    #elsif ($line =~ /^Shelf/) {
    #  #print "NO EID for $line\n";
    #}

    if (!(defined $eid) || ($eid eq "")) {
      #print "NO EID for $line\n";
      next;
    }
    ($mac, $dev) = $line =~ / MAC: ([0-9:a-fA-F]+)\s+DEV: (\S+)/;
    if ((defined $mac) && ($mac ne "")) {
      #print "$eid MAC: $line\n";
      $rh_eid_map->{$eid}->{mac} = $mac;
      $rh_eid_map->{$eid}->{dev} = $dev;
    }

    ($parent) = $line =~ / Parent.Peer: (\S+) /;
    if ((defined $parent) && ($parent ne "")) {
      #print "$eid PARENT: $line\n";
      $rh_eid_map->{$eid}->{parent} = $parent;
    }

    ($ip) = $line =~ m/ IP: *([^ ]+) */;
    if ((defined $ip) && ($ip ne "")) {
      #print "$eid IP: $line\n";
      $rh_eid_map->{$eid}->{ip} = $ip;
    }
  } # foreach

  #foreach $eid (keys %eid_map) {
  #  print "eid $eid ";
  #}
  return $rh_eid_map;
}

##
## retrieve an eid/name record by name using a refrence
## to an eid_map
##
sub find_by_name {
  my ($self, $rh_eid_map, $devname) = @_;
  while (my ($eid, $rh_rec) = each %{$rh_eid_map}) {
    #print "fbn: ".$rh_rec->{dev}."\n";
    if ((defined $rh_rec->{dev}) && ($rh_rec->{dev} eq $devname)) {
      return $rh_rec;
    }
  }
  return -1;
}

##
## retrieve ports on radio from EID map
## EG: $ra_interfaces = $u->ports_on_radio($rh_eid_map, $radio_name);
##
sub ports_on_radio {
  my ($self, $rh_rec2_map, $radio) = @_;
  my $ra_ifs = [];
  #print "PARENT IS $radio\n";

  foreach my $rh_rec2 (values %{$rh_rec2_map}) {
    next if (!(defined $rh_rec2->{parent}));
    #print "\npor: ".$rh_rec2->{parent}.">".$rh_rec2->{dev}."\n";
    if ($rh_rec2->{parent} eq $radio) {
      #print $rh_rec2->{dev}."<-".$rh_rec2->{parent}." ";
      my $devn = $rh_rec2->{dev};
      push(@$ra_ifs, $devn);
    }
  }
  return $ra_ifs;
}

sub test_groups {
  my ($self) = @_;
  my @group_lines = split(/\r?\n/, $self->doAsyncCmd("show_group all"));
  sleep_ms(30);

  #print Dumper(\@group_lines);
  my @matches = grep {/TestGroup name:\s+/} @group_lines;
  #print Dumper(\@matches);
  my $ra_group_names = [];
  for my $line (@matches) {
    push(@$ra_group_names, ($line =~ /TestGroup name:\s+(\S+)\s+\[/));
  }
  #print Dumper($ra_group_names);

  return $ra_group_names;
}

##
sub group_items {
   my ($self, $tg_name) = @_;
   die("Utils::group_items wants a test group name, bye.")
      if (!(defined $tg_name) || ("" eq $tg_name));
   my @lines = split(/\r?\n/, $self->doAsyncCmd( "show_group '$tg_name'"));
   sleep_ms(30);
   my $ra_items = [];
   my $started = 0;
   foreach my $line (@lines) {
      $started ++ if ($line =~ /\s*Cross Connects:/);
      next unless ($started);
      last if ($line =~ /^\s*$/);
      $line =~ s/^\s*Cross Connects:\s*//;
      $line =~ s/^\s+//;
      $line =~ s/\s+$//;
      my @hunks = split(/\s+/, $line);
      push(@$ra_items, split(/\s+/, $line));
   }
   if (@$ra_items < 1) {
     print STDERR "No cross connects found for test group $tg_name.\n";
     return [];
   }
   return $ra_items;
}

# Generic disassembly of lines created by show
our @starting_exceptions = (
   # please keep these sorted
   "Access Denied:",
   "Bad Protocol:",
   "Bad URL:",
   "Buffers Read:",
   "Buffers Written:",
   "Bytes Read:",
   "Bytes Read-3s:",
   "Bytes Written:",
   "Bytes Written-3s:",
   "Command:",
   "Conn Established:",
   "Conn Timeouts:",
   "Couldn't Connect:",
   "Cx Detected:",
   "DNS-Latency: ",
   "DNS Servers:",
   "Endpoint [",
   "Files Read:",
   "Files Written:",
   "First-RW-Latency:",
   "Flags:",
   "FTP HOST Error:",
   "FTP STOR Error:",
   "FTP PORT Error:",
   "GenericEndp [",
   "HTTP RANGE Error:",
   "HTTP POST Error:",
   "HTTP PORT Error:",
   "Latency:",
   "Login Denied:",
   "No Resolve Host:",
   "No Resolve Proxy:",
   "Not Found (404):",
   "Pkt-Gaps:",
   "Read CRC Failed:",
   "Read Error:",
   "Redirect Loop Err:",
   "Results[",
   ">>RSLT:",
   "Rx Bytes:",
   "Rx Bytes (On Wire):",
   "Rx Duplicate Pkts:",
   "Rx OOO Pkts:",
   "Rx Pkts:",
   "Rx Pkts (On Wire):",
   "RX-Silence:",
   "Shelf: 1,",
   "SMTP-From:",
   "TCP Retransmits:",
   "Timed Out:",
   "Total CURL Errors:",
   "Tx Bytes:",
   "Tx Bytes (On Wire):",
   "Tx Failed Bytes:",
   "Tx Failed Pkts:",
   "Tx Pkts:",
   "Tx Pkts (On Wire):",
   "Tx-Retries:",
   "URL:",
   "URL-Latency:",
   "URLs Processed:",
   "Write Error:",
   );

# Generic disassembly of lines created by show
our @port_starting_exceptions = (
   # please keep these sorted
   "Advertising:",
   "Current:",
   "Missed-Beacons:",
   "Partner:",
   "Supported:",
   "Tx-Excessive-Retry:",
   "Rx-Invalid-CRYPT:",
   "Rx-Invalid-MISC:",
   );

our @one_line_keys = (
   "Latency:",
   "Pkt-Gaps:",
   "RX-Silence:",
   "Cx Detected:",
   );
#
# examples of using this:
# $rh = u->show_as_hash($txt)
# $rh = u->show_as_hash(\$txt)
# $rh = u->show_as_hash(split(/\n/, $txt))
# $rh = u->show_as_hash(\@lines)
#
sub show_as_hash {
   my ($self, $in, $isport) = (undef, undef, 0);
   if (@_ > 1) {
      ($self, $in, $isport) = @_;
   }
   else {
      $in = pop(@_);
   }
   my @lines = ();

   # this allows us to pass in \$txt, split(/\n/, $txt) or just $txt
   if ((ref $in) eq "") {
      @lines = split(/\r?\n/, $in);
   }
   elsif ((ref $in) eq "SCALAR") {
      @lines = split(/\r?\n/, $$in);
   }
   elsif ((ref $in) eq "ARRAY") {
      @lines = @$in;
   }

   #print "show_as_hash, isport: $isport\n";

   my $rh_pairs = {};
   my @special = ();

   # https://stackoverflow.com/questions/31724503/most-efficient-way-to-check-if-string-starts-with-needle-in-perl
   my $key = undef;
   my $value = undef;
   my @hunks = ();
   my $prefix = "";
   #print Dumper(\@lines);
   chomp(@lines);
   my $found_start_x = 0;
   foreach my $line (@lines) {
      if ($isport) {
         #print "Port line -:$line:-\n";
         foreach my $start (@LANforge::Utils::port_starting_exceptions) {
            # we purposefully are not wasting time trimming whitespace
            my $i = index($line, $start);
            if ($i >= 0) {
               push(@special, $line);
               $found_start_x++;
               last;
            }
         }
      }
      else {
         foreach my $start (@LANforge::Utils::starting_exceptions) {
            # we purposefully are not wasting time trimming whitespace
            my $i = index($line, $start);
            if ($i >= 0) {
               push(@special, $line);
               $found_start_x++;
               last;
            }
         }
      }
      if ($found_start_x) {
         $found_start_x = 0;
         next;
      }

      if ($isport) {
         #print "line -:$line:-\n";
         if ($line =~ /^\s+\[Configured\]/) {
            #print "Prefix to cfg\n";
            $prefix = "Cfg";
            next;
         }
         if ($line =~ /^\s+\[Probed\]/) {
            $prefix = "Probed";
            next;
         }

         $line =~ s/ (dbm|[kmg]?bps)/$1/ig;
         $line =~ s/DNS Servers/DNS-Servers/ig;
         $line =~ s/TX Queue Len/TX-Queue-Len/ig;
         $line =~ s/Missed Beacons/Missed-Beacons/ig;
         #print "$i: ".$lines[$i]."\n";
      }

      # at this point, every line should be split using colons and spaces
      @hunks = split(/\s+/, $line);
      foreach my $hunk (@hunks) {
         if (rindex($hunk, ':') == length($hunk)-1) {
            $key = substr($hunk, 0, rindex($hunk, ':'));
            next;
         }
         $value = $hunk;
         if ((defined $key) && ("" ne $key)) {
            my $val = (defined $value) ? $value : "";
            #print "Adding key -:$key:-  val -:$val:-\n";
            $rh_pairs->{$key} = $val;
            if ($prefix ne "") {
               #print "Adding prefixed key -:$prefix-$key:-  val -:$val:-\n";
               $rh_pairs->{"$prefix-$key"} = $val;
            }
            $key = undef;
            $value = undef;
         }
      }
   }

   @hunks = ();
   $key = undef;
   $value = undef;
   foreach my $line (@special) {
      #print "\nspecial: $line";
      my $rh_vals = undef;

      # special cases for certain lines
      if (index($line, '>>RSLT:') >= 0) {
         $rh_vals = {
            'Cmd' => substr($line, index($line, 'Cmd:')+5),
            'RSLT' => substr($line, index($line, ':')+2, (index($line, ' Cmd:') - index($line, ':')-3)),
         };
         foreach my $subkey (keys %$rh_vals) {
            $rh_pairs->{$subkey} = $rh_vals->{$subkey}
         }
         #$rh_pairs->{"RSLT"} = $rh_vals;
         #print Dumper($rh_pairs->{"RSLT"});
         $rh_vals = undef;
         $key = undef;
         $value = undef;
         next;
      }
      if (index($line, 'Endpoint [') >= 0) {
         my $flags = substr($line, index($line, '(')+1, -1); # split(/\s+/,
         my $name = substr($line, index($line, '[')+1, index($line, ']') - index($line, '[')-1);
         $rh_vals = {
            'Endpoint-name' => $name,
            'Endpoint-flags' => $flags,
         };
         foreach my $subkey (keys %$rh_vals) {
            $rh_pairs->{$subkey} = $rh_vals->{$subkey}
         }
         #$rh_pairs->{"Endpoint"} = $rh_vals;
         $rh_vals = undef;
         $key = undef;
         $value = undef;
         next;
      }
      if (index($line, 'Shelf: 1,') >= 0) {
         $line =~ s/1,/1/;
         if ($line =~ /Endpoint/ ) {
            my ($card, $port, $endpoint, $eptype, $patt ) =
               $line =~ /Shelf:\s+1\s+Card:\s+(\d+)\s+Port:\s+(\S+)\s+Endpoint:\s+(\S+)\s+Type:\s+(\S+)\s+Pattern:\s+(\S+)$/;
            $rh_pairs->{Shelf} = 1;
            $rh_pairs->{Card} = $card;
            $rh_pairs->{Resource} = $card;
            $rh_pairs->{Port} = $port;
            $rh_pairs->{Endpoint} = $endpoint;
            $rh_pairs->{Type} = $eptype;
            $rh_pairs->{Pattern} = $patt;
         }
      }
      my $found_oneline = 0;
      foreach my $keyv (@LANforge::Utils::one_line_keys) {
         if (index($line, $keyv) >= 0) {
            $found_oneline++;
            if (rindex($keyv, ':') >= 1) {
               $keyv = substr($keyv, 0, rindex($keyv, ':'));
            }
            $rh_pairs->{$keyv} = substr($line, index($line, ":")+2);
            last;
         }
         next if ($found_oneline);
      }

      # This is parsing bucket counters, maybe more
      my $i = index($line, ':');
      $key = substr($line, 0, $i);
      $key =~ s/^\s*//g;
      $value = substr($line, $i+1);
      $rh_pairs->{$key} = $value;  # Add full line to hash
      $value =~ s/^\s*//g;
      @hunks = split(/\s+/, $value);
      $rh_vals = $self->hunks_to_hashes($key, \@hunks);
      foreach my $subkey (keys %$rh_vals) {
         my $val = $rh_vals->{$subkey};
         #print("Adding subkey -:$subkey:-  val -:$val:-\n");
         $rh_pairs->{$subkey} = $val;
      }
      $rh_vals = undef;
      $key = undef;
      $value = undef;
   }

   # Add some common short-hand actions that we supported in the past.
   my $val;

   $val = $rh_pairs->{"Rx-Pkts-Per-Sec"};
   if (defined($val)) {
     $rh_pairs->{"rx_pps"} = $val;
   }
   $val = $rh_pairs->{"Tx-Pkts-Per-Sec"};
   if (defined($val)) {
     $rh_pairs->{"tx_pps"} = $val;
   }
   $val = $rh_pairs->{"Rx-Pkts-Total"};
   if (defined($val)) {
     $rh_pairs->{"rx_pkts"} = $val;
     $rh_pairs->{"Rx Pkts"} = $val;
     $rh_pairs->{"Rx-Pkts"} = $val;
   }
   $val = $rh_pairs->{"Tx-Pkts-Total"};
   if (defined($val)) {
     $rh_pairs->{"tx_pkts"} = $val;
     $rh_pairs->{"Tx Pkts"} = $val;
     $rh_pairs->{"Tx-Pkts"} = $val;
   }
   $val = $rh_pairs->{"Rx-Bytes-bps"};
   if (defined($val)) {
     $rh_pairs->{"rx_bps"} = $val;
   }
   $val = $rh_pairs->{"Tx-Bytes-bps"};
   if (defined($val)) {
     $rh_pairs->{"tx_bps"} = $val;
   }

   $val = $rh_pairs->{"Rx-Bytes-Total"};
   if (defined($val)) {
     $rh_pairs->{"Rx-Bytes"} = $val;
     $rh_pairs->{"Rx Bytes"} = $val;
   }

   $val = $rh_pairs->{"Tx-Bytes-Total"};
   if (defined($val)) {
     $rh_pairs->{"Tx-Bytes"} = $val;
     $rh_pairs->{"Tx Bytes"} = $val;
   }

   #foreach $key (sort keys %$rh_pairs) {
   #   print "{$key} => $rh_pairs->{$key}\n";
   #}
   #die("debugging");
   return $rh_pairs;
}

sub hunks_to_hashes {
   my ($self, $prefix, $input) = (undef, undef, undef);
   if (@_ > 2) {
      ($self, $prefix, $input) = @_;
   }
   else {
      $prefix = shift;
      $input = shift;
   }
   my @hunks = ();
   if (ref($input) eq "ARRAY") {
      @hunks = @$input;
   }
   elsif (ref($input) eq "SCALAR") {
      @hunks = (@$input);
   }
   else {
      die("Utils::hunks_to_hashes() expects an array");
   }
   if (index($prefix, ' ') >= 0) {
      $prefix =~ s/\s+/-/g
   }

   my $rh = {};
   my $key = undef;
   my $value = undef;
   foreach my $hunk (@hunks) {

      if (rindex($hunk, '/s') >= 1) {
         $key = $prefix."-Per-Sec";
         $value = substr($hunk, 0, index($hunk, '/s'));
         $rh->{$key} = (defined $value) ? $value : "";

         # create bps not just Bps
         if (index($prefix, "Bytes") >= 1) {
            my $bps = (0 + $value) * 8;
            $rh->{$prefix."-bps"} = $bps;
         }
         $key = undef;
         $value = undef;
         next;
      }
      if (rindex($hunk, ':') == length($hunk)-1) {
         $key = $prefix .'-'. substr($hunk, 0, rindex($hunk, ':'));
         next;
      }
      $value = $hunk;
      if ((defined $key) && ("" ne $key)) {
         $rh->{$key} = (defined $value) ? $value : "";
         if ((index($prefix, "Bytes") >= 1)
            && ((index($key, "Total") >=0 ) || (index($key, "Cur") >=0 ))) {
            my $bits = (0 + $value) * 8;
            my $nkey = $key;
            $nkey =~ s/Bytes/Bits/;
            $rh->{$nkey} = $bits;
         }
         $key = undef;
         $value = undef;
      }
   }
   return $rh;
}

sub expand_unit_str {
   my ($self, $string) = @_;
   die("Utils::expand_unit_str expects string to parse")
      if (!(defined $string) || ("" eq $string));

   return 0 if ($string =~ /^[0\.]+\s*\w+$/);

   my ($num, $suf) = $string =~ /^([\.0-9]+)\s*(\w*)$/;
   if (!(defined $num) || ("" eq $num)) {
      die("Utils::expand_unit_str exects something like 33Mbps or '33 Mbps', not $string");
   }
   my $multiplier = 1;
   #print "String[$string] => $num Suffix $suf\n";
   if (!(defined $suf) || ("" eq $suf)) {
      $multiplier = 1;
      print STDERR "Utils::expand_unit_str saw no suffix in [$string]\n";
   }
   elsif ($suf =~ /^bps$/i) {
      $multiplier = 1;
   }
   elsif ($suf =~ /^kbps$/i) {
      $multiplier = 1000;
   }
   elsif ($suf =~ /^mbps$/i) {
      $multiplier = 1000 * 1000;
   }
   elsif ($suf =~ /^gbps$/i) {
      $multiplier = 1000 * 1000 * 1000;
   }
   return int($num) * $multiplier;
}

sub mac_add {
   my ($self, $first_mac, $second_dec) = @_;
   $first_mac =~ s/[:]//g if ($first_mac =~ /[:]/);
   $first_mac = "0x".$first_mac if ($first_mac !~ /^0x/);
   my $newdec = Math::BigInt->new($first_mac);
   $newdec->badd(0+$second_dec);
   my $pad = Math::BigInt->new('0x1000000000000');
   $newdec->badd($pad);
   my $newhex = "".$newdec->as_hex();
   my $rv = "";
   $newhex = substr($newhex, -12); # we begin 0x100...much bigger than we need
   for (my $i = length($newhex); $i > 0; $i-=2) {
      $rv = substr($newhex, $i-2, 2).":$rv";
   }
   $rv =substr($rv, 0, -1);
   undef($newdec);
   undef($pad);
   return $rv;
}



####
1;
__END__


=head1 NAME
  Port - class to implement various LANforge utility and helper functions.

=head1 SYNOPSIS

  use LANforge::Utils

  #################
  # class methods #
  #################
  $ob    = LANforge::Utils->new;

  #######################
  # object data methods #
  #######################

  ### get versions ###
  $telnet = $ob->telnet();

  ### set versions ###
  $ob->telnet($t);

  ########################
  # other object methods #
  ########################

  $ob->doCmd("$Some CLI command\n");
  $ob->doAsyncCmd("$Some Asynchronous CLI command\n");

=head1 DESCRIPTION
  The Utils class gives you some powerful and packaged access to various
  LANforge CLI objects.

=head1 AUTHOR
  Ben Greear (greearb@candelatech.com)
  Copyright (c) 2020  Candela Technologies.  All rights reserved.
  This program is free software; you can redistribute it and/or
  modify it under the same terms as Perl itself.

=end
