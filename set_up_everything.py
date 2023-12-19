#!/usr/bin/env python
import socket
import bluetooth
import subprocess
import os
import time
passwd = "humantouchnovo"
WiFi_Command = "python /home/pi/setWifiNetwork.py"
hotspot_command = " /usr/bin/autohotspot >/dev/null 2>&1"
daemon_command = "python /home/pi/NovoDaemon.py start"
BT_Command = "python /home/pi/set_BT_sound.py"
pair_Command = "/home/pi/BT_pair.sh"
airplay_command = "systemctl restart shairport-sync"


# OLD: BT commands before WiFi
#q = os.system('echo %s|sudo -S %s' % (passwd, BT_Command))
#time.sleep(1)
#r = os.system('echo %s|sudo -S %s' % (passwd, pair_Command))
#p = os.system('echo %s|sudo -S %s' % (passwd, WiFi_Command))
#time.sleep(2)
#t = os.system('echo %s|sudo -S %s' % (passwd, hotspot_command))

# NEW: WiFi before BT commands
p = os.system('echo %s|sudo -S %s' % (passwd, WiFi_Command))
time.sleep(2)
t = os.system('echo %s|sudo -S %s' % (passwd, hotspot_command))
time.sleep(1)


time.sleep(10) # time for both the wifi and bluetooth connections to establish


q = os.system('echo %s|sudo -S %s' % (passwd, BT_Command))
time.sleep(1)
r = os.system('echo %s|sudo -S %s' % (passwd, pair_Command))


mac_address = ""
filepath = '/home/pi/chosenBlueTooth.txt'
try:
    with open(filepath, 'r+') as aFile:
        myInfo = aFile.readlines()
        ssid = myInfo[0]
        mac_address = ssid
        print mac_address
        pass
except Exception as e:
    print e
    time.sleep(1)
    pass
finally:
    pass	

try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname("www.google.com")
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    cmd_string = """aplay -D bluealsa:HCI=hci0,DEV=""" + mac_address + """,PROFILE=a2dp bell.wav"""
    print cmd_string

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((mac_address, 7))
    time.sleep(1)
    sock.send('\xf0\x83\x01\x7b\xf1')
    time.sleep(2)
    sock.send('\xf0\x83\x16\x66\xf1')
    time.sleep(5)
    sock.send('\xf0\x83\x01\x7b\xf1')
    time.sleep(10)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    
    os.system(cmd_string)

except Exception as e:
    print "BT connection error", e
    time.sleep(5)
    os.system(cmd_string)
    try:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except Exception as sockerr:
        print "BT socket close error", sockerr
    pass


z = os.system('echo %s|sudo -S %s' % (passwd, daemon_command))

time.sleep(5)

s = os.system('echo %s|sudo -S %s' % (passwd, airplay_command))

