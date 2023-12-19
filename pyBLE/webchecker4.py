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
timeDelay = 1.5
isAsleep = True
CurrentProgramLength = 600
elsapledProgramLength = 0
remainingProgramTime = 0


while True:
	try:
	
		response = requests.get('http://54.154.182.7:4567/command')
		text = str(response.text)
		print text
		test = "new"
		if test not in text:

			qwerty = True
			if isAsleep:
				Chair.WAKECHAIR()
				time.sleep(timeDelay)


			if "10" in text:
				Chair.DEMO()
				remainingProgramTime = 300
				isAsleep = False

			elif "11" in text:
				Chair.STOP()

			elif "12" in text:
				Chair.RESTORE()
				remainingProgramTime = 20
				isAsleep = True

			elif "13" in text:
				Chair.HEATON()

			elif "20" in text:
				Chair.INTENSITY1()

			elif "21" in text:
				Chair.INTENSITY2()

			elif "22" in text:
				Chair.INTENSITY3()

			elif "23" in text:
				Chair.INTENSITY4()


			elif "24" in text:
				Chair.INTENSITY5()
			
			elif "1" in text:
				Chair.ENERGIZE()
				remainingProgramTime = 600
				isAsleep = False

			elif "2" in text:
				Chair.PERFORMANCE()
				remainingProgramTime = 600
				isAsleep = False

			elif "3" in text:
				Chair.AWAKE()
				remainingProgramTime = 600
				isAsleep = False

			elif "4" in text:
				Chair.RECOVERY()
				remainingProgramTime = 600
				isAsleep = False

			elif "5" in text:
				Chair.UPPERBACK()
				remainingProgramTime = 600
				isAsleep = False

			elif "6" in text:
				Chair.LOWERBACK()
				remainingProgramTime = 600
				isAsleep = False

			elif "7" in text:
				Chair.DEEPSTRETCH()
				remainingProgramTime = 600
				isAsleep = False

			elif "8" in text:
				Chair.DEEPBREATH()
				remainingProgramTime = 600
				isAsleep = False

			elif "9" in text:
				Chair.DEEPSOOTHE()
				remainingProgramTime = 600
				isAsleep = False



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
	if remainingProgramTime > 0:
		remainingProgramTime = remainingProgramTime -2
		pass
	else:
		isAsleep = True


	pass