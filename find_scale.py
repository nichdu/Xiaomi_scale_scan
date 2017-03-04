#!/usr/bin/env python2.7
# mipushbox by Tjark Saul
# based on Xiaomi_scale_scan.py by chaeplin@gmail.com 
# based on SwitchDoc Labs's iBeacon-Scanner-
# https://github.com/switchdoclabs/iBeacon-Scanner-

import blescan
import sys
import time

dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print "error accessing bluetooth device..."
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

try:
    while True:
        returnedList = blescan.parse_events(sock, 1)
        if len(returnedList) > 0:
            (mac, uuid, major, minor, txpower, rssi) = returnedList[0].split(',', 6)
            if uuid[0:22] == '01880f10877fc30d161d18':
                print("Possible Mi Scale found. MAC address: %s" % mac)
except KeyboardInterrupt:
        sys.exit(1)