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
# cookie
import http.cookiejar
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
    cookie_jar = http.cookiejar.LWPCookieJar('pixiv_cookie.secret')
    if os.path.exists('pixiv_cookie.secret'):
        cookie_jar.load()
    cookie = urllib.request.HTTPCookieProcessor(cookie_jar)

    # TODO(LuHa): create opener
    opener = urllib.request.build_opener(cookie)
    opener.addheaders = [('User-agent', 'Mozilla/5.0'),
                         ('Accept', 'text/html')]

    # TODO(LuHa) get hidden value for login
    hidden_parser = LoginTagParser()
    base_url = 'https://accounts.pixiv.net/'
    page_url = 'login'
    request_url = base_url + page_url
    response = opener.open(request_url, timeout = 60)
    try:
        hidden_parser.feed(response.read().decode('utf-8'))
    except socket.timeout:
        print('\x1B[38;5;5m[Pixiv] Response timeout\x1B[0m')
        return
    auth = hidden_parser.get_hidden()

    # TODO(LuHa): if the cookie is not login, login with cookie
    try:
        if 'post_key' in auth.keys():
            auth['pixiv_id'] = user_id
            auth['password'] = user_passwd
            auth = urllib.parse.urlencode(auth)
            auth = auth.encode('ascii')
            opener.open(request_url, data = auth, timeout = 60)
    
        # TODO(LuHa): query to daily rank
        # rank start url:
        #    https://www.pixiv.net/ranking.php?mode=daily&date=20070913
        for tag in tags:
            base_url = 'https://www.pixiv.net/'
            page_url = 'ranking.php' + tag
            request_url = base_url + page_url
            if tag.endswith('date='):
                request_url = request_url + get_random_date()
            response = opener.open(request_url, timeout = 60)
    
            # TODO(LuHa): get page uri
            image_page_parser = ImagePageParser()
            try:
                image_page_parser.feed(response.read().decode('utf-8'))
            except socket.timeout:
                print('\x1B[38;5;5m[Pixiv] Response timeout\x1B[0m')
                return
    
            # TODO(LuHa): get image uri, but remain multiple page
            image_url_parser = ImageURLParser()
            for image_page in image_page_parser.get_pages():
                request_url = base_url + image_page
                response = opener.open(request_url, timeout = 60)
                try:
                    image_url_parser.feed(response.read().decode('utf-8'))
                except socket.timeout:
                    print('\x1B[38;5;5m[Pixiv] Response timeout\x1B[0m')
                    return
                #print('[P] image url ready {0}'.format(len(image_url_parser.get_urls())))
            print('[Pixiv] Get ranking page')
    
            # TODO(LuHa): get multiple image uri
            image_urls = image_url_parser.get_urls() 
            multi_page_parser = MultiPageParser()
            multi_url_parser = MultiURLParser()
            final_urls = list()
            for image_url in image_urls:
                #print('[P] final URL ready {0}'.format(len(final_urls)))
                if image_url.startswith('https://'):
                    final_urls.append(image_url)
                    continue
                multi_url_parser.clear_urls()
                multi_page_parser.clear_pages()
                request_url = 'https://www.pixiv.net/' + image_url
                response = opener.open(request_url, timeout = 60)
                try:
                    multi_page_parser.feed(response.read().decode('utf-8'))
                except socket.timeout:
                    print('\x1B[38;5;5m[Pixiv] Response timeout\x1B[0m')
                    return
                for multi_page in multi_page_parser.get_pages():
                    request_url = 'https://www.pixiv.net' + multi_page
                    response = opener.open(request_url, timeout = 60)
                    try:
                        multi_url_parser.feed(response.read().decode('utf-8'))
                    except socket.timeout:
                        print('\x1B[38;5;5m[Pixiv] Response timeout\x1B[0m')
                        return
                final_urls.extend(multi_url_parser.get_urls())
            print('[Pixiv] Get URLs of all images in ranking')
    
            # TODO(LuHa): download image
            for image_url in final_urls:
                image_id = image_url.split('/')[-1]
                if image_id in downloaded:
                    print('[Pixiv] Already downloaded {0}'.format(image_id))
                    continue
                elif image_id in ban_db['pixiv']:
                    print('[Pixiv] Ban downloaded {0}'.format(image_id))
                    continue
                elif image_id in mute_db['pixiv']:
                    print('[Pixiv] Mute downloaded {0}'.format(image_id))
                    continue
                else:
                    downloaded.add(image_id)
                file_name = ('./downloads'
                           + '/pixiv-'
                           + image_url.split('/')[-1])
                with open(file_name, 'wb') as f:
                    referer = 'https://www.pixiv.net/member_illust.php'
                    referer = referer + '?mode=medium&illust_id='
                    referer = referer + file_name.split('_')[0]
                    opener.addheaders = [('User-agent', 'Mozilla/5.0'),
                                         ('Referer', referer)]
                    response = opener.open(image_url, timeout = 60)
                    try:
                        f.write(response.read())
                    except socket.timeout:
                        print('\x1B[38;5;5m[Pixiv] Response timeout\x1B[0m')
                        return
                print('[Pixiv] Downloaded {0}'.format(file_name))
                # sleep for prevent blocking
                utils.dynamic_sleep()

    except KeyboardInterrupt:
        print('[Pixiv] Keyboard Interrupt')
    except:
        print('[Pixiv] Some Interrupt')

    # TODO(LuHa): save cookie to file
    cookie_jar.save()

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



class ImagePageParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.pages = list()

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        if len(attrs) < 2:
            return
        if ('class', 'title') != attrs[1]:
            return
        self.pages.append(attrs[0][1])

    def get_pages(self):
        return self.pages

    def clear_pages(self):
        self.pages.clear()



class ImageURLParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.urls = list()

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            if len(attrs) < 5:
                return
            if ('class', 'original-image') == attrs[4]:
                self.urls.append(attrs[3][1])
        if tag == 'a':
            if len(attrs) < 3:
                return
            if 'class' != attrs[2][0]:
                return
            if 'multiple' in attrs[2][1]:
                self.urls.append(attrs[0][1])

    def get_urls(self):
        return self.urls

    def clear_urls(self):
        self.urls.clear()



class MultiPageParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.pages = list()

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        if len(attrs) < 3:
            return
        if 'class' != attrs[2][0]:
            return
        if 'full-size-container' in attrs[2][1]:
            self.pages.append(attrs[0][1])

    def get_pages(self):
        return self.pages

    def clear_pages(self):
        self.pages.clear()



class MultiURLParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.urls = list()

    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        if len(attrs) < 2:
            return
        if 'src' != attrs[0][0]:
            return
        self.urls.append(attrs[0][1])

    def get_urls(self):
        return self.urls

    def clear_urls(self):
        self.urls.clear()



def get_random_date():
    max_days = datetime.date.fromtimestamp(time.time())
    max_days = max_days - datetime.date(2007, 9, 13)
    max_days = max_days.days

    random_day = random.randint(0, max_days)
    random_day = datetime.timedelta(days = random_day)
    target_day = datetime.date(2007, 9, 13) + random_day
    
    return target_day.strftime('%Y%m%d')


# Maybe it is good, right?
if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('[Pixiv] Need python3')
        sys.exit()
    sys.exit(main(sys.argv))
