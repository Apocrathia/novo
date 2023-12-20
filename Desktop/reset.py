#!/usr/bin/env python

import subprocess
import os
import time
passwd = "humantouchnovo"
hotspot_command = " /usr/bin/autohotspot >/dev/null 2>&1"

WiFi_Command = "python /home/pi/reset_WifiNetwork.py"

p = os.system('echo %s|sudo -S %s' % (passwd, WiFi_Command))

time.sleep(2)
t = os.system('echo %s|sudo -S %s' % (passwd, hotspot_command))