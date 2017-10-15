#!/usr/bin/env python3

# exit
import sys
# json
import json
# exists
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
    os.makedirs('./downloads', exist_ok = True)

    # TODO(LuHa): load tags
    with open('tags.secret', 'r') as f_tags:
        tags = json.load(f_tags)
        tags = tags['danbooru']

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
        response = opener.open(request_url)
        posts = json.loads(response.read().decode('utf-8'))

        # TODO(LuHa): loop download by posts
        # get 20 images at one time in dandooru
        for post in posts:
            request_url = (base_url
                         + post['file_url'])
            response = opener.open(request_url)
            image_path = ('./downloads'
                        + '/danbooru-'
                        + str(post['id'])
                        + '.'
                        + post['file_ext'])
            image_file = open(image_path, 'wb')
            image_file.write(response.read())
            print('[Danbooru] Downloaded {0}'.format(image_path))
    
    # TODO(LuHa): print message about program terminaion
    print('[Danbooru] Terminate danbooru downloader')





if __name__ == '__main__':
    sys.exit(main(sys.argv))
