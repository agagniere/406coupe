#!/usr/bin/perl

use warnings;
use strict;
use Data::Dumper;

my %result;

open(my $fh, "<", "raw.html") or die "Unable to open file. ";

while (my $line = <$fh>)
{
	chomp ($line);
	if ($line =~ /"subject":"([a-zA-Z 0-9]+?)"/)
	{
		$result{"Title"} = $1;
	}
	if ($line =~ /"price":\[(\d+?)\]/)
	{
		$result{"Price"} = int($1);
	}
	if ($line =~ /"key":"brand","value":"([a-zA-Z]+?)"/)
	{
		$result{"Brand"} = $1;
	}
	if ($line =~ /"key":"issuance_date","value":"([\/0-9]+?)"/)
	{
		$result{"Issuance date"} = $1;
	}
	if ($line =~ /"key":"model","value":"([-0-9a-zA-Z]+?)"/)
	{
		$result{"Model"} = $1;
	}
	if ($line =~ /"key":"mileage","value":"(\d+?)"/)
	{
		$result{"Mileage"} = int($1);
	}
	if ($line =~ /"key":"doors","value":"(\d+?)"/)
	{
		$result{"Doors"} = int($1);
	}
	if ($line =~ /"key":"vehicle_type","value":"(.+?)"/)
	{
		$result{"Type"} = $1;
	}
	if ($line =~ /"key":"fuel","value":"(\d+?)",.+?,"value_label":"([a-zA-Z]+)"/)
	{
		$result{"Fuel_id"} = int($1);
		$result{"Fuel"} = $2;
	}
	if ($line =~ /"key":"gearbox","value":"(\d+?)",.+?,"value_label":"([a-zA-Z]+)"/)
	{
		$result{"Gearbox_id"} = int($1);
		$result{"Gearbox"} = $2;
	}

	#	if ($line =~ /"body":"([:-_ a-zA-Z0-9]+)"/)
	if ($line =~/<span class="_1fFkI">(.+?)<\/span>/)
	{
		$result{"Description"} = $1;
	}
}

print Dumper(\%result);
