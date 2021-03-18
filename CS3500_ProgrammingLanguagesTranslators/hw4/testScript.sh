#!/bin/bash
for i in HW3_sample_input/*.txt
do
  IFILE=$i
  FILE_NAME=$(echo $i | rev | cut -d '/' -f 1 | rev)
  OFILE=HW3_my_output/my_$FILE_NAME
  DIFF_FILE=HW3_expected_output/$FILE_NAME.out
  ./parser < $IFILE > $OFILE 
  if cmp -s "$DIFF_FILE" "$OFILE"
  then
	  echo $FILE_NAME WORKING AS INTENDED
    echo $(diff "$DIFF_FILE" "$OFILE")
  else
  	echo $FILE_NAME NOT WORKING AS INTENDED
	  echo $(diff "$DIFF_FILE" "$OFILE")
  fi
done
