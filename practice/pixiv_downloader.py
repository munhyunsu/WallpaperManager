#!/usr/bin/env python3

# exit, argv
import sys
# json
import json
# exists, makedirs, path
import os
# urlencode
import urllib.parse
# openner
import urllib.request
# html.parser
import html.parser
# timeout
import socket
# shuffle
import random

# utils
#import utils

def main(argv):
    """
    main flow
    """
    # TODO(LuHa): print message about program execution
    print('\x1B[38;5;5m[Pixiv] Execute pixiv downloader\x1B[0m')

    # TODO(LuHa): create downloads directory
    # actually, this code use only downloads directory.
    # but to ensure execution of source code,
    #   make save directory.
#    os.makedirs('./downloads', exist_ok = True)
#    os.makedirs('./save', exist_ok = True)

    # TODO(LuHa): load ban database
#    ban_db = utils.get_database('ban.secret')

    # TODO(LuHa): load mute database
#    mute_db = utils.get_database('mute.secret')

    # TODO(LuHa): read pre-downloaded image
#    downloaded = utils.get_downloaded_images('pixiv')

    # TODO(LuHa): load tags
#    if os.path.exists('tags.secret'):
#        with open('tags.secret', 'r') as f_tags:
#            tags = json.load(f_tags)
#            tags = tags['pixiv']
#    else:
#        print('[Pixiv] Need tags in file named tags.secret')
#        return

    # TODO(LuHa): load API keys
    if os.path.exists('pixiv_api.secret'):
        print('[Pixiv] API key exists')
        with open('pixiv_api.secret', 'r') as f_api:
            api_key = json.load(f_api)
            user_id = api_key['id'].strip()
            user_passwd = api_key['passwd'].strip()
    else:
        print('[Pixiv] Need User ud and passwd file '
            + 'named pixiv_api.secret')
        print('[Pixiv] The format is below')
        print('{')
        print('    "id": "ID",')
        print('    "passwd": "PASSWD"')
        print('}')
        return

    # TODO(LuHa): create opener
    cookie = urllib.request.HTTPCookieProcessor()
    opener = urllib.request.build_opener(cookie)
    opener.addheaders = [('User-agent', 'Mozilla/5.0'), 
                         ('Referer', 'login.php?return_to=0')]
    base_url = 'https://accounts.pixiv.net/login'
    auth = {'pixiv_id': user_id,
            'password': user_passwd,
            'return_to': 'https://www.pixiv.net/',
            'post_key'}
    auth = urllib.parse.urlencode(auth)
    auth = auth.encode('ascii')
    opener.open(base_url, data = auth)

    print(opener)

    # TODO(LuHa): print message about program termination
    print('\x1B[38;5;5m[Pixiv] Terminate pixiv downloader\x1B[0m')



# Maybe it is good, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[Pixiv] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
