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
# html.cookie
import http.cookiejar
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
            '\x1B[38;5;5m[Wallhaven] Execute wallhaven downloader\x1B[0m')

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
    downloaded = utils.get_downloaded_images('wallhaven')

    # TODO(LuHa): load tags
    if os.path.exists('tags.secret'):
        with open('tags.secret', 'r') as f_tags:
            tags = json.load(f_tags)
            tags = tags['wallhaven']
    else:
        utils.logger.error('[Wallhaven] Need tags in file named tags.secret')
        return

    # TODO(LuHa): load API keys
    if os.path.exists('wallhaven_api.secret'):
        print('[Wallhaven] API key exists')
        with open('wallhaven_api.secret', 'r') as f_api:
            api_key = json.load(f_api)
            user_id = api_key['id'].strip()
            user_passwd = api_key['passwd'].strip()
    else:
        print('[Wallhaven] Need User id and passwd file '
            + 'named wallhaven_api.secret')
        print('[Wallhaven] The format is below')
        print('{')
        print('    "id": "ID",')
        print('    "passwd": "PASSWD"')
        print('}')
        return

    # TODO(LuHa): load cookie from file
    cookie_jar = http.cookiejar.LWPCookieJar('wallhaven_cookie.secret')
    if os.path.exists('wallhaven_cookie.secret'):
        cookie_jar.load()
    cookie = urllib.request.HTTPCookieProcessor(cookie_jar)

    # TODO(LuHa): create opener
    opener = urllib.request.build_opener(cookie)
    opener.addheaders = [('User-agent', 'Mozilla/5.0'),
                         ('Accept', 'text/html')]

    # TODO(LuHa): check logined or not logined
    request_url = 'https://alpha.wallhaven.cc/auth/login'
    response = opener.open(request_url, timeout = TIMEOUT)
    login_parser = LoginParser()
    try:
        login_parser.feed(response.read().decode('utf-8'))
    except socket.timeout:
        print('\x1B[38;5;5m[Wallhaven] Response timeout\x1B[0m')
        return

    # TODO(LuHa): if the cookie is not login, login with cookie
    try:
        if login_parser.get_logined() == False:
            request_url = 'https://alpha.wallhaven.cc/auth/login'
            auth = {'username': user_id,
                    'password': user_passwd}
            auth = urllib.parse.urlencode(auth)
            auth = auth.encode('ascii')
            opener.open(request_url, data = auth)
    
        # TODO(LuHa): loop search by tags
        base_url = 'https://alpha.wallhaven.cc/search'
        max_page_parser = MaxPageParser()
        id_parser = ImageIdParser()
        uri_parser = ImageURIParser()
        # for fun
        random.shuffle(tags)
        for tag in tags:
            base_url = 'https://alpha.wallhaven.cc/search'
            max_page_parser.clear_data()
            id_parser.clear_ids()
            uri_parser.clear_uris()
    
            # TODO(LuHa): get max page
            opener.addheaders = [('User-agent', 'Mozilla/5.0'),
                                 ('Accept', 'text/html')]
            request_url = base_url + tag
            print('\x1B[38;5;5m[Wallhaven] Request: {0}\x1B[0m'.format(request_url))
            response = opener.open(request_url, timeout = TIMEOUT)
            try:
                max_page_parser.feed(response.read().decode('utf-8'))
            except socket.timeout:
                print('\x1B[38;5;5m[Wallhaven] Response timeout\x1B[0m')
                return
            max_page = max_page_parser.get_data()
            max_page = max_page.split()
            if len(max_page) > 3:
                max_page = int(max_page[3])
            else:
                max_page = 1
    
            # TODO(LuHa): get image id
            random_page = random.randint(1, max_page)
            random_page = '&page=' + str(random_page)
            request_url = base_url + tag + random_page
            response = opener.open(request_url, timeout = TIMEOUT)
            try:
                id_parser.feed(response.read().decode('utf-8'))
            except socket.timeout:
                print('\x1B[38;5;5m[Wallhaven] Response timeout\x1B[0m')
                return
    
            # TODO(LuHa): loop parse image path
            # get 24 images at one time in wallhaven
            print('[Wallhaven] Search image path')
            for image_id in id_parser.get_ids():
                # skip target image is already downloaded
                if image_id in downloaded:
                    print('[Wallhaven] Already downloaded {0}'.format(image_id))
                    continue
                elif image_id in ban_db['wallhaven']:
                    print('[Wallhaven] Ban downloaded {0}'.format(image_id))
                    continue
                elif image_id in mute_db['wallhaven']:
                    print('[Wallhaven] Mute downloaded {0}'.format(image_id))
                    continue
                else:
                    downloaded.add(image_id)
    
                base_url = 'https://alpha.wallhaven.cc/'
                request_url = (base_url
                             + 'wallpaper/'
                             + image_id)
                response = opener.open(request_url, timeout = TIMEOUT)
                try:
                    uri_parser.feed(response.read().decode('utf-8'))
                except socket.timeout:
                    print('\x1B[38;5;5m[Wallhaven] Response timeout\x1B[0m')
                    return
                # sleep for prevent blocking
                utils.dynamic_sleep()
    
            # TODO(LuHa): loop download by posts
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            for image_uri in uri_parser.get_uris():
                request_url = ('https:'
                             + image_uri)
                response = opener.open(request_url, timeout = TIMEOUT)
                image_path = ('./downloads/'
                            + image_uri.split('/')[-1])
                with open(image_path, 'wb') as f:
                    try:
                        f.write(response.read())
                    except socket.timeout:
                        print('\x1B[38;5;5m[Wallhaven] Response timeout\x1B[0m')
                        return
                print('[Wallhaven] Downloaded {0}'.format(image_path))
                # sleep for prevent blocking
                utils.dynamic_sleep()

    except KeyboardInterrupt:
        print('[Wallhaven] keyboard Interrupt')
    except Exception as e:
        print('[Wallhaven] Some Interrupt', e)
    
    # TODO(LuHa): save cookie
    cookie_jar.save()

    # TODO(Luha): print message about program termination
    utils.logger.info(
            '\x1B[38;5;5m[Wallhaven] Terminate wallhaven downloader\x1B[0m')



class LoginParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.username = False
        self.password = False

    def handle_starttag(self, tag, attrs):
        if tag != 'input':
            return
        if len(attrs) < 1:
            return
        if (('id', 'username') == attrs[0]):
            self.username = True
        if (('id', 'password') == attrs[0]):
            self.password = True

    def get_logined(self):
        return (self.username) and (self.password)

    def clear_logined(self):
        self.username = False
        self.password = False


class MaxPageParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.in_header_tag = False
        self.in_h2_tag = False
        self.data = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'header':
            self.in_header_tag = True
        elif tag == 'h2':
            self.in_h2_tag = True

    def handle_endtag(self, tag):
        if tag == 'header':
            self.in_header_tag = False
        elif tag == 'h2':
            self.in_h2_tag = False
            self.data = self.data + '\n'

    def handle_data(self, data):
        if self.in_header_tag and self.in_h2_tag:
            self.data = self.data + data

    def get_data(self):
        return self.data

    def clear_data(self):
        self.in_header_tag = False
        self.in_h2_tag = False
        self.data = ''



class ImageIdParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.ids = list()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if ('class', 'preview') == attrs[0]:
                image_id = attrs[1][1]
                image_id = image_id.split('/')[-1]
                self.ids.append(image_id)

    def get_ids(self):
        return self.ids

    def clear_ids(self):
        self.ids.clear()



class ImageURIParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.uris = list()

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            if ('id', 'wallpaper') == attrs[0]:
                image_uri = attrs[1][1]
                self.uris.append(image_uri)

    def get_uris(self):
        return self.uris

    def clear_uris(self):
        self.uris.clear()


if __name__ == '__main__':
    # Check the python version is 3
    if sys.version_info.major != 3:
        print('[Wallhaven] Need python3')
        sys.exit()
    
    # Argument parse
    import argparse
    parser = argparse.ArgumentParser()
    
    parser.add_arguments('-q', '--query', type=str,
                         required=True,
                         help='Search keyword')
    parser.add_arguments('-p', '--purity', type=int,
                         default=6,
                         help='The purity of images for downloading')
    parser.add_arguments('-n' '--nums', type=int,
                         default=24,
                         help='The number of images for downloading')


                         

    # Excute main
    main()

