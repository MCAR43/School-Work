#!/usr/bin/env bash
#Computer should be configured as a secure webserver support http and https traffic
#remote ssh access for a particular static ip address
#Connection tracking stateful in both directions
#Reject ALL incoming and outgoing TCP and UDP traffic not necessary for above functionality

#First rule to Reject All Incoming and Outgoing traffic by default, make exceptions later
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT DROP


#INPUT CHAIN
#allow all local connections
sudo iptables -A INPUT -i lo -j ACCEPT

#limit SSH connections to a particular static ip address
#for some reason IPtables doesn't want to play well with NEW, ESTABLISHED in one rule so these two are split up
sudo iptables -A INPUT -p tcp -s 192.168.56.1 --dport 22 -m conntrack --ctstate NEW -j ACCEPT
sudo iptables -A INPUT -p tcp -s 192.168.56.1 --dport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT

#Allows all incoming HTTP (port 80) and HTTPS (port 443) traffic in
sudo iptables -A INPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate ESTABLISHED -j ACCEPT
#incase we missed anything
sudo iptables -A INPUT -j REJECT

#FORWARD CHAIN
sudo iptables -A FORWARD -j REJECT

#OUTPUT CHAIN
#allow all local traffic out
sudo iptables -A OUTPUT -o lo -j ACCEPT
#Because we have OUTPUT DROP set we must allow established output connections
sudo iptables -A OUTPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate ESTABLISHED -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT

#In case we missed any rules
sudo iptables -A OUTPUT -j REJECT

sudo iptables-save

