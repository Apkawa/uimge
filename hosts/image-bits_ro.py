# -*- coding: utf-8 -*-
from base_host import *
class Host(BaseHost):
    short_key = 'ir'
    long_key  = 'imagebits'
    host='image-bits.ro'
    action = 'http://%s/'%host
    form = {
            'title':'uimge',
            'submit.x':'51',
            'submit.y':'9',
            'submit':'About submit buttons',
            }

    def as_file(self, _file):
        return {'__upload': _file }
    #def thumb_size(self, _thumb_size):
    #    return { 'thumb_size': _thumb_size, }
    def postload(self ):
        _src = self.get_src()
        _regx = r'src="thumb.php\?file=uploads/(.*?)" id="thumb"'
        _url = findall(_regx ,_src)[0]
        self.img_url = 'http://image-bits.ro/uploads/%s'%_url
        self.img_thumb_url = 'http://image-bits.ro/thumb.php?file=uploads/%s'%_url


if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
