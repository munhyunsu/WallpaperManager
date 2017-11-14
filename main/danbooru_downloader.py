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

def main(argv):
    """
    main flow
    """
    # TODO(LuHa): print message about program execution
    print('\x1B[38;5;5m[Danbooru] Execute danbooru downloader\x1B[0m')

    # TODO(LuHa): create downloads directory
    # actually, this code use only downloads directory.
    # but to ensure execution of source code,
    #   make save directory.
    os.makedirs('./downloads', exist_ok = True)
    os.makedirs('./save', exist_ok = True)

    # TODO(LuHa): load ban database
    ban_db = utils.get_database('ban.secret')
#    if os.path.exists('ban.secret'):
#        with open('ban.secret', 'r') as f_ban:
#            ban_db = json.load(f_ban)
#            ban_db['danbooru'] = set(ban_db.get('danbooru', list()))
#    else:
#        ban_db = dict()
#        ban_db['danbooru'] = set()

    # TODO(LuHa): load mute database
    mute_db = utils.get_database('mute.secret')
#    if os.path.exists('mute.secret'):
#        with open('mute.secret', 'r') as f_mute:
#            mute_db = json.load(f_mute)
#            mute_db['danbooru'] = set(mute_db.get('danbooru', list()))
#    else:
#        mute_db = dict()
#        mute_db['danbooru'] = set()
    
    # TODO(LuHa): read pre-downloaded image
    downloaded = utils.get_downloaded_images('danbooru')

    # TODO(LuHa): load tags
    if os.path.exists('tags.secret'):
        with open('tags.secret', 'r') as f_tags:
            tags = json.load(f_tags)
            tags = tags['danbooru']
    else:
        print('[Danbooru] Need tags in file named tags.secret')
        return

    # TODO(LuHa): load API keys
    if os.path.exists('danbooru_api.secret'):
        print('[Danbooru] API key exists')
        with open('danbooru_api.secret', 'r') as f_api:
            api_key = f_api.read()
            api_key = api_key.strip()
    else:
        print('[Danbooru] Need API key in file named danbooru_api.secret')
        print('[Danbooru] The format is ID:APIKEY')
        return

    # TODO(LuHa): create opener
    auth = api_key
    auth = auth.encode('ascii')
    auth = base64.b64encode(auth)
    auth = auth.decode('utf-8')
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'Basic ' + auth)]

    # TODO(LuHa): loop search by tags
    base_url = 'https://danbooru.donmai.us'
    # for fun
    random.shuffle(tags)
    for tag in tags:
        request_url = (base_url
                     + '/posts.json?tags='
                     + tag
                     + '&random=true')
        response = opener.open(request_url, timeout = 60)
        try:
            posts = json.loads(response.read().decode('utf-8'))
        except socket.timeout:
            print('\x1B[38;5;5m[Danbooru] Response timeout\x1B[0m')
            return

        # TODO(LuHa): loop download by posts
        # get 20 images at one time in dandooru
        for post in posts:
            # skip target image is already downloaded
            if int(post['id']) in downloaded:
                print('[Danbooru] Already downloaded {0}'.format(post['id']))
                continue
            elif int(post['id']) in ban_db['danbooru']:
                print('[Danbooru] Ban downloaded {0}'.format(post['id']))
                continue
            elif int(post['id']) in mute_db['danbooru']:
                print('[Danbooru] Mute downloaded {0}'.format(post['id']))
                continue
            else:
                downloaded.add(int(post['id']))

            request_url = (base_url
                         + post['file_url'])
            try:
                response = opener.open(request_url, timeout = 60)
            except socket.timeout:
                print('[Danbooru] Request timeout')
                return
            image_path = ('./downloads'
                        + '/danbooru-'
                        + str(post['id'])
                        + '.'
                        + post['file_ext'])
            with open(image_path, 'wb') as f:
                try:
                    f.write(response.read())
                except socket.timeout:
                    print('\x1B[38;5;5m[Danbooru] Response timeout\x1B[0m')
                    return
            print('[Danbooru] Downloaded {0}'.format(image_path))
            # sleep for prevent block
            utils.dynamic_sleep()

    # TODO(LuHa): print message about program terminaion
    print('\x1B[38;5;5m[Danbooru] Terminate danbooru downloader\x1B[0m')


# Maybe it is good, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[Danbooru] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
