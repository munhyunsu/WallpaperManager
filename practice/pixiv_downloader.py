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
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    # TODO(LuHa) get login hidden value
    hidden_parser = LoginTagParser()
    base_url = 'https://accounts.pixiv.net/login'
    response = opener.open(base_url)
    hidden_parser.feed(response.read().decode('utf-8'))
    auth = hidden_parser.get_hidden()

    # TODO(LuHa): login
    auth['pixiv_id'] = user_id
    auth['password'] = user_passwd
    auth = urllib.parse.urlencode(auth)
    auth = auth.encode('ascii')
    response = opener.open(base_url, data = auth)

    # TODO(LuHa): query to daily rank
    base_url = 'https://www.pixiv.net/ranking.php?mode=daily'
    response = opener.open(base_url)
    html_save(response)

    # TODO(LuHa): print message about program termination
    print('\x1B[38;5;5m[Pixiv] Terminate pixiv downloader\x1B[0m')



class LoginTagParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.hidden = dict()

    def handle_starttag(self, tag, attrs):
        if tag != 'input':
            return
        if ('type', 'hidden') != attrs[0]:
            return
        if 'name' == attrs[1][0]:
            self.hidden[attrs[1][1]] = attrs[2][1]

    def get_hidden(self):
        return self.hidden

    def clear_hidden(self):
        self.hidden.clear()



def html_save(response):
    with open('temp.html', 'w') as f:
        f.write(response.read().decode('utf-8'))
    



# Maybe it is good, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[Pixiv] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
