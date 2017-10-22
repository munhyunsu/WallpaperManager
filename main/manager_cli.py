#!/usr/bin/env python3

# exit
import sys
# isfile
import os
# config
import json
# subprocess
import subprocess

# manage list of available image source
IMAGESOURCES = ['danbooru',
                'yandere',
                'wallhaven']

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
            for source in IMAGESOURCES:
                tags[source] = tags.get(source, list())
    else:
        tags = dict()
        for source in IMAGESOURCES:
            tags[source] = tags.get(source, list())

    # TODO(LuHa): junction loop according users' input
    while True:
        print('\n----+----+ Wallpaper Manager CLI ----+----+')
        print('----+----+----+ Main menu ----+----+----+')
        for index in range(0, len(IMAGESOURCES)):
            print('{0}. Edit {1} search tags'.format(
                      index+1, IMAGESOURCES[index]))
            print(tags[IMAGESOURCES[index]])
        print('c. Check downloaded wallpaper')
        print('s. Start download wallpaper')
        print('r. Random slideshow using downloaded wallpaper(unchecked)')
        print('q. Terminate programm')
        print('----+----+----+----+----+----+----+----+')
        user_input = input('User input: ')
        user_input = user_input.lower()
        # TODO(LuHa): jump to function
        if user_input.isdecimal():
            if int(user_input) < 1:
                continue
            if int(user_input) < len(tags)+1:
                edit_tags(tags, IMAGESOURCES[int(user_input)-1])
        elif user_input == 'c':
            check_wallpaper()
        elif user_input == 's':
            start_download()
        elif user_input == 'r':
            random_slideshow()
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
    for source in IMAGESOURCES:
        downloader = (source + '_downloader.py')
        subprocess.Popen(['python3', downloader])



def check_wallpaper():
    """
    change mode to wallpaper changer.
    that module have indivitual menu and input handler.
    so, we use subprocess.run
    """
    subprocess.run(['python3', 'wallchanger.py'])



def random_slideshow():
    """
    start slideshow using downloaded images
    but, those images are unchecked
    """
    subprocess.run(['python3', 'random_slideshow.py'])


# maybe it is good thing, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[WallpaperManagerCLI] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
