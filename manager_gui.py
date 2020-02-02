import os
import random

from tkinter import Frame, Tk, Label, Button, Canvas, PhotoImage
from PIL import ImageTk, Image
import yaml

from config_manager import load_config

FLAGS = None
_ = None
CFG = None
IMAGE_SIZE = ([1366, 768])
IMAGE = None


class Application(Frame):
    def __init__(self, master=None):
        global CFG
        super().__init__(master)
        self.master = master
        self.master.tk.call('wm', 'iconphoto', 
                            self.master._w, 
                            PhotoImage(file=CFG['icon']))
        self.create_widgets()
        self.bind_shortcut()

    def create_widgets(self):
        self._get_images()
        self.next_image()
        self._create_buttons()

    def next_image(self):
        self._update_image()
        self._create_canvas()
        if self.images:
            self.my_canvas.after(100*CFG['timeout'], self.next_image)
        else:
            self.my_canvas.after(100*CFG['timeout'], self.master.quit)

    def _get_images(self):
        self.images = list()
        dirs = [CFG['output']]
        while dirs:
            path = dirs.pop(0)
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file():
                        self.images.append(entry.path)
                    elif entry.is_dir():
                        continue # TODO(LuHa): Config file
                        dirs.append(entry.path)
        random.shuffle(self.images)

    def _create_canvas(self):
        self.my_canvas = Canvas(width=CFG['size']['width'],
                                height=CFG['size']['height'])
        self.my_canvas.create_image(CFG['size']['width']/2,
                                    CFG['size']['height']/2,
                                    image=self.my_img)
        self.my_canvas.grid(row=0, column=0, columnspan=4)

    def _create_buttons(self):
        self.buttons = dict()
        self.buttons['Download'] = Button(self.master, text='[S] Download', 
                                          command=self.download)
        self.buttons['Delete'] = Button(self.master, text='[D] Delete',
                                        command=self.delete)
        self.buttons['AddFav'] = Button(self.master, text='[F] Add to favorite', 
                                        command=self.addfav)
        self.buttons['Ban'] = Button(self.master, text='[B] Ban', 
                                     command=self.ban)
    
        self.buttons['Download'].grid(row=1, column=0)
        self.buttons['Delete'].grid(row=1, column=1)
        self.buttons['AddFav'].grid(row=1, column=2)
        self.buttons['Ban'].grid(row=1, column=3)

    def _update_image(self):
        img = Image.open(self.images.pop(0))
        img.thumbnail((CFG['size']['width'], CFG['size']['height']))
        self.my_img = ImageTk.PhotoImage(img)

    def _configure(self, event):
        print(event)

    def bind_shortcut(self):
        self.master.bind('s', self.download)
        self.master.bind('a', self.addfav)
        self.master.bind('d', self.delete)
        self.master.bind('b', self.ban)
        self.master.bind('q', self.quit)

    def download(self, event):
        print(f'clicked download {event}')
        return

    def delete(self, event):
        print(f'clicked delete {event}')
        return

    def ban(self, event):
        print(f'clicked ban {event}')
        return

    def addfav(self, event):
        print(f'clicked addfav {event}')
        return

    def quit(self, event):
        print(f'clicked quit {event}')
        self.master.quit()
        return


def main():
    global CFG
    # Print Parameters
    print(f'Parsed: {FLAGS}')
    print(f'Unparsed: {_}')

    # load configuration
    CFG = load_config(FLAGS.config)

    # Create Tk Application
    root = Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
 
    parser.add_argument('-c', '--config', type=str,
                        default='config.yaml',
                        help='The configuration file path')
    FLAGS, _ = parser.parse_known_args()

    # Preprocessing for some arguments
    FLAGS.config = os.path.abspath(os.path.expanduser(FLAGS.config))

    # Excute main
    main()

