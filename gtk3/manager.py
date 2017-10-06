#!/usr/bin/env python3

import sys # exit
import gi # gtk3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk




import downloader

class MainMenu(object):
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title('Wallpaper Manager')
        self.window.connect_after('destroy', self.destroy)

        grid = Gtk.Grid(row_homogeneous = False, 
                        column_homogeneous = True)
        grid.set_row_spacing(10)
        grid.set_column_spacing(4)
        self.window.add(grid)
        self.grid = grid

        bt_start = Gtk.Button(label = 'View new wallpaper')
        bt_start.connect_after('clicked', self.on_button_clicked)
        bt_ban = Gtk.Button(label = 'Ban')
        bt_save = Gtk.Button(label = 'Save')
        bt_pass = Gtk.Button(label = 'Pass')

        grid.attach(bt_start, 0, 0, 6, 1)
        grid.attach(bt_ban, 0, 1, 1, 1)
        grid.attach_next_to(bt_save, bt_ban, Gtk.PositionType.RIGHT, 3, 1)
        grid.attach_next_to(bt_pass, bt_save, Gtk.PositionType.RIGHT, 2, 1)

        self.window.show_all()

    def on_button_clicked(self, widget):
        image = downloader.get_image()
        self.image = Gtk.Image()
        self.image.set_from_file(image)
        self.window.remove(self.grid)
        self.window.add(self.image)
        self.window.show_all()
        print('Hello world')

    def destroy(self, window):
        Gtk.main_quit()

def main(argv):
    win = MainMenu()
    Gtk.main()
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
