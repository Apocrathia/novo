import bluetooth
import pexpect
from subprocess import Popen, call
import time

import serial

class NovoComm:
    
    def __init__(self, mac_str):
        self.connect(mac_str)
        pass

    def connect(self, mac_str):
        self.sock = serial.Serial("/dev/rfcomm2", baudrate=9600, timeout=0.5)
    	#self.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        #self.sock.connect((mac_str, 3))
        
    def disconnect(self):
        self.sock.close()
    
    def ENERGIZE(self):
    	print "ENERGIZE"
    	self.sock.write('\xf0\x83\x01\x7b\xf1')
    	time.sleep(2)
    	self.sock.write( '\xF0\x83\x1B\x61\xF1')
    	#self.sock.send( bytearray([0xF0,  0x83,  0x1B,  0x61,  0xF1]))
        # self.sock.send('char-write-cmd 0xFFF1 f0831b61f1')

    def AWAKE(self):
    	print "AWAKE"
        self.sock.write('\xf0\x83\x01\x7b\xf1')
    	time.sleep(2)
    	self.sock.write( '\xF0\x83\x17\x65\xF1]')
    	#self.sock.send( bytearray([0xF0,  0x83,  0x17,  0x65,  0xF1]))
        # self.sock.send('char-write-cmd 0xFFF1 f0831765f1')

    def RESTORE(self):
    	print "RESTORE"
    	self.sock.write('\xf0\x83\x01\x7b\xf1')
    	# self.sock.write( bytearray([0xF0,  0x83,  0x01,  0x7b,  0xF1]))
    	#self.sock.send( bytearray([0xF0,  0x83,  0x01,  0x7b,  0xF1]))
        # self.sock.send('char-write-cmd 0xFFF1 f083017bf1')

    def STOP(self):
        self.sock.write('\xf0\x83\x75\x07\xf1')
    	# self.sock.write( bytearray([0xF0,  0x83,  0x75,  0x07,  0xF1]))
    	#self.sock.send( bytearray([0xF0,  0x83,  0x75,  0x07,  0xF1]))
        # self.sock.send('char-write-cmd 0xFFF1 f0837507f1')
