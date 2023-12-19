
#!/usr/bin/python
import codecs
filepath = '/home/pi/chosenNetwork.txt'
writeTo = '/etc/wpa_supplicant/wpa_supplicant.conf'
myInfo = []
shouldWrite = True


with codecs.open(filepath, 'r+', encoding='utf-8') as aFile:
	myInfo = aFile.readlines()

if len(myInfo) < 2:
	shouldWrite = False


if len(myInfo) > 1 and shouldWrite:
	with codecs.open(writeTo, 'w', encoding='utf-8') as aTarget:
		ssid = myInfo[0]
		ssid = ssid[:-1]
		wifiPass = myInfo[1]
		wifiPass = wifiPass[:-1]
		writeMe = r"""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

"""
		writeMe = writeMe + "\nnetwork={\n\tssid=\"" + ssid + "\"\n\tpsk=\"" + myInfo[1] + "\"\n\tkey_mgmt=WPA-PSK\n}"
		aTarget.write(writeMe)



