#!/usr/bin/env python3

# version_info
import sys
# scandir
import os
# sleep
import time
# randint
import random
# json
import json
# subprocess
import subprocess
# logging
import logging

# global variable
from global_variable import IMAGESOURCES



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
                        downloaded.add(image_id)
    else:
        for path in paths:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file():
                        if (entry.name).startswith(source):
                            image_id = (entry.name).split('-')[1]
                            image_id = (image_id).split('.')[0]
                            downloaded.add(image_id)

    return downloaded



def dynamic_sleep(minimum = 0, maximum = 5):
    """
    sleep dynamic duration
    """
    time.sleep(random.randint(minimum, maximum))

    return None



# TODO(LuHa): the function to load database
def get_database(db_name, across = False):
    """
    read database
    if across is True, it do not divide by image source.
    """
    # global variable
    sources = IMAGESOURCES

    # initialize
    database = dict()
    if across == False:
        for source in sources:
            database[source] = set()

    # load database
    if os.path.exists(db_name):
        with open(db_name, 'r') as f_database:
            database = json.load(f_database)
            if across == False:
                for source in sources:
                    database[source] = set(database.get(source, list()))

    # return
    return database



# TODO(LuHa): the function to save database
def set_database(db_name, db_object, across = False):
    """
    write database
    if across is True, it do not divide by image source.
    """
    # global variable
    sources = IMAGESOURCES

    # initialize
    if across == False:
        db_target = dict()
        for source in sources:
            db_target[source] = list(db_object[source])
            db_target[source].sort()
    else:
        db_target = db_object

    # save database
    with open(db_name, 'w') as f_database:
        json.dump(db_target,
                  f_database,
                  indent = 4,
                  sort_keys = True)



def change_wallpaper(image_path):
    """
    change wallpaper
    for now, it change just Linux Mint Cinnamon
    """
    image_path = 'file://' + image_path
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



def delete_file_size0():
    """
    delete file size 0
    """
    # TODO(LuHa): delete file size 0
    counter = 0
    if sys.version_info.minor < 6:
        for entry in os.scandir('./downloads'):
            if entry.is_file():
                if os.path.getsize(os.path.abspath(entry.path)) == 0:
                    os.remove(os.path.abspath(entry.path))
                    counter = counter + 1
                    
    else:
        with os.scandir('./downloads') as it:
            for entry in it:
                if entry.is_file():
                    if os.path.getsize(os.path.abspath(entry.path)) == 0:
                        os.remove(os.path.abspath(entry.path))
                        counter = counter + 1
    return counter




# TODO(LuHa): This variable is shared across program.
options = get_database('options.secret', across = True)
# TODO(LuHa): set logger level
# CRITICAL 50
# ERROR 40
# WARNING 30
# INFO 20
# DEBUG 10
# NOTSET 0
logging.basicConfig(format = 
        '%(asctime)s:%(created)s:%(levelno)s:%(message)s',
                    level = logging.NOTSET)
logger = logging.getLogger('WM')
logger.propagate = False
file_handler = logging.FileHandler('wm.log')
file_handler.setLevel(logging.ERROR)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(options['log'])
logger.addHandler(file_handler)
logger.addHandler(console_handler)
