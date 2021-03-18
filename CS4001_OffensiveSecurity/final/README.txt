Must be compiled with `g++ -std=c++11 -lcurl *.cpp`

Important Files for grading:
 -> MarcoPolo/
 | -> polo/
   | -> cmds.txt
   | -> src/
     | -> requests.cpp: contains most of the functionality for the Polo implant
 | -> marco/
   | -> nartan.py: Contains the logic for intepreting commands from the implants as well as distributing commmands to the implants.
   | -> cmds.txt: Commands are input here to be distributed to the implants before being wiped by nartan.py to prevent duplicates
   | -> static/
     | -> bin/
       | -> enum.sh: Enumeration script for delivering system information, pieced together from multiple popular enumeration scripts available online
       | -> install.sh: install script that is retrieved from the server when the user runs the auto run command.
