import sys
import json
import os
import urllib.parse
import urllib.request
import html.parser
import http.cookiejar
import socket
import random
import configparser


FLAGS = None
_ = None


def get_cookiejar(jar_path):
    jar = http.cookiejar.LWPCookieJar(jar_path)
    if os.path.exists(jar_path):
        jar.load()
    return jar


def get_opener(jar, api_key):
    cookie = urllib.request.HTTPCookieProcessor(jar)
    opener = urllib.request.build_opener(cookie)
    ## If we needed, then add header to opener at here
    opener.addheaders = [('X-API-Key', api_key),
                        # ('User-agent', 'Mozilla/5.0'),
                        ]

    return opener


def read_config():
    config = configparser.ConfigParser()
    config.read(FLAGS.config)

    return config


def get_images(opener):
    # build request URI
    ## TODO(LuHa): Need parse Arguments
    request_url = 'https://wallhaven.cc/api/v1/search'
    params = {'categories': '010',
              'purity': '111',
              'sorting': 'random',
             }
    params_encoded = urllib.parse.urlencode(params)
    url = f'{request_url}?{params_encoded}'

    # send requests
    response = opener.open(url)
    bdata = response.read()

    # parse response
    jdata = json.loads(bdata.decode('utf-8'))

    for data in jdata['data']:
        yield data['path']


def download_images(opener, url):
    response = opener.open(url)
    bdata = response.read()
    opath = os.path.join(os.path.abspath(os.path.expanduser('./images')),
                         os.path.basename(response.url))

    with open(opath, 'wb') as f:
        f.write(bdata)

    return


def main():
    # Print Parameters
    print(f'Parsed: {FLAGS}')
    print(f'Unparsed: {_}')

    # Load configuration
    config = read_config()

    # make saved directory
    os.makedirs(os.path.abspath(os.path.expanduser('./images')),
                exist_ok=True)

    # Build opener
    jar = get_cookiejar(config['Wallhaven']['jar'])
    opener = get_opener(jar,
                        config['Wallhaven']['api_key'])

    for image_path in get_images(opener):
        print(image_path)
        download_images(opener, image_path)
        break

    # Terminate
    jar.save()


if __name__ == '__main__':
    # Check the python version is 3
    if sys.version_info.major != 3:
        print('[Wallhaven] Need python3')
        sys.exit()
    
    # Argument parse
    import argparse
    parser = argparse.ArgumentParser()
 
    parser.add_argument('-c', '--config', type=str,
                        default='config.ini',
                        help='The configuration file path')
    parser.add_argument('-q', '--query', type=str,
                        help='Search keyword')
    parser.add_argument('-p', '--purity', type=int,
                        default=6,
                        help='The purity of images for downloading')
    parser.add_argument('-n' '--nums', type=int,
                        default=24,
                        help='The number of images for downloading')
    FLAGS, _ = parser.parse_known_args()

    # Preprocessing for some arguments
    FLAGS.config = os.path.abspath(os.path.expanduser(FLAGS.config))

    # Excute main
    main()

