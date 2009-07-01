# -*- coding: utf-8 -*-
from base_host import test_host, findall
@test_host(__name__)
class Host_up_upimg:
    host='upimg.ru'
    action = 'http://upimg.ru/u/'
    form = {'Submit': 'Загрузить'}


    def as_file(self, _file):
        return {'img': _file }
    def postload(self ):
        __url = findall('value=\"http://upimg.ru/i/(.*?)\"', self.get_src() )
        self.img_url = 'http://upimg.ru/i/%s'%(__url[0])
        self.img_thumb_url = 'http://upimg.ru/p/%s'%__url[0]

