import os
import random

from tkinter import Tk, Label, Button, Canvas
from PIL import ImageTk, Image

IMAGE_DIR = os.path.abspath(os.path.expanduser('~/.slideshow'))
IMAGE_SIZE = ([1366, 768])
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
                    continue # TODO(LuHa): Need to change
                    dirs.append(entry.path)

    random.shuffle(images)
    return images

def refresh(root, images):
    global IMAGE
    ## Grid containner
    my_img = resized_image(images.pop(0))
    my_canvas = Canvas(width=IMAGE_SIZE[0], height=IMAGE_SIZE[1])
    my_canvas.create_image(IMAGE_SIZE[0]/2, IMAGE_SIZE[1]/2, image=my_img)
    my_canvas.grid(row=0, column=0, columnspan=3)
    
    ## Button
    button_download = Button(root, text='Download', command=download)
    button_addfav = Button(root, text='Add to favorite', command=root.quit)
    button_ban = Button(root, text='Ban', command=ban)
    
    button_download.grid(row=1, column=0)
    button_addfav.grid(row=1, column=1)
    button_ban.grid(row=1, column=2)
    
    IMAGE = my_img
    if images:
        my_canvas.after(100*10, refresh, root, images)
    else:
        my_canvas.after(100*10, root.quit)

def configure(event):
    pass

def main():
    global IMAGE_SIZE
    ## Prepare excution
    os.makedirs(IMAGE_DIR, mode=0o766, exist_ok=True)
    images = get_images()
    root = Tk()
    root.resizable(False, False)
    IMAGE_SIZE[0] = root.winfo_screenwidth()/1.5
    IMAGE_SIZE[1] = root.winfo_screenheight()/1.5
    IMAGE_SIZE = tuple(IMAGE_SIZE)

    ## Window title and icon
    root.title('Wallpaper Manager GUI')
    icon = ImageTk.PhotoImage(file=os.path.abspath(
                           os.path.expanduser('./icon.png')))
    root.tk.call('wm', 'iconphoto', root._w, icon)

    refresh(root, images)

    root.bind('<Configure>', configure)

    ## Tkinter mainloop
    root.mainloop()


if __name__ == '__main__':
    main()

