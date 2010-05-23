# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    dev_mode = True
    short_key = 'pc'
    long_key  = 'piccy'
    host='piccy.info'
    action = 'http://piccy.info/ru/upload/'
    form = {'Submit': ''}
    cookie = 'sid=634771c4b7ab8fa0715169b4a7a7d409; xid=1015847830023050127464604473199:bf821008e7ad77cf11c139583ddbd60f'

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
