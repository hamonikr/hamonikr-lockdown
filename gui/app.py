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

# set check buttons status with existing rules file
def set_status():
    initial_status = [False,False,False]
    try:
        with open("/etc/udev/rules.d/50-usb-lockdown.rules", "r") as rulefile:
            ruledata = rulefile.read()
            
            # strings to read from existing rules file
            mass_storage_line = 'ACTION=="add", SUBSYSTEMS=="usb", ENV{DEVTYPE}=="usb_interface", ATTRS{bInterfaceClass}=="08", RUN+="/bin/bash -c \'[[ -f \\\"/sys$devpath/authorized\\\" ]] && echo 0 | tee \\\"/sys$devpath/authorized\\\" | tee -a /tmp/usb-lockdown.log\'"'
            printer_line = 'ACTION=="add", SUBSYSTEMS=="usb", ENV{DEVTYPE}=="usb_interface", ATTRS{bInterfaceClass}=="07", RUN+="/bin/bash -c \'[[ -f \\\"/sys$devpath/authorized\\\" ]] && echo 0 | tee \\\"/sys$devpath/authorized\\\" | tee -a /tmp/usb-lockdown.log\'"'
            hid_line = 'ACTION=="add", SUBSYSTEMS=="usb", ENV{DEVTYPE}=="usb_interface", ATTRS{bInterfaceClass}=="0e", RUN+="/bin/bash -c \'[[ -f \\\"/sys$devpath/authorized\\\" ]] && echo 0 | tee \\\"/sys$devpath/authorized\\\" | tee -a /tmp/usb-lockdown.log\'"'
        
            # set check button status if each string exists in rules file
            if mass_storage_line in ruledata:
                checkb1.set_active(True)
                initial_status[0] = True
            if printer_line in ruledata:
                checkb2.set_active(True)
                initial_status[1] = True
            if hid_line in ruledata:
                checkb3.set_active(True)
                initial_status[2] = True
            rulefile.close()

    # rules file may not exist
    except FileNotFoundError:
        print('rules file doesn\'t exist')

    return initial_status

# confirm before apply
def confirm(message):
    # when quit button pressed
    if message=='quit':
        dialog = Gtk.MessageDialog(
                            buttons=Gtk.ButtonsType.YES_NO)
        dialog.props.text = _("Do you want to apply the changes?")
        response = dialog.run()
        dialog.destroy()

        # Apply when the user presses the YES button
        if response == Gtk.ResponseType.YES:
            print('YES button pressed')
            return True
        else:
            print('NO button pressed')
            return False

    # when apply button pressed
    elif message=='stay':
        # Show confirm message dialog
        dialog = Gtk.MessageDialog(
                            buttons=Gtk.ButtonsType.OK_CANCEL)
        dialog.props.text = _("Do you want to apply the changes?")
        response = dialog.run()
        dialog.destroy()

        # Apply when the user presses the OK button
        if response == Gtk.ResponseType.OK:
            print('ok button pressed')
            return True
        else:
            print('cancel button pressed')
            return False
    

def apply(apply_event):
    # ask before apply
    # OK/YES button pressed
    if confirm(apply_event):
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

        print("usb_mass_storage : " + usb_mass_storage + " usb_printer : " + usb_printer + " usb_hid : " + usb_hid )
        os.system("sudo systemctl restart udev")
        # quit after apply
        Gtk.main_quit()

    # cancel button pressed
    else:
        print('cancled')

class Handler:
    # delete_event (quit button) handler
    def onDelete(self, *args):
        # apply (if changes detected) before quit
        if initial_status[0] != checkb1.get_active() or initial_status[1] != checkb2.get_active() or initial_status[2] != checkb3.get_active():
            apply('quit')
        Gtk.main_quit()

    # clicked (apply button) handler
    def onButtonPressed(self, button):
        apply('stay')


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

# set check buttons status and get initial status
initial_status = set_status()

window.show_all()

Gtk.main()