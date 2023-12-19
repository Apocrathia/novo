#!/usr/bin/python

from wifi import Cell, Scheme

cell = Cell.all('wlan0')


filepath = '/home/pi/WiFiNetworks.txt'
with open(filepath, 'w+') as the_file:
	for thing in cell:
		the_file.write(thing.ssid + '\n')

