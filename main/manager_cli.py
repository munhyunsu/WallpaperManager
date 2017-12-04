#!/usr/bin/env python3
# colored text hint: https://en.wikipedia.org/wiki/ANSI_escape_code

# exit
import sys
# isfile
import os
# config
import json
# subprocess
import subprocess

# utils
import utils
# global variable
from global_variable import IMAGESOURCES

def main(argv):
    """
    main loop
    This function show that all of tags as well as menu in initial version 
    but, since 1.1.3 it do not show tags of image sources
    for source code simplity and menu visibility, tag privacy.
    """
    # TODO(LuHa): print message about program execution
    print('[WallpaperManagerCLI] Execute wallpaper manager')

    # TODO(LuHa): junction loop according users' input
    while True:
        print('\x1B[38;5;3m'
            + '\n----+----+ Wallpaper Manager CLI ----+----+'
            + '\x1B[0m')
        print('----+----+----+ Main menu ----+----+----+')
        print('1. Edit danbooru search tags')
        print('2. Edit yandere search tags')
        print('3. Edit wallhaven search tags')
        print('4. Edit pixiv search tags(not available now)')
        print('c. Check downloaded wallpaper')
        print('d. Delete file with size 0')
        print('p. Start wallpaper downloading in parallel')
        print('s. Start wallpaper downloading in sequential')
        print('q. Terminate programm')
        print('----+----+----+----+----+----+----+----+')
        user_input = input('User input: ')
        user_input = user_input.strip()
        user_input = user_input.lower()
        # TODO(LuHa): jump to function
        if user_input == '1':
            edit_tags('danbooru')
        elif user_input == '2':
            edit_tags('yandere')
        elif user_input == '3':
            edit_tags('wallhaven')
        elif user_input == '4':
            edit_tags('pixiv')
        elif user_input == 'c':
            check_wallpaper()
        elif user_input == 'd':
            delete_file_size0()
        elif user_input == 'p':
            start_download(mode = 'parallel')
        elif user_input == 's':
            start_download(mode = 'sequential')
        elif user_input == 'q':
            break

    # TODO(LuHa): print message about program termination
    print('[WallpaperManagerCLI] Terminate wallpaper manager')
    


def edit_tags(source):
    """
    edit tag function
    """
    subprocess.run(['python3', 'tag_editor.py', source])



def start_download(mode = 'sequential'):
    """
    start download image from site each.
    if we use subprocess.Popen, then we can execute it parallel.
    if we do not want mixing the standard output, 
      then we have to use subprocess.run
    """
    if mode == 'parallel':
        # global_variable
        sources = IMAGESOURCES

        # execute downloader
        for index in range(0, len(sources)):
            downloader = (sources[index] + '_downloader.py')
            subprocess.Popen(['python3', downloader])

    elif mode == 'sequential':
        print('\n----+----+ Sequential download menu ----+----+')
        print('1. Danbooru')
        print('2. Yandere')
        print('3. Wallhaven')
        print('4. Pixiv')
        print('Input the sequence between space(ex. 1 2 3 4')
        print('----+----+----+----+----+----+')
        user_input = input('User input :')
        user_input = user_input.strip()
        user_input = user_input.lower()
        user_input = user_input.split(' ')

        for cursor in user_input:
            if cursor == '1':
                subprocess.run(['python3', 'danbooru_downloader.py'])
            elif cursor == '2':
                subprocess.run(['python3', 'yandere_downloader.py'])
            elif cursor == '3':
                subprocess.run(['python3', 'wallhaven_downloader.py'])
            elif cursor == '4':
                subprocess.run(['python3', 'pixiv_downloader.py'])
    print('End download')



def check_wallpaper():
    """
    change mode to wallpaper changer.
    that module have indivitual menu and input handler.
    so, we use subprocess.run
    """
    subprocess.run(['python3', 'wallchanger.py'])



def delete_file_size0():
    """
    delete file size 0
    """
    # TODO(LuHa): delete file size 0
    counter = utils.delete_file_size0()
    print('Delete {0} files complete'.format(counter))



# maybe it is good thing, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[WallpaperManagerCLI] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
