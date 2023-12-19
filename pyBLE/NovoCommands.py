import bluetooth
import pexpect
from subprocess import Popen, call
import time

import serial

class NovoComm:
    
    def __init__(self):
        self.connect()
        pass

    def connect(self):
        self.sock = serial.Serial("/dev/rfcomm2", baudrate=9600, timeout=0.5)

        
    def disconnect(self):
        self.sock.close()
    
    def ENERGIZE(self):
    	print "ENERGIZE"
    	self.sock.write( '\xF0\x83\x1B\x61\xF1')
 

    def AWAKE(self):
    	print "AWAKE"
    	self.sock.write( '\xF0\x83\x17\x65\xF1')


    def RESTORE(self):
    	print "RESTORE"
    	self.sock.write('\xf0\x83\x01\x7b\xf1')

    def WAKECHAIR():
        print "waking Up The chair"
        self.sock.write('\x02\x05\x20\x0e\x00\x0a\x00\x42\x04\x0b\xff\x0b\xff\x0b\x02\xf0\x83\x01\x7b\xf1')
        pass


    def STOP(self):
        self.sock.write('\xf0\x83\x75\x07\xf1')

    def PERFORMANCE(self):
        print "PERFORMANCE"
        self.sock.write('\xf0\x83\x12\x6a\xf1')
        pass

    def RECOVERY(self):
        print "RECOVERY"
        self.sock.write('\xf0\x83\x10\x69\xf1')
        pass


    def UPPERBACK(self):
        print "UPPERBACK"
        self.sock.write('\xf0\x83\x14\x68\xf1')
        pass


    def LOWERBACK(self):
        print "LOWERBACK"
        self.sock.write('\xf0\x83\x15\x67\xf1')
        pass

    def DEEPSTRETCH(self):
        print "DEEPSTRETCH"
        self.sock.write('\xf0\x83\x39\x43\xf1')
        pass

    def DEEPBREATH(self):
        print "DEEPBREATH"
        self.sock.write('\xf0\x83\x38\x44\xf1')
        pass

    def DEEPSOOTHE(self):
        print "DEEPSOOTHE"
        self.sock.write('\xf0\x83\x5f\x45\xf1')
        pass


    def DEMO(self):
        print "DEMO"
        self.sock.write('\xf0\x83\x16\x66\xf1')
        pass

    def INTENSITY1(self):
        print "INTENSITY 1"
        self.sock.write('\xf0\x83\x54\x28\xf1')
        pass

    def INTENSITY2(self):
        print "INTENSITY 2"
        self.sock.write('\xf0\x83\x55\x27\xf1')
        pass

    def INTENSITY3(self):
        print "INTENSITY 3"
        self.sock.write('\xf0\x83\x56\x26\xf1')
        pass

    def INTENSITY4(self):
        print "INTENSITY 4"
        self.sock.write('\xf0\x83\x57\x25\xf1')
        pass

    def INTENSITY5(self):
        print "INTENSITY 5"
        self.sock.write('\xf0\x83\x4f\x2d\xf1')
        pass

    def HEATON(self):
        print "HEAT ON"
        self.sock.write('\xf0\x83\x27\x55\xf1')
        pass

    def HEATOFF():
        print "HEAT OFF"
        self.sock.write('\xf0\x83\x27\x55\xf1')
        pass


