# JsonUtils
package LANforge::JsonUtils;
use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{ __DIE__  } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };

# Un-buffer output
$| = 1;
use Getopt::Long;
use JSON::XS;
use HTTP::Request;
use LWP;
use LWP::UserAgent;
use JSON;
use Data::Dumper;

if (defined $ENV{'DEBUG'}) {
   use Data::Dumper;
   use diagnostics;
   use Carp;
   $SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
}

our $NL="\n";
use Exporter 'import';
our @EXPORT_OK=qw(err logg xpand json_request get_links_from get_thru json_post get_port_names flatten_list);

sub err {
   my $i;
   for $i (@_) {
      print STDERR "$i";
   }
   print STDERR $NL;
}

sub logg {
   my $i;
   for $i (@_) {
      print STDOUT "$i ";
   }
   # print STDOUT $NL;
}

sub xpand {
   my ($rrl) = @_;
   die("Will not expand a blank URI") if ("" eq $rrl || $rrl =~ m/^\s*$/);
   return $rrl if ($rrl =~ /^http/);
   return $rrl if ($rrl =~ m{^$main::HostUri/});
   return "${main::HostUri}$rrl" if ($rrl =~ m{^/});
   return "${main::HostUri}/$rrl";
}

sub json_request {
   my ($uri) = @_;
   my $url = xpand($uri);
   #logg("$uri becomes $url\n");
   my $req = new HTTP::Request("GET" => $url);
   $req->header("Accept" => "application/json");
   my $response = $::Web->request($req);
   if ($response->code != 200) {
      err("Status ".$response->code.": ".$response->content."\n");
      if ($response->content =~ /(Can't connect|Connection refused)/) {
         exit(1);
      }
      return {};
   }
   #print Dumper($response->content);
   return $::Decoder->decode($response->content);
}

sub json_post {
   my ($uri, $rh_data) = @_;
   my $url = xpand($uri);
   #print STDERR "URI $uri\n";
   my $req = HTTP::Request->new("POST" => $url);
   $req->header('Accept' => 'application/json');
   $req->header('Content-Type' => 'application/json; charset=UTF-8');
   $req->content(encode_json($rh_data));
   #print "json_post: ".Dumper($rh_data);
   #print Dumper($req);
   my $response = $::Web->request($req);
   #print Dumper($response);
   if ($response->code != 200) {
      err("Status ".$response->code.": ".$response->content."\n");
      if ($response->content =~ /(Can't connect|Connection refused)/) {
         exit(1);
      }
      return {};
   }
   my $rh_response =  $::Decoder->decode($response->content);

   print Dumper($rh_response)
      if (  defined $rh_response->{"Resource"}
         && defined $rh_response->{"Resource"}->{"warnings"});
   print Dumper($rh_response)
      if (  defined $rh_response->{"errors"}
         || defined $rh_response->{"error_list"});
   return $rh_response;
}

# use this to create a flat hash of $eid ->{result data} when given
# [ { $eid->{data}}, {}, {} ] which is harder to navigate
sub flatten_list {
   my $rh_list = shift;
   my $list_name = shift;
   my $rh_irefs = {};
   return if (!defined $rh_list);
   #print "\n- FF ------------------------------------------------------------\n";
   #print Dumper($rh_list);
   #print "\n~ FF ------------------------------------------------------------\n";
   if (!defined $rh_list->{$list_name}) {
      print "flatten_list: $list_name not found\n";
      return;
   }
   if (ref $rh_list->{$list_name} eq "HASH") {
      return if ( (keys %{$rh_list->{$list_name}} < 1));
   }
   if (ref $rh_list->{$list_name} ne "ARRAY") {
      print "flatten_list: $list_name not Array Ref:\n";
      print "-------------------------------------------------\n";
      print Dumper($rh_list);
      print "-------------------------------------------------\n";
      return;
   }
   #print "\n- FG -------------------------------------------------------------------\n";
   #print Dumper($rh_list->{$list_name});
   #print "\n~ FG -------------------------------------------------------------------\n";
   my $v = @{$rh_list->{$list_name}};
   my @k = (@{$rh_list->{$list_name}});
   for (my $i=0; $i < $v; $i++) {
      my @rh_k = keys %{$k[$i]};
      my @rh_v = values %{$k[$i]};
      my $rh_id = $rh_k[0];
      #print "\n- FG -------------------------------------------------------------------\n";
      #print Dumper($rh_id);
      #print "\n~ FG -------------------------------------------------------------------\n";
      $rh_irefs->{$rh_id} = $rh_v[0];
   }
   #print "\n- FG -------------------------------------------------------------------\n";
   #print Dumper($rh_irefs);
   #print "\n~ FG -------------------------------------------------------------------\n";
   $rh_list->{"flat_list"} = $rh_irefs;
}

sub get_port_names {
   my ($rh_gpn, $arrayname) = @_;
   my $ra_gpn2 = $rh_gpn->{$arrayname};
   my $ra_gpn_links2 = [];
   #print Dumper($ra_gpn2);
   for my $rh_gpn2 (@$ra_gpn2) {
      #print Dumper($rh_gpn2);
      for my $key (keys %$rh_gpn2) {
         my $v = $rh_gpn2->{$key};
         next if (!(defined $v->{'_links'}));
         my $rh_i = {
            'uri' => $v->{'_links'},
            'alias' => $v->{'alias'}
         };
         if (defined $v->{'device'}) {
            $rh_i->{'device'} = $v->{'device'};
         }
         push(@$ra_gpn_links2, $rh_i);
      }
   }
   #print Dumper($ra_links2);
   return $ra_gpn_links2;
}

sub get_links_from {
   my ($rh_glf, $arrayname) = @_;
   my $ra_glf2 = $rh_glf->{$arrayname};
   my $ra_glf_links2 = [];
   for my $rh_glf2 (@$ra_glf2) {
      for my $key (keys %$rh_glf2) {
         my $v = $rh_glf2->{$key};
         next if (!(defined $v->{'_links'}));
         push(@$ra_glf_links2, $v->{'_links'});
      }
   }
   #print Dumper($ra_links2);
   return $ra_glf_links2;
}

# eg get_thru( 'interface', 'device' )
sub get_thru {
   my ($inner, $key, $rh_top) = @_;
   if (!(defined $rh_top->{$inner})) {
      print Dumper($rh_top);
      return -1;
   }
   my $rh_inner = $rh_top->{$inner};
   return $rh_inner->{$key};
}
1;
