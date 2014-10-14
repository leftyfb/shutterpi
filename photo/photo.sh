#!/bin/bash

for i in `ls *.jpg`;do convert $i -border 4x2 new-$i ;done
convert $(ls new*.jpg) -append result.jpg
convert result.jpg result.jpg +append result2.jpg

