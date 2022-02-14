package LANforge::GuiJson;
use strict;
use warnings;
use JSON;
#use Exporter 'import';
use Scalar::Util 'blessed';

if (defined $ENV{'DEBUG'}) {
   use Data::Dumper;
   use diagnostics;
   use Carp;
   $SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
}

our $NL="\n";

our @EXPORT_OK=qw(new);
our $refs_example = q( \@portnames or ["sta1", "sta2"] not ("sta1", "sta2"));

sub new {
  my $this = {
    'url'       => undef,
    'handler'   => undef,
    'uri'       => undef,
    'header'    => undef,
    'data'      => undef,
    'headermap' => {},
  };  # Create an anonymous hash, and #self points to it.

  bless $this;       # Connect the hash to the package Cocoa.
  return $this;     # Return the reference to the hash.
}

=pod
=head1 GuiResponseToHash
=cut
sub GuiResponseToHash {
   my $self = shift;
   my $response = shift;
   my $ra_data = JSON::decode($response);
   my $rh_data = {};
   $rh_data->{'handler'} = $ra_data->[0]->{'handler'};
   $rh_data->{'uri'} = $ra_data->[1]->{'uri'};
   $rh_data->{'header'} = $ra_data->[2]->{'header'};
   $rh_data->{'data'} = $ra_data->[3]->{'data'};
   #print Dumper($rh_data);
   return $rh_data;
}

sub Request {
  my $self = shift;
  $self->{'url'} = shift;
  if (!defined $self->{'url'}) {
    die("Request wants url; example 'http://localhost:8080/PortTab')");
  }
  my $json = JSON->new;
  my $ra_data = $json->decode(`curl -s $self->{'url'}`);
  #print "---------------------------------------------------------------------\n";
  #print Dumper($ra_data);
  #print "---------------------------------------------------------------------\n";

  $self->{'handler'} = @$ra_data[0]->{'handler'};
  die("GuiJson response missing 'handler'") if (!defined $self->{'handler'});

  $self->{'uri'}     = @$ra_data[1]->{'uri'};
  die("GuiJson response missing 'uri'") if (!defined $self->{'uri'});

  $self->{'header'}  = @$ra_data[2]->{'header'};
  die("GuiJson response missing 'header'") if (!defined $self->{'header'});

  $self->{'data'}    = @$ra_data[3]->{'data'};
  die("GuiJson response missing 'data'") if (!defined $self->{'data'});

  $self->MakeHeaderMap();
} # ~Request

sub MakeHeaderMap {
   my $self = shift;
   $self->{'headermap'} = {};
   if (!defined $self->{'header'}) {
     print STDERR Dumper($self);
      die("MakeHeaderMap: self->{'header'} unset\n");
   }
   my $index = 0;
   for my $headername (@{$self->{'header'}}) {
      $self->{'headermap'}->{$headername} = $index;
      $index++;
   }
}

sub GetHeaderMap {
  my $self = shift;
  return $self->{'headermap'};
}

=pod
=head1 GetRecordsMatching
GetRecordsMatching expects results of GetGuiResponseToHash and a list of port EIDs or names
$ra_ports = GetRecordsMatching($rh_data, $header_name, $value)
=cut
sub GetRecordsMatching {
   my $self = shift;
   my $header_name = shift;
   my $ra_needles = shift;
   my $ra_results = [];

   if (!defined $header_name || $header_name eq '') {
      print STDERR "GetRecordsMatching wants arg1: header name\n";
      return $ra_results;
   }

   if (!defined $ra_needles || ref($ra_needles) ne 'ARRAY') {
      print Dumper($ra_needles);
      my $example = q( \@portnames or ["sta1", "sta2"] not ("sta1", "sta2"));
      print STDERR "GetRecordsMatching wants arg3: list values to match against <$header_name>.\nPass array references, eg:\n$example\n";
      return $ra_results;
   }

   my $value = undef;
   my @matches = undef;
   for my $ra_port (@{$self->{'data'}}) {
      $value = $ra_port->[ $self->HeaderIdx($header_name)];
      #print "$header_name: $value\n";
      @matches = grep { /$value/ } @$ra_needles;
      if (@matches) {
         push(@$ra_results, $ra_port);
      }
   }
   return $ra_results;
} # ~GetRecordsMatching

=pod
=head1 HeaderTrans
HeaderTrans($name) is used to resolve header regex to a field
name. HeaderTrans uses $headermap keys if they match exactly,
even if the $name passed in looks like a regex. Field names
Not found in $self->headertrans hash are then resolved as
regexes using grep { /$name/ } @fieldnames. Only the first
match is cached.

