# mipushbox

This reads the weight from a Xiami Mi Scale, records it into a CSV in a Dropbox App Folder, and pushes it to your smartphone via Pushover. It is tested on a raspberry pi.

## Installation

1. Download this repo and install the dropbox and bluetooth modules via pip
	
	```
	pip install dropbox bluetooth
	```
2. Download blescan from [here](https://github.com/switchdoclabs/iBeacon-Scanner-/blob/master/blescan.py)
3. Create a Dropbox "App Folder" app [see here](https://dropbox.com/developers/apps)
4. Create a Pushover account and application
5. Find out your Mi Scale MAC address (any bluetooth le scanner should work fine for this)
6. Call mipushbox like this:
	
	```
	DROPBOX_ACCESS_KEY=abc123 MI_SCALE_MAC="ab:cd:ef:12:34:56" PUSHOVER_API_KEY=abc1234 PUSHOVER_USER_KEY=abc12345 ./mipushbox.py 
	```