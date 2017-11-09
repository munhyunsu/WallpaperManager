#!/usr/bin/env python3

# version_info
import sys
# scandir
import os
# sleep
import time
# randint
import random


def get_downloaded_images(source):
    """
    read pre-downloaded images from paths
    it search only paths
    arg:
        source: image source (image prefix)
    ret:
        set: downloaded image number
    """
    paths = ['./downloads',
             './save']
    downloaded = set()
    if sys.version_info.minor < 6:
        for path in paths:
            for entry in os.scandir(path):
                if entry.is_file():
                    if (entry.name).startswith(source):
                        image_id = (entry.name).split('-')[1]
                        image_id = (image_id).split('.')[0]
                        image_id = int(image_id)
                        downloaded.add(image_id)
    else:
        for path in paths:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file():
                        if (entry.name).startswith(source):
                            image_id = (entry.name).split('-')[1]
                            image_id = (image_id).split('.')[0]
                            image_id = int(image_id)
                            downloaded.add(image_id)

    return downloaded



def dynamic_sleep(minimum = 0, maximum = 5):
    """
    sleep dynamic duration
    """
    time.sleep(random.randint(minimum, maximum))

    return None
