#!/usr/bin/python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")

        self.set_title("Device lockdown")
        self.set_default_size(450, 200)

        vbox = Gtk.VBox()
        self.btn1 = Gtk.CheckButton(label="USB 저장장치")
        self.btn1.connect("toggled", self.on_checked)
        self.btn2 = Gtk.CheckButton(label="프린터")
        self.btn2.connect("toggled", self.on_checked)
        self.btn3 = Gtk.CheckButton(label="키보드/마우스 등 입력장치")
        self.btn3.connect("toggled", self.on_checked)
                
        self.lbl = Gtk.Label()

        self.btn10 = Gtk.Button(label="OK")
        self.btn10.connect("clicked", self.on_button_clicked)

        vbox.add(self.btn1)
        vbox.add(self.btn2)
        vbox.add(self.btn3)
        vbox.add(self.lbl)
        vbox.add(self.btn10)

        self.add(vbox)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def on_button_clicked(self, widget):
        print("Selected Element : \r\n")
        if self.btn1.get_active():
            print("usb-storage")
        if self.btn2.get_active():
            print("printer")
        if self.btn3.get_active():
            print("keyboard-mouse")
        # TO-DO : Save config and restart udev 

    def on_checked(self, widget, data = None):
        state = "btn1 : "+str(self.btn1.get_active())+" / btn2 : "+str(self.btn2.get_active())+" / btn3 : "+str(self.btn3.get_active())
        self.lbl.set_text(state)


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()