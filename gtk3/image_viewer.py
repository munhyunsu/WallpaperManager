#!/usr/bin/env python3

import gi # GObject Introspection
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import sys # exit, argv

class GUI:
    def __init__(self):
        window = Gtk.Window()
        window.set_title('Image slideshow')
        window.connect_after('destroy', self.destroy)
        
        box = Gtk.Box()
        box.set_spacing(5)
        box.set_orientation(Gtk.Orientation.VERTICAL)
        window.add(box)

        self.image = Gtk.Image()
        box.pack_start(self.image, False, False, 0)

        button = Gtk.Button(label = 'Open a picture...')
        button.connect_after('clicked', self.on_open_clicked)
        box.pack_start(button, False, False, 0)

        window.show_all()

    def destroy(window, self):
        Gtk.main_quit()

    def on_open_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
                title = 'Open Image', 
                transient_for = button.get_toplevel(),
                action = Gtk.FileChooserAction.OPEN);
        dialog.add_button(Gtk.STOCK_CANCEL, 0)
        dialog.add_button(Gtk.STOCK_OK, 1)
        dialog.set_default_response(1)

        filefilter = Gtk.FileFilter()
        filefilter.add_pixbuf_formats()
        dialog.set_filter(filefilter)

        if dialog.run() == 1:
            self.image.set_from_file(dialog.get_filename())

        dialog.destroy()


def main(argv):
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
