#!/bin/bash
for file in `find . -name '*.html'`
do
	echo $file
	folder=${file%.html}
	( mkdir $folder && cd $folder && perl ../../code/parser.pl < ../$file)
done
