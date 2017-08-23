# -*- encoding: utf-8 -*-
# Sarah M. - 2017 on the basis of Hugo Chargois - 17 jan. 2010 - v.0.1
import os
import sys
import subprocess
from colors import farben

#BSSID    
def such_mac(cell):
    return matching_line(cell,"Address: ")

#ESSID
def such_name(cell):
    return matching_line(cell,"ESSID:")[1:-1]

#Verschlüsselung
def such_versch(cell):
    enc=""
    if matching_line(cell,"Encryption key:") == "off":
        enc="Offen" 
    if matching_line(cell,"Encryption key:") == "on":
        A = matching_line(cell, "IE: WPA Version ")
        B = matching_line(cell,"IE: IEEE 802.11i/WPA2 Version ")
        if A and B:
            enc ="WPA v."+str(A) +"/""WPA2 v."+str(B)
        else:
            for line in cell:
                matching = match(line,"IE:")
                if matching!=None:
                    wpa=match(matching,"WPA Version ")
                    wpa2=match(matching, "IEEE 802.11i/WPA2 Version ")
                    if wpa!=None:
                        enc="WPA v. "+str(wpa)
                    if wpa2!=None:
                        enc="WPA2 v. "+str(wpa2)
            if enc=="":
                enc="WEP"
    return enc

# Authentifizierung
def such_schlussel(cell):
    auth =""
    for line in cell:
        match = matching_line(cell,"Authentication Suites (1) : ")
        if match!=None:
            auth = match
        if match == None:
            auth = "Offen"
    return auth

#Regeln
rules={"ESSID":such_name,
       "PROT.":such_versch,
       "MAC":such_mac,
       "AUTH.":such_schlussel,
    }

#Spalten
columns=["ESSID","MAC","AUTH.","PROT."]

#Information entnehmen
def matching_line(lines, keyword):
    for line in lines:
        matching=match(line,keyword)
        if matching!=None:
            return matching

    return None

def match(line,keyword):
    line=line.lstrip()
    length=len(keyword)
    if line[:length] == keyword:
        return line[length:]
    else:
        if keyword in line:
            return line[line.index(keyword):]
        else:
            return None

#tabellarische Strukturierung 
       
def parse_cell(cell):
    parsed_cell={}
    for key in rules:
        rule=rules[key]
        parsed_cell.update({key:rule(cell)})
    return parsed_cell

def print_table(table):
    justified_table = []
    filter(None, table)
    #print(table)
    for line in table:
        justified_line=[]
        for i,el in enumerate(line):
            widths=list(map(max,map(lambda l: map(len,l), zip(*table))))
            justified_line.append(el.ljust(widths[i]+2))
        justified_table.append(justified_line)

    for line in justified_table:
        for el in line:
            print (farben.AUF + el, end = " ") 
        print()

def print_cells(cells):
    table=[columns]
    for cell in cells:
        cell_properties=[]
        for column in columns:
            cell_properties.append(cell[column])
        table.append(cell_properties)
    print_table(table)

# Ausgabe
def main():
    cells=[[]]
    parsed_cells=[]

    proc = subprocess.Popen(["iwlist", "wlan1" , "scan"],stdout=subprocess.PIPE, universal_newlines=True)
    out, err = proc.communicate()
    for line in out.split("\n"):
        cell_line = match(line,"Cell ")
        if cell_line != None:
            cells.append([])
            line = cell_line[-27:]
        cells[-1].append(line.rstrip())
    cells=cells[1:]

    for cell in cells:
        parsed_cells.append(parse_cell(cell))

    print_cells(parsed_cells)

main()


