# test utilities for LANforge scripts
package LANforge::Test;
use strict;
use warnings;
use diagnostics;
use Carp;

# Ubuntu: libtest2-suite-perl
use Test2::V0 qw(ok fail done_testing);
use Test2::Tools::Basic qw(plan);


$SIG{ __DIE__  } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };

# Un-buffer output
$| = 1;
use Data::Dumper;

if (defined $ENV{'DEBUG'}) {
   use Data::Dumper;
   use diagnostics;
   use Carp;
   $SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
}

require Exporter;
our @EXPORT_OK=qw(new test);

#our $FAIL   = 'fail';
#our $OK     = 'pass';
#our $PASS     = 'pass';
our @test_errors = ();

sub new {
   my $class = shift;
   my $self = {};
   my %parm = @_;
   $self->{'Name'} = $parm{'Name'};
   $self->{'Desc'} = $parm{'Desc'};
   $self->{'Errors'} = [];
   $self->{'ExpectedNumber'} = 1;
   $self->{'Test'} = undef;
   if (defined $parm{'Test'}) {
      #print "new: Creating Test $self->{'Name'}\n";
      $self->{'Test'} = $parm{'Test'};
   }
   if (defined $parm{'ExpectedNumber'}) {
      $self->{'ExpectedNumber'} = $parm{'ExpectedNumber'};
   }
   bless $self, $class;
   return $self;
}

sub run {
  plan(1);
  my $self = shift;
  print "Run $self->{Name}\n";
  my $result = shift;
  
  ok($result, $self->{'Name'}) || fail($self->{'Name'});
  done_testing();
}

sub test {
   my $self = shift;
   if (! (defined $self->{'Test'})) {
      print "LANforge::test lacks self->Test, please rewrite your script.\n";
      return $::FAIL;
   }
   return  $self->{'Test'}($self, @_);
}
sub test_err {
  my $self = shift;
  for my $e (@_) {
    my $ref = "".(caller(1))[3].":".(caller(1))[2]."";
    push (@::test_errors, "$ref: $e");
  }
}
1;