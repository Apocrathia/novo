#!/usr/bin/python

filepath = '/home/pi/chosenNetwork.txt'
writeTo = '/etc/wpa_supplicant/wpa_supplicant.conf'
myInfo = []
shouldWrite = True


if True and shouldWrite:
	with open(writeTo, 'w') as aTarget:
		ssid = "WifiNetwork"
		wifiPass = "WifiPass"
		writeMe = r"""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

"""
		writeMe = writeMe + "\nnetwork={\n\tssid=\"" + ssid + "\"\n\tpsk=\"" + wifiPass + "\"\n\tkey_mgmt=WPA-PSK\n}"
		aTarget.write(writeMe)


with open(filepath, 'w') as old_networks:
    old_networks.write( "ssid \nwifipass" )



