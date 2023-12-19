# NOTE: this code is the same as appears in set_up_everything.py
# NOTE: if chosenBlueTooth.txt is written before this is run, 
#       NovoDaemon.py will pick it up somehow and initiate a BT connection, 
#       causing this script to throw a "BT connection error (16, 'Device 
#       or resource busy')" error upon sock.connect(). To mitigate this we 
#       only write to chosenBlueTooth.txt at the end of the setup process.

import sys
import bluetooth
import time
import socket

bluetooth_mac = sys.argv[1]

try:
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bluetooth_mac, 7))
    time.sleep(1)
    sock.send('\xf0\x83\x01\x7b\xf1')
    time.sleep(2)
    sock.send('\xf0\x83\x16\x66\xf1')
    time.sleep(5)
    sock.send('\xf0\x83\x01\x7b\xf1')
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

except Exception as e:
    print "BT connection error", e
    time.sleep(5)
    try:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except Exception as sockerr:
        print "BT socket close error", sockerr
    pass
