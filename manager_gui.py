import os
import random
import csv
import subprocess
import shlex
import time

import tkinter as tk
from tkinter import Frame, Tk, Label, Button, Canvas, PhotoImage
from PIL import ImageTk, Image
import yaml
from send2trash import send2trash


FLAGS = _ = None
DEBUG = False
CFG = None


class Application(Frame):
    def __init__(self, master=None):
        global CFG
        super().__init__(master)
        self.master = master
        self.master.title('Wallpaper manager')
        self.master.tk.call('wm', 'iconphoto', self.master._w,
                            PhotoImage(file=CFG['icon']))
        # member variables
        self.object = dict()
        self.ban = set()
        # call
        self.create_main()
#        self.bind_shortcut()

    def create_main(self):
        self.object['fr_main'] = Frame(master=self.master, relief=tk.RAISED,
                                       borderwidth=1)
        self.object['fr_main'].grid_rowconfigure(0, weight=1)
        self.object['fr_main'].grid_rowconfigure(1, weight=1)
        self.object['fr_main'].grid_columnconfigure(0, weight=1)
        self.object['fr_main'].grid_columnconfigure(1, weight=1)
        self.object['fr_main'].grid_columnconfigure(2, weight=1)
        self.object['bt_download'] = Button(self.object['fr_main'], text='[S] Download',
                                            command=self.download)
        self.object['bt_download'].grid(row=0, column=0)
        self.object['bt_delete'] = Button(self.object['fr_main'], text='[D] Delete',
                                          command=self.delete)
        self.object['bt_delete'].grid(row=1, column=0)
        self.object['bt_addFav'] = Button(self.object['fr_main'], text='[F] Add to favorite',
                                          command=self.addfav)
        self.object['bt_addFav'].grid(row=1, column=1)
        self.object['bt_ban'] = Button(self.object['fr_main'], text='[B] Ban',
                                       command=self.ban)
        self.object['bt_ban'].grid(row=1, column=2)
        self.object['fr_main'].pack(expand=2, fill='both', side=tk.LEFT)

#    def create_widgets(self):
#        self._get_images()
#        self.next_image()
#        self._create_buttons()

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
            if DEBUG:
                print('re-after at _check_proc')
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
        if self.proc is not None:
            if DEBUG:
                print(f'Wait for terminating {self.proc.pid}')
            print('Wait for download completed')
            return
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


def load_config(cfg_path):
    with open(cfg_path, 'r') as f:
        cfg = yaml.safe_load(f)
    return cfg


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

    parser.add_argument('--debug', action='store_true',
                        help='enable debug mode')
    parser.add_argument('--config', type=str,
                        default='config.yaml',
                        help='The configuration file path')
    FLAGS, _ = parser.parse_known_args()

    FLAGS.config = os.path.abspath(os.path.expanduser(FLAGS.config))

    DEBUG = FLAGS.debug

    # Excute main
    main()

