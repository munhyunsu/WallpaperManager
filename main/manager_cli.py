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

# global variable
from global_variable import IMAGESOURCES

def main(argv):
    """
    main loop
    """
    # TODO(LuHa): print message about program execution
    print('[WallpaperManagerCLI] Execute wallpaper manager')

    # TODO(LuHa): manage image source
    sources = IMAGESOURCES
    sources.sort()
    # adding dumy data for indexing convenience
    sources.insert(0, 'dumy')

    # TODO(LuHa): restore tags
    if os.path.isfile('tags.secret'):
        with open('tags.secret', 'r') as fp_tags:
            tags = json.load(fp_tags)
            for source in sources:
                tags[source] = tags.get(source, list())
    else:
        tags = dict()
        for source in sources:
            tags[source] = tags.get(source, list())

    # TODO(LuHa): junction loop according users' input
    while True:
        print('\x1B[38;5;3m'
            + '\n----+----+ Wallpaper Manager CLI ----+----+'
            + '\x1B[0m')
        print('----+----+----+ Main menu ----+----+----+')
        for index in range(1, len(sources)):
            print('{0}. Edit {1} search tags'.format(
                      index, sources[index]))
            print(tags[sources[index]])
        print('c. Check downloaded wallpaper')
        print('s. Start download wallpaper')
        print('q. Terminate programm')
        print('----+----+----+----+----+----+----+----+')
        user_input = input('User input: ')
        user_input = user_input.lower()
        # TODO(LuHa): jump to function
        if user_input.isdecimal():
            user_input = int(user_input)
            if user_input < 1:
                continue
            if user_input < len(tags):
                edit_tags(tags, sources[user_input])
        elif user_input == 'c':
            check_wallpaper()
        elif user_input == 's':
            for index in range(1, len(sources)):
                start_download(sources[index])
        #elif user_input == 'r':
        #    random_slideshow()
        elif user_input == 'q':
            break

    # TODO(LuHa): print message about program termination
    print('[WallpaperManagerCLI] Terminate wallpaper manager')
    


def edit_tags(tags, key):
    """
    edit tag function
    """
    # TODO(LuHa): junction loop
    while(True):
        print('\n----+----+ Edit {0} tags ----+----+'.format(key))
        print('Current tag list')
        print(tags[key])
        print('a. Add tag')
        print('d. Delete tag')
        print('b. back')
        print('----+----+----+----+')
        user_input = input('User input: ')
        user_input = user_input.lower()
        # TODO(LuHa): processing user's input
        if user_input == 'a':
            user_input = input('Tag to add: ')
            tags[key].append(user_input)
        if user_input == 'd':
            user_input = input('Tag to delete: ')
            if user_input in tags[key]:
                tags[key].remove(user_input)
        if user_input == 'b':
            break
    # TODO(LuHa): save tags
    with open('tags.secret', 'w') as fp_tags:
        tags[key].sort()
        json.dump(tags, fp_tags,
                  indent = 4,
                  sort_keys = True)



def start_download(source):
    """
    start download image from site each.
    if we use subprocess.Popen, then we can execute it parallel.
    if we do not want mixing the standard output, 
      then we have to use subprocess.run
    """
    downloader = (source + '_downloader.py')
    subprocess.Popen(['python3', downloader])



def check_wallpaper():
    """
    change mode to wallpaper changer.
    that module have indivitual menu and input handler.
    so, we use subprocess.run
    """
    subprocess.run(['python3', 'wallchanger.py'])



# maybe it is good thing, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[WallpaperManagerCLI] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
