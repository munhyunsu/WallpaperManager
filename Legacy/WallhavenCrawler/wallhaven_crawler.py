#!/usr/bin/env python3

username = 'munhyunsu'
passwd = '32323674'
headers = {'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) '
                        + 'AppleWebKit/537.36 (KHTML, like Gecko) '
                        + 'Chrome/57.0.2987.110 Safari/537.36')}
























import urllib.request
import base64
from bs4 import BeautifulSoup


request = urllib.request.Request('https://alpha.wallhaven.cc/', 
                                 headers = headers)
response = urllib.request.urlopen(request)
#response = urllib.request.urlopen('https://alpha.wallhaven.cc/')
soup = BeautifulSoup(response.read(), 'lxml')
soup_token = soup.find('input', {'name':'_token'})
token = soup_token.attrs['value']

data = {'username': username, 'passwd': passwd, '_token': token}
data_ascii = repr(data).encode('ascii')
headers['Referer'] = 'https://alpha.wallhaven.cc/'
request = urllib.request.Request('https://alpha.wallhaven.cc/auth/login',
                                 headers = headers,
                                 data = data_ascii)
response = urllib.request.urlopen(request)
print(response.getheaders())
#soup = BeautifulSoup(response.read(), 'lxml')
#print(soup)

#
#
#data = {'username': username, 'passwd': passwd}
#data_ascii = repr(data).encode('ascii')
#
#
#
#response = urllib.request.urlopen('https://alpha.wallhaven.cc/auth/login', 
#                                 data = data64)
#
#print(response)
