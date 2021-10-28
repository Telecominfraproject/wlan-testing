#!/usr/bin/perl

use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{ __DIE__  } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };
use Data::Dumper;
use POSIX;
# Un-buffer output
$| = 1;

# use lib prepends to @INC, so put lower priority first
# This is before run-time, so cannot condition this with normal 'if' logic.
use lib '/home/lanforge/scripts';
use lib "./";

use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
use Net::Telnet ();
use Getopt::Long;
use Time::HiRes qw(usleep gettimeofday);
our $has_usleep = (defined &usleep) ? 1 : 0;

my  $NA              ='NA';
our $resource        = 1;
our $upstream_res    = 1;
our $quiet           = "yes";
our $silent          = 0;
our $endp_name       = "";
our $speed           = "-1";
our $action          = "";
our $do_cmd          = "NA";
our $lfmgr_host      = "localhost";
our $lfmgr_port      = 4001;
our $tx_style        = "";
our $cx_name         = "";
our $tx_side         = "B";
our $min_tx          = 0;
our $max_tx          = 920 * 1024 * 1024; # 920Mbps default
our $buf_size        = 3 * 1024 * 1024; # 3MB default
our $log_cli         = "unset"; # do not set to 0, it turns into logfile "./0"
our $stream_key      = undef;
our $quit_when_const = 0;
our $sta             = "";
our $upstream        = "";
our $proto           = "udp"; # for constant
our $est_fill_time_sec = 0;
our $last_fill_time_sec = 0;
our $begin_running   = 1; # set to 0 to not start CX running; 0 is appropriate for batch creation or bufferfill

# https://en.wikipedia.org/wiki/Standard-definition_television
# https://www.adobe.com/devnet/adobe-media-server/articles/dynstream_live/popup.html
# https://en.wikipedia.org/wiki/ISDB-T_International
# https://en.wikipedia.org/wiki/Frame_rate
# https://en.wikipedia.org/wiki/List_of_broadcast_video_formats
# https://blog.forret.com/2006/09/27/hd-720p-1080i-and-1080p/
# Framerate is highly subjective in digital formats, because there are
# variable frame rates dictated by min- and max-frame rate.
our %stream_keys = (
  'w'           => 0,
  'width'       => 0,
  'x'           => 0,
  'h'           => 1,
  'height'      => 1,
  'y'           => 1,
  'i'           => 2,
  'interlaced'  => 2,
  'audio'       => 3,
  'audio_bps'   => 3,
  'video'       => 4,
  'video_bps'   => 4,
  'stream'      => 5,
  'stream_bps'  => 5,
  'fps'         => 6,
  'frames'      => 6,
  'framerate'   => 6,
  );

