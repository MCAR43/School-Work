#!/bin/bash
EXECNAME="./parser"
INPUTFOLDER="input"
OUTPUTFOLDER="output"
MYOUTPUTFOLDER="myoutput"
MYDIFFS="mydiffs"
if [ ! -d "$INPUTFOLDER" ]; then
  echo "Error: Directory "$INPUTFOLDER" does not exist"
  exit 9999
elif [ ! -d "$OUTPUTFOLDER" ]; then
  echo "Error: Directory "$OUTPUTFOLDER" does not exist"
  exit 9999
elif [ ! -f "$EXECNAME" ]; then  
  echo "Error: "$EXECNAME" does not exist"
  exit 9999
fi

if [ ! -d "$MYOUTPUTFOLDER" ]; then
  echo "Error: Directory "$MYOUTPUTFOLDER" does not exist"
  echo "Creating Directory "$MYOUTPUTFOLDER""
  mkdir "$MYOUTPUTFOLDER"
fi

rm -r "$MYDIFFS"
if [ ! -d "$MYDIFFS" ]; then
  echo "Creating Directory "$MYDIFFS""
  mkdir "$MYDIFFS"
fi

for i in "$INPUTFOLDER"/*.txt
do
  IFILE="$i"
  FILE_NAME=$(echo "$i" | rev | cut -d '/' -f 1 | rev)
  OFILE="$MYOUTPUTFOLDER"/my_"$FILE_NAME"
  DIFF_FILE="$OUTPUTFOLDER"/"$FILE_NAME".out
  "$EXECNAME" "$IFILE" > "$OFILE" 
  if ! cmp -s "$DIFF_FILE" "$OFILE"
  then
    echo $(diff --brief "$IFILE" "$OFILE")
    diff "$DIFF_FILE" "$OFILE" > "$MYDIFFS"/"$FILE_NAME"
  fi
done
