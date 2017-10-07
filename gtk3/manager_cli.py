#!/usr/bin/env python3

import sys

# global variable
danbooru_tags = list()
yandere_tags = list()

def main(argv):
    """
    main loop
    """
    # TODO(LuHa): print message about program execution
    print('Execute wallpaper manager')

    # input variable for user
    user_input = None

    # TODO(LuHa): junction loop according users' input
    while(True):
        print_menu()
        user_input = input('User input: ')
        if(user_input is None):
            continue
        user_input = user_input.lower()
        # TODO(LuHa): jump to function
        if(user_input == '1'):
            edit_danbooru_tags()
        elif(user_input == '2'):
            edit_yandere_tags()
        elif(user_input == '3'):
            start_download()
        elif(user_input == 'q'):
            break

    # TODO(LuHa): print message about program termination
    print('Terminate wallpaper manager')
    

def print_menu():
    print('----+----+----+ Main menu ----+----+----+')
    print('1. Edit danbooru search tags')
    print(danbooru_tags)
    print('2. Edit yandere search tags')
    print(yandere_tags)
    print('3. Start download wallpaper')
    print('q. Terminate programm')
    print('----+----+----+----+----+----+----+----+')


def edit_danbooru_tags():
    """
    """
    print('danbooru')


def edit_yandere_tags():
    """
    """
    print('yandere')


def start_download():
    """
    """
    print('download')



if __name__ == '__main__':
    sys.exit(main(sys.argv))
