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
    print('[WM] Execute wallpaper manager')

    # TODO(LuHa): restore tags
    if os.path.isfile('tags.secret'):
        with open('tags.secret', 'r') as fp_tags:
            tags = json.load(fp_tags)
    else:
        tags = dict()
        tags['danbooru'] = list()
        tags['yandere'] = list()

    # TODO(LuHa): junction loop according users' input
    while True:
        print('\n----+----+----+ Main menu ----+----+----+')
        print('1. Edit danbooru search tags')
        print(tags['danbooru'])
        print('2. Edit yandere search tags')
        print(tags['yandere'])
        print('3. Start download wallpaper')
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
            start_download()
        elif user_input == 'q':
            break

    # TODO(LuHa): print message about program termination
    print('[WM] Terminate wallpaper manager')
    

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
            if user_input in tags:
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
    """
    #subprocess.run(['python3', 'danbooru_downloader.py'])
    #with subprocess.Popen(['python3', 'danbooru_downloader.py']) as proc:
    #    print(proc.stdout.read())
    subprocess.Popen(['python3', 'danbooru_downloader.py'])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
