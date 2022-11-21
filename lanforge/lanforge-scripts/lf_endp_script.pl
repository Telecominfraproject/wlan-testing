#!/usr/bin/perl -w

# This program is used to create a hunt-script 
# used for matrix load emulation on LANforge
# (C) Candela Technologies 2015

use strict;
use warnings;
#use Carp;
#$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };

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

use constant      NA          => "NA";
use constant      NL          => "\n";
use constant      shelf_num   => 1;

# Default values for ye ole cmd-line args.
our $resource         = 1;
our $quiet            = "yes";
our $endp_name        = "";
our $action           = "";
our $lfmgr_host       = "localhost";
our $lfmgr_port       = 4001;

our $script_name     = undef;
our $script_type     = "";
our $flags           = "";
our $loops           = 0;
our $private         = "";
our $group_action    = "ALL";
our $log_cli         = "unset"; # use ENV{LOG_CLI} elsewhere

########################################################################
# Nothing to configure below here, most likely.
########################################################################

=pod
Below is an example of a set_script for script name bunny 
set_script hunt-sta-A bunny 4096 ScriptHunt '60000 1000 50000,100000,500000,20,56000,30000,1,100000, 60,128,256,512,1024,1280,1460,1472,1514 60,128,256,512,1024,1280,1460,1472,1514 100,300,400,600,800,955 NONE' ALL 0
which should follow this syntax:

   endp:          hunt-sta-A
   name:          bunny
   flags:         4096
   type:          ScriptHunt
   private:       '60000 1000 50000,100000,500000,20,56000,30000,1,100000, 60,128,256,512,1024,1280,1460,1472,1514 60,128,256,512,1024,1280,1460,1472,1514 100,300,400,600,800,955 NONE' 
   group_action:  ALL
   loop_count:    0

The private syntax is very opaque
   ScriptHunt syntax is: run_duration pause_duration constraints payload_sizes_a payload_sizes_b attenuations attenuator
   run_duration      60000
   pause_duration    1000
   constraints       50000,100000,500000,20,56000,30000,1,100000,
   payload_sizes_a   60,128,256,512,1024,1280,1460,1472,1514 60,128,256,512,1024,1280,1460,1472,1514 100,300,400,600,800,955
   payload_sizes_b   NONE
   attenuations      ?
   attenuator        ?
=cut


our $usage = qq<$0 ...
  [--action { set_script|start_cx|quiece_cx|stop_cx|show_report|del_script } ]
   set_script: configure a cx with script parameters set in script_type, script_flags
   show_port:  show script report for cx
   del_script: remove script from cx
   start_cx:   start traffic on a connection (thus starting script)
   quiece_cx:  stop transmitting traffic and wait a period before stopping connection recieve
   stop_cx:    stop transmit and recieve immediately
   # --action start_cx --cx_name bunbun
  [--mgr          {host-name | IP}]
  [--mgr_port     {ip port}]
  [--resource     {number}]
  [--quiet        { yes | no }]
  [--endp_name    {endpoint name}]
  [--cx_name      {endpoint name}]
  [--script_type  {2544|Hunt|WanLink|Atten} ]
                     2544        - RFC 2544 type script
                     Hunt        - Hunt for maximum speed with constraints
                     WanLink     - iterate thru wanlink settings
                     Atten       - use with attenuators
  [--flags        - see LF CLI User Guide script flags for set_port]
  [--script_name  - script name]
  [--loops        - how many time to loop before stopping; (0 is infinite)]
  [--private      - the nested script-type parameters in a single string]
  [--log_cli      {1|filename}]

Please refer to LANforge CLI Users Guide: http://www.candelatech.com/lfcli_ug.php#set_script

Examples:
# add a script to an endpoint
$0 --action set_script --script_type Hunt \\
   --script_name bunny --endp_name cx3eth0 -loops 1 --flags 4096 \\
   --private '60000 1000 50000,100000,500000,20,56000,30000,1,100000, 60,128,256,512,1024,1280,1460,1472,1514 60,128,256,512,1024,1280,1460,1472,1514 100,300,400,600,800,955 NONE' 

# start the cx to start the script:
$0 --action start_cx --cx_name hunt-sta 

# quiesce the cx
$0 --action quiece_cx --cx_name hunt-sta

# show the report
$0 --action show_report --endp_name hunt-sta-A

# stop the cx
$0 --action stop_cx --cx_name hunt-sta

# remove endpoint script
$0 --action del_script --endp_name hunt-sta-A
>;

my $i = 0;
my $cmd;
die($::usage) if (@ARGV < 2);

