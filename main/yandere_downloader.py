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

# file util
import util_file

def main(argv):
    """
    main flow
    """
    # TODO(LuHa): print message about program execution
    print('[Yandere] Execute yandere downloader')

    # TODO(LuHa): create downloads directory
    # actually, this code use only downloads directory.
    # but to ensure execution of source code,
    #   make save directory.
    os.makedirs('./downloads', exist_ok = True)
    os.makedirs('./save', exist_ok = True)

    # TODO(LuHa): load image database
    if os.path.exists('ban.secret'):
        with open('ban.secret', 'r') as f_ban:
            ban_db = json.load(f_ban)
            ban_db['yandere'] = set(ban_db.get('yandere', list()))
    else:
        ban_db = dict()
        ban_db['yandere'] = set()
    
    # TODO(LuHa): read pre-downloaded image
    downloaded = util_file.get_downloaded_images('yandere')
#    downloaded = set()
#    if sys.version_info.minor < 6:
#        for entry in os.scandir('./downloads'):
#            if entry.is_file():
#                if (entry.name).startswith('yandere'):
#                    image_id = (entry.name).split('-')[1]
#                    image_id = (image_id).split('.')[0]
#                    image_id = int(image_id)
#                    downloaded.add(image_id)
#        for entry in os.scandir('./save'):
#            if entry.is_file():
#                if (entry.name).startswith('yandere'):
#                    image_id = (entry.name).split('-')[1]
#                    image_id = (image_id).split('.')[0]
#                    image_id = int(image_id)
#                    downloaded.add(image_id)
#    else:            
#        with os.scandir('./downloads') as it:
#            for entry in it:
#                if entry.is_file():
#                    if (entry.name).startswith('yandere'):
#                        image_id = (entry.name).split('-')[1]
#                        image_id = (image_id).split('.')[0]
#                        image_id = int(image_id)
#                        downloaded.add(image_id)
#        with os.scandir('./save') as it:
#            for entry in it:
#                if entry.is_file():
#                    if (entry.name).startswith('yandere'):
#                        image_id = (entry.name).split('-')[1]
#                        image_id = (image_id).split('.')[0]
#                        image_id = int(image_id)
#                        downloaded.add(image_id)

    # TODO(LuHa): load tags
    if os.path.exists('tags.secret'):
        with open('tags.secret', 'r') as f_tags:
            tags = json.load(f_tags)
            tags = tags['yandere']
    else:
        print('[Yandere] Need tags in file named tags.secret')
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
    for tag in tags:
        request_url = (base_url
                     + '/post.json?tags='
                     + tag
                     + '+order:random')
        try:
            response = opener.open(request_url, timeout = 60)
        except socket.timeout:
            print('[Yandere] Request timeout')
            return
        try:
            posts = json.loads(response.read().decode('utf-8'))
        except socket.timeout:
            print('[Yandere] Response timeout')
            return

        # TODO(LuHa): loop download by posts
        # get 40 images at one time in yandere
        for post in posts:
            # skip target image is already downloaded
            if int(post['id']) in downloaded:
                print('[Yandere] Already downloaded {0}'.format(post['id']))
                continue
            elif int(post['id']) in ban_db['yandere']:
                print('[Yandere] Ban downloaded {0}'.format(post['id']))
                continue
            else:
                downloaded.add(int(post['id']))

            request_url = post['file_url']
            try:
                response = opener.open(request_url, timeout = 60)
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
                    print('[Yandere] Response timeout')
                    return
            print('[Yandere] Downloaded {0}'.format(image_path))

    # TODO(LuHa): print message about program terminaion
    print('[Yandere] Terminate yandere downloader')


# Maybe it is good, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[Yandere] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
