import os
import random

from tkinter import Frame, Tk, Label, Button, Canvas, PhotoImage
from PIL import ImageTk, Image

ICON = os.path.abspath(os.path.expanduser('./icon.png'))
IMAGE_DIR = os.path.abspath(os.path.expanduser('~/.slideshow'))
IMAGE_SIZE = ([1366, 768])
IMAGE = None


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.tk.call('wm', 'iconphoto', 
                            self.master._w, PhotoImage(file=ICON))
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
            self.my_canvas.after(100*10, self.next_image)
        else:
            self.my_canvas.after(100*10, root.quit)

    def _get_images(self):
        self.images = list()
        dirs = [IMAGE_DIR]
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
        self.my_canvas = Canvas(width=IMAGE_SIZE[0], height=IMAGE_SIZE[1])
        self.my_canvas.create_image(IMAGE_SIZE[0]/2, IMAGE_SIZE[1]/2, 
                                    image=self.my_img)
        self.my_canvas.grid(row=0, column=0, columnspan=4)

    def _create_buttons(self):
        self.buttons = dict()
        self.buttons['Download'] = Button(root, text='Download', 
                                          command=self.download)
        self.buttons['Delete'] = Button(root, text='Delete',
                                        command=self.delete)
        self.buttons['AddFav'] = Button(root, text='Add to favorite', 
                                        command=self.addfav)
        self.buttons['Ban'] = Button(root, text='Ban', 
                                     command=self.ban)
    
        self.buttons['Download'].grid(row=1, column=0)
        self.buttons['Delete'].grid(row=1, column=1)
        self.buttons['AddFav'].grid(row=1, column=2)
        self.buttons['Ban'].grid(row=1, column=3)

    def _update_image(self):
        img = Image.open(self.images.pop(0))
        img.thumbnail(IMAGE_SIZE)
        self.my_img = ImageTk.PhotoImage(img)

    def _configure(self, event):
        print(event)

    def bind_shortcut(self):
        self.master.bind('a', self.addfav)
        self.master.bind('d', self.delete)
        self.master.bind('b', self.ban)

    def download(self):
        print('clicked download')
        return

    def delete(self):
        print('clicked delete')
        return

    def ban(self):
        print('clicked ban')
        return

    def addfav(self):
        print('clicked addfav')
        return


if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()

