# SpyPi
An (un-)ethical hacking-station based on Raspberry Pi and Python.
OS: Raspbian
![1503514241914](https://user-images.githubusercontent.com/31287043/29633707-69c2e620-8847-11e7-989a-b9c80488df3d.jpg)
## What is SpyPi?
SpyPi is a white-hat hacking-station I've created as part of my high school graduation-work (2017). The device aims at raising awareness of data protection by letting people interactively get in touch with the topic. SpyPi provides different applications which help its user to learn about the risks of everyday tasks/activities involving technologies such as networks, contactless payment or social media. The interactive aspect allows user and SpyPi to meet at eye-level. The hacking-station is meant to be an on-going project. Its applications and the hardware can be expanded and improved by its user or creator.

## (un-)ethical, what do you mean?!
If the hacking-station in ethical or unethical is entirely dependent upon the operator. It's simply out of my control, although SpyPi is intended to be an ethical device.
## Hardware 
If you are interested in the hardware please visit my website *(coming soon)*.

## Please remember 
SpyPi is a **high school** project and was **created with very little programming** experience. Don't expect flawless code. Constructive criticism is appreciated!

The Project is licensed under the Apache License 2.0
## Okay cool, but what does it do?
### Network Scanner
Gets basic information from surrounding networks like BSSID, ESSID, encryption and authentication type.
### Brute-Force dict.
Allows user to attack network with a custom or pre-made password list.
### Mifare default key attack
Tests out if Mifare Classic 1K card uses any default read-permission keys.
### Mitmproxy Login-Data Catcher
Catches formular data from HTTPS POST requests by the SpyPi AP (transparent proxy) client. Every chatch is stored in a file and listed with it's host and time of request.
### Twitter Data-Miner
Mines incoming Tweets containing a string the user chooses himself. Collects Data until ```Ctrl + C```

## How to use
### scanner.py
```
sudo python3 scanner.py
```
### Bruteforce.py
```
sudo python3 Bruteforce.py
```
### login_proxy.py
Make sure you've... 
- installed mitmproxy, Python 3.5 or above (I suggest pyenv) and OpenSSL 1.0.2 via Jessie Backports
- created a wireless AP following [this tutorial](https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/overview) 
- created a text files named proxy.txt

Open two terminal windows or split screen:

Window 1:
```
tail -f proxy.txt
```
Window 2:
Set iptable rules:
```
sudo iptables -F
sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
sudo iptables -A FORWARD -i wlan1 -o wlan0 -m state — state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp — dport 80 -j REDIRECT — to-port 8080
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp — dport 443 -j REDIRECT — to-port 8080
```
run:
```
mitmproxy ~s "/home/pi/login_proxy.py" -T --host
```
### mifare.py
```
sudo python mifare.py
```
### twitter-mining.py
Make sure you've created your own Twitter application and inserted the keys in the key.py file.
```
sudo python3 twitter-mining.py
```
