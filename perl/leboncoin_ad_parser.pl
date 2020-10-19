#!/usr/bin/perl

use warnings;
use strict;
use Data::Dumper;

my %result;

while (my $line = <STDIN>)
{
	chomp ($line);

	if (not $line =~ /"attributes":/) {
		next;
	}

	if ($line =~ /"subject":"(.+?)"/) {
		$result{"Title"} = $1;
	}
	if ($line =~ /"price":\[(\d+?)\]/) {
		$result{"Price"} = int($1);
	}
	if ($line =~ /"body":"(.+?)"/) {
		$result{"Description"} = $1;
	}
	if ($line =~ /"city_label":"(.+?)"/) {
		$result{"City"} = $1;
	}
	if ($line =~ /"url":"https:\/\/(www.leboncoin.fr\/voitures\/\d+?.htm)"/) {
		$result{"Link"} = $1;
	}
	if ($line =~ /"urls_large":\[(.+?)\]/) {
		my $urls = $1;
		while ($urls =~ /"(.+?\/(\w+\.[a-z]+))",?/g ) {
			system "curl -O $1";
			push @{$result{"Pictures"}}, $2
		}
	}
	foreach my $key ( qw(brand issuance_date model vehicle_type vehicule_color) ) {
		if ($line =~ /"key":"$key","value":"(.+?)"/) {
			$result{$key} = $1;
		}
	}
	foreach my $key ( qw(mileage doors regdate seats horsepower horse_power_din) ) {
		if ($line =~ /"key":"$key","value":"(\d+?)"/) {
			$result{$key} = int($1);
		}
	}
	foreach my $key ( qw(fuel gearbox) ) {
		if ($line =~ /"key":"$key","value":"(\d+?)",.+?,"value_label":"(\w+?)"/) {
			$result{$key . "_id"} = int($1);
			$result{$key} = $2;
		}
	}
}

if (not defined $result{"issuance_date"} and defined $result{"regdate"}) {
	$result{"issuance_date"} = $result{"regdate"}
}

foreach my $pic (@{$result{"Pictures"}}) {
	print "$pic,$result{horse_power_din},$result{regdate},$result{gearbox_id},$result{fuel_id},$result{Price},$result{mileage},$result{vehicule_color}\n"
}

open(FH, '>>', "ads.csv") or die $!;
print FH "$result{Price},$result{City},$result{brand},$result{model},$result{vehicle_type},$result{issuance_date},$result{mileage},$result{horse_power_din},$result{fuel},$result{gearbox},$result{vehicule_color},$result{Link}\n";
close(FH);
