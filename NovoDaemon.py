#!/usr/bin/env python
import subprocess
import requests
import functools
import os
import random
import time
import sys
import json
import NovoBluetoothCommands
import sys, time
from daemon import Daemon
 
class MyDaemon(Daemon):
    def run(self):

        Chair = NovoBluetoothCommands.NovoComm()
        filepath = '/home/pi/chair_id.txt'
        url = 'https://therapist.humantouch.com/jsonCommand'

        current_dir = os.path.dirname(os.path.abspath(__file__))
        chair_id = "123456"
        firstTime = True
        timeDelay = 1.5
        isAsleep = True
        CurrentProgramLength = 10
        elsapledProgramLength = 0
        remainingProgramTime = 0
        currentStatusCode = 'meee'

        fail_count = 0
        currentIntensity = 1

        while True:
            try:
                with open(filepath, 'r+') as aFile:
                    myInfo = aFile.readlines()
                    ssid = myInfo[0]
                    chair_id = ssid
                    pass
            except Exception as e:
                print e
                pass
            finally:
                pass

            try:
                data = {'id': chair_id, 'intensity': currentIntensity, 'chairConnected': 'MEEEP!'}
                headers = {'Content-type': 'application/json'}

                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=4.0)
                text = str(response.text)

                try:
                    test = "nov"

                    if test in text:
                        currentStatusCode = Chair.KEEPALIVE()
                        print "Intensity is " + currentStatusCode[28:30]
                        currentIntensity = int(currentStatusCode[29:30])
                        currentIntensity = int(currentIntensity) - 1
                        print "Status is " + currentStatusCode[12:14]
                        fail_count = 0
                        time.sleep(timeDelay)

                    else:

                        print currentStatusCode[12:14]
                        if "00" in (currentStatusCode[12:14]):
                            Chair.WAKECHAIR()
                        time.sleep(timeDelay)
                        payload = json.loads(text)

                        if payload["reset"] == 1:
                            WiFi_Command = "python /home/pi/Desktop/reset.py"
                            passwd = "humantouchnovo"
                            p = os.system('echo %s|sudo -S %s' % (passwd, WiFi_Command))
                            pass

                        elif payload["move"] == 1:
                          #  Chair.WAKECHAIR()
                          #  time.sleep(2)
                            Chair.play_sound()
                            Chair.DEMO()
                            time.sleep(5)
                            Chair.RESTORE()
                            pass

                        elif payload["myCommand"] == 1:
                            Chair.SendCommand(payload["myProgram"], payload["myStyle"])
                            time.sleep(2)
                            Chair.SendHeight(payload["myHeight"])
                            time.sleep(2)
                            Chair.SendTime(payload["myTime"])

                        elif payload["myCommand"] == 2:
                            Chair.SendIntensity(payload["myIntensity"])
                            pass

                        elif payload["myCommand"] == 3:
                            Chair.SendHeight(payload["myHeight"])
                            pass

                        elif payload["myCommand"] == 4:
                            Chair.SendTime(payload["myTime"])
                            pass

                        elif payload["myCommand"] == 5:
                            Chair.RESTORE()
                            pass

                        elif payload["myCommand"] == 6:
                            Chair.STOP()
                            pass

                        elif payload["myCommand"] == 7:
                            Chair.DEMO()
                            pass

                        pass

                except Exception as e:
                    print  e
                    print  "Re-Connecting"
                    time.sleep(2)
                    Chair.connect() 

            except Exception as err:
                print "web fail"
                text = "novo"
                time.sleep(5)
                pass


            finally:

                pass

            time.sleep(2)


if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