our %avail_stream_res = (
  # nicname             w,    h,  interlaced,   audio,    vid bps,   tt bps   framerate
  "sqvga-4:3"     => [  160,  120,    0,         16000,    32000,        48000,    30],
  "sqvga-16:9"    => [  160,   90,    0,         16000,    32000,        48000,    30],
  "qvga-4:3"      => [  320,  240,    0,         16000,    32000,        48000,    30],
  "qvga-16:9"     => [  320,  180,    0,         16000,    32000,        48000,    30],
  "qcif-48k-4:3"  => [  144,  108,    0,         16000,    32000,        48000,    30],
  "qcif-48k-16:9" => [  192,  108,    0,         16000,    32000,        48000,    30],
  "qcif-96k-4:3"  => [  192,  144,    0,         16000,    80000,        96000,    30],
  "qcif-96k-16:9" => [  256,  144,    0,         16000,    80000,        96000,    30],
  "cif"           => [  352,  288,    0,         32000,   268000,       300000,    30],
  "cif-300k-4:3"  => [  288,  216,    0,         32000,   268000,       300000,    30],
  "cif-300k-16:9" => [  384,  216,    0,         32000,   268000,       300000,    30],
  "cif-500k-4:3"  => [  320,  240,    0,         32000,   468000,       500000,    30],
  "cif-500k-16:9" => [  384,  216,    0,         32000,   468000,       500000,    30],
  "d1-800k-4:3"   => [  640,  480,    0,         32000,   768000,       800000,    30],
  "d1-800k-16:9"  => [  852,  480,    0,         32000,   768000,       800000,    30],
  "d1-1200k-4:3"  => [  640,  480,    0,         32000,  1168000,      1200000,    30],
  "d1-1200k-16:9" => [  852,  480,    0,         32000,  1168000,      1200000,    30],
  "hd-1800k-16:9" => [ 1280,  720,    0,         64000,  1736000,      1800000,    59.94],
  "hd-2400k-16:9" => [ 1280,  720,    0,         64000,  2272000,      2336000,    59.94],

  "108p4:3"       => [  144,  108,    0,         16000,    32000,        48000,    30],
  "144p16:9"      => [  192,  144,    0,         16000,    80000,        96000,    30],
  "216p4:3"       => [  288,  216,    0,         32000,   268000,       300000,    30],
  "216p16:9"      => [  384,  216,    0,         32000,   268000,       300000,    30],
  "240p4:3"       => [  320,  240,    0,         32000,   468000,       500000,    30],

  "360p4:3"       => [  480,  360,    0,         32000,   768000,       800000,    30],
  "480i4:3"       => [  640,  480,    1,         32000,   768000,       800000,    30],
  "480p4:3"       => [  640,  480,    0,         32000,   768000,       800000,    30],
  "480p16:9"      => [  852,  480,    0,         32000,  1168000,      1200000,    30],

  # unadopted standard
  #"720i"          => [ 1280,  720,    1,        64000,  1736000,    1800000,    30],
  # 0.92 megapixels, 2.76MB per frame
  "720p"          => [ 1280,  720,    0,         64000,   1736000,     1800000,    59.94],

  # https://support.google.com/youtube/answer/1722171?hl=en
  # h.264 stream rates, SDR quality
  "yt-sdr-360p30"  => [  640,  360,    0,       128000,   1000000,     1128000,    30],
  "yt-sdr-480p30"  => [  852,  480,    0,       128000,   2500000,     2628000,    30],
  "yt-sdr-720p30"  => [ 1280,  720,    0,       384000,   5000000,     5384000,    30],
  "yt-sdr-1080p30" => [ 1920, 1080,    0,       384000,   8000000,     8384000,    30],
  "yt-sdr-1440p30" => [ 2560, 1440,    0,       512000,  16000000,    16512000,    30],
  "yt-sdr-2160p30" => [ 3840, 2160,    0,       512000,  40000000,    40512000,    30],

  "yt-sdr-360p60"  => [  640,  360,    0,       128000,   1500000,     1628000,    60],
  "yt-sdr-480p60"  => [  852,  480,    0,       128000,   4000000,     4128000,    60],
  "yt-sdr-720p60"  => [ 1280,  720,    0,       384000,   7500000,     7884000,    60],
  "yt-sdr-1080p60" => [ 1920, 1080,    0,       384000,  12000000,    12384000,    60],
  "yt-sdr-1440p60" => [ 2560, 1440,    0,       512000,  24000000,    24512000,    60],
  "yt-sdr-2160p60" => [ 3840, 2160,    0,       512000,  61000000,    61512000,    60],
  #"yt-hdr-360p60"  => [ 1280,  720,    0,        32000,  1000000,   1800000,    60], # yt unsupported
  #"yt-hdr-480p60"  => [ 1280,  720,    0,        32000,  1000000,   1800000,    60], # yt unsupported

  "yt-hdr-720p30"  => [ 1280,  720,    0,       384000,   6500000,     6884000,    30],
  "yt-hdr-1080p30" => [ 1920, 1080,    0,       384000,  10000000,    10384000,    30],
  "yt-hdr-1440p30" => [ 2560, 1440,    0,       512000,  20000000,    20512000,    30],
  "yt-hdr-2160p30" => [ 3840, 2160,    0,       512000,  50000000,    50512000,    30],

  "yt-hdr-720p60"  => [ 1280,  720,    0,       384000,   9500000,     9884000,    60],
  "yt-hdr-1080p60" => [ 1920, 1080,    0,       384000,  15000000,    15384000,    60],
  "yt-hdr-1440p60" => [ 2560, 1440,    0,       512000,  30000000,    30512000,    60],
  "yt-hdr-2160p60" => [ 3840, 2160,    0,       512000,  75500000,    76012000,    60],

  "raw720p30"      => [ 1280,  720,    0,        64000,  221120000,  221184000,    30],
  "raw720p60"      => [ 1280,  720,    0,        64000,  442304000,  442368000,    60],

  # frame size 6.2MB
  # 1080i60 1920x1080 186MBps
  "raw1080i"       => [ 1920,  540,    1,       128000, 1486384000, 1486512000,    59.94],
  "raw1080i30"     => [ 1920,  540,    1,       128000, 1487872000, 1488000000,    30],
  "raw1080i60"     => [ 1920,  540,    1,       128000, 1487872000, 1488000000,    60],

  # 1080p60 1920x1080 373MBps, 6.2Mbps frame size
  "raw1080p"       => [ 1920, 1080,    0,       128000, 2975872000, 2976000000,    60],

  # Skype requirements below as listed on https://support.skype.com/en/faq/FA1417/how-much-bandwidth-does-skype-need
  # ^--- indicates there is a minimum TX requirement for stations
  #      group calls range from 128k up to 512k up, roughly HQ-recommended, maybe 1280x720x15
  # https://www.quora.com/Does-Skype-support-1080p-HD-video-calls
  # https://tomtalks.blog/2018/04/set-skype-for-business-to-record-meetings-at-1080p-and-30-fps/
  # Transmission quality is fundamentally different than YouTube -- it is constant TX that varies by
  # the amount of compression available. Variation between minimum required bandwidth and recommended
  # bandwidth is visible in packet captures.
  # Actual capture resolutions depend on your camera and can be manipulated via settings, esp frame rate:
  # https://superuser.com/questions/180690/how-to-reduce-the-skype-video-settings-to-work-with-an-older-computer
  # https://lifehacker.com/how-to-get-better-quality-out-of-your-video-chats-5836186
  # https://docs.microsoft.com/en-us/skypeforbusiness/plan-your-deployment/clients-and-devices/video-resolutions
  # ^--- This outlines a requirements for 4 core processors as requirement for Skype at 720p!
  # Jed is roughly interpolating many of these values for this table
  # nicname                       w,    h,  interlaced,   audio,    vid bps,   tt bps   framerate
  "skype-vox-min"          => [   0,    0,      0,        30000,      0,        30000,        0 ],
  "skype-vox-rcmd"         => [   0,    0,      0,       100000,      0,       100000,        0 ],
  # screen sharing falls into min requirement
  "skype-vid-min"          => [   424,  240,    0,        30000,      98000,     128000,     15 ],
  "skype-vid-rcmd"         => [   640,  360,    0,       100000,     200000,     300000,     30 ],
  "skype-vid-hq-min"       => [   960,  540,    0,       100000,     300000,     400000,     15 ],
  "skype-vid-hq-rcmd"      => [  1280,  720,    0,       100000,     400000,     500000,     30 ],
  "skype-vid-hd-min"       => [  1920, 1080,    0,       100000,    1100000,    1200000,     15 ],
  "skype-vid-hd-rcmd"      => [  1920, 1080,    0,       100000,    1400000,    1500000,     30 ],
  "skype-vid-grp3-min"     => [   640,  480,    0,        30000,     482000,     512000,     15 ],
  "skype-vid-grp3-rcmd"    => [  1280,  720,    0,       100000,     900000,    2000000,     15 ],
  "skype-vid-grp5-min"     => [   640,  360,    0,        30000,    1700000,    2000000,     15 ],
  "skype-vid-grp5-rcmd"    => [  1280,  720,    0,       100000,    3700000,    4000000,     15 ],
  "skype-vid-grp7-min"     => [   640,  360,    0,        30000,    3700000,    4000000,     15 ],
  "skype-vid-grp7-rcmd"    => [  1280,  720,    0,       100000,    7700000,    8000000,     15 ],

);

