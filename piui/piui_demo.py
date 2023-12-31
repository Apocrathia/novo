import functools
import os
import random
import time
from piui import PiUi
import bluetooth
import requests




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

    def page_static(self):
        self.page = self.ui.new_ui_page(title="Static Content", prev_text="Back",
            onprevclick=self.main_menu)
        self.page.add_textbox("Add a mobile UI to your Raspberry Pi project", "h1")
        self.page.add_element("hr")
        self.page.add_textbox("You can use any static HTML element " + 
            "in your UI and <b>regular</b> <i>HTML</i> <u>formatting</u>.", "p")
        self.page.add_element("hr")
        self.page.add_textbox("Your python code can update page contents at any time.", "p")
        update = self.page.add_textbox("Like this...", "h2")
        time.sleep(2)
        for a in range(1, 10):
            response = requests.get('http://54.154.182.7:4567/command')

            update.set_text(response.text)
            time.sleep(1)

    def page_buttons(self):
        self.page = self.ui.new_ui_page(title="Buttons", prev_text="Back", onprevclick=self.main_menu)
        self.title = self.page.add_textbox("Buttons!", "h1")
        plus = self.page.add_button("Up Button &uarr;", self.onupclick)
        minus = self.page.add_button("Down Button &darr;", self.ondownclick)

    def page_input(self):
        self.page = self.ui.new_ui_page(title="Input", prev_text="Back", onprevclick=self.main_menu)
        self.title = self.page.add_textbox("Input", "h1")
        self.txt = self.page.add_input("text", "Name")
        button = self.page.add_button("Say Hello", self.onhelloclick)

    def page_images(self):
        self.page = self.ui.new_ui_page(title="Images", prev_text="Back", onprevclick=self.main_menu)
        self.img = self.page.add_image("sunset.png")
        self.page.add_element('br')
        button = self.page.add_button("Change The Picture", self.onpicclick)

    def page_toggles(self):
        self.page = self.ui.new_ui_page(title="Toggles", prev_text="Back", onprevclick=self.main_menu)
        self.list = self.page.add_list()
        self.list.add_item("Lights", chevron=False, toggle=True, ontoggle=functools.partial(self.ontoggle, "lights"))
        self.list.add_item("TV", chevron=False, toggle=True, ontoggle=functools.partial(self.ontoggle, "tv"))
        self.list.add_item("Microwave", chevron=False, toggle=True, ontoggle=functools.partial(self.ontoggle, "microwave"))
        self.page.add_element("hr")
        self.title = self.page.add_textbox("Home Appliance Control", "h1")
        

    def page_console(self):
        con = self.ui.console(title="Console", prev_text="Back", onprevclick=self.main_menu)
        con.print_line("Hello Console!")

    def main_menu(self):
        self.page = self.ui.new_ui_page(title="Novo - Bluetooth")
        self.list = self.page.add_list()
        nearby_devices = bluetooth.discover_devices(lookup_names = True)
        
        for addr, name in nearby_devices:
            self.list.add_item(name, chevron=True, onclick= functools.partial(self.testConnection, addr))

        # self.list.add_item("Static Content", chevron=True, onclick=self.page_static)
        # self.list.add_item("Buttons", chevron=True, onclick=self.page_buttons)
        # self.list.add_item("Input", chevron=True, onclick=self.page_input)
        # self.list.add_item("Images", chevron=True, onclick=self.page_images)
        # self.list.add_item("Toggles", chevron=True, onclick=self.page_toggles)
        # self.list.add_item("Console!", chevron=True, onclick=self.page_console)
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
            self.list.add_item("    Provided By: %s" % svc["provider"])
            self.list.add_item("    Protocol:    %s" % svc["protocol"])
            self.list.add_item("    channel/PSM: %s" % svc["port"])
            self.list.add_item("    svc classes: %s "% svc["service-classes"])
            self.list.add_item("    profiles:    %s "% svc["profiles"])
            self.list.add_item("    service id:  %s "% svc["service-id"])
            self.list.add_item("")
        



def main():
  piui = DemoPiUi()
  piui.main()

if __name__ == '__main__':
    main()