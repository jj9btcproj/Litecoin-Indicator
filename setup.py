import os
import shutil
from os.path import expanduser
import subprocess
from subprocess import call
import codecs

HOME = expanduser("~")

ICON = os.path.abspath(HOME+"/.local/share/applications/litecoinicon.png")
SETTINGSFILE = os.path.abspath(HOME+"/.local/share/applications/settingsLTC.txt")
INDICATORFILE = os.path.abspath(HOME+"/.local/share/applications/ltc-price-indicator.py")
DESKTOPFILE = os.path.abspath(HOME+"/.config/autostart/ltc-price-indicator.desktop")


removeIn = raw_input("Setup Or Remove? :")

removePack = False
if "emove" in removeIn.lower().strip():
    removePack = True
    print "Removing from system"

if removePack:
    os.remove(ICON)
    os.remove(DESKTOPFILE)
    os.remove(SETTINGSFILE)
    os.remove(INDICATORFILE)

else:
    dirIn = raw_input( "Enter a directory of zip file without an ending / (You can type just a period if in the directory):")
    dirIn = os.path.abspath(dirIn)
    print "Setup from  : ",dirIn
    iconTemp =dirIn+"/res/litecoinicon.png"
    indTemp =dirIn+"/litecoin-price-indicator.py"
    deskTemp =dirIn+"/litecoin-price-indicator.desktop"

    if not os.path.exists(HOME+"/.config/autostart/"):
		subprocess.call(["mkdir", HOME+"/.config/autostart/"])
    
    if not os.path.exists(HOME+"/.local/share/applications/"):
		subprocess.call(["mkdir", HOME+"/.local/share/applications/"])

    shutil.copyfile(iconTemp,ICON)
    shutil.copyfile(indTemp,INDICATORFILE)
    shutil.copyfile(deskTemp,DESKTOPFILE)



    try:
        print 'Make settings file :',SETTINGSFILE
        file = open(SETTINGSFILE, 'w')
        file.write('3 \n')
        file.write('True \n')
        file.write('False \n')
        file.close()
    except IOError:
        print "IO ERROR"

    subprocess.call(['./setupAlias.sh'])
    print "Script is located at : "+INDICATORFILE
    subprocess.call(["chmod","+x",INDICATORFILE])


    print " You can use that for auto start etc"
