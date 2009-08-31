# -*- coding: utf-8 -*-
from base_host import *
class Host(BaseHost):
    dev_mode = True

    short_key = 'up'
    long_key  = 'upimg'
    host='upimg.ru'
    action = 'http://upimg.ru/u/'
    form = {'Submit': 'Загрузить'}


    def as_file(self, _file):
        return {'img': _file }
    def postload(self ):
        __url = findall('value=\"http://upimg.ru/i/(.*?)\"', self.get_src(True) )
        self.img_url = 'http://upimg.ru/i/%s'%(__url[0])
        self.img_thumb_url = 'http://upimg.ru/p/%s'%__url[0]




if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