our $avail_stream_desc = join(", ", keys(%avail_stream_res));
our $resolution = "yt-sdr-1080p30";
my $list_streams = undef;

our $usage = "$0:    # modulates a Layer 3 CX to emulate a video server
    # Expects an existing L3 connection
  --mgr         {hostname | IP}
  --mgr_port    {ip port}
  --tx_style    { constant | bufferfill | L4 }
      # constant: for variable-br constant streaming, like Skype. UDP or TCP.
      # bufferfill: for framebuffer transmission, like YouTube, that monitors and throttles an existing Layer-3 connection
      #              High cpu load and imprecise technique, but uses a single constant connection. UDP or TCP
      # L4: for framebuffer transmission, like YouTube, but using more precise Layer-4 URL fetching pattern.
      #     This repeats the same curl fetch over and over, creating a new connection every time. More efficient, TCP only.
  --cx_name     {name}
  --tx_side     {A|B} # which side is emulating the server,
                      # default $::tx_side
  --max_tx      {speed in bps [K|M|G]} # use this to fill buffer
  --min_tx      {speed in bps [K|M|G]} # use when not filling buffer, default 0
  --buf_size    {size[K|M|G]}  # fill a buffer at max_tx for this long
  --stream_res  {$avail_stream_desc}
  --list_streams  # show stream bps table and exit
                  # default $resolution
  --log_cli {0|1} # use this to record cli commands
  --quiet {0|1|yes|no} # print CLI commands
  --silent        # do not print status output
  --quit_when_const # quits connection when constant tx detected
  --sta          {1.1.sta0 or 1.sta0} # use with L4 or constant
  --upstream     {1.1.eth1 or 1.eth1} # use with L4 or constant; will create HTTP service on port if necessary
  --proto        {udp|tcp} # use with constant tx style
  --begin_running {0|1} # bufferfill does not get created running, but constant and L4 do, overrides this

  Example:
  1) create the L3 connection:
    ./lf_firemod.pl --resource 1 --action create_endp bursty-udp-A --speed 0 --endp_type lf_udp --port_name eth1 --report_timer 500
    ./lf_firemod.pl --resource 1 --action create_endp bursty-udp-B --speed 0 --endp_type lf_udp --port_name eth2 --report_timer 500
    ./lf_firemod.pl --resource 1 --action create_cx --cx_name bursty-udp  --cx_endps bursty-udp-A,bursty-udp-B
   $0  --cx_name bursty-udp --stream 720p --buf_size 8M --max_tx 40M

  2) Create a Layer-4 connection:
   $0 --tx_style L4 --cx_name hunker --stream yt-sdr-1080p30 --buf_size 3M --port 1.sta0000
";

my $show_help = undef;
our $debug = 0;

$::stream_key = $resolution;
GetOptions
(
   'help|h'               => \$show_help,
   'quiet|q=s'            => \$::quiet,
   'debug|d'              => \$::debug,
   'silent+'              => \$::silent,
   'mgr|m=s'              => \$::lfmgr_host,
   'mgr_port|p:i'         => \$::lfmgr_port,
   'resource|r:i'         => \$::resource,
   'log_cli:s{0,1}'       => \$log_cli,
   'tx_style|style:s'     => \$::tx_style,
   'cx_name|e=s'          => \$::cx_name,
   'tx_side|side|s:s'     => \$::tx_side,
   'max_tx=s'             => \$::max_tx,
   'min_tx:s'             => \$::min_tx,
   'buf_size|buf=s'       => \$::buf_size,
   'stream_res|stream=s'  => \$::stream_key,
   'list_streams+'        => \$list_streams,
   'quit_when_const'      => \$::quit_when_const,
   'sta=s'                => \$::sta,
   'upstream|up|u=s'      => \$::upstream,
   'proto=s'              => \$::proto,
   'begin_running'        => \$::begin_running,
) || die($!);


if ($show_help) {
   print $usage;
   exit 0;
}

