#!/usr/bin/env python3

# exit, argv
import sys
# scandir
import os
# subprocess
import subprocess
# shuffle 
import random
# sleep
import time

# manage list of available image source
IMAGESOURCES = ['danbooru',
                'yandere',
                'wallhaven']

def main(argv):
    """
    """
    # TODO(LuHa): print message about program execution
    print('[RandomChanger] Execute random changer')

    # TODO(LuHa): create save directory
    os.makedirs('./downloads', exist_ok = True)
    os.makedirs('./save', exist_ok = True)

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

    # TODO(LuHa): ask about sleep time
    print('[RandomChanger] We need how much sleep between images')
    sleep_time = int(input('User input: '))

    # TODO(LuHa): loop images
    print('[RandomChanger] Downloaded images slideshow'
        + '(Sleep: {0})'.format(sleep_time))
    print('[RandomChanger] To terminate slideshow, press CTRL+C')
    try:
        while True:
            cursor = random.choice(downloaded)
            print('[RandomChanger] Path: {0}'.format(cursor))
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
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print('[RandomChanger] Keyboard interrupt detected')

    # TODO(LuHa): print message about program termination
    print('[RandomChanger] Terminate wallpaper changer')



# Maybe it is good, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[RandomChanger] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
