#!/bin/bash

workingdir=/home/leftyfb/Pictures/Webcam/

while true
	do
         pics=$(ls $workingdir/*.jpg|wc -l)
	 result=$(date +%Y%m%d%H%M%S)
	 if [ "$pics" = "0" ]
	  then
	   sleep 0.1
	 elif [ "$pics" = "4" ]
	  then
	   sleep 1
	   echo "merging them..."
	   cd $workingdir
	   for i in `ls *.jpg`;do convert $i -border 8x2 new-$i ;done
	   convert $(ls new*.jpg) -append singlestrip.jpg
	   convert singlestrip.jpg singlestrip.jpg +append doublestrip.jpg
	   echo "printing ..."
           lp -o media=Custom.4x6in doublestrip.jpg
	echo "moving singlestrip to Halloween"
	   mv singlestrip.jpg /home/leftyfb/Dropbox/Photos/Halloween/$result.jpg
	echo "deleting temp files and doublestrip"
	   rm new* doublestrip.jpg
	echo "moving singles to photo stream"
	   mv *.jpg /home/leftyfb/Dropbox/Photo\ Stream/Uploads
	  fi
	  sleep 1
	done
