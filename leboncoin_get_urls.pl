#!/usr/bin/perl

use warnings;
use strict;
use Data::Dumper;

while (my $line = <STDIN>)
{
	chomp ($line);
	if ($line =~ /"urls_large":\[(.+?)\]/) {
		my $urls = $1;
		while ($urls =~ /"(.+?\/(\w+\.[a-z]+))",?/g ) {
			print "$1\n";
		}
	}
}
