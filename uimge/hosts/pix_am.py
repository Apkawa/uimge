# -*- coding: utf-8 -*-
import base
import json
import os

class Host(base.BaseHost):
    dev_mode = False

    short_key = 'pa'
    long_key = 'pixam'
    host='pix.am'
    max_file_size = 5*(1024*1024) #5Mb

    action = 'http://%s/upload/'%host

    #headers = {}
    #cookie = ''
    #user_agent = "string"

    form = {
            }

    def as_file(self, _file):
        self.action = 'http://%s/upload/'%self.host
        return {
                'image': _file,
                }

    def as_url(self, _url):
        self.action = 'http://%s/upload/url/'%self.host
        return {
                'url': _url,
                }

    def postload(self):
        src = self.response.body
        try:
            key = json.loads(src)['key']
        except ValueError:
            key = self.findall(r'key:"([\w]+)"', src)[0]
        ext = os.path.splitext(self.filename)[1]
        self.img_url = 'http://pix.am/%s%s'%(key, ext)
        self.img_thumb_url = 'http://pix.am/%ss%s'%(key, ext)

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
