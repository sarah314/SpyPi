# -*- coding: utf-8 -*-
# Sarah M. 2017 on the basis of MFRC522-python by mxgxw
import RPi.GPIO as GPIO
import signal
import MFRC522
import os
from colors import farben


continue_reading = True
GPIO.setwarnings(False)

# Programmbeendung
def end_read(signal,frame):
    global continue_reading
    print "Das Programm wird beendet"
    continue_reading = False
    GPIO.cleanup()

# Funksignale emfangen
signal.signal(signal.SIGINT, end_read)

# Zur Klasse MFRC522 wird ein Objekt erstellt
MIFAREReader = MFRC522.MFRC522()

# Mifare Classic Standardschlüssel
k0 = [0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5] # A0 A1 A2 A3 A4 A5
k1 = [0xb0, 0xb1, 0xb2, 0xb3, 0xb4, 0xb5] # B0 B1 B2 B3 B4 B5
k2 = [0x4d, 0x3a, 0x99, 0xc3, 0x51, 0xdd] # 4D 3A 99 C3 51 DD
k3 = [0x1a, 0x98, 0x2c, 0x7e, 0x45, 0x9a] # 1A 98 2C 7E 45 9A
k4 = [0xd3, 0xf7, 0xd3, 0xf7, 0xd3, 0xf7] # D3 F7 D3 F7 D3 F7
k5 = [0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff] # AA BB CC DD EE FF
k6 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00] # 00 00 00 00 00 00
k7 = [0xd3, 0xf7, 0xd3, 0xf7, 0xd3, 0xf7] # d3 f7 d3 f7 d3 f7
k8 = [0xa0, 0xb0, 0xc0, 0xd0, 0xe0, 0xf0] # a0 b0 c0 d0 e0 f0
k9 = [0xa1, 0xb1, 0xc1, 0xd1, 0xe1, 0xf1] # a1 b1 c1 d1 e1 f1
k10 = [0x71, 0x4c, 0x5c, 0x88, 0x6e, 0x97] # 71 4c 5c 88 6e 97
k11 = [0x58, 0x7e, 0xe5, 0xf9, 0x35, 0x0f] # 58 7e e5 f9 35 0f
k12 = [0xa0, 0x47, 0x8c, 0xc3, 0x90, 0x91] # a0 47 8c c3 90 91
k12 = [0x53, 0x3c, 0xb6, 0xc7, 0x23, 0xf6] # 53 3c b6 c7 23 f6
k13 = [0x8f, 0xd0, 0xa4, 0xf2, 0x56, 0xe9] # 8f d0 a4 f2 56 e9
k14 = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff] # FF FF FF FF FF FF

#Aufforderung
print farben.AUF + "Bitte halten Sie den RFID-Tag solange an den Leser, bis die gescannten Informationen erscheinen!" + farben.END

# Austesten der Standardpasswörter
key = []
sector = []
x = 0
while x < 64:
    for k in k0, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14:
        # Scan nach Tags
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # Die UID eines Tags entnehmen
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # Wenn die UID entnommen wurde, fortfahren...
        if status == MIFAREReader.MI_OK:

            # Den gescannten Tag auswählen
            MIFAREReader.MFRC522_SelectTag1(uid)

             # Authentifizierungsversuch
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, x, k, uid)
            
            # Check ob authentifiziert
            # Wenn ja infos speichern
            if status == MIFAREReader.MI_OK:
                content = "Sektor %s " % x + "Leseschlüssel: " +"{}".format(", ".join(hex(x) for x in k))
                sector.append(content)
                MIFAREReader.MFRC522_StopCrypto1()
                x = x + 1


# Ausgabe der UID und der gefundenen Schlüssel
print "UID: "+ farben.AUF +str(uid[0])+","+str(uid[1])+","+str(uid[2]) +","+str(uid[3])+","+str(uid[4])  + farben.END
for item in sector:
    print farben.IN + item + farben.END


