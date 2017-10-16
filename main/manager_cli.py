#!/usr/bin/env python3

# exit
import sys
# isfile
import os
# config
import json
# subprocess
import subprocess

def main(argv):
    """
    main loop
    """
    # TODO(LuHa): print message about program execution
    print('[WallpaperManagerCLI] Execute wallpaper manager')

    # TODO(LuHa): restore tags
    if os.path.isfile('tags.secret'):
        with open('tags.secret', 'r') as fp_tags:
            tags = json.load(fp_tags)
            tags['danbooru'] = tags.get('danbooru', list())
            tags['yandere'] = tags.get('yandere', list())
            tags['wallhaven'] = tags.get('wallhaven', list())
    else:
        tags = dict()
        tags['danbooru'] = list()
        tags['yandere'] = list()
        tags['wallhaven'] = list()

    # TODO(LuHa): junction loop according users' input
    while True:
        print('\n----+----+ Wallpaper Manager CLI ----+----+')
        print('----+----+----+ Main menu ----+----+----+')
        print('1. Edit danbooru search tags')
        print(tags['danbooru'])
        print('2. Edit yandere search tags')
        print(tags['yandere'])
        print('3. Edit wallhaven search tags')
        print(tags['wallhaven'])
        print('c. Check downloaded wallpaper')
        print('s. Start download wallpaper')
        print('q. Terminate programm')
        print('----+----+----+----+----+----+----+----+')
        user_input = input('User input: ')
        user_input = user_input.lower()
        # TODO(LuHa): jump to function
        if user_input == '1':
            edit_tags(tags, 'danbooru')
        elif user_input == '2':
            edit_tags(tags, 'yandere')
        elif user_input == '3':
            edit_tags(tags, 'wallhaven')
        elif user_input == 's':
            start_download()
        elif user_input == 'c':
            check_wallpaper()
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
        print('\n----+----+ Edit tags ----+----+')
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



def start_download():
    """
    start download image from site each.
    if we use subprocess.Popen, then we can execute it parallel.
    if we do not want mixing the standard output, 
      then we have to use subprocess.run
    """
    subprocess.Popen(['python3', 'danbooru_downloader.py'])
    subprocess.Popen(['python3', 'yandere_downloader.py'])
    subprocess.Popen(['python3', 'wallhaven_downloader.py'])



def check_wallpaper():
    """
    change mode to wallpaper changer.
    that module have indivitual menu and input handler.
    so, we use subprocess.run
    """
    subprocess.run(['python3', 'wallchanger.py'])



# maybe it is good thing, right?
if __name__ == '__main__':
    sys.exit(main(sys.argv))