if ($list_streams) {
  print "Predefined Video Streams\n";
  print "=" x 72, "\n";
  print "         Stream         W      H         Audio+Video\n";
  my %sortedkeys = ();
  foreach my $oldkey (keys(%::avail_stream_res)) {
    my $ra_row  = $::avail_stream_res{$oldkey};
    my $x       =    10000000 + int(@$ra_row[$::stream_keys{x}]);
    my $y       =    10000000 + int(@$ra_row[$::stream_keys{y}]);
    my $b       = 10000000000 + int(@$ra_row[$::stream_keys{video_bps}]);
    my $newkey = "${b}_${x}_${y}_${oldkey}";
    $sortedkeys{$newkey} = $oldkey;
  }
  foreach my $sorted_key (sort(keys(%sortedkeys))) {
    my $key = $sortedkeys{$sorted_key};
    my $ra_row1 = $::avail_stream_res{$key};
    my $x       = @$ra_row1[$::stream_keys{x}];
    my $y       = @$ra_row1[$::stream_keys{y}];
    my $bps     = int(@$ra_row1[$::stream_keys{stream_bps}]);
    my $bps_sum = int(@$ra_row1[$::stream_keys{video_bps}]) + int(@$ra_row1[$::stream_keys{audio_bps}]);
    #my $warning = "";
    printf("[ %15s ]  %4s x %4s using %8s kbps", $key, $x, $y, ($bps/1000));
    if ($bps != $bps_sum) {
      print " Invalid BPS $bps, correct to $bps_sum";
    }
    print "\n";
  }
  exit 0;
}

if ($::quiet eq "0") {
  $::quiet = "no";
}
elsif ($::quiet eq "1") {
  $::quiet = "yes";
}

if (defined $log_cli) {
  if ($log_cli ne "unset") {
    # here is how we reset the variable if it was used as a flag
    if ($log_cli eq "") {
      $ENV{'LOG_CLI'} = 1;
      #print "LOG_CLI now 1\n";
    }
    else {
      $ENV{'LOG_CLI'} = $log_cli;
      #print "LOG_CLI now $log_cli\n";
    }
  }
}

#my @sigkeys = keys %SIG;
#print join(";", sort @sigkeys);
# ABRT;ALRM;BUS;CHLD;CLD;CONT;FPE;HUP;ILL;INT;IO;IOT;KILL;
# NUM32;NUM33;NUM35;NUM36;NUM37;NUM38;NUM39;NUM40;NUM41;NUM42;NUM43;NUM44;NUM45;NUM46;NUM47;NUM48;NUM49;
# NUM50;NUM51;NUM52;NUM53;NUM54;NUM55;NUM56;NUM57;NUM58;NUM59;NUM60;NUM61;NUM62;NUM63;
# PIPE;POLL;PROF;PWR;QUIT;RTMAX;RTMIN;SEGV;STKFLT;STOP;SYS;TERM;TRAP;TSTP;TTIN;TTOU;UNUSED;
# URG;USR1;USR2;VTALRM;WINCH;XCPU;XFSZ;__DIE__;__WARN__
#
# install signal handlers for stopping connections
$SIG{ABRT} = \&cleanexit;
$SIG{HUP} = \&cleanexit;
$SIG{INT} = \&cleanexit;
$SIG{KILL} = \&cleanexit;
$SIG{PIPE} = \&cleanexit; # <- this is how we're terminated, no output message seen
$SIG{SEGV} = \&cleanexit;
$SIG{STOP} = \&cleanexit;
$SIG{TERM} = \&cleanexit;
$SIG{QUIT} = \&cleanexit;

# ========================================================================
sub cleanexit {
   my ($msg) = @_;
   if (!(defined $msg) || ("" eq $msg)) {
      $msg = 'no msg';
   }
   if ((defined $::cx_name) && ("" ne $::cx_name)) {
      if (defined $::utils->telnet) {
         if ($::stop_cx_on_exit) {
            print STDERR "\nStopping $::cx_name: $msg\n";
            $::utils->doAsyncCmd($::utils->fmt_cmd("set_cx_state", "all", $::cx_name, "STOPPED"));
         }
         else {
            print STDERR ("CX '$::cx_name' will not be stopped.") unless $::silent;
         }
      }
      else {
         print STDERR ("No telnet session remains, CX '$::cx_name' will not be stopped.");
      }
   }
   exit 0;
}