GetOptions
(
     'action|a=s'       => \$::action,
     'mgr|m=s'          => \$::lfmgr_host,
     'mgr_port|p=i'     => \$::lfmgr_port,
     'resource|r=i'     => \$::resource,
     'quiet|q=s'        => \$::quiet,
     'endp_name|e=s'    => \$::endp_name,
     'cx_name|c=s'      => \$::cx_name,
     'script_type|t=s'  => \$::script_type,
     'flags|f=i'        => \$::flags,
     'script_name|n=s'  => \$::script_name,
     'loops|l=i'        => \$::loops,
     'private|b=s'      => \$::private,
     'log_cli=s{0,1}'=> \$log_cli,
) || die("$::usage");


die("please specify action\n$usage")
   if (!defined $::action || $::action eq "");

if ($::action eq "set_script"
   || $::action eq "show_report"
   || $::action eq "del_script") {
   die("please specify endpoint name\n$usage")
      if (!defined $::endp_name || $::endp_name eq "");
}
if ($::action eq "set_script"
   || $::action eq "del_script") {

   die("please specify script name\n$usage")
      if (!defined $::script_name || $::script_name eq "");
}

if (defined $log_cli) {
  if ($log_cli ne "unset") {
    # here is how we reset the variable if it was used as a flag
    if ($log_cli eq "") {
      $ENV{'LOG_CLI'} = 1;
    }
    else {
      $ENV{'LOG_CLI'} = $log_cli;
    }
  }
}

# Open connection to the LANforge server.

our $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/',
          Timeout => 20);
$t->open(Host    => $lfmgr_host,
         Port    => $lfmgr_port,
         Timeout => 10);
$t->waitfor("/btbits\>\>/");

# Configure our utils.
our $utils = new LANforge::Utils();
$utils->telnet($t);         # Set our telnet object.
if ($::quiet eq "yes") {
  $utils->cli_send_silent(1); # Do show input to CLI
  $utils->cli_rcv_silent(1);  # Repress output from CLI ??
}
else {
  $utils->cli_send_silent(0); # Do show input to CLI
  $utils->cli_rcv_silent(0);  # Repress output from CLI ??
}

$::utils->log_cli("# $0 ".`date "+%Y-%m-%d %H:%M:%S"`);
our %script_types = (
   "2544"         => "Script2544",
   "Atten"        => "ScriptAtten",
   "Hunt"         => "ScriptHunt",
   "Script2544"   => "Script2544",
   "ScriptAtten"  => "ScriptAtten",
   "ScriptHunt"   => "ScriptHunt",
   "ScriptWanLink"=> "ScriptWL",
   "ScriptWL"     => "ScriptWL",
   "WanLink"      => "ScriptWL",
);

if ($::action eq "start_cx" 
   || $::action eq "stop_cx"
   || $::action eq "quiece_cx") {
   die("Please state cx_name")
      if (  !defined $::cx_name || $::cx_name eq "" );
}

if ($::action eq "set_script") {
   my $scr_type = $::script_types{ $::script_type };
   die("Unknown script type [$::script_type]")
      if (  !defined $::script_type
         || !defined $scr_type
         || $::script_type eq ""
         || $scr_type eq "" );
   die("Cannot use blank action.")
      if (! defined $::private || $::private eq "");

   $cmd = $::utils->fmt_cmd("set_script", $::endp_name, "$::script_name", $::flags, $scr_type, "$::private", $::group_action, $::loops);
   $::utils->doAsyncCmd($cmd);
}
elsif ($::action eq "show_report") {
   $cmd = $::utils->fmt_cmd("show_script_results", $::endp_name);
   $::utils->doAsyncCmd($cmd);
}
elsif ($::action eq "del_script") {
   $cmd = $::utils->fmt_cmd("set_script", $::endp_name, "$::script_name", "0", "NA", "NONE");
   $::utils->doAsyncCmd($cmd);
}
elsif ($::action eq "start_cx") {
   $cmd = $::utils->fmt_cmd("set_cx_state", "ALL", $::cx_name, "RUNNING");
   $::utils->doAsyncCmd($cmd);
}
elsif ($::action eq "quiece_cx") {
   $cmd = $::utils->fmt_cmd("set_cx_state", "ALL", $::cx_name, "QUIESCE");
   $::utils->doAsyncCmd($cmd);
}
elsif ($::action eq "stop_cx") {
   $cmd = $::utils->fmt_cmd("set_cx_state", "ALL", $::cx_name, "STOPPED");
   $::utils->doAsyncCmd($cmd);
}
else {
   die( "Unknown action.\n$usage");
}



#eof
