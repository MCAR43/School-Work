import socket
import os
import subprocess
import binascii

print("Starting LSO Hop Point Listener...")
#print("\n")


ssFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssFT.bind(("0.0.0.0", 1337))
ssFT.listen(1)

i = 0

while True:
    (conn, address) = ssFT.accept()

    if not os.path.exists("./Payloads"):
        os.mkdir("./Payloads")

    file_path = "./Payloads/"
    text_file = str(i) + '_payload.txt'
    while os.path.isfile(file_path + text_file):
        i += 1
        text_file = str(i) + '_payload.txt'

    #Accept command string
    with open(file_path + text_file, "wb") as fw:
        i += 1
        print("Waiting... \n")
        while True:
            conn.send(b"Receiving File... \n")
            print("Receiving Payload... \n")
            data = conn.recv(1024)
            if len(data) < 1:
	        break
            print(data)
            fw.write(data)
            #fw.close()
        fw.close()
        conn.send(b"File Received! \n")
        #print("Payload Received! \n")


ssFT.close()