$fieldname = HeaderIdx( "No CX (us)")
  # plain return 'No CX (us)'

$idx = HeaderIdx( "No CX.*")
  # regex evaluated only if 'No CX.*' doesn't exist
  # as a literal key in $self->headertrans
=cut
sub HeaderTrans {
  my $self = shift;
  my $headername = shift;
  my %headermap = %{$self->{'headermap'}};
  $self->{'headertrans'} = {}
    if (!defined $self->{'headertrans'});

  if (!defined $headername || "$headername" eq "") {
    die("HeaderTrans: Header name is empty or unset, bye\n");
    return -1;
  }
  my %headertrans = %{$self->{'headertrans'}};

  if (defined $headertrans{$headername}) {
    return $headertrans{$headername};
  }
  if (defined $headermap{$headername}) {
    $headertrans{$headername} = $headername;
    return $headername;
  }
  # look for regex matches next
  my @matches = grep { /$headername/ } keys %{$self->{'headermap'}};
  if (@matches < 1) {
    print STDERR "HeaderTrans: Headermap name <$headername> unmached, you get -1.\n";
    $headertrans{$headername} = -1;
    return -1;
  }
  my $a = $matches[0];
  $headertrans{$headername} = $a;
  if (@matches > 1) {
    print STDERR "Headermap name <$headername> has multiple matches, you get $a.\n";
  }
  return $a;
}

=pod
=head1 HeaderIdx
HeaderIdx($name) is used to resolve header name to index in
array holding record data. HeaderIdx uses HeaderTrans() to
map names ore regexes to resolved field names and only do
regex lookups once per pattern.
$idx = HeaderIdx( "Alias")   # plain name
$idx = HeaderIdx( "No CX.*") # regex
=cut
sub HeaderIdx {
  my $self = shift;
  my $headername = shift;
  my %headermap = %{$self->{'headermap'}};

  if (!defined $headername || "$headername" eq "") {
    die("Header name is empty or unset, bye\n");
    return -1;
  }
  my $key = $self->HeaderTrans($headername);

  if (defined $headermap{$key}) {
    return $headermap{$key};
  }
  print STDERR "headermap{$key} undefined, you get -1\n";
  return -1;
} # ~HeaderIdx

=pod
=head1 GetFields
Returns matching fields from a record;
$ra_needles are an array of strings to match to select records
$ra_field_names are field names to return from those records
$rh = GetFields($header_name, $ra_needles, $ra_field_names)
=cut
sub GetFields {
  my $self = shift;
  my $header_name = shift;
  my $ra_needles = shift;
  my $ra_field_names = shift;
  my $ra_records = [];
  my $rh_field_values = {};

  if (!defined $header_name || $header_name eq '') {
     print STDERR "GetFields wants arg2: header name\n";
     return $rh_field_values;
  }

  if (!defined $ra_needles || ref($ra_needles) ne 'ARRAY') {
     print Dumper($ra_needles);

     print STDERR "GetFields wants arg3: list values to match against <$header_name>.\nPass array references, eg:\n$::refs_example\n";
     return $rh_field_values;
  }
  if (!defined $ra_field_names || ref($ra_field_names) ne 'ARRAY') {
     my $arg_str = join(", ", @$ra_needles);
     print STDERR "GetFields wants arg4: list field names to return if <$header_name> matches <$arg_str>\nPass array references, eg:\n$::refs_example\n";
     return $rh_field_values;
  }

  $ra_records = $self->GetRecordsMatching($header_name, $ra_needles);
  return $rh_field_values if (@$ra_records < 1);

  for my $ra_record (@$ra_records) {
    next if (@$ra_record < 1);
    next if (! defined @$ra_record[$self->HeaderIdx($header_name)]);
    my $record_name = @$ra_record[$self->HeaderIdx($header_name)];
    next if (!defined $record_name || "$record_name" eq "");
    #print "record name[$record_name]\n";
    #print Dumper($ra_record);
    my $rh_record_vals = {};
    $rh_field_values->{$record_name} = $rh_record_vals;
    #print Dumper($ra_field_names);

    for my $field_name (@$ra_field_names) {
      next if (!defined $field_name || "$field_name" eq "");
      my $xl_name = $self->HeaderTrans($field_name);
      my $field_idx = $self->HeaderIdx($xl_name);
      next if (!defined @$ra_record[$field_idx]);
      #print "Field Name $field_name [".@$ra_record[$field_idx]."] ";
      $rh_record_vals->{$xl_name} = @$ra_record[$field_idx];
    }
    #print Dumper($rh_record_vals);
  }
  return $rh_field_values;
}
1;
