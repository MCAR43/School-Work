#!/usr/bin/env python3
from scapy.all import *
from time import sleep

def sendProbe(src, bssid, dst="ff:ff:ff:ff:ff:ff"):
    packet = RadioTap()/Dot11(type=0, subtype=4,addr1=dst ,addr2=src,addr3=bssid)/Dot11ProbeReq()/Dot11Elt(ID="SSID",info="")
    sendp(packet)

while(True):
    sendProbe("00:00:li:sp:ya", "ff:ff:ff:ff:ff:ff")
