# -*- coding: utf-8 -*-
from base_host import *
class Host( BaseHost ):
    dev_mode = False

    short_key = 'ps'
    long_key = 'pictureshack'
    host='pictureshack.ru'
    max_file_size = 11*(1024*1024) #5Mb

    action = 'http://www.%s/index2.php'%host
    form = {
            'thumbsize':'small',
            'Upload': 'залить картинку',
            }

    def as_file(self, _file):
        return {'userfile': _file }
    def postload(self ):
        _src = self.get_src()
        _regx = r'\[IMG\]http://www.pictureshack\.ru/images/(.*?)\[/IMG\]'
        _url = self.findall(_regx ,_src)[0]
        self.img_url = 'http://www.pictureshack.ru/images/%s'%_url
        self.img_thumb_url = 'http://www.pictureshack.ru/thumbs/%s'%_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
