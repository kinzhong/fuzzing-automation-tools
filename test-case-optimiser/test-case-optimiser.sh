#!/bin/bash

DisplayHelp(){
        #display help
        echo "test-minimiser.sh - Runs afl-cmin and afl-tmin (parallelised) with no memory limits enabled."
        echo "Usage: ./test-minimiser.sh [input_dir] [output_dir] [cores] [timeout] [\"./AFL-INSTRUMENTED-PROGRAM @@\"]"
}



while getopts ":h" option; do
   case $option in
      h) # display Help
         DisplayHelp
         exit;;
     \?) # incorrect option
         echo "Error: No such option"
         exit;;
   esac
done

# Main Program                                                              

if [ "$#" -ne 5 ]; then
	echo "Illegal number of arguments!"
	DisplayHelp
	exit
fi

curr_dir=$(pwd)
input_dir=${curr_dir}/${1}
output_dir=${curr_dir}/${2}
cores=$3
timeout=$4
command=$5

cores=$(( cores - 1 ))

echo $input_dir
echo $output_dir

mkdir temp_dir
mkdir $output_dir

#Run afl-cmin
afl-cmin -m none -t $timeout -i $input_dir -o temp_dir $command


files=(temp_dir/*)
no_of_files=`ls temp_dir | wc -l`


#echo total cores $cores

for i in `seq 0 $cores $no_of_files`
do
	for j in `seq 0 $cores`	
	do
		#echo Using Core $j
		file=${files[$i+$j]}
		short_file="${file##*/}"
		if [ ! -z "$file" ]
		then
			afl-tmin -m none -i $file -o $output_dir/$short_file.min $command &
		fi
	done
done
