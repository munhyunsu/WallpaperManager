#!/usr/bin/env python3

# exit, argv
import sys
# scandir
import os
# subprocess
import subprocess
# shuffle 
import random
# json
import json
# move
import shutil
# select
import select

# manage list of available image source
IMAGESOURCES = ['danbooru',
                'yandere',
                'wallhaven']

def main(argv):
    """
    """
    # TODO(LuHa): print message about program execution
    print('[Changer] Execute wallpaper changer')

    # TODO(LuHa): create save directory
    os.makedirs('./downloads', exist_ok = True)
    os.makedirs('./save', exist_ok = True)

    # TODO(LuHa): load ban database
    if os.path.exists('ban.secret'):
        with open('ban.secret', 'r') as f_db:
            ban_db = json.load(f_db)
            for source in IMAGESOURCES:
                ban_db[source] = set(ban_db.get(source, list()))
    else:
        ban_db = dict()
        for source in IMAGESOURCES:
            ban_db[source] = set(ban_db.get(source, list()))

    # TODO(LuHa): load mute database
    if os.path.exists('mute.secret'):
        with open('mute.secret', 'r') as f_db:
            mute_db = json.load(f_db)
            for source in IMAGESOURCES:
                mute_db[source] = set(mute_db.get(source, list()))
    else:
        mute_db = dict()
        for source in IMAGESOURCES:
            mute_db[source] = set(mute_db.get(source, list()))

    # TODO(LuHa): get all of downloaded images
    downloaded = list()
    if sys.version_info.minor < 6:
        for entry in os.scandir('./downloads'):
            if entry.is_file():
                downloaded.append(os.path.abspath(entry.path))
    else:
        with os.scandir('./downloads') as it:
            for entry in it:
                if entry.is_file():
                    downloaded.append(os.path.abspath(entry))
    random.shuffle(downloaded)    

    # TODO(LuHa): get user preference about enable or disable auto change
    print('If you want to enable auto-change input the sleep time')
    print('If you type 0 then disable zuto-change feature')
    sleep_time = input('User input about sleep time: ')
    sleep_time = int(sleep_time)

    # TODO(LuHa): loop images
    while len(downloaded) > 0:
        cursor = downloaded.pop()

        # TODO(LuHa): change wallpaper
        image_path = 'file://' + cursor
        subprocess.run(['gsettings',
                        'set',
                        'org.cinnamon.desktop.background',
                        'picture-uri',
                        image_path])
        subprocess.run(['gsettings',
                        'set',
                        'org.cinnamon.desktop.background',
                        'picture-opacity',
                        '100'])
        subprocess.run(['gsettings',
                        'set',
                        'org.cinnamon.desktop.background',
                        'picture-options',
                        'scaled'])

        # TODO(LuHa): print menu and handle user's input
        image_name = cursor.split('/')[-1]
        print('\n----+----+ {0} image left ----+----+'.format(
                                                        len(downloaded)))
        print('b. Ban image')
        print('d. Delete image')
        print('m. Mute image')
        print('s. Save image')
        print('q. Quit')
        print('Current image name: {0}'.format(image_name))
        print('----+----+----+----+')
        if sleep_time > 0:
            left_time = sleep_time
            print('\x1B[31C\x1B[s\x1B[31D', end = '')
            while left_time > 0:
                print('User input({0:5} second left): \x1B[u'.format(left_time),
                      end = '', flush = True)
                (r, w, e) = select.select([sys.stdin], [], [], 1)
                if r:
                    user_input = sys.stdin.readline().strip()
                    user_input = user_input.lower()
                    break
                else:
                    left_time = left_time-1
                    print('\x1B[s\x1B[1F')
            if left_time == 0:
                downloaded.insert(0, cursor)
                print('Auto-change')
                continue
        else:
            user_input = input('User input: ')
            user_input = user_input.lower()

        if user_input == 'b':
            print('[Changer] Ban image {0}'.format(image_name))
            [site, number] = image_name.split('-')
            number = number.split('.')[0]
            ban_db[site].add(int(number))
            os.remove(cursor)
        elif user_input == 'd':
            print('[Changer] Delete image {0}'.format(image_name))
            os.remove(cursor)
        elif user_input == 'm':
            print('[Changer] Mute image {0}'.format(image_name))
            [site, number] = image_name.split('-')
            number = number.split('.')[0]
            mute_db[site].add(int(number))
            os.remove(cursor)
        elif user_input == 's':
            print('[Changer] Save image {0}'.format(image_name))
            src_path = './downloads/' + image_name
            dst_path = './save/' + image_name
            shutil.move(src_path, dst_path)
        elif user_input == 'q':
            break

    # TODO(LuHa): save ban database
    with open('ban.secret' ,'w') as f_ban:
        for source in IMAGESOURCES:
            ban_db[source] = list(ban_db[source])
            ban_db[source].sort()
        json.dump(ban_db,
                  f_ban,
                  indent = 4,
                  sort_keys = True)

    # TODO(LuHa): save mute database
    with open('mute.secret' ,'w') as f_mute:
        for source in IMAGESOURCES:
            mute_db[source] = list(mute_db[source])
            mute_db[source].sort()
        json.dump(mute_db,
                  f_mute,
                  indent = 4,
                  sort_keys = True)

    # TODO(LuHa): print message about program termination
    print('[Changer] Terminate wallpaper changer')



# Maybe it is good, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[Changer] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
