SUBZIP="submissions.zip"
SUBFOLDER="submissions"
#unzip the folders
unzip -d $SUBFOLDER $SUBZIP

#ensure the grades.txt file is empty
echo "" > grades.txt


for i in "$SUBFOLDER"/*.cpp
do
  #RENAME THE FILES
  STUNAME=$(echo "$i" | cut -d '_' -f 4 | cut -d '.' -f 1) 
  mv $i $SUBFOLDER/$STUNAME.cpp
  #COMPILATION
  g++ $SUBFOLDER/$STUNAME.cpp
  #RUN AND GET OUTPUT
  OUTPUT=$(./a.out 10 5)
  if [ $OUTPUT -eq 352 ]; then
    echo "$STUNAME, correct" >> grades.txt
  else
    echo "$STUNAME, incorrect" >> grades.txt
  fi
done

#cleanup executable
rm a.out

#cleanup directories
rm -r $SUBFOLDER

