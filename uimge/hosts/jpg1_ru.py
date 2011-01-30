# -*- coding: utf-8 -*-
import base
class Host( base.BaseHost ):
    short_key = 'j1'
    long_key = 'jpg1'
    host='jpg1.ru'

    action = 'http://%s/upload/'%host

    def as_file(self, _file):
        return {
                'imgfile': _file,
                }

    def postload(self ):
        _src = self.response.body
        print _src
        _url = self.findall("\[img=(.*?)\]\[" ,_src)[0]
        self.img_url = '%s'%_url
        self.img_thumb_url = '%s_th.jpg'%_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
