import subprocess
import bluetooth
import requests
import functools
import os
import random
import time
import sys
# import NovoSerial
import NovoCommands


# if len(sys.argv) != 2:
# 	print "Usage:\n sudo python test.py (MAC ADDRESS)"
# 	sys.exit()

# mac_str = sys.argv[1]


Chair = NovoCommands.NovoComm()

url = 'http://54.154.182.7:4567/command'

current_dir = os.path.dirname(os.path.abspath(__file__))

firstTime = True

while True:
	try:
	
		response = requests.get('http://54.154.182.7:4567/command')
		text = str(response.text)
		print text
		test = "new"
		if test not in text:

			qwerty = True
			
			if "1" in text:
				Chair.RESTORE()
				time.sleep(1)
				Chair.ENERGIZE()

			if "2" in text:
				Chair.RESTORE()
				time.sleep(1)
				Chair.PERFORMANCE()

			if "3" in text:
				Chair.RESTORE()
				time.sleep(1)
				Chair.AWAKE()

			if "4" in text:
				Chair.RESTORE()
				time.sleep(1)
				Chair.RECOVERY()

			if "5" in text:
				Chair.RESTORE()
				time.sleep(1)
				Chair.UPPERBACK()

			if "6" in text:
				Chair.RESTORE()
				time.sleep(1)
				Chair.LOWERBACK()

			if "7" in text:
				Chair.RESTORE()
				time.sleep(1)
				Chair.DEEPSTRETCH()

			if "8" in text:
				Chair.RESTORE()
				time.sleep(1)
				Chair.DEEPBREATH()

			if "9" in text:
				Chair.RESTORE()
				time.sleep(1)
				Chair.DEEPSOOTHE()


			if "10" in text:
				Chair.RESTORE()
				time.sleep(1)
				Chair.DEMO()

			if "11" in text:
				Chair.RESTORE()
				time.sleep(1)
				Chair.STOP()

			if "12" in text:
				Chair.RESTORE()


			if "13" in text:
				Chair.HEATON()

			if "20" in text:
				Chair.INTENSITY1()


			if "21" in text:
				Chair.INTENSITY2()


			if "22" in text:
				Chair.INTENSITY3()


			if "23" in text:
				Chair.INTENSITY4()


			if "24" in text:
				Chair.INTENSITY5()


				# subprocess.call('mpg321 /home/pi/piui/otherbeepsound.mp3' , shell=True)
			# else:
			# 	subprocess.call('mpg321 /home/pi/piui/beepsound.mp3 &', shell=True)
	
	
    		pass
	except Exception as e:
		print e
		pass
	finally:
		pass

	time.sleep(2)
	pass