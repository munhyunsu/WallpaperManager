import sys
import json
import os
import urllib.parse
import urllib.request
import html.parser
import http.cookiejar
import socket
import random
import yaml
import configparser
import time
import random


FLAGS = None
_ = None
CFG = None
OPENER = None
JAR = None


def load_config():
    global CFG
    with open(FLAGS.config, 'r') as f:
        CFG = yaml.safe_load(f)


def get_images():
    global CFG
    global OPENER
    base_url = 'https://wallhaven.cc/api/v1/search'

    for params in CFG['wallhaven']['tags']:
        params_encoded = urllib.parse.urlencode(params)
        url = f'{base_url}?{params_encoded}'
        response = OPENER.open(url)
        jdata = json.loads(response.read().decode('utf-8'))
        for data in jdata['data']:
            yield data['path']


def download_images(url):
    global CFG
    global OPENER
    response = OPENER.open(url)
    opath = os.path.join(os.path.abspath(os.path.expanduser(CFG['output'])),
                         os.path.basename(response.url))

    with open(opath, 'wb') as f:
        f.write(response.read())


def before_job():
    global CFG
    global OPENER
    global JAR
    os.makedirs(os.path.abspath(os.path.expanduser(CFG['output'])),
                exist_ok=True)
    JAR = http.cookiejar.LWPCookieJar(CFG['wallhaven']['jar'])
    if os.path.exists(CFG['wallhaven']['jar']):
        JAR.load()
    cookie = urllib.request.HTTPCookieProcessor(JAR)
    OPENER = urllib.request.build_opener(cookie)
    OPENER.addheaders = [('X-API-Key', CFG['wallhaven']['api_key']),
                        ]


def after_job():
    global JAR
    JAR.save()


def do_job():
    for image_path in get_images():
        download_images(image_path)
        print(f'downloaded {image_path}')
        time.sleep(random.randint(0, 3))


def main():
    # Print Parameters
    print(f'Parsed: {FLAGS}')
    print(f'Unparsed: {_}')

    # Load configuration
    load_config()

    before_job()

    do_job()

    after_job()


if __name__ == '__main__':
    # Check the python version is 3
    if sys.version_info.major != 3:
        print('[Wallhaven] Need python3')
        sys.exit()
    
    # Argument parse
    import argparse
    parser = argparse.ArgumentParser()
 
    parser.add_argument('-c', '--config', type=str,
                        default='config.yaml',
                        help='The configuration file path')
    FLAGS, _ = parser.parse_known_args()

    # Preprocessing for some arguments
    FLAGS.config = os.path.abspath(os.path.expanduser(FLAGS.config))

    # Excute main
    main()

