#!/usr/bin/python3
# 
# hamonikr-lockdown
# Copyright (C) 2021 Kevin Kim <chaeya@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
import os, subprocess
import locale
import gettext
import ctypes, sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def prompt_sudo():
    ret = 0
    if os.geteuid() != 0:
        msg = "[sudo] password for %u:"
        ret = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)
    return ret

if prompt_sudo() != 0:
    sys.exit("You need root permissions!")

# i18n
APP = 'hamonikr-lockdown'
LOCALE_DIR = "/usr/share/locale"
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

def on_checkbutton_toggled(button, name):
    if button.get_active():
        state = "Active"
    else:
        state = "Inactive"
    print("Common handler: Checkbutton " + name + " toggled, state is " + state + " Label : " + button.get_label() + " Name : " + name )

class Handler:
    def onButtonPressed(self, button):
        os.system("rm -f /etc/udev/rules.d/50-usb-lockdown.rules")
        if checkb1.get_active():
            usb_mass_storage = "lockdown"
            with open("/etc/udev/rules.d/50-usb-lockdown.rules", "a") as rulefile:
                rulefile.write('ACTION=="add", SUBSYSTEMS=="usb", ENV{DEVTYPE}=="usb_interface", ATTRS{bInterfaceClass}=="08", RUN+="/bin/bash -c \'[[ -f \\\"/sys$devpath/authorized\\\" ]] && echo 0 | tee \\\"/sys$devpath/authorized\\\" | tee -a /tmp/usb-lockdown.log\'"\r\n')
                rulefile.close()
        else: 
            usb_mass_storage = ""

        if checkb2.get_active():
            usb_printer = "lockdown"            
            with open("/etc/udev/rules.d/50-usb-lockdown.rules", "a") as rulefile:
                rulefile.write('ACTION=="add", SUBSYSTEMS=="usb", ENV{DEVTYPE}=="usb_interface", ATTRS{bInterfaceClass}=="07", RUN+="/bin/bash -c \'[[ -f \\\"/sys$devpath/authorized\\\" ]] && echo 0 | tee \\\"/sys$devpath/authorized\\\" | tee -a /tmp/usb-lockdown.log\'"\r\n')
                rulefile.close()            
        else:
            usb_printer = ""            

        if checkb3.get_active():
            usb_hid = "lockdown"
            with open("/etc/udev/rules.d/50-usb-lockdown.rules", "a") as rulefile:
                rulefile.write('ACTION=="add", SUBSYSTEMS=="usb", ENV{DEVTYPE}=="usb_interface", ATTRS{bInterfaceClass}=="0e", RUN+="/bin/bash -c \'[[ -f \\\"/sys$devpath/authorized\\\" ]] && echo 0 | tee \\\"/sys$devpath/authorized\\\" | tee -a /tmp/usb-lockdown.log\'"\r\n')
                rulefile.close()            
        else:
            usb_hid = ""

        # Do somethings here
        print("usb_mass_storage : " + usb_mass_storage + " usb_printer : " + usb_printer + " usb_hid : " + usb_hid )
        os.system("sudo systemctl restart udev")


builder = Gtk.Builder()
builder.set_translation_domain(APP)
builder.add_from_file("/usr/local/hamonikr-lockdown/main.glade")
builder.connect_signals(Handler())
window = builder.get_object("window1")

checkb1 = builder.get_object("chk1")
checkb2 = builder.get_object("chk2")
checkb3 = builder.get_object("chk3")

checkb1.connect ("toggled", on_checkbutton_toggled, "usb-mass-storage")
checkb2.connect ("toggled", on_checkbutton_toggled, "usb-printer")
checkb3.connect ("toggled", on_checkbutton_toggled, "usb-hid")

window.connect("destroy", Gtk.main_quit)

window.show_all()

Gtk.main()