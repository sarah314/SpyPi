#Solomon 2017 
#Adjustment Sarah Mühlemann 2017

#!/bin/bash

#Creating a new IP table for the proxy
sudo iptables -F
sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
sudo iptables -A FORWARD -i wlan1 -o wlan0 -m state — state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp — dport 80 -j REDIRECT — to-port 8080
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp — dport 443 -j REDIRECT — to-port 8080

#Execute mitmdump
mitmdump -s "/home/pi/login_proxy.py" -T --host
