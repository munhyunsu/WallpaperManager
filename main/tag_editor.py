#!/usr/bin/env python3

# exit
import sys

# utils
import utils



def main(argv):
    """
    edit tag with argv about image source
    """
    # TODO(LuHa): initialize
    if len(argv) < 2:
        print('[TagEditor] The image source is not selected')
        return
    source = argv[1]
    
    # TODO(LuHa): load tags
    tags = utils.get_database('tags.secret')

    # TODO(Luha): branch by source
    if source == 'danbooru':
        edit_danbooru(tags)
    elif source == 'yandere':
        edit_yandere(tags)
    elif source == 'wallhaven':
        edit_wallhaven(tags)
    else:
        print('[TagEditor] Unknown image source')
        return

    # TODO(LuHa): save tags
    utils.set_database('tags.secret', tags)


def edit_danbooru(tags):
    while True:
        print('\n----+----+ Edit danbooru tags ----+----+')
        print('Current tag list')
        print(tags['danbooru'])
        print('a. Add tag')
        print('d. delete tag')
        print('b. back')
        user_input = input('User input: ')
        user_input = user_input.strip()
        user_input = user_input.lower()
        
        if user_input == 'a':
            user_input = input('Tag to add: ')
            user_input = user_input.strip()
            tags['danbooru'].add(user_input)
        elif user_input == 'd':
            user_input = input('Tag to delete: ')
            user_input = user_input.strip()
            if user_input in tags['danbooru']:
                tags['danbooru'].remove(user_input)
        elif user_input == 'b':
            break
    


def edit_yandere(tags):
    while True:
        print('\n----+----+ Edit yandere tags ----+----+')
        print('Current tag list')
        print(tags['yandere'])
        print('a. Add tag')
        print('d. delete tag')
        print('b. back')
        user_input = input('User input: ')
        user_input = user_input.strip()
        user_input = user_input.lower()
        
        if user_input == 'a':
            user_input = input('Tag to add: ')
            user_input = user_input.strip()
            tags['yandere'].add(user_input)
        elif user_input == 'd':
            user_input = input('Tag to delete: ')
            user_input = user_input.strip()
            if user_input in tags['yandere']:
                tags['yandere'].remove(user_input)
        elif user_input == 'b':
            break



def edit_wallhaven(tags):
    while True:
        print('\n----+----+ Edit wallhaven tags ----+----+')
        print('Current tag list')
        print(tags['wallhaven'])
        print('a. Add tag')
        print('d. delete tag')
        print('b. back')
        user_input = input('User input: ')
        user_input = user_input.strip()
        user_input = user_input.lower()
        
        if user_input == 'a':
            user_input = input('Tag to add: ')
            user_input = user_input.strip()
            tags['wallhaven'].add(user_input)
        elif user_input == 'd':
            user_input = input('Tag to delete: ')
            user_input = user_input.strip()
            if user_input in tags['wallhaven']:
                tags['wallhaven'].remove(user_input)
        elif user_input == 'b':
            break



def edit_pixiv(tags):
    while True:
        print('\n----+----+ Edit pixiv tags ----+----+')
        print('Current tag list')
        print(tags['pixiv'])
        print('a. Add tag')
        print('d. delete tag')
        print('b. back')
        user_input = input('User input: ')
        user_input = user_input.strip()
        user_input = user_input.lower()
        
        if user_input == 'a':
            user_input = input('Tag to add: ')
            user_input = user_input.strip()
            tags['pixiv'].add(user_input)
        elif user_input == 'd':
            user_input = input('Tag to delete: ')
            user_input = user_input.strip()
            if user_input in tags['pixiv']:
                tags['pixiv'].remove(user_input)
        elif user_input == 'b':
            break



# maybe it is good thing, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[TagEditor] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
