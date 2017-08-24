#!/usr/bin/env python3

import sys # exit
import gi # gtk3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk




import downloader

class MainMenu(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = 'Wallpaper Manager')

        self.button = Gtk.Button(label = 'Download wallpapers')
        self.button.connect('clicked', self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        image = downloader.get_image()
        self.remove(self.button)
        self.image = Gtk.Image()
        self.image.set_from_file(image)
        self.add(self.image)
        self.show_all()
        print('Hello world')


def main(argv):
    win = MainMenu()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
