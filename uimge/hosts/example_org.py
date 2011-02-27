# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    dev_mode = True

    short_key = 'ex'
    long_key = 'example'
    host='example.org'
    max_file_size = 5*(1024*1024) #5Mb

    action = 'http://%s/upload'%host

    #headers = {}
    #cookie = ''
    #user_agent = "string"

    form = {
            'Submit': '',
            }

    def as_file(self, _file):
        return {
                'image': _file,
                }

    def as_url(self, _url):
        return {
                'url': _url,
                }

    def postload(self):
        _src = self.response.body
        _regx = r'example'
        _url = self.findall(_regx ,_src)[0]
        self.img_url = '%s'%_url
        self.img_thumb_url = '%s'%_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
