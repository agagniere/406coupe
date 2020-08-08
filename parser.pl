#!/usr/bin/perl

use warnings;
use strict;
use Data::Dumper;

my %result;

while (my $line = <STDIN>)
{
	chomp ($line);

	#if ($line =~ /"body":"([:-_ a-zA-Z0-9]+)"/)
	if ($line =~/<span class="_1fFkI">(.+?)<\/span>/)
	{
		$result{"Description"} = $1;
	}

	if (not $line =~ /"attributes":/) {
		next;
	}

	if ($line =~ /"subject":"(.+?)"/) {
		$result{"Title"} = $1;
	}
	if ($line =~ /"price":\[(\d+?)\]/) {
		$result{"Price"} = int($1);
	}

	foreach my $key ( qw( brand issuance_date model vehicle_type ) ) {
		if ($line =~ /"key":"$key","value":"(.+?)"/) {
			$result{$key} = $1;
		}
	}
	foreach my $key ( qw( mileage doors ) ) {
		if ($line =~ /"key":"$key","value":"(\d+?)"/) {
			$result{$key} = int($1);
		}
	}

	if ($line =~ /"key":"fuel","value":"(\d+?)",.+?,"value_label":"([a-zA-Z]+)"/)
	{
		$result{"fuel_id"} = int($1);
		$result{"Fuel"} = $2;
	}
	if ($line =~ /"key":"gearbox","value":"(\d+?)",.+?,"value_label":"([a-zA-Z]+)"/)
	{
		$result{"gearbox_id"} = int($1);
		$result{"Gearbox"} = $2;
	}

}

print Dumper(\%result);