# ========================================================================
# ========================================================================
sub rxbytes {
  my ($endp) = @_;
  die ("called rxbytes with no endp name, bye")
    unless((defined $endp) && ("" ne $endp));

  my @lines = split("\n", $::utils->doAsyncCmd("nc_show_endpoints $endp"));
  #Rx Bytes:           Total: 0           Time: 60s   Cur: 0         0/s
  my $bytes = 0;
  my @matches = grep {/^\s+Rx Bytes/} @lines;
  if (@matches < 1) {
    warn "rx-bytes not found for [$endp]\n";
    print join("\n> ", @lines), "\n";
    return 0;
  }
  ($bytes) = $matches[0] =~ /Rx Bytes:\s+Total: (\d+)/;
  if (!(defined $bytes)) {
    warn "no rx-bytes match for [$endp]\n";
    print "="x72, "\n";
    print $matches[0], "\n";
    print "="x72, "\n";
    print join("\n> ", @lines), "\n";
    return 0;
  }
  return $bytes;
}
# ========================================================================
# look for any TX/RX rates associated with station
sub get_txrx_rate {
   my ($lf_host, $lf_port, $rez, $cxnam, $rx_sid) = @_;
   my $rxendp = "${cxnam}-${rx_sid}";
   my $cmd = "./lf_firemod.pl --mgr $lf_host --mgr_port $lf_port -r $rez "
      ."--action show_endp --endp_name $rxendp --endp_vals EID";
   print "GET_TXRX: $cmd\n";
   my @lines = `$cmd`;
   chomp(@lines);
   my @matches = grep {/EID:/} @lines;
   return -1 if (@matches < 1);

   my ($discard1, $port_eid) = split(/:\s*/, $matches[0]);
   my $max_rate = 0;
   if (!(defined $port_eid) || ("" eq $port_eid)) {
      print STDERR "Unable to determine port eid, unable to update max_tx\n";
      return -1;
   }
   # find tx/rx rate
   my ($discard2, $rez2, $portid) = split(/[.]/, $port_eid);
   $cmd = "lf_portmod.pl --mgr $lf_host --mp $lf_port --resource $rez2"
         ." --port_name $portid --show_port Probed-TX-Rate,Probed-RX-Rate";
   @lines = `$cmd`;
   chomp(@lines);
   my $rate = 0;
   for my $line (@lines) {
      my @hunks = split(/:\s*/, $line);
      if (@hunks > 1) {
         $rate = $::utils->expand_unit_str($hunks[1]);
      }
      $max_rate = $rate if ($rate > $max_rate);
   }
   #if ($max_rate > 0) {
   #   print "Adjusting max-rate closer to $max_rate\n";
   #}
   return $max_rate
} # ~get_txrx_rate()

# ========================================================================

