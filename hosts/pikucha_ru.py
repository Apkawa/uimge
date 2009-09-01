# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    max_file_size = 10485760
    short_key = 'pu'
    long_key  = 'pikucha'
    host='pikucha.ru'
    action = 'http://pikucha.ru/upload'

    form = {
            'MAX_FILE_SIZE':'10485760',
            'description':'on',
            'description_value':'uimge',
            'upload':'',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'image': _file }
    def postload(self ):
        _src = self.get_src()
        _url = self.findall('\[img\]http://pikucha.ru/([\d]{4,10})/thumbnail/(.*?)\[/img\]',_src)[0]
        self.img_url = 'http://pikucha.ru/%s/%s'%_url
        self.img_thumb_url = 'http://pikucha.ru/%s/thumbnail/%s'%_url



if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
