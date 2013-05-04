#!/usr/bin/env python

#	Litecoin-Price-Indicator
#--------------------------------------
#	by jj9 
#
#	if you feel the need to share some litecoin thanks or love
#	do so here. If you use this please credit it 
#
#	send any litecoin donations 
#     LUJz8yaS4uL1zrzwARbA4CiMpAwbpUwWY6
#

import sys
import gtk
import appindicator
import urllib2
from bs4 import BeautifulSoup
import json
import os
from os.path import expanduser
HOME = expanduser("~")

ICON = os.path.abspath(HOME+"/.local/share/applications/litecoinicon.png")
SETTINGSFILE = os.path.abspath(HOME+"/.local/share/applications/settingsLTC.txt")


BAD_RETRIEVE = 0.00001

class LitecoinPriceIndicator:
    PING_FREQUENCY = 2 # seconds
    showBTCE = True
    showMtGox = False
    showBitfloor = False
    showBit24 = False


    def __init__(self):
        self.ind = appindicator.Indicator("new-litecoin-indicator",
                                          ICON,
                                          appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.menu_setup()
        self.initFromFile()
        self.ind.set_menu(self.menu)

    def initFromFile(self):
        try:
            with open(SETTINGSFILE): pass
        except IOError:
            print 'Need to make new file.'
            file = open(SETTINGSFILE, 'w')
            file.write('3 \n')
            file.write('True \n')
            file.write('False \n')
            file.close()
        f = open(SETTINGSFILE, 'r')
        lines = f.readlines()
        self.PING_FREQUENCY = int(lines[0])
        #print "Show MtGox: ",self.str2bool(lines[2].strip())
        #self.showMtGox = self.str2bool(lines[2].strip())
        print "Show BTC-E: ",self.str2bool(lines[1].strip())
        self.showBTCE = self.str2bool(lines[1].strip())

    def str2bool(self,word):
        return word.lower() in ("yes", "true", "t", "1","ok")

    def menu_setup(self):
        self.menu = gtk.Menu()
        togBTCE = gtk.MenuItem("Show/Hide BTC-E")
        togBTCE.connect("activate", self.toggleBTCdisplay)
        togBTCE.show()
        #togMtGox = gtk.MenuItem("Show/Hide MtGox")
        #togMtGox.connect("activate", self.toggleMtGoxdisplay)
        #togMtGox.show()
        #self.menu.append(togMtGox)
        self.menu.append(togBTCE)
        
        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def toggleBTCdisplay(self, widget):
        if self.showBTCE:
            self.showBTCE = False
        else:
            self.showBTCE = True

    def toggleMtGoxdisplay(self, widget):
        if self.showMtGox:
            self.showMtGox = False
        else:
            self.showMtGox = True

    def main(self):
        self.getNewPrices()
        gtk.timeout_add(self.PING_FREQUENCY * 1000, self.getNewPrices)
        gtk.main()

    def quit(self, widget):
        try:
            print 'Saving Last State.'
            file = open(SETTINGSFILE, 'w')
            file.write(str(self.PING_FREQUENCY)+'\n')
            file.write(str(self.showBTCE)+'\n')
            file.write(str(self.showMtGox)+'\n')
            file.close()
        except IOError:
            print " ERROR WRITING QUIT STATE"
        gtk.main_quit()
        sys.exit(0)

    def getNewPrices(self):
        updatedRecently = self.update_price()
        return True

    def update_price(self):
        dataOut = ""
        priceNow = BAD_RETRIEVE
        if self.showBTCE:
            priceNow = float(self.getBTCELitecoinData())
            if priceNow == BAD_RETRIEVE:
                priceNow = "TempDown"
            else:
                priceNow = str(priceNow)+"USD"
            dataOut = dataOut + "|BTC-E: "+priceNow
            priceNow = float(self.getBTCELitecoinBTCData())
            if priceNow == BAD_RETRIEVE:
                priceNow = "TempDown"
            else:
                priceNow = str(priceNow)+"USD"
            dataOut = dataOut + "  :  LTC/BTC: "+priceNow
        if self.showMtGox:
            priceNow = float(self.getMtGoxData())
            if priceNow == BAD_RETRIEVE:
                priceNow = "TempDown"
            else:
                priceNow = str(priceNow)+"USD"
            dataOut = dataOut + "|MtGox: "+ priceNow
        self.ind.set_label(dataOut)
        return True

    def getMtGoxData(self):
        lstMtGox = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("http://data.mtgox.com/api/1/LTCUSD/ticker").read()
            data = json.loads(web_page)
            lstMtGox = data['return']['last']['value']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print 'Decoding JSON has failed'
        return lstMtGox


    def getBTCELitecoinData(self):
        lstLTCEprice = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("https://btc-e.com/exchange/ltc_usd").read()
            soup = BeautifulSoup(web_page)
            ind = 0
            for link in soup.find_all('strong'):
                ind = ind + 1
                if ind < 2 :
                    if ind == 1 :
                        lstLTCEprice = float((link.contents[0]).string[:-3])
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        return lstLTCEprice

    def getBTCELitecoinBTCData(self):
        lstLTCEprice = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("https://btc-e.com/exchange/ltc_btc").read()
            soup = BeautifulSoup(web_page)
            ind = 0
            for link in soup.find_all('strong'):
                ind = ind + 1
                if ind < 2 :
                    if ind == 1 :
                        lstLTCEprice = float((link.contents[0]).string[:-3])
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        return lstLTCEprice


if __name__ == "__main__":
    indicator = LitecoinPriceIndicator()
    indicator.main()
