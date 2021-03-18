#!/bin/bash

#Zip File Names
INPUT_ZIP="sampleInput.ZIP"
OUTPUT_ZIP="expectedOutput.ZIP"
SUBMISSIONS_ZIP="submissions.ZIP"
#Folder Names
STUOUTPUT="stuOutput"
INPUTFOLDER="sampleInput"
OUTPUTFOLDER="expectedOutput"
SUBMISSIONSFOLDER="submissions"
#OUTPUT TEXT FILES
GRADES="grades.txt"
#unzipping our input and output
if [ ! -d "$INPUTFOLDER" ]; then
  unzip -d "$INPUTFOLDER" "$INPUT_ZIP"
fi

if [ ! -d "$OUTPUTFOLDER" ]; then
  unzip -d "$OUTPUTFOLDER" "$OUTPUT_ZIP"
fi

if [ ! -d "$SUBMISSIONSFOLDER" ]; then
  unzip -d "$SUBMISSIONSFOLDER" "$SUBMISSIONS_ZIP"
fi


if [ ! -d "$STUOUTPUT" ]; then
  mkdir "$STUOUTPUT"
fi

for stuExec in "$SUBMISSIONSFOLDER"/*.pl
do
  numFiles=0
  numRight=0
  #looping through the student submissions
  for inputFile in "$INPUTFOLDER"/*.txt
  do

    numFiles=$((numFiles + 1))
    #prepping theninputfile
    input=$(cat "$inputFile")

    #extracting the name of the student from the input file
    IFILE=$(echo "$inputFile" | rev |cut -d '/' -f 1 | rev) 

    #extracting the name of the input plus the name of the sutdent to append to the output file
    STUNAME=$(echo "$stuExec" | rev | cut -d '/' -f 1 | rev)
    STUNAME=$(echo "$STUNAME" | cut -d '.' -f 1)

    #executing the students program with the input file to thee output folder
    swipl -s "$stuExec" $input > "$STUOUTPUT"/"$IFILE".out 
    #Execute the diffs for each student
    for stuOut in "$STUOUTPUT"/*.out
    do
      diff --strip-trailing-cr -w "$stuOut" "$OUTPUTFOLDER"/"$IFILE".out > /dev/null 2>&1
      error=$?
      if [ $error -eq 0 ]; then
        numRight=$((numRight + 1))
        returnVal=$(grep -F $(cat "$OUTPUTFOLDER"/"$IFILE".out) $stuExec)
        echo "$returnVal"

        if grep -F $(cat "$OUTPUTFOLDER"/"$IFILE".out) $stuExec; then
          hardcoded="*"
        else
          hardcoded=""
        fi
      fi
    done #END INPUT LOOP

    #CLEAN OUT THE STUDENT FILES FROM THE OUTPUT FOLDER
    rm "$STUOUTPUT"/*.out
  done
  percent=$((100 / $numFiles))
  percent=$((percent * $numRight))
  echo "$STUNAME, $percent "$hardcoded"" >> grades.txt
done
#CLEANUP
rm -r "$STUOUTPUT"
rm -r "$INPUTFOLDER"
rm -r "$OUTPUTFOLDER"
rm -r "$SUBMISSIONSFOLDER"
