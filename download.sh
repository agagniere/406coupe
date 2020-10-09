#!/bin/bash
echo "Filename,Horsepower,Registration date,Gearbox,Fuel,Price,Mileage,Color" > data.csv
echo "Title,Price,City,Brand,Model,Type,Registration date,Mileage,Horsepower,Fuel,Gearbox,Color" > ads.csv
for file in `find . -name '*.html'`
do
	echo $file
	perl parser.pl < $file >> data.csv 2>/dev/null
done
