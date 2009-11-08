# -*- coding: utf-8 -*-
import base
class Host( base.BaseHost ):
    dev_mode = False

    short_key = '10p'
    long_key = '10pix'
    host='10pix.ru'
    max_file_size = 5242880 #5Mb

    user_agent = 'Client 10pix 1.2.5.3 (Microsoft Windows NT 5.1.2600 Service Pack 3)'
    action = 'http://%s/'%host
    form = {
            'xml':'1',
            'sizeBar':'1',
            }

    def as_file(self, _file):
        return {
                'uploadType':'0',
                'fileUpload': _file,
                }

    def as_url(self, _url):
        return {
                'uploadType':'1',
                'url': _url,
                }

    def postload(self ):
        _src = self.response.body
        _regx = r'<thumbnailLink>(.+?)</thumbnailLink>'
        _url = self.findall(_regx ,_src)[0]
        self.img_url = '%s'%_url.replace('th.','')
        self.img_thumb_url = '%s'%_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
