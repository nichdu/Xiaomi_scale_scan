#!/usr/bin/env python2.7
# mipushbox by Tjark Saul
# based on Xiaomi_scale_scan.py by chaeplin@gmail.com 
# based on SwitchDoc Labs's iBeacon-Scanner-
# https://github.com/switchdoclabs/iBeacon-Scanner-
 

# test BLE Scanning software
# jcs 6/8/2014

# ble scan with nrf51822
# https://github.com/chaeplin/nrf51822_and_arduino/blob/master/_12-xiaomi_scale_scan/_12-xiaomi_scale_scan.ino

import blescan
import sys
import time

import bluetooth._bluetooth as bluez

import dropbox
import os
from datetime import datetime
import httplib, urllib

def Dropbox_Upload(val, unit):
    db = dropbox.Dropbox(os.environ['DROPBOX_ACCESS_KEY'])
    try:
        md, file = db.files_download("/weight.csv")
        content = file.content
    except:
        content = "timestamp;weight;unit\n"

    content +=  str(datetime.now()) + ";" + str(val) + ";" + unit + "\n"

    db.files_upload(content, "/weight.csv", mode=dropbox.files.WriteMode('overwrite', None))

def push(val, unit):
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
        "token": os.environ['PUSHOVER_API_KEY'],
        "user": os.environ['PUSHOVER_USER_KEY'],
        "message": str(val) + " " + unit,
        "title": "New scale measurement"
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    #print "ble thread started"

except:
    print "error accessing bluetooth device..."
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

measure_time = 0
value = 0.0

try:
    while True:
        returnedList = blescan.parse_events(sock, 1)
        if len(returnedList) > 0:
            (mac, uuid, major, minor, txpower, rssi) = returnedList[0].split(',', 6)
            # change mac and uuid
            if mac == os.environ['MI_SCALE_MAC'] and uuid[0:22] == '01880f10877fc30d161d18':
                measunit = uuid[22:24]  
                measured = int((uuid[26:28] + uuid[24:26]), 16) * 0.01

                unit = ''

                if measunit.startswith(('03', 'b3')): unit = 'lbs'
                if measunit.startswith(('12', 'b2')): unit = 'jin'
                if measunit.startswith(('22', 'a2')): unit = 'kg' ; measured = measured / 2
                  
                if unit:
                    if (int(time.time()) - measure_time) > os.environ['RESEND_TIME_SPAN'] or not measured == value:
                        print("measured : %s %s" % (measured, unit))
                        Dropbox_Upload(measured, unit)
                        push(measured, unit)
                        measure_time = int(time.time())
                        value = measured
                else:
                    print 'scale is sleeping'

        time.sleep(2)
                
        # to compare previous measurement , use major and minor ( should be time of measurement)
    
except KeyboardInterrupt:
        sys.exit(1)


