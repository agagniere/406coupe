#!/bin/bash
for file in `find . -name '*.html'`
do
	echo $file
	folder=${file%.html}
	( mkdir $folder && cd $folder && perl ../parser.pl < ../$file > ad.txt )
done
