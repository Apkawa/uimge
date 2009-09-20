# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    short_key = 'zi'
    long_key  = 'zikuka'
    host='zikuka.ru'
    action = 'http://zikuka.ru:8080/upload.php'
    form = {
            'submit':'..',
            'comment':'',
            'newwidth':'',
            'newwidthpr':'',
            'quality':'85',
            'rotate':'0',
            'rightclick':'yes',
            'rating':'yes',
            'texttext':'',
            'textfontsize':'14',
            'textposition':'bottom',
            'textalign':'left',
            'textalpha':'0',
            'textcolor':'black',
            'fontcolor':'verdana.ttf',
            'Submit': '',
            }

    def as_file(self, _file):
        return {
            'uploadtype':'1',
            'method':'file',
            'userurl':'',
            'userimg': _file }
    def as_url(self, _url):
        return {
            'uploadtype':'2',
            'method':'url',
            'userimg':'filename="" Content-Type: application/octet-stream',
            'userurl': _url}
    def thumb_size(self, _thumb_size):
        return { 'thumb_size': _thumb_size, }
    def postload(self ):
        _src = self.response.body
        _regx = r'var useLink = "http://(.*?)";'
        _url = self.findall(_regx ,_src)[0]
        self.img_url = 'http://%s'%_url
        us = _url.split('/')
        self.img_thumb_url = 'http://%s/t%s'%('/'.join(us[:-1]), us[-1])



if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
