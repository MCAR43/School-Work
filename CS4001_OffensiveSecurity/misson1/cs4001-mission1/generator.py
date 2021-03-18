import socket

HOST = "m1t1.hackback.dev"
PORT = 16850
with open("notbad", "r") as file:
	BASE_PAYLOAD = file.readline()

def connect(host, port, command):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	s.sendall(command)
	while True:
		data = s.recv(1024)
		if data == "":
			break
		print(str(repr(data)))
	print("done")
	s.close()

connect(HOST, PORT, BASE_PAYLOAD)
