# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    dev_mode = True
    short_key ='s'
    long_key = 'smages'
    host='smages.com'
    action = 'http://smages.com/upload'
    form = {'Submit': ''}

    def as_file(self, _file):
        return {'img': _file }
    def postload(self ):
        __url = self.response.url.split('/')[-3:]
        self.img_url = 'http://smages.com/i/%s/%s/%s'%(__url[0], __url[1], __url[2][:-4] )
        self.img_thumb_url = 'http://smages.com/t/%s/%s/%s.jpg'%(__url[0], __url[1],
                __url[2].split('.')[0] )

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
