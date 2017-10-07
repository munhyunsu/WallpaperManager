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
    while(user_input != 'q'):
        print_menu()
        user_input = input('User input: ')
        if(user_input is not None):
            user_input = user_input.lower()

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





if __name__ == '__main__':
    sys.exit(main(sys.argv))
