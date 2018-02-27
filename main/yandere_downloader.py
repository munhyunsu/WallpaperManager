#!/usr/bin/env python3

# exit, argv
import sys
# json
import json
# exists, makedirs, path
import os
# b64encode
import base64
# openner
import urllib.request
# timeout
import socket
# shuffle
import random

# utils
import utils
# global variable
from global_variable import TIMEOUT

def main(argv):
    """
    main flow
    """
    # TODO(LuHa): print message about program execution
    utils.logger.info(
            '\x1B[38;5;5m[Yandere] Execute yandere downloader\x1B[0m')

    # TODO(LuHa): create downloads directory
    # actually, this code use only downloads directory.
    # but to ensure execution of source code,
    #   make save directory.
    os.makedirs('./downloads', exist_ok = True)
    os.makedirs('./save', exist_ok = True)

    # TODO(LuHa): load ban database
    ban_db = utils.get_database('ban.secret')
    
    # TODO(LuHa): load mute database
    mute_db = utils.get_database('mute.secret')

    # TODO(LuHa): read pre-downloaded image
    downloaded = utils.get_downloaded_images('yandere')

    # TODO(LuHa): load tags
    if os.path.exists('tags.secret'):
        with open('tags.secret', 'r') as f_tags:
            tags = json.load(f_tags)
            tags = tags['yandere']
    else:
        utils.logger.error('[Yandere] Need tags in file named tags.secret')
        return

    # TODO(LuHa): load API keys
    if os.path.exists('yandere_api.secret'):
        print('[Yandere] API key exists')
        with open('yandere_api.secret', 'r') as f_api:
            api_key = f_api.read()
            api_key = api_key.strip()
    else:
        print('[Yandere] Need API key in file named yandere_api.secret')
        print('[Yandere] The format is ID:APIKEY')
        return

    # TODO(LuHa): create opener
    auth = api_key
    auth = auth.encode('ascii')
    auth = base64.b64encode(auth)
    auth = auth.decode('utf-8')
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'Basic ' + auth)]

    # TODO(LuHa): loop search by tags
    base_url = 'https://yande.re'
    # for fun
    random.shuffle(tags)
    for tag in tags:
        request_url = (base_url
                     + '/post.json?tags='
                     + tag
                     + '+order:random')
        print('\x1B[38;5;5m[Yandere] Request: {0}\x1B[0m'.format(request_url))
        response = opener.open(request_url, timeout = TIMEOUT)
        try:
            posts = json.loads(response.read().decode('utf-8'))
        except socket.timeout:
            print('\x1B[38;5;5m[Yandere] Response timeout\x1B[0m')
            return

        # TODO(LuHa): loop download by posts
        # get 40 images at one time in yandere
        for post in posts:
            # skip target image is already downloaded
            if post['id'] in downloaded:
                print('[Yandere] Already downloaded {0}'.format(post['id']))
                continue
            elif post['id'] in ban_db['yandere']:
                print('[Yandere] Ban downloaded {0}'.format(post['id']))
                continue
            elif post['id'] in mute_db['yandere']:
                print('[Yandere] Mute downloaded {0}'.format(post['id']))
                continue
            else:
                downloaded.add(post['id'])

            request_url = post['file_url']
            try:
                response = opener.open(request_url, timeout = TIMEOUT)
            except socket.timeout:
                print('[Yandere] Request timeout')
                return
            image_path = ('./downloads'
                        + '/yandere-'
                        + str(post['id'])
                        + '.'
                        + post['file_ext'])
            with open(image_path, 'wb') as f:
                try:
                    f.write(response.read())
                except socket.timeout:
                    print('\x1B[38;5;5m[Yandere] Response timeout\x1B[0m')
                    return
            print('[Yandere] Downloaded {0}'.format(image_path))
            # sleep for prevent block
            utils.dynamic_sleep()

    # TODO(LuHa): print message about program terminaion
    utils.logger.info(
            '\x1B[38;5;5m[Yandere] Terminate yandere downloader\x1B[0m')


# Maybe it is good, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[Yandere] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
