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


def main(argv):
    """
    main flow
    """
    # TODO(LuHa): print message about program execution
    print('[Wallhaven] Execute wallhaven downloader')

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
            ban_db['wallhaven'] = set(ban_db.get('wallhaven', list()))
    else:
        ban_db = dict()
        ban_db['wallhaven'] = set()

    # TODO(LuHa): read pre-downloaded image
    downloaded = set()
    if sys.version_info.minor < 6:
        for entry in os.scandir('./downloads'):
            if entry.is_file():
                if (entry.name).startswith('wallhaven'):
                    image_id = (entry.name).split('-')[1]
                    image_id = (image_id).split('.')[0]
                    image_id = int(image_id)
                    downloaded.add(image_id)
        for entry in os.scandir('./save'):
            if entry.is_file():
                if (entry.name).startswith('wallhaven'):
                    image_id = (entry.name).split('-')[1]
                    image_id = (image_id).split('.')[0]
                    image_id = int(image_id)
                    downloaded.add(image_id)
    else:
        with os.scandir('./downloads') as it:
            for entry in it:
                if entry.is_file():
                    if (entry.name).startswith('wallhaven'):
                        image_id = (entry.name).split('-')[1]
                        image_id = (image_id).split('.')[0]
                        image_id = int(image_id)
                        downloaded.add(image_id)
        with os.scandir('./save') as it:
            for entry in it:
                if entry.is_file():
                    if (entry.name).startswith('wallhaven'):
                        image_id = (entry.name).split('-')[1]
                        image_id = (image_id).split('.')[0]
                        image_id = int(image_id)
                        downloaded.add(image_id)

    # TODO(LuHa): load tags
    if os.path.exists('tags.secret'):
        with open('tags.secret', 'r') as f_tags:
            tags = json.load(f_tags)
            tags = tags['wallhaven']
    else:
        print('[Wallhaven] Need tags in file named tags.secret')
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

    # TODO(LuHa): create opener
    cookie = urllib.request.HTTPCookieProcessor()
    opener = urllib.request.build_opener(cookie)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    base_url = 'http://alpha.wallhaven.cc/auth/login'
    auth = {'username': user_id,
            'password': user_passwd}
    auth = urllib.parse.urlencode(auth)
    auth = auth.encode('ascii')
    opener.open(base_url, data = auth)

    # TODO(LuHa): loop search by tags
    base_url = 'https://alpha.wallhaven.cc'
    id_parser = ImageIdParser()
    uri_parser = ImageURIParser()
    for tag in tags:
        id_parser.clear_ids()
        uri_parser.clear_uris()

        request_url = (base_url
                     + '/search?q='
                     + tag
                     + '&categories=010&purity=111&sorting=random')
        try:
            response = opener.open(request_url, timeout = 60)
        except socket.timeout:
            print('[Wallhaven] Request timeout')
            return
        try:
            id_parser.feed(response.read().decode('utf-8'))
        except socket.timeout:
            print('[Wallhaven] Response timeout')
            return


        # TODO(LuHa): loop parse image path
        # get 24 images at one time in wallhaven
        print('[Wallhaven] Search image path')
        for image_id in id_parser.get_ids():
            # skip target image is already downloaded
            if int(image_id) in downloaded:
                print('[Wallhaven] Already downloaded {0}'.format(image_id))
                continue
            elif int(image_id) in ban_db['wallhaven']:
                print('[Wallhaven] Ban downloaded {0}'.format(image_id))
                continue
            else:
                downloaded.add(int(image_id))

            request_url = (base_url
                         + '/wallpaper/'
                         + image_id)
            try:
                response = opener.open(request_url, timeout = 60)
            except socket.timeout:
                print('[Wallhaven] Request timeout')
                return
            try:
                uri_parser.feed(response.read().decode('utf-8'))
            except socket.timeout:
                print('[Wallhaven] Response timeout')
                return

        # TODO(LuHa): loop download by posts
        for image_uri in uri_parser.get_uris():
            request_url = ('https:'
                         + image_uri)
            try:
                response = opener.open(request_url, timeout = 60)
            except socket.timeout:
                print('[Wallhaven] Request timeout')
                return
            image_path = ('./downloads/'
                        + image_uri.split('/')[-1])
            with open(image_path, 'wb') as f:
                try:
                    f.write(response.read())
                except socket.timeout:
                    print('[Wallhaven] Response timeout')
                    return
            print('[Wallhaven] Downloaded {0}'.format(image_path))

    # TODO(Luha): print message about program termination
    print('[Wallhaven] Terminate wallhaven downloader')


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



# Maybe it is good, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[Wallhaven] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
