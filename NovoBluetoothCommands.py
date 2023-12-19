import time

import bluetooth


class NovoComm:

    def __init__(self):

        self.mac_address = ""
        self.failure_count = 0
        self.CommandArray = []
        # commands list
        # Energise
        self.CommandArray.append(
            ['\xF0\x83\x11\x6B\xF1', '\xF0\x83\x1B\x61\xF1', '\xF0\x83\x1C\x60\xF1', '\xF0\x83\x1D\x5F\xF1',
             '\xF0\x83\x1E\x5E\xF1', '\xF0\x83\x07\x75\xF1'])
        # Awake][
        self.CommandArray.append(
            ['\xF0\x83\x12\x6A\xF1', '\xF0\x83\x1F\x5D\xF1', '\xF0\x83\x71\x0B\xF1', '\xF0\x83\x72\x0A\xF1',
             '\xF0\x83\x3A\x42\xF1'])
        # Perform][
        self.CommandArray.append(
            ['\xF0\x83\x10\x6C\xF1', '\xF0\x83\x17\x65\xF1', '\xF0\x83\x18\x64\xF1', '\xF0\x83\x19\x63\xF1',
             '\xF0\x83\x1A\x62\xF1'])
        # Recvoery][
        self.CommandArray.append(
            ['\xF0\x83\x13\x69\xF1', '\xF0\x83\x3B\x41\xF1', '\xF0\x83\x3C\x40\xF1', '\xF0\x83\x3D\x3F\xF1',
             '\xF0\x83\x3E\x3E\xF1'])
        # UperBack][
        self.CommandArray.append(
            ['\xF0\x83\x14\x68\xF1', '\xF0\x83\x3F\x3D\xF1', '\xF0\x83\x58\x24\xF1', '\xF0\x83\x59\x23\xF1',
             '\xF0\x83\x5A\x22\xF1'])
        # LowerBack][
        self.CommandArray.append(
            ['\xF0\x83\x15\x67\xF1', '\xF0\x83\x5B\x21\xF1', '\xF0\x83\x5C\x20\xF1', '\xF0\x83\x5D\x1F\xF1',
             '\xF0\x83\x5E\x1E\xF1'])
        # Demo][
        self.CommandArray.append([])
        # DeepStretch][
        self.CommandArray.append(
            ['\xF0\x83\x39\x43\xF1', '\xF0\x83\x28\x54\xF1', '\xF0\x83\x29\x53\xF1', '\xF0\x83\x2A\x52\xF1'])
        # DeepBreathe][
        self.CommandArray.append(
            ['\xF0\x83\x38\x44\xF1', '\xF0\x83\x28\x54\xF1', '\xF0\x83\x29\x53\xF1', '\xF0\x83\x2A\x52\xF1'])
        # DeepSoothe][
        self.CommandArray.append(
            ['\xF0\x83\x5F\x45\xF1', '\xF0\x83\x28\x54\xF1', '\xF0\x83\x29\x53\xF1', '\xF0\x83\x2A\x52\xF1'])

        # Height Array
        self.HeightArray = ['\xF0\x83\x76\x06\xF1', '\xF0\x83\x78\x04\xF1', '\xF0\x83\x7A\x02\xF1',
                            '\xF0\x83\x7C\x00\xF1', '\xF0\x83\x7E\x7E\xF1']
        # Time Array
        self.TimeArray = ['\xF0\x83\x50\x2C\xF1', '\xF0\x83\x51\x2B\xF1', '\xF0\x83\x52\x2A\xF1']
        # Intenisty Array
        self.IntenistyArray = ['\xF0\x83\x54\x28\xF1', '\xF0\x83\x55\x27\xF1', '\xF0\x83\x56\x26\xF1',
                               '\xF0\x83\x57\x25\xF1', '\xF0\x83\x4F\x2D\xF1']

        self.connect()
        pass

    def connect(self):
        # post CES.....
        mac = "FC:58:FA:F1:D4:C5"
        mac = "4C:E1:73:B3:D2:50"

        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        time.sleep(1)
        self.get_new_BT()
        try:
            self.sock.connect((self.mac_address, 7))
        except Exception as e:
            print e
            myInfo = ""
            self.get_new_BT()
            self.failure_count += 1
            time.sleep(5)
            self.connect()
        finally:
            pass

    def disconnect(self):
        self.sock.close()

    def SendCommand(self, Program, OptionMode):
        print "sending command " + str(Program) + " " + str(OptionMode)
        localArray = self.CommandArray[Program]
        Comand = ''

        try:
            command = localArray[OptionMode]
        except Exception as e:
            command = localArray[0]
        finally:
            pass

        self.sock.send(command)
        pass

    def SendHeight(self, HeightNumber):
        print "sending Hight " + str(HeightNumber)
        command = ''

        try:
            command = self.HeightArray[HeightNumber]
        except Exception as e:
            command = self.HeightArray[0]
        finally:
            pass

        self.sock.send(command)
        pass

    def SendTime(self, TimeNumber):
        print "sending time " + str(TimeNumber)
        command = ''

        try:
            command = self.TimeArray[TimeNumber]
        except Exception as e:
            command = self.TimeArray[0]
        finally:
            pass
        self.sock.send(command)
        pass

    def SendIntensity(self, IntenistyNumber):
        print "sending intensity / " + str(IntenistyNumber)
        command = ''

        try:
            command = self.IntenistyArray[IntenistyNumber]
        except Exception as e:
            command = self.IntenistyArray[0]
        finally:
            pass
        self.sock.send(command)
        pass

    def RESTORE(self):
        print "RESTORE"
        self.sock.send('\xf0\x83\x01\x7b\xf1')

    def WAKECHAIR(self):
        print "waking Up The chair"
        self.sock.send('\xf0\x83\x01\x7b\xf1')
        pass

    def STOP(self):
        self.sock.send('\xf0\x83\x75\x07\xf1')

    def DEMO(self):
        print "DEMO"
        self.sock.send('\xf0\x83\x16\x66\xf1')
        pass

    def HEATOFF(self):
        print "HEAT OFF"
        self.sock.send('\xf0\x83\x27\x55\xf1')
        pass

    def KEEPALIVE(self):
        print "HeartBeat"
        # self.sock.send('\x00\x00\x00\x00\x00')
        data = self.sock.recv(1024)
        codes = (data.encode('hex')).split("f1f0")
        print codes[3]

        print codes[4]
        return max(codes[3], codes[4], key=len)

    def get_new_BT(self):
        filepath = '/home/pi/chosenBlueTooth.txt'
        try:
            with open(filepath, 'r+') as aFile:
                myInfo = aFile.readlines()
                ssid = myInfo[0]
                self.mac_address = ssid
                pass
        except Exception as e:
            print e
            time.sleep(1)
            pass
        finally:
            pass

    def play_sound(self):
        cmd_string = "aplay -D bluealsa:HCI=hci0,DEV=" + self.mac_address + ",PROFILE=a2dp bell.wav &"
        os.system(cmd_string)





