#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainMenu(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = 'Wallpaper Manager')

        self.button = Gtk.Button(label = 'Download wallpapers')
        self.button.connect('clicked', self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        print('Hello world')

win = MainMenu()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
