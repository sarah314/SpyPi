#Solomon 2017

#!/bin/bash

#Check if this script is run with root priveleges
if [$EUID -ne0]; then
    echo "[!]This script must be run as root!" 1>&2
    exit 1
fi

#Creating a new IP table for the proxy
iptables -F
iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
iptables -A FORWARD -i wlan1 -o wlan0 -m state — state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT
iptables -t nat -A PREROUTING -i wlan0 -p tcp — dport 80 -j REDIRECT — to-port 8080
iptables -t nat -A PREROUTING -i wlan0 -p tcp — dport 443 -j REDIRECT — to-port 8080

#Execute mitmdump
mitmdump -s "/home/pi/login_proxy.py" -T --host
