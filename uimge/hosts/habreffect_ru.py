# -*- coding: utf-8 -*-
import base
from urlparse import urlsplit
import urllib

class Host( base.BaseHost ):
    dev_mode = True

    short_key = 'hr'
    long_key = 'habreffect'
    host='habreffect.ru'
    max_file_size = 5*(1024*1024) #5Mb

    action = 'http://%s/upload.php'%host
    form = {
            'Submit': '',
            }

    def as_file(self, _file):
        return {
                'file': _file,
                }
    def preload(self):
        cookie = urllib.urlopen('http://%s'%self.host).headers['set-cookie']
        self.cookie = cookie

    def postload(self):
        uri_path = urlsplit(self.response.url).path
        self.img_url = 'http://habreffect.ru/files%s'%uri_path
        self.img_thumb_url = self.img_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h= Host()
    h.test_url()
