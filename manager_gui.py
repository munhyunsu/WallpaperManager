import os
import random

from tkinter import Tk, PhotoImage, Label, Button
from PIL import ImageTk, Image

IMAGE_DIR = os.path.abspath(os.path.expanduser('~/.slideshow'))
IMAGE_SIZE = ((1366, 768))
IMAGE = None

def download():
    print('clicked download')
    return

def ban():
    print('clicked ban')
    return

def resized_image(path):
    img = Image.open(path)
    img.thumbnail(IMAGE_SIZE)
    my_img = ImageTk.PhotoImage(img)
    return my_img

def get_images():
    images = list()
    dirs = [IMAGE_DIR]

    while dirs:
        path = dirs.pop(0)
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    images.append(entry.path)
                elif entry.is_dir():
                    dirs.append(entry.path)

    random.shuffle(images)
    return images

def refresh(root, images):
    global IMAGE
    ## Grid containner
    my_img = resized_image(images.pop(0))
    IMAGE = my_img
    my_label = Label(image=my_img)
    my_label.grid(row=0, column=0, columnspan=3)
    
    ## Button
    button_download = Button(root, text='Download', command=download)
    button_addfav = Button(root, text='Add to favorite', command=root.quit)
    button_ban = Button(root, text='Ban', command=ban)
    
    button_download.grid(row=1, column=0)
    button_addfav.grid(row=1, column=1)
    button_ban.grid(row=1, column=2)
    
    my_label.after(1000, refresh, root, images)


def main():
    ## Prepare excution
    os.makedirs(IMAGE_DIR, mode=0o766, exist_ok=True)
    images = get_images()
    root = Tk()

    ## Window title and icon
    root.title('Wallpaper Manager GUI')
    icon = PhotoImage(file=os.path.abspath(
                           os.path.expanduser('./icon.png')))
    root.tk.call('wm', 'iconphoto', root._w, icon)

    refresh(root, images)

    ## Tkinter mainloop
    root.mainloop()


if __name__ == '__main__':
    main()

