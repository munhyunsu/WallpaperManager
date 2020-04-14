import os
import random
import csv
import subprocess
import shlex
import time

from tkinter import Frame, Tk, Label, Button, Canvas, PhotoImage
from PIL import ImageTk, Image
import yaml
from send2trash import send2trash

from config_manager import load_config

FLAGS = None
_ = None
CFG = None


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
        # member variables
        self.ban = set()
        self.proc = None

    def create_widgets(self):
        self._get_images()
        self.next_image()
        self._create_buttons()

    def next_image(self):
        if not self.images:
            self.quit()
            return
        self._update_image()
        self._create_canvas()
        self.my_canvas.after_cancel(self.after)
        self.after = self.my_canvas.after(1000*CFG['timeout'], 
                                          self.next_image)

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
                        # CFG['rec'] 
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
        self.my_path = self.images.pop(0)
        img = Image.open(self.my_path)
        img.thumbnail((CFG['size']['width'], CFG['size']['height']))
        self.my_img = ImageTk.PhotoImage(img)

    def _configure(self, event):
        print(event)

    def bind_shortcut(self):
        self.master.protocol('WM_DELETE_WINDOW', self.quit)
        self.master.bind('s', self.download)
        self.master.bind('a', self.addfav)
        self.master.bind('<Return>', self.addfav)
        self.master.bind('d', self.delete)
        self.master.bind('<space>', self.delete)
        self.master.bind('b', self.ban)
        self.master.bind('q', self.quit)

    def download(self, event=None):
        if self.proc is None:
            cmd = 'python3 wallhaven_crawler.py'
            cmd = shlex.split(cmd)
            self.proc = subprocess.Popen(cmd)
            self._check_proc()
            print(f'Executed downloader {self.proc.pid}')
        else:
            print(f'Still running {self.proc.pid}')

    def _check_proc(self):
        ret = self.proc.poll()
        if ret is None:
            self.buttons['Download'].after(1000*CFG['timeout'],
                                           self._check_proc)
        else:
            self.proc = None
            print(f'Terminated with return code {ret}')

    def delete(self, event=None):
        if os.path.exists(self.my_path):
            send2trash(self.my_path)
            self.next_image()
            print(f'Deleted image {self.my_path}')

    def ban(self, event=None):
        bname = os.path.basename(self.my_path)
        self.ban.add(bname)
        self.delete()

    def addfav(self, event=None):
        os.makedirs(os.path.abspath(os.path.expanduser(CFG['fav'])),
                    exist_ok=True)
        if os.path.exists(self.my_path):
            fname = os.path.basename(self.my_path)
            dst = os.path.join(CFG['fav'], fname)
            os.rename(self.my_path, dst)
            self.next_image()
            print(f'Add {self.my_path} to fav')

    def quit(self, event=None):
        while self.proc is not None:
            print(f'Wait for terminating {self.proc.pid}')
            time.sleep(1000*CFG['timeout'])
        if os.path.exists(CFG['ban']):
            with open(CFG['ban'], 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.ban.add(row[0])
        with open(CFG['ban'], 'w') as f:
            writer = csv.writer(f)
            for entry in sorted(list(self.ban)):
                writer.writerow([entry])
        self.master.quit()
        print(f'Save ban list and quit')


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
    root_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(root_path)
    os.chdir(root_dir)

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

