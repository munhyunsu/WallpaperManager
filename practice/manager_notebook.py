#!/usr/bin/env python3

import sys # exit
import gi # gtk3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



class MainMenu(object):
    def __init__(self):
        # Create parent window
        self.window = Gtk.Window()
        self.window.set_size_request(800, 600)
        self.window.set_title('Wallpaper Manager')
        self.window.connect_after('destroy', self.destroy)
        notebook = Gtk.Notebook()
        self.window.add(notebook)

        # Create Danbooru downloader view
        page1 = Gtk.Grid(row_homogeneous = False,
                         column_homogeneous = True)
        page1.set_row_spacing(10)
        page1.set_column_spacing(10)
        # Inputbox
        entry = Gtk.Entry()
        entry.set_placeholder_text('Search keyword')
        page1.attach(entry, 0, 0, 9, 1)
        notebook.append_page(page1, Gtk.Label(label = 'Danbooru'))
        # Listbox
        listbox = Gtk.ListBox()
        items = ['a',
                 'b',
                 'c',
                 'd',
                 'e',
                 'f']
        for item in items:
            listbox.add(Gtk.Label(label = item))
        vscrollbar = Gtk.Scrollbar(orientation = Gtk.Orientation.VERTICAL,
                                   adjustment = listbox)
        page1.attach(listbox, 0, 1, 9, 4)
        # plus button
        bt_plus = Gtk.Button(label = '+')
        page1.attach(bt_plus, 9, 0, 1, 1)
        # minus button
        bt_minus = Gtk.Button(label = '-')
        page1.attach(bt_minus, 9, 1, 1, 1)




        page2 = Gtk.Grid(row_homogeneous = False,
                         column_homogeneous = True)
        page2.set_row_spacing(10)
        page2.set_column_spacing(4)
        notebook.append_page(page2, Gtk.Label(label = 'Yandere'))

        self.window.show_all()

    def destroy(self, window):
        Gtk.main_quit()

def main(argv):
    win = MainMenu()
    Gtk.main()
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
