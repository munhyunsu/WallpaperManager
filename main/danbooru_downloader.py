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

def main(argv):
    """
    main flow
    """
    # TODO(LuHa): print message about program execution
    print('[Danbooru] Execute danbooru downloader')

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
            ban_db['danbooru'] = set(ban_db['danbooru'])
    else:
        ban_db = dict()
        ban_db['danbooru'] = set()
    
    # TODO(LuHa): read pre-downloaded image
    downloaded = set()
    with os.scandir('./downloads') as it:
        for entry in it:
            if entry.is_file():
                if (entry.name).startswith('danbooru'):
                    image_id = (entry.name).split('-')[1]
                    image_id = (image_id).split('.')[0]
                    image_id = int(image_id)
                    downloaded.add(image_id)
    with os.scandir('./save') as it:
        for entry in it:
            if entry.is_file():
                if (entry.name).startswith('danbooru'):
                    image_id = (entry.name).split('-')[1]
                    image_id = (image_id).split('.')[0]
                    image_id = int(image_id)
                    downloaded.add(image_id)

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
    for tag in tags:
        request_url = (base_url
                     + '/posts.json?tags='
                     + tag
                     + '&random=true')
        try:
            response = opener.open(request_url, timeout = 60)
        except socket.timeout:
            print('[Danbooru] Request timeout')
            return
        posts = json.loads(response.read().decode('utf-8'))

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
                f.write(response.read())
            print('[Danbooru] Downloaded {0}'.format(image_path))

    # TODO(LuHa): print message about program terminaion
    print('[Danbooru] Terminate danbooru downloader')


# Maybe it is good, right?
if __name__ == '__main__':
    sys.exit(main(sys.argv))