sub txbytes {
  my ($endp, $check_exit) = @_;
  die ("called txbytes with no endp name, bye")
    unless((defined $endp) && ("" ne $endp));

  my @lines = split("\n", $::utils->doAsyncCmd("nc_show_endpoints $endp"));
  #Tx Bytes:           Total: 0           Time: 60s   Cur: 0         0/s
  my $bytes = 0;
  my @matches = grep {/^L4Endp \[/} @lines;
  my $is_4 = (@matches > 0)? 1 : 0;

  if ($is_4) {
     @matches = grep {/^\s+Bytes Written/} @lines;
     if (@matches < 1) {
       warn "bytes-written not found for [$endp]\n";
       print join("\n> ", @lines), "\n";
       return 0;
     }
     ($bytes) = $matches[0] =~ /Bytes Written:\s+Total: (\d+)/;
  }
  else {
     @matches = grep {/^\s+Tx Bytes/} @lines;
     if (@matches < 1) {
       warn "tx-bytes not found for [$endp]\n";
       print join("\n> ", @lines), "\n";
       return 0;
     }
     ($bytes) = $matches[0] =~ /Tx Bytes:\s+Total: (\d+)/;
  }

  if (!(defined $bytes)) {
    warn "no tx-bytes match for [$endp]\n";
    print "="x72, "\n";
    print $matches[0], "\n";
    print "="x72, "\n";
    print join("\n> ", @lines), "\n";
    return 0;
  }
  # we want to exit if connection indicates stopped
  if ($check_exit) {
     @matches = grep { /Endpoint .*?NOT_RUNNING, .*/ } @lines;
     if (@matches > 0) {
        #print "Endpoint has stopped, exiting\n";
        cleanexit("Endpoint has stopped, exiting\n");
     }
  }
  return $bytes;
}

# ========================================================================
#     M A I N
# ========================================================================

if ($::quiet eq "1" ) {
   $::quiet = "yes";
}

# Configure our utils.
our $utils = new LANforge::Utils();
$::utils->connect($::lfmgr_host, $::lfmgr_port);

die ("Please provide buffer size")
  unless((defined $buf_size) && ("" ne $buf_size));
if ($buf_size =~ /[kmg]$/i) {
  my($n) = $buf_size =~ /(\d+)/;
  if ($buf_size =~ /k$/i) {
    $buf_size = $n * 1024;
  }
  elsif ($buf_size =~ /m$/i) {
    $buf_size = $n * 1024 * 1024;
  }
  elsif ($buf_size =~ /g$/i) {
    $buf_size = $n * 1024 * 1024 * 1024;
  }
  else {
    die("Whhhhhuuuuuut?");
  }
}

die("Please specify max tx bps")
  unless("" ne $::max_tx);
if ($::max_tx =~ /[kmg]$/i) {
  my($n) = $::max_tx =~ /(\d+)/;
  if ($::max_tx =~ /k$/i) {
    $::max_tx = $n * 1000;
  }
  elsif ($::max_tx =~ /m$/i) {
    $::max_tx = $n * 1000 * 1000;
  }
  elsif ($::max_tx =~ /g$/i) {
    $::max_tx = $n * 1000 * 1000 * 1000;
  }
  else {
    die("Whhhhhuuuuuut?");
  }
}
if ($::min_tx =~ /[kmg]$/i) {
  my($n) = $::min_tx =~ /(\d+)/;
  if ($::min_tx =~ /k$/i) {
    $::min_tx = $n * 1000;
  }
  elsif ($::min_tx =~ /m$/i) {
    $::min_tx = $n * 1000 * 1000;
  }
  elsif ($::min_tx =~ /g$/i) {
    $::min_tx = $n * 1000 * 1000 * 1000;
  }
  else {
    die("Whhhhhuuuuuut?");
  }
}


my @hunks = ();
my @lines = ();
my @matches = ();

if ((defined $::sta) && ("" ne $::sta)) {
   if ($::sta =~ /\./) {
      @hunks = split(/\./, $::sta);
      $::sta = $hunks[-1];
      if (("$::resource" ne $hunks[-2])) {
         print "Mismatch between station resource(${hunks[-2]}) and declared resource($::resource), bye.\n";
         exit(1);
      }
      @lines = split(/\r?\n/, $::utils->doAsyncCmd("nc_show_port 1 $::resource $::sta"));
      @matches = grep {/^Shelf: 1,/} @lines;
      if (@matches < 1) {
         print "Cannot find port $::resource.$::sta, bye\n";
         exit(1);
      }
   }
}

my $endp = $::cx_name."-".$::tx_side; # change me if L4
@hunks = ();
if ($::tx_style =~ /^l(ayer)?[-_]?4$/i ) {
   $::tx_style = "L4";
}
if ($::tx_style =~ /^const(ant)?$/i) {
   $::tx_style = "constant";
}
if (($::tx_style eq "L4") || ($::tx_style eq "constant")) {
   if (!(defined $::sta) || ("" eq $::sta)) {
      print "L4 and constant connections needs a station, bye\n";
      exit 1;
   }
   if (!(defined $::upstream) || ("" eq $::upstream)) {
      print "L4 and constant connection needs an upstream port, bye\n";
      exit 1;
   }
   if ($::upstream !~ /[.]/) {
      $::upstream_res = $::resource;
   }
   else {
      @hunks = split(/[.]/, $::upstream);
      $::upstream = $hunks[-1];
      $::upstream_res = $hunks[-2];
   }
   @lines = split(/\r?\n/, $::utils->doAsyncCmd("nc_show_port 1 $::upstream_res $::upstream"));
   @matches = grep {/^Shelf: 1,/} @lines;
   if (@matches < 1) {
      print "Cannot find upstream port $::upstream_res.$::upstream, bye\n";
      exit(1);
   }
   if ($::sta =~ /\./) {
      @hunks = split(/[.]/, $::sta);
      $::sta = $hunks[-1];
      die("resource ${hunks[-2]} for station $::sta is not listed resource: $::resource, bye.")
         if ($hunks[-2] ne $::resource);
   }
}
else {
   $::begin_running = 0;
}


# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# Layer-3 constant setup
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

if ($::tx_style =~ /constant/) {
   if ($::stream_key !~ /^skype-/) {
      print "Using 'constant' tx-style only makes sense when emulating Skype calls. Please choose different stream.\n";
      exit 1;
   }
   if ($::stream_key =~ /grp\d+/) {
      print "group calls not implemented presently\n";
      exit 1;
   }
   else {
      print "Call upload requirements still under development.\n";
   }

   # if someone sets stream resolution to "-min$", that's not a cap that Skype respects, skype will
   # search for more bandwidth...stream max will be /-rcmd$/, min will be /-min$/
   if ($::stream_key =~ /-min$/) {
      $::stream_key =~ s/-min/-rcmd/;
   }
}
die ("Please provide cx_name")
  unless((defined $::cx_name) && ("" ne $::cx_name));

my $stream_bps = 0;
die("Unknown stream key $::stream_key")
  unless(exists $::avail_stream_res{$::stream_key});

$stream_bps = @{$::avail_stream_res{$::stream_key}}[$::stream_keys{stream_bps}];

my $drain_time_sec = 0;
my $drain_wait_sec = 0;
my $stream_kbps = 0;

if ($::tx_style =~ /constant/) {
   my $stream_min = $::stream_key;
   $stream_min =~ s/-rcmd/-min/;

   $::min_tx = @{$::avail_stream_res{$stream_min}}[$::stream_keys{stream_bps}];
   $::max_tx = @{$::avail_stream_res{$::stream_key}}[$::stream_keys{stream_bps}];
   $stream_bps = $::max_tx;
   $stream_kbps = $stream_bps / 1000;
}
else {
   # estimated fill time is probably not going to be accurate because
   # there's no way to know the txrate between the AP and station.
   $::est_fill_time_sec  = (8 * $::buf_size) / ($::max_tx * 0.5);
   my $drain_time_sec = (8 * $::buf_size) / $stream_bps;
   my $drain_wait_sec = $drain_time_sec - $est_fill_time_sec;

   if ($drain_wait_sec <= 0) {
     my $stream_kbps = $stream_bps / 1000;
     print "Warning: constant transmit! Raise max_tx to at least $stream_kbps Kbps\n";
     $drain_wait_sec = 0;
   }

   my $buf_kB = $::buf_size / 1024;
   print "Filling $::stream_key $buf_kB KB buffer est ${est_fill_time_sec}sec, empties in ${drain_time_sec} sec\n"
     unless($::silent);
}
$stream_kbps = $stream_bps / 1000;

# check for cx if we're bufferfill
my $cx_exists = 0;
@lines = split("\r?\n", $::utils->doAsyncCmd($::utils->fmt_cmd("show_cx", "all", $::cx_name)));
@matches = grep {/Could not find/} @lines;
$cx_exists = 1 if (@matches == 0);

if (($::tx_style eq "bufferfill") && !$cx_exists) {
   print "Tx_style bufferfill requires your connection already exists, bye.\n";
   exit 1;
}

if (($::tx_style =~ /constant/) && !$cx_exists) {
   my $cmd = "./lf_firemod.pl --mgr $::lfmgr_host --mgr_port $::lfmgr_port --action create_cx "
      ."--cx_name $::cx_name --use_ports $::sta,$::upstream --use_speeds 128000,$::max_tx "
      ."--speed $::min_tx --max_speed $::max_tx --endp_type udp --report_timer 3000";
   my $result = `$cmd`;
   print "x"x72, "\n";
   print $result, "\n";
   print "x"x72, "\n";
}

print "Stopping and configuring $::cx_name\n" unless($silent);
if (($::tx_style eq "L4") && ($::cx_name !~ /^CX_/)) {
   $::cx_name = "CX_$::cx_name";
}
$::utils->doCmd($::utils->fmt_cmd("set_cx_state", "all", $::cx_name, "STOPPED"));

my @reports = ();
my $fill_starts = 1;
my $fill_stops = 0;
my $tt_bytes = 0;
my $ave_fill_bytes = 0;
my ($starttime_sec, $starttime_usec) = gettimeofday();
$starttime_sec = $starttime_sec + ($starttime_usec / 1000000);
my $begin = $starttime_sec;
my $last_report_sec = $starttime_sec;
my $report_period_sec = 6;
my $check_if_stopped = 0;
my $cmd ="";
my $res = 1;
my $port = "Unknown";
my $type = $::proto;
our $stop_cx_on_exit = 1;

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# Layer-4 setup
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
if ($::tx_style eq "L4") {
   # check that the upstream port has http enabled
   $::stop_cx_on_exit = 0;
   my $cmd = "./lf_portmod.pl --mgr $::lfmgr_host --mgr_port $::lfmgr_port --port_name $::upstream --show_port Current,IP";
   my @lines = `$cmd`;
   chomp(@lines);

   if ($lines[0] !~ / SVC-HTTPD/m ) {
      print "Enabling HTTP on $::upstream...\n";
      #"set_port 1 1 eth1 NA NA NA NA 0 NA NA NA NA 134217730 " # <--- and to turn off
      $cmd = $::utils->fmt_cmd("set_port", 1, $::resource,  $::upstream,
                              "NA", "NA", "NA", "NA", 35184372088832, "NA", "NA", "NA", "NA", 134217730);
      $::utils->doCmd($cmd);
      sleep(1);
   }
   my $ip = "0.0.0.0";
   if ($lines[1] =~ /^IP:\s+([^ ]+)$/) {
      $ip = $1;
   }
   else {
      print "Unable to find IP address for upstream port, bye.";
      exit 1;
   }
   my ($short_cx) = $::cx_name =~ /CX_(\S+)/;
   my $tmp_ep1 = $short_cx;
   my $tmp_ep2 = "D_$short_cx";

   $endp = $tmp_ep1; # L4 endpoints are not '-A', '-B'
   my $timeout = 2000; # ms
   die("Invalid drain time: $drain_time_sec")
      if ($drain_time_sec <= 0);
   my $url_rate = floor(600 / $drain_time_sec);

   my $short_size = $::buf_size;
   while ($short_size > 1024) {
      $short_size = floor($short_size / 1024);
   }
   my $url = "dl http://".$ip."/".$short_size."m.bin /dev/null";
   #print "URL $url\n";
   #sleep 10;

   # do not need to add dummy endpoint
   $::utils->doCmd($::utils->fmt_cmd(
      "add_l4_endp", $tmp_ep1, 1, $::resource, $::sta, "l4_generic", 0, $timeout, $url_rate, $url, ' '));
   #sleep 1;
   $cmd = $::utils->fmt_cmd("add_cx", $::cx_name, "default_tm", $tmp_ep1, "NA");
   $::utils->doAsyncCmd($cmd);
}

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# Layer-3 constant bufferfill
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#print "Stopping and configuring $::cx_name\n" unless($silent);
#$::utils->doCmd($::utils->fmt_cmd("set_cx_state", "all", $::cx_name, "STOPPED"));

@lines = split("\r?\n", $::utils->doAsyncCmd($::utils->fmt_cmd("nc_show_endp", $endp)));
@matches = grep {/ Shelf: 1, Card: /} @lines;
# create a L3 connection
if ($::tx_style =~ /constant/) {
   $::stop_cx_on_exit = 0;

   die ("No matches for show endp $endp")
     unless($matches[0]);
   ($res, $port, $type) = $matches[0] =~ /, Card: (\d+)\s+Port: (\d+)\s+Endpoint: \d+ Type: ([^ ]+)\s+/;
   if (!(defined $res) || !(defined $port) || !(defined $type)) {
      die("Unable to determine endpoint [$endp], bye");

   }
   $cmd = $::utils->fmt_cmd("add_endp", $endp, 1, $res, $port, $type,
       $NA,             # ip_port
       $NA,             # is_rate_bursty
       $::min_tx,       # min_rate
       (($::tx_style eq "bufferfill") ? $::min_tx : $::max_tx) # max_rate
     );
   print "CMD[$cmd]\n";
   sleep 5;
   $::utils->doAsyncCmd($cmd);
}



#
#     start CX
#
# avoid a stampede of scripts starting at the same time
my $rand_start_delay = rand(7);
   if (! $::debug) {
   print "Random start delay: $rand_start_delay...\n";
   $::utils->sleep_sec($rand_start_delay);
}

if (!(defined $endp) || !(defined $res) || !(defined $port) || !(defined $type) || !(defined $::max_tx) || !(defined $::min_tx)) {
   die("Unable to continue, missing values in: endp($endp) res($res) port($port) type($type) max_tx($::max_tx)");
}

if ($::tx_style !~ /bufferfill/) {
   if ($::begin_running) {
      $cmd = $::utils->fmt_cmd("set_cx_state", "all", $::cx_name, "RUNNING");
      #print "Starting $::cx_name: $cmd\n" unless($silent);
      $::utils->doCmd($cmd);
      print "started $::cx_name\n";
   }
   cleanexit("Done with setup on $::tx_style $::cx_name\n");
}

$cmd = $::utils->fmt_cmd("add_endp", $endp, 1, $res, $port, $type, $NA, $NA, $::max_tx, $::max_tx);
$::utils->doAsyncCmd($cmd);

my $startbytes = txbytes($endp, $check_if_stopped);
my @delta_reports = ();

do {
   ($starttime_sec, $starttime_usec) = gettimeofday();
   my $starttime = $starttime_sec + ($starttime_usec / 1000000 );
   if (($starttime - $begin) > 20) {
      $check_if_stopped = 1;
   }
   my $bytes = 0;
   my $num_checks = 0;
   my $prev_bytes = 0;
   # this might not be
   while($bytes < ($buf_size + $startbytes)) {
      $num_checks++;
      my ($delta1_sec, $delta1_usec) = gettimeofday();
      $prev_bytes = $bytes;
      $bytes = txbytes($endp, $check_if_stopped);
      my ($delta2_sec, $delta2_usec) = gettimeofday();
      my $rx_side = ($::tx_side eq "A") ? "B" : "A";
      my $updated_txbps = get_txrx_rate($::lfmgr_host, $lfmgr_port, $::resource, $::cx_name, $rx_side);
      if ($updated_txbps > 0) {
         $::max_tx = $updated_txbps;
         $::est_fill_time_sec  = (8 * $::buf_size) / ($::max_tx * 0.5);
         $drain_wait_sec = $drain_time_sec - $::est_fill_time_sec;
      }
      $delta1_sec = $delta1_sec + ($delta1_usec/1000000);
      $delta2_sec = $delta2_sec + ($delta2_usec/1000000);
      #push(@delta_reports, sprintf(" Sent %d B, d %.5f",($bytes-$prev_bytes), ($delta2_sec - $delta1_sec)));
      push(@delta_reports, sprintf(" Sent %d B/ %.5f bps;",
         ($bytes-$prev_bytes),
         ($bytes-$prev_bytes)/($delta2_sec - $starttime) ));
      last if ($bytes > ($buf_size + $startbytes));

      # if we're taking unreasonably long, let's just escape
      if (($delta2_sec - $starttime) > (12 * $last_fill_time_sec)) {
         push(@reports, sprintf("Likely overfill detected, txsec: %.4f", ($delta2_sec - $starttime)));
         last;
      }
      #push(@delta_reports, "z");
      $::utils->sleep_ms(200);
      #$::utils->sleep_ms( 5 * ($delta2_sec - $delta1_sec));
   }
   # startbytes is only needed on iteration 0
   $startbytes = 0;
   my ($finishtime_sec, $finishtime_usec) = gettimeofday();
   $finishtime_sec = ($finishtime_sec + ($finishtime_usec / 1000000));
   $last_fill_time_sec =  $finishtime_sec - $starttime_sec;
   $tt_bytes += $bytes;

   $drain_wait_sec = $drain_time_sec - $last_fill_time_sec;
   push(@reports, sprintf("## drain_wait_seconds: %.4f; est fill: %.4f; actual fill %.4f; dev: %.4f",
      $drain_wait_sec, $est_fill_time_sec, $last_fill_time_sec, ($est_fill_time_sec - $last_fill_time_sec )));
   push(@reports, "deltas: ".join(',', @delta_reports));

   if ($::quit_when_const && ($fill_stops > 1) && ($drain_wait_sec <= 0)) {
      # this is a failure condition, we are misconfigured or overloaded
      cleanexit("Constant TX Quit: Wait $drain_wait_sec = Drain $drain_time_sec - Fill time $last_fill_time_sec;\n"
               .join("\n", @reports));
   }

   #push(@reports, "   deltas: ".join(',', @delta_reports));
   @delta_reports = ();

   #if ($drain_wait_sec > 0) { # we don't really want to never stop, that's not useful
   $cmd = $::utils->fmt_cmd("add_endp", $endp, 1, $res, $port, $type, $NA, $NA, $::min_tx, $::min_tx);
   $::utils->doCmd($cmd);
   $fill_stops++;
   #$ave_fill_bytes = $tt_bytes / $fill_stops;
   #push(@reports, "# $fill_starts fills for ave ${ave_fill_bytes}B/fill");

   $::utils->sleep_sec($drain_wait_sec);
   $startbytes = txbytes($endp, $check_if_stopped);
   push(@reports, "Setting max_tx to $::max_tx");
   $cmd = $::utils->fmt_cmd("add_endp", $endp, 1, $res, $port, $type, $NA, $NA, $::max_tx, $::max_tx);
   $::utils->doCmd($cmd);
   $fill_starts++;
   #}
   if (($finishtime_sec - $last_report_sec) >= $report_period_sec) {
      print (join("\n", @reports), "\n");
      @reports = ();
      $last_report_sec = $finishtime_sec;
   }
} while(1);

#