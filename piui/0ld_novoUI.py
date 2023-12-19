#!/usr/bin/python
import codecs
import functools
import os
import random
import time
from piui import PiUi
import bluetooth
import requests
import socket
from wifi import Cell, Scheme

url = 'http://54.154.182.7:4567/command'

current_dir = os.path.dirname(os.path.abspath(__file__))


class DemoPiUi(object):

    def check_for_ble(self):
        pass

    def __init__(self):
        self.title = "Novo Setup"
        self.txt = None
        self.img = None
        self.ui = PiUi(img_dir=os.path.join(current_dir, 'imgs'))
        self.src = "sunset.png"
        self.address = None
        self.myWIFI = None
        self.myBluetooth = None
        self.myPass = None
        self.wifi_pass = ""
        self.myCode = ""
        self.myCodebox = None
        self.listOfNetworks = [None] * 10
        self.infobox = None

    def toggleWifi(self, what, value):
        if value:
            self.myWIFI = what
        else:
            self.myWIFI = None

    def bt_scan(self):
        self.list = self.page.add_list()

        nearby_devices = bluetooth.discover_devices(lookup_names=True)

        for addr, name in nearby_devices:
            self.list.add_item(name, chevron=True, onclick=functools.partial(self.connect_bluetooth, addr))

            # if ("super" in name.lower()) or ("oneplus" in name.lower()):
            #     self.list.add_item(name, chevron=True, onclick=functools.partial(self.connect_bluetooth, addr))
            # else:
            #     self.list.add_item(name, chevron=False, onclick=functools.partial(self.passing_func))
        self.infoBox.set_text("Scan Complete")

    def page_bluetooth(self):
        self.page = self.ui.new_ui_page(title="Bluetooth Connection")
        self.img = self.page.add_image("Bluetooth2.png")
        self.page.add_textbox("First we have to set-up Novo / Bridge Bluetooth connection.", "h2")
        self.page.add_textbox("Please ensure your chair is powered on and not obstructed.", "h2")
        self.page.add_textbox("Select your Super Novo below:", "h2")
        self.infoBox = self.page.add_textbox("Scanning Bluetooth...", "h2")

        plus = self.page.add_button("Re-scan Bluetooth", self.page_bluetooth)

        self.list = self.page.add_list()
        self.bt_scan()
        self.page.add_textbox("<br/>")

    def page_landing(self):
        self.page = self.ui.new_ui_page(title="Novo Virtual therapist setup")
        self.img = self.page.add_image("SuperNovo.png")
        self.page.add_textbox("<br/>", "h3")

        self.page.add_textbox("Welcome to the Setup for the Super Novo Virtual Therapist", "h2")

        self.page.add_textbox(
            "If you have not already created your Virtual therapist account at Humantouch.com/VirtualTherapist do so and return here",
            "h3")
        self.page.add_textbox("<br/>", "h3")
        self.page.add_button("Continue", self.page_bluetooth)
        self.page.add_textbox("<br/><br/>")

    def passing_func(self):
        pass

    def page_buttons(self):
        self.page = self.ui.new_ui_page(title="Buttons", prev_text="Back", onprevclick=self.main_menu)
        self.title = self.page.add_textbox("Buttons!", "h2")

        plus = self.page.add_button("Up Button &uarr;", self.onupclick)
        minus = self.page.add_button("Down Button &darr;", self.ondownclick)

    def page_wifi(self):
        self.page = self.ui.new_ui_page(title="WiFi Setup", prev_text="Back", onprevclick=self.page_Profile)
        self.img = self.page.add_image("WiFi2.png")
        self.title = self.page.add_textbox("Please select your WiFi network from the list below:", "h2")
        self.list = self.page.add_list()
        filepath = '/home/pi/WiFiNetworks.txt'
        with open(filepath) as fp:
            self.ListOfWifiNetworks = fp.readlines()
        for idx, val in enumerate(self.ListOfWifiNetworks):
            self.list.add_item(val, chevron=True, onclick=functools.partial(self.page_wifiPass, val))

    def page_wifiPass(self, my_ssid):
        self.page = self.ui.new_ui_page(title="WiFi Setup", prev_text="Back", onprevclick=self.page_wifi)
        self.img = self.page.add_image("WiFi2.png")
        self.myWIFI = my_ssid
        self.page.add_textbox("<br/>")
        self.page.add_textbox("Enter the Wifi password for:", "h2")
        self.title = self.page.add_textbox(my_ssid, "h2")
        self.page.add_textbox("<br/>")
        self.txt = self.page.add_input("text", "Wifi password")
        self.page.add_button("Submit", self.connect_to_wifi)
        self.saving_box = self.page.add_textbox("<br/>")
        self.page.add_textbox("<br/>")

    def page_BT_test(self):
        self.page = self.ui.new_ui_page(title="Novo Bluetooth", prev_text="Back", onprevclick=self.main_menu)
        self.page.add_textbox("We are currently trying to connect to your Novo device", "h2")
        self.page.add_textbox(
            "Once the connection is successful the wired controller will light up and the chair may play a short sound, once complete please press Continue",
            "h2")
        self.list = self.page.add_list()
        # self.list.add_item("Test Connection to: Super Novo", chevron=True, onclick=self.page_input)

        plus = self.page.add_button("Continue to WiFi Setup", self.onupclick)

    def page_Profile(self):
        self.page = self.ui.new_ui_page(title="Novo Profile", prev_text="Back", onprevclick=self.page_bluetooth)
        self.img = self.page.add_image("Blank.png")

        self.page.add_textbox("<br/>", "h2")
        self.page.add_textbox(
            "Enter the 6 digit Virtual Therapist Profile Code issued when you registered your Virtual Therapist Account",
            "h2")
        self.page.add_textbox("")

        self.myCodebox = self.page.add_input("text", "6 digit Profile code")
        button = self.page.add_button("Submit", self.add_Profile_code)

    def page_console(self):
        con = self.ui.console(title="Console", prev_text="Back", onprevclick=self.main_menu)
        con.print_line("Hello Console!")

    def main_menu(self):
        self.page = self.ui.new_ui_page(title="Edit Settings")
        self.list = self.page.add_list()

        self.list.add_item("Bluetooth", chevron=True, onclick=self.page_bluetooth)
        self.list.add_item("Profile Code", chevron=True, onclick=self.page_Profile)
        self.list.add_item("Wifi", chevron=True, onclick=self.page_wifi)

        self.list.add_item("Confirm and connect", chevron=True, onclick=self.page_Connect)

        # self.list.add_item("Connect everything", chevron=True, onclick=self.set_up_stuff)
        self.ui.done()

    def page_Connect(self):
        self.page = self.ui.new_ui_page(title="Connect", prev_text="Edit", onprevclick=self.main_menu)

        self.page.add_textbox("Please confirm the details below are correct, and press Connect.", "h2")
        self.page.add_textbox("If you need to edit, press the Edit button.", "h2")
        self.page.add_textbox("________________________________________", "h2")
        # self.page.add_textbox("<br/>", "h2")
        self.page.add_textbox("Profile Code: " + self.myCode, "h2")
        self.page.add_textbox("WiFi Network: " + self.myWIFI, "h2")
        self.page.add_textbox("WiFi Password: " + self.wifi_pass, "h2")

        button = self.page.add_button("Connect", self.set_up_stuff)

        self.page.add_textbox("________________________________________", "h2")
        self.page.add_textbox(
            "It will take up to 120 seconds for your chair to connect. The Chair will light and move briefly when the connections are complete.",
            "h2")

    def add_Profile_code(self):
        filepath = '/home/pi/chair_id.txt'
        with open(filepath, 'w+') as the_file:
            the_file.write(self.myCodebox.get_text())
        self.page.add_textbox("Saving Profile Code", "h2")
        self.myCode = self.myCodebox.get_text()
        time.sleep(2)
        self.page_wifi()

    def main(self):
        self.page_landing()
        self.ui.done()

    def onupclick(self):
        self.title.set_text("Up ")
        print "Up"

    def ondownclick(self):
        self.title.set_text("Down")
        print "Down"

    def onhelloclick(self):
        print "onstartclick"
        self.title.set_text("Hello " + self.txt.get_text())
        print "Start"

    def onpicclick(self):
        if self.src == "sunset.png":
            self.img.set_src("sunset2.png")
            self.src = "sunset2.png"
        else:
            self.img.set_src("sunset.png")
            self.src = "sunset.png"

    def ontoggle(self, what, value):
        self.title.set_text("Toggled " + what + " " + str(value))

    def connect_to_wifi(self):
        filepath = '/home/pi/chosenNetwork.txt'
        with codecs.open(filepath, 'w+', encoding='utf-8') as the_file:
            the_file.write(self.myWIFI)
            output_string = self.txt.get_text()
            self.wifi_pass = output_string
            if type(output_string) != unicode:
                output_string = unicode(output_string, "utf-8")
            the_file.write(self.txt.get_text())
            self.myPass = self.txt.get_text()

        self.saving_box.set_text("Saving Wifi")
        time.sleep(2)
        self.page_Connect()

    def connect_bluetooth(self, bluetooth_mac):
        filepath = '/home/pi/chosenBlueTooth.txt'
        self.infoBox.set_text("testing connection...")
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((bluetooth_mac, 7))
            time.sleep(1)
            sock.send('\xf0\x83\x01\x7b\xf1')
            time.sleep(2)
            sock.send('\xf0\x83\x16\x66\xf1')
            time.sleep(5)
            sock.send('\xf0\x83\x01\x7b\xf1')
        except Exception as e:
            time.sleep(5)
            print e
            pass

        self.infoBox.set_text("If your chair moved, contine on")
        with open(filepath, 'w') as the_file:
            the_file.write(bluetooth_mac)
        plus = self.page.add_button("Continue to Profile Setup", self.page_Profile)
        self.myBluetooth = bluetooth_mac


    def saveWifi(self, passkey):
        if self.myWIFI is not None:
            scheme = Scheme.for_cell('wlan0', 'home', self.myWIFI, passkey)
            scheme.save()
            scheme.activate()

    def set_up_stuff(self):
        passwd = "humantouchnovo"
        WiFi_Command = "python /home/pi/set_up_everything.py"
        #BT_Command = "python /home/pi/set_BT_sound.py"
        p = os.system('echo %s|sudo -S %s' % (passwd, WiFi_Command))
       #q = os.system('echo %s|sudo -S %s' % (passwd, BT_Command))
        update = self.page.add_textbox("    \n", "h2")
        count = 120
        host = "8.8.8.8"
        port = 53
        timeout = 2
        number = 120
        while number > 1:
            update.set_text(str(number) + " seconds remaining.")

            number -= 1
            pass
            time.sleep(1)

        update.set_text("If your Chair didn't move, you may have made an error in your WiFi Setup. Press Edit, then on the menu, please select Wifi and try again.")


def main():
    piui = DemoPiUi()
    piui.main()


if __name__ == '__main__':
    main()

