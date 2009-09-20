# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    short_key = 'pc'
    long_key  = 'piccy'
    host='piccy.info'
    action = 'http://piccy.info/ru/upload/'
    form = {'Submit': ''}
    cookie = 'sid=460e033265472bd2a69b1e4cc1c50bf0'

    def as_file(self, _file):
        return {'file': _file }
    def postload(self ):
        _src =  self.response.body
        self.img_url = self.findall( 'value=\"(http://.*?)\"></td>', _src)[1]
        self.img_thumb_url = self.findall('src=\"(http://.*?)\" alt=\"Piccy.info', _src)[0]



if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
