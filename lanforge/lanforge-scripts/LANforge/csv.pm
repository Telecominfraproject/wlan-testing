package LANforge::csv;
use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
#use Data::Dumper;
#use Data::Dumper::Concise;

sub new {
   my $proto = shift;
   my $class = ref($proto) || $proto;
   my $self = {};
   $self->{'ignore_comments'} = 1;
   $self->{'skip_comments'}   = 0;
   $self->{'trim_whitespace'} = 1;
   $self->{'rows'}=();

   bless($self, $class);
   return $self;
}

sub readFile {
   my $self       = shift;
   my $filename   = shift;
   die ("readFile: no filename provided.")
      if (!defined $filename || $filename eq "");

   open(my $fh, "<", "$filename")
      or die("readFile: $!");

   my @lines = ();
   while(<$fh>) {
      chomp;
      my @row = undef;
      #print "COMMENT: $_\n" if (/^\s*?\#.*/ && $self->{ignore_comments});
      next if (/^\s*?\#.*/ && $self->{skip_comments});

      if (/^\s*?\#.*/ && $self->{ignore_comments}) {
         @row = ();
         push(@{$self->{rows}}, \@row);
         next;
      }
      else {
         @row = split(/,/);
      }
      # trim() on all cell values
      if ($self->{trim_whitespace}) {
         s{^\s+|\s+$}{}g foreach @row;
      }
      push(@{$self->{rows}}, \@row);
   }
   close $fh;
}

sub getRow {
   my $self       = shift;
   my $row_num    = shift;
   die("getRow: no row number provided")
      if (!defined($row_num) || $row_num eq "");

   return undef if ($row_num >= @{$self->rows});
   return ${$self->rows}[$row_num];
}

sub getCell {
   my $self       = shift;
   my $cell_num   = shift;
   my $row_num    = shift;
   my $default    = (shift || 'undef');

   die("getCell: no row number provided")
      if (!defined($row_num) || $row_num eq "");
   die("getCell: no cell number provided")
      if (!defined($cell_num) || $cell_num eq "");

   if ($row_num >= @{$self->{rows}}) {
      #warn Dumper(@{$self->{rows}});
      warn "row $row_num greater than number of rows(@{$self->{rows}})\n";
      return $default;
   }

   my $ra_row = ${$self->{rows}}[$row_num];

   if (!defined $ra_row) {
      #warn "row $row_num unset\n";
      return $default;
   }

   if ($cell_num >= @{$ra_row}) {
      #warn "cell $cell_num beyond size of row (".@{$ra_row}.")\n";
      #warn Dumper($ra_row);
      return $default;
   }

   if (!defined $ra_row->[$cell_num]) {
      #warn "value at [$cell_num,$row_num] unset\n";
      #warn Dumper($ra_row);
      return $default;
   }
   return $ra_row->[$cell_num];
}

sub getRows {
   my $self       = shift;
   return $self->{rows};
}

sub rows {
   my $self       = shift;
   return $self->{rows};
}

sub numRows {
   my $self       = shift;
   return 0+@{$self->{rows}};
}

1;
=pod
This is a simple CSV parser, please install Text::CSV or someting more sophisticated
For instance, do not embed commas or newlines into the csv cells.
=end
