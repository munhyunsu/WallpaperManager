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
# pickle
import pickle

# utils
import utils

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
    os.makedirs('./downloads', exist_ok = True)
    os.makedirs('./save', exist_ok = True)

    # TODO(LuHa): load ban database
    ban_db = utils.get_database('ban.secret')

    # TODO(LuHa): load mute database
    mute_db = utils.get_database('mute.secret')

    # TODO(LuHa): read pre-downloaded image
    downloaded = utils.get_downloaded_images('pixiv')

    # TODO(LuHa): load tags
    if os.path.exists('tags.secret'):
        with open('tags.secret', 'r') as f_tags:
            tags = json.load(f_tags)
            tags = tags['pixiv']
    else:
        print('[Pixiv] Need tags in file named tags.secret')
        return

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

    # TODO(LuHa): load cookie from file
    if os.path.exists('pixiv_cookie.secret'):
        with open('pixiv_cookie.secret', 'rb') as f_cookie:
            cookie = pickle.load(f_cookie)
    else:
        cookie = urllib.request.HTTPCookieProcessor()

    # TODO(LuHa): create opener
    opener = urllib.request.build_opener(cookie)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    # TODO(LuHa) get hidden value for login
    hidden_parser = LoginTagParser()
    base_url = 'https://accounts.pixiv.net/'
    page_url = 'login'
    request_url = base_url + page_url
    response = opener.open(request_url)
    hidden_parser.feed(response.read().decode('utf-8'))
    auth = hidden_parser.get_hidden()

    # TODO(LuHa): if the cookie is not login, login with cookie
    if 'post_key' in auth.keys():
        auth['pixiv_id'] = user_id
        auth['password'] = user_passwd
        auth = urllib.parse.urlencode(auth)
        auth = auth.encode('ascii')
        opener.open(request_url, data = auth)

    # TODO(LuHa): query to daily rank
    base_url = 'https://www.pixiv.net/'
    page_url = 'ranking.php?mode=daily'
    request_url = base_url + page_url
    response = opener.open(request_url)

    # TODO(LuHa): get page uri
    id_parser = ImageIdParser()
    id_parser.feed(response.read().decode('utf-8'))
    page_url = id_parser.get_ids()[0]

    # TODO(LuHa): get image uri
    request_url = base_url + page_url
    response = opener.open(request_url)
    uri_parser = ImageURIParser()
    uri_parser.feed(response.read().decode('utf-8'))

    print(uri_parser.get_uris())
    
    file_name = uri_parser.get_uris()[0].split('/')[-1]
    with open(file_name, 'wb') as f:
        ref = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='
        ref = ref + file_name.split('_')[0]
        opener.addheaders = [('User-agent', 'Mozilla/5.0'),
                             ('Referer', ref)]
        response = opener.open(uri_parser.get_uris()[0])
        f.write(response.read())


    #save_html(response)



    # TODO(LuHa): save cookie to file
    with open('pixiv_cookie.secret', 'wb') as f_cookie:
        pickle.dump(cookie, f_cookie)

    # TODO(LuHa): print message about program termination
    print('\x1B[38;5;5m[Pixiv] Terminate pixiv downloader\x1B[0m')



class LoginTagParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.hidden = dict()

    def handle_starttag(self, tag, attrs):
        if tag != 'input':
            return
        if len(attrs) < 2:
            return
        if ('type', 'hidden') != attrs[0]:
            return
        if 'name' == attrs[1][0]:
            self.hidden[attrs[1][1]] = attrs[2][1]

    def get_hidden(self):
        return self.hidden

    def clear_hidden(self):
        self.hidden.clear()



class ImageIdParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.ids = list()

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        if len(attrs) < 2:
            return
        if ('class', 'title') != attrs[1]:
            return
        self.ids.append(attrs[0][1])

    def get_ids(self):
        return self.ids

    def clear_ids(self):
        self.ids.clear()



class ImageURIParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.uris = list()

    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        if len(attrs) < 4:
            return
        if ('class', 'original-image') != attrs[4]:
            return
        self.uris.append(attrs[3][1])

    def get_uris(self):
        return self.uris

    def clear_uris(self):
        self.uris.clear()



def save_html(response):
    result = response.read().decode('utf-8')
    with open('temp.html', 'w') as f:
        f.write(result)
    return result
    

def print_html(response):
    result = response.read().decode('utf-8')
    print(result)
    return result


# Maybe it is good, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[Pixiv] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
