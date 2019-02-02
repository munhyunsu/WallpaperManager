#!/usr/bin/env python

import sys


# Need input in here?
class WallpaperViewer(object):
    def start(self):
        print('\x1B[38;5;3m'
            + '\n----+----+ Wallpaper Manager CLI ----+----+'
            + '\x1B[0m')

    def main(self):
        user = dict()
        print('----+----+----+ Main menu ----+----+----+')
        print('0. Change tags set(not available now)')
        print('1. Edit danbooru search tags')
        print('2. Edit yandere search tags')
        print('3. Edit wallhaven search tags')
        print('4. Edit pixiv search tags')
        print('c. Check downloaded wallpaper')
        print('d. Delete file with size 0')
        print('o. Configuration')
        print('p. Start wallpaper downloading in parallel')
        print('s. Start wallpaper downloading in sequential')
        print('q. Terminate programm')
        print('----+----+----+----+----+----+----+----+')
        user_input = input('Main menu select: ')
        user_input = user_input.strip().lower()
        # TODO(LuHa): convert string to global variables(state)
        if user_input == '0':
            user['intent'] = 'change_tag_set'
        elif user_input == '1':
            user['intent'] = 'edit_danbooru_tag'
        elif user_input == '2':
            user['intent'] = 'edit_yandere_tag'
            

    def end(self):
        print('\x1B[38;5;3m'
            + '\n[WallpaperManagerCLI] Terminate wallpaper manager'
            + '\x1B[0m')

    def tag(self, target, tags):
        print('\n----+----+ Edit {0} tags ----+----+'.format(target))
        print('Current tag list')
        print(tags)
        print('a. Add tag')
        print('d. delete tag')
        print('b. back')


wviewer = WallpaperViewer()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
