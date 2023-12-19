#!/usr/bin/python

import functools
import os
import random
import time
from piui import PiUi
#import bluetooth
import requests
from wifi import Cell, Scheme



url = 'http://54.154.182.7:4567/command'

current_dir = os.path.dirname(os.path.abspath(__file__))


class DemoPiUi(object):
    

    def check_for_ble():
        v
        print "  %s - %s" % (addr, name)

    def __init__(self):
        self.title = None
        self.txt = None
        self.img = None
        self.ui = PiUi(img_dir=os.path.join(current_dir, 'imgs'))
        self.src = "sunset.png"
        self.address = None
        self.myWIFI = None
        self.myPAss = None

    def toggleWifi(self, what, value):
        if value:
            self.myWIFI = what
        else:
            self.myWIFI = None

    def page_static(self):
        self.page = self.ui.new_ui_page(title="Novo Set Up", prev_text="Back", onprevclick=self.main_menu)
        self.page.add_textbox("Welcome to the Setup for the Super Novo bridge, Soon you will be able to control your super novo with your Amazon Echo Novo Skill", "h1")
        self.page.add_textbox("First we have to set up the Bluetooth connection to your chair, please select it from the list below", "h1")
        self.page.add_textbox("please ensure your chair is powered on and not obstructed", "h2")
        self.list = self.page.add_list()


        self.list.add_item("Super Novo", chevron=True, onclick=self.page_input)

        self.list.add_item("Novo XT 2 (not compatable)", chevron=True, onclick=self.page_input)
       

        # update = self.page.add_textbox("Like this...", "h2")
        # time.sleep(2)
        # for a in range(1, 10):
        #     response = requests.get('http://54.154.182.7:4567/command')

        #     update.set_text(response.text)
        #     time.sleep(1)

    def page_buttons(self):
        self.page = self.ui.new_ui_page(title="Buttons", prev_text="Back", onprevclick=self.main_menu)
        self.title = self.page.add_textbox("Buttons!", "h1")

        plus = self.page.add_button("Up Button &uarr;", self.onupclick)
        minus = self.page.add_button("Down Button &darr;", self.ondownclick)

    def page_input(self):
        self.page = self.ui.new_ui_page(title="Novo WiFi", prev_text="Back", onprevclick=self.main_menu)
        self.title = self.page.add_textbox("Please select your WiFi network from the list below", "h1")
        self.list = self.page.add_list()
        self.list.add_item("Commcast inifity 123", chevron=True, onclick=self.page_input)
        self.list.add_item("Time Warner X", chevron=True, onclick=self.page_input)
        self.list.add_item("FBI undercover Van", chevron=True, onclick=self.page_input)
        self.list.add_item("Android AP", chevron=True, onclick=self.page_input)
        self.page.add_textbox("please enter your WiFi password carefully, on successful connection the wired controller will light up again and the chair may beep", "h2")
        self.txt = self.page.add_input("text", "Wifi password")
        button = self.page.add_button("Submit", self.onhelloclick)


    def page_wifi(self):
        self.page = self.ui.new_ui_page(title="Novo WiFi", prev_text="Back", onprevclick=self.main_menu)
        self.title = self.page.add_textbox("Please select your WiFi network from the list below", "h1")
        self.list = self.page.add_list()
        filepath = '/home/pi/WiFiNetworks.txt'
        with open(filepath) as fp:
            self.ListOfWifiNetworks = fp.readlines()
        for idx, val in enumerate(self.ListOfWifiNetworks):
            self.list.add_item(val,  chevron=False, toggle=True, ontoggle=functools.partial(self.toggleWifi, val))

        self.page.add_textbox("please enter your WiFi password carefully, on successful connection the wired controller will light up again and the chair may beep", "h2")
        self.txt = self.page.add_input("text", "Wifi password")
        button = self.page.add_button("Submit", self.saveWifi(self.txt.get_text()))

    def page_images(self):
        self.page = self.ui.new_ui_page(title="Novo Bluetooth", prev_text="Back", onprevclick=self.main_menu)
        self.page.add_textbox("We are currently trying to connect to your Novo device", "h1")
        self.page.add_textbox("Once the connection is successful the wired controller will light up and the chair may play a short sound, once complete please press Continue", "h1")
        self.list = self.page.add_list()
        self.list.add_item("Test Connection to: Super Novo", chevron=True, onclick=self.page_input)

        plus = self.page.add_button("Continue to WiFi Setup", self.onupclick)

        # self.list.add_item("Novo XT 2 (not compatable)", chevron=True, onclick=self.page_input)
        # self.page = self.ui.new_ui_page(title="Images", prev_text="Back", onprevclick=self.main_menu)
        # self.img = self.page.add_image("sunset.png")
        # self.page.add_element('br')
        # button = self.page.add_button("Change The Picture", self.onpicclick)

    def page_toggles(self):
        self.page = self.ui.new_ui_page(title="Novo Account", prev_text="Back", onprevclick=self.main_menu)

        self.page.add_textbox("Please enter the control code from your novo account this will be in your sign up email", "h2")
        self.txt = self.page.add_input("text", "6 digit controll code")
        button = self.page.add_button("Submit", self.onhelloclick)
        

    def page_console(self):
        con = self.ui.console(title="Console", prev_text="Back", onprevclick=self.main_menu)
        con.print_line("Hello Console!")

    def main_menu(self):
        self.page = self.ui.new_ui_page(title="Novo Setup Demo")
        self.list = self.page.add_list()
        # nearby_devices = bluetooth.discover_devices(lookup_names = True)
        
        # for addr, name in nearby_devices:
        #     self.list.add_item(name, chevron=True, onclick= functools.partial(self.testConnection, addr))
        self.list.add_item("Wifi network page", chevron=True, onclick=self.page_wifi)
        self.list.add_item("Demo Start page", chevron=True, onclick=self.page_static)
        self.list.add_item("Buttons", chevron=True, onclick=self.page_buttons)
        self.list.add_item("Demo Wifi", chevron=True, onclick=self.page_input)
        self.list.add_item("Demo Bluetooth", chevron=True, onclick=self.page_images)
        self.list.add_item("Bluetooth scan", chevron=True, onclick=self.testConnection)
        self.list.add_item("Demo Account", chevron=True, onclick=self.page_toggles)

        self.ui.done()


    def main(self):
        self.main_menu()
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


    def testConnection( self):
        self.page = self.ui.new_ui_page(title="Bluetooth Services", prev_text="Back", onprevclick=self.main_menu)
        self.list = self.page.add_list()
        services = bluetooth.find_service(address=self.address)

        if len(services) > 0:
            print("found %d services on %s" % (len(services), sys.argv[1]))
            print("")
        else:
            print("no services found")
        
        for svc in services:
            self.list.add_item("Service Name: %s"    % svc["name"])
            self.list.add_item("    Host:        %s" % svc["host"])
            self.list.add_item("    Description: %s" % svc["description"])
            self.list.add_item("")



    def saveWifi(self, passkey):
        if self.myWIFI is not None:
            scheme = Scheme.for_cell('wlan0', 'home', self.myWIFI, passkey)
            scheme.save()
            scheme.activate()
        

    # def testConnection( self):
    #     self.page = self.ui.new_ui_page(title="Bluetooth Services", prev_text="Back", onprevclick=self.main_menu)
    #     self.list = self.page.add_list()
    #     services = bluetooth.find_service(address=self.address)

    #     if len(services) > 0:
    #         print("found %d services on %s" % (len(services), sys.argv[1]))
    #         print("")
    #     else:
    #         print("no services found")
        
    #     for svc in services:
    #         self.list.add_item("Service Name: %s"    % svc["name"])
    #         self.list.add_item("    Host:        %s" % svc["host"])
    #         self.list.add_item("    Description: %s" % svc["description"])
    #         self.list.add_item("    Provided By: %s" % svc["provider"])
    #         self.list.add_item("    Protocol:    %s" % svc["protocol"])
    #         self.list.add_item("    channel/PSM: %s" % svc["port"])
    #         self.list.add_item("    svc classes: %s "% svc["service-classes"])
    #         self.list.add_item("    profiles:    %s "% svc["profiles"])
    #         self.list.add_item("    service id:  %s "% svc["service-id"])
    #         self.list.add_item("")
        



def main():
  piui = DemoPiUi()
  piui.main()

if __name__ == '__main__':
    main()
