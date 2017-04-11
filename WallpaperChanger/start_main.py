#!/usr/bin/env python3

import sys
import tkinter

class Application(tkinter.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.master = master

    def create_widgets(self):
        self.hi_there = tkinter.Button(self)
        self.hi_there['text'] = 'Hello World\n(click me)'
        self.hi_there['command'] = self.say_hi
        self.hi_there.pack(side = 'top')
        self.quit = tkinter.Button(self, 
                              text = 'QUIT',
                              fg = 'red',
                              command = self.master.destroy)
        self.quit.pack(side = 'bottom')

    def say_hi(self):
        print('hi there, everyone!')


def main(argv):
    root = tkinter.Tk()
    app = Application(master = root)
    app.mainloop()



if __name__ == '__main__':
    sys.exit(main(sys.argv))
