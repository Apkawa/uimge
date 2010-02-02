# -*- coding: utf-8 -*-
import base

class Host(base.BaseHost):
    short_key = 'ig'
    long_key  = 'imgur'
    host='imgur.com'
    action = 'http://%s/api/upload'%host
    form = {
            'key': '31352728bc6f6031cc78a39037658cdb',
            }
	#31352728bc6f6031cc78a39037658cdb

    def as_file(self, _file):
        return { 'image': _file }
    def as_url(self, _url):
        return { 'image': _url }
    def postload(self ):
        _src = self.response.body
        __url = self.findall('<image_hash>(.*?)</image_hash>',  _src )[0]
        self.img_url = 'http://i.imgur.com/%s.png'%__url
        self.img_thumb_url = 'http://i.imgur.com/%ss.jpg'%__url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
