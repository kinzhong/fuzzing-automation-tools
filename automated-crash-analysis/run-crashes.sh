#!/bin/bash

#For non-AFL fuzzers, change the header variable to correctly match crash filename!
header="/crashes/id*"

if [ "$#" -ne 3 ]; then
	echo "Illegal number of parameters"
	exit
fi

curr_dir=$(pwd)
input_dir=${curr_dir}/${1}
program_loc=${2}
other_options=${3}
count=0

for i in $input_dir*
do
        
        DIR="$i"$header
	
	for x in $DIR;
	do
    		[ -f "$x" ] || break
		echo "Error No. #"$count
    		ls "$x"
		./${program_loc} ${other_options} ${x}
		((count+=1))
	done

done

if [[ $count -eq 0 ]]
then
	echo "No crashes found!"
else
	echo "run-crashes.sh completed."
	echo "$count crashes were executed"
fi
